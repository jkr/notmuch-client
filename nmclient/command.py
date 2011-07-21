#!/usr/bin/env python

from __future__ import print_function
from subprocess import Popen, PIPE
from hashlib import sha1
from email import message_from_file
from itertools import islice
import os
import sys

class NotmuchCommandError(Exception):
    pass

def _run_command_locally (nmconfig, command, args):
    connection_commands = [nmconfig.notmuch_bin]
    command_list = connection_commands + [command] + args
    command = Popen(command_list, 
                    stdin = PIPE, stdout = PIPE, stderr = PIPE)
    return command.communicate()

def _run_command_over_ssh (nmconfig, command, args):
    connection_commands = [nmconfig.ssh_bin, nmconfig.user + "@" + nmconfig.server, nmconfig.notmuch_bin]
    command_list = connection_commands + [command] + args
    command = Popen(command_list, 
                    stdin = PIPE, stdout = PIPE, stderr = PIPE)
    return command.communicate()


class NotmuchCommand (object):

    def __init__(self, nmconfig, args):
        self.args = args
        self.config = nmconfig

    @classmethod
    def make_command(cls, nmconfig, args):
        if not args:
            raise NotmuchCommandError, "Empty argument list"
        
        cmd = args[0]
        arglist = args[1:]
        if cmd in ("new", "search", "count", 
                   "tag", "reply", "help", "config"):
            return NotmuchGeneric(nmconfig, cmd, arglist)
        elif cmd == "show":
            return NotmuchShow(nmconfig, arglist)
        else:
            raise NotmuchCommandError, \
                "Unknown (or unimplemented) command: %s" % cmd

    def get_params (self):
        params = [arg[2:].split("=") for arg in self.args
                  if arg[:2] == "--"]
        # Correct for the ones with no value:
        modified_params = [(param + [False]) if (len(param) == 1) else param
                           for param in params]

        return dict(modified_params)

    def get_search_terms (self):
        i = 1
        while self.args[i][:2] == "--":
            i += 1
        return self.args[i:]

    def run (self):
        if self.config.remote:
            return _run_command_over_ssh (self.config, self.command, self.args)
        else:
            return _run_command_locally (self.config, self.command, self.args)

class NotmuchGeneric (NotmuchCommand):
    
    def __init__(self, nmconfig, command, args):
        super(NotmuchGeneric, self).__init__(nmconfig, args)
        self.command = command

class NotmuchShow (NotmuchCommand):

    def __init__(self, nmconfig, args):
        super(NotmuchShow, self).__init__(nmconfig, args)
        self.command = "show"
        params = self.get_params()

        if "format" in params:
            format_param = params["format"]
            if format_param in ("text", "json", "mbox", "raw"):
                self.format = format_param
            else:
                raise NotmuchCommandError, \
                    "Unknown \"notmuch show\" format: %s" % format
        else:
            self.format = "text"

        if "part" in params:
            try:
                self.partnum = int(params["part"])
            except ValueError:
                raise NotmuchCommandError, \
                    "Non-integral part value: %s" % params["part"]
        else:
            self.partnum = None

    def _get_cached_file(self):
        if not self.format == "raw":
            raise NotmuchCommandError, \
                "Should only be caching when show format is \"raw\""

        search_terms = self.get_search_terms()
        hashed_terms = sha1(' '.join(search_terms)).hexdigest()
        cached_file_name = os.path.join(self.config.cache, hashed_terms)

        if not os.path.isfile(cached_file_name):
            raw_file_output = \
                _run_command_over_ssh(self.config, "show", ["--format=raw"] + search_terms)
            if raw_file_output[1]:
                raise NotmuchCommandError, \
                    "Output on stderr"
            
            raw_file = raw_file_output[0]
            try:
                fp = open(cached_file_name, "w")
                fp.write(raw_file)
                fp.close()
            except IOError:
                raise NotmuchCommandError, \
                    "Couldn't write to cache file: %s" % cached_file_name

        return cached_file_name

    def _get_local_file(self):
        if not self.format == "raw":
            raise NotmuchCommandError, \
                "Should only be fetching a local file when show format is \"raw\""

        search_terms = self.get_search_terms()
        filename_output = _run_command_locally(self.config, "search", ["--output=files"] + search_terms)
        return filename_output[0].strip().split('\n')[0]

    def _run_raw(self):
        if self.config.remote:
            mail_file = self._get_cached_file()
        else:
            mail_file = self._get_local_file()
        fp = open(mail_file)
        data = fp.read()
        fp.close()
        return data

    def _run_part(self):
        if self.config.remote:
            mail_file = self._get_cached_file()
        else:
            mail_file = self._get_local_file()
        fp = open(mail_file)
        msg = message_from_file(fp)
        fp.close()
        
        msg_parts = msg.walk()

        # We need to deal with the fact that python's email parser
        # skips the message mime-part at the top-level. I.e., there
        # should be another part between the message and the toplevel
        # mime part.
        if self.partnum == 0:
            modified_partnum = 0
        else:
            modified_partnum = self.partnum - 1
        part = islice(msg_parts, modified_partnum, None).next()
        if part.is_multipart():
            return part.as_string()
        else:
            return part.get_payload(decode=True)

    def run (self):
        if self.partnum:
            return (self._run_part(), '')
        elif self.format == "raw":
            return (self._run_raw(), '')
        else:
            return _run_command_over_ssh(self.config, self.command, self.args)


