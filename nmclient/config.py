from ConfigParser import ConfigParser, NoOptionError, NoSectionError
import getpass
import os

CONFIG_LOCATION = os.path.expanduser("~/.notmuch-client.config")

TOPLEVEL_CONFIG_SECTION = "general"

class NotmuchClientConfigError(Exception):
    pass

class NotmuchClientConfig(object):

    def __init__(self, configfile = None):
        self._config_parser = ConfigParser()
        if configfile:
            self._config_parser.read(configfile)

    @property
    def account(self):
        if not hasattr(self, "_account"):
            if self._config_parser.has_option(TOPLEVEL_CONFIG_SECTION, 
                                              "account"):
                self._account = self._config_parser.get(TOPLEVEL_CONFIG_SECTION,
                                                        "account")
            else:
                self._account = None
        return self._account

    @property
    def remote(self):
        if not hasattr(self, "_remote"):
            if self.account and self._config_parser.has_option(self.account, 
                                                               "server"):
                self._server = self._config_parser.get(self.account, 
                                                       "server")
                self._remote = True
                # If we're remote, we'll also get all the other
                # attributes we'll want if we're remote.
                #
                # We'll get the ssh binary path as well. NOTE: This is
                # in the toplevel, since it's not really a
                # per-account setting.
                try:
                    self._ssh_bin = self._config_parser.get (
                        TOPLEVEL_CONFIG_SECTION, "ssh_bin"
                        )
                except NoOptionError:
                    self._ssh_bin = "ssh"

                # User. This will default to the current logged in user.
                try:
                    self._user = self._config_parser.get(self.account, 
                                                         "user")
                except NoOptionError:
                    self._user = getpass.getuser()

                # Private key. This will default to None, in which
                # case it just won't be used, and we'll let
                # openssh figure it out.
                try:
                    self._private_key = self._config_parser.get (
                        self.account, "public_key"
                        )
                except NoOptionError:
                    self._private_key = None

                # And the cache. This will default to
                # "${HOME}/.notmuch-client-cache.d"
                try:
                    self._cache = os.path.expanduser (
                        self._config_parser.get(self.account, "cache")
                        )
                except NoOptionError:
                    self._cache = os.path.expanduser (
                        "~/.notmuch-client-cache.d"
                        )

            else:
                self._remote = False
        return self._remote

    @property
    def server(self):
        if self.remote:
            return self._server
        else:
            return None

    @property
    def ssh_bin(self):
        if self.remote:
            return self._ssh_bin
        else:
            return None

    @property
    def user(self):
        if self.remote:
            return self._user
        else:
            return None

    @property
    def private_key(self):
        if self.remote:
            return self._private_key
        else:
            return None

    @property
    def cache(self):
        if self.remote:
            return self._cache
        else:
            return None


    @property
    def notmuch_bin(self):
        if not hasattr(self, "_notmuch_bin"):
            if self.account and self._config_parser.has_option(self.account, 
                                                               "notmuch_bin"):
                self._notmuch_bin = self._config_parser.get(self.account, 
                                                            "notmuch_bin")
            else:
                self._notmuch_bin = "notmuch"
        return self._notmuch_bin

    @property
    def notmuch_config(self):
        if not hasattr(self, "_notmuch_config"):
            if self.account and self._config_parser.has_option (self.account, 
                                                                "notmuch_config"):
                self._notmuch_bin = self._config_parser.get(self.account, 
                                                            "notmuch_config")
            else:
                self._notmuch_bin = None
        return self._notmuch
