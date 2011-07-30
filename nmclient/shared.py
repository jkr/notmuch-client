# -*- python;  coding: utf-8  -*-
#########################################################################
# shared.py: functions shared by classes in other modules.              #
#                                                                       #
# Copyright © 2011 Jesse Rosenthal                                      #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see http://www.gnu.org/licenses/ .  #
#                                                                       #
# Author: Jesse Rosenthal <jrosenthal@jhu.edu>                          #
#########################################################################

from subprocess import Popen, PIPE

def _run_command_locally (nmconfig, command, args):
    connection_commands = [nmconfig.notmuch_bin]
    command_list = connection_commands + [command] + args
    command = Popen(command_list, 
                    stdin = PIPE, stdout = PIPE, stderr = PIPE)
    return command

def _run_command_over_ssh (nmconfig, command, args):
    connection_commands = [nmconfig.ssh_bin, 
                           nmconfig.user + "@" + nmconfig.server, 
                           nmconfig.notmuch_bin]
    command_list = connection_commands + [command] + args
    command = Popen(command_list, 
                    stdin = PIPE, stdout = PIPE, stderr = PIPE)
    return command


class AliasRecursionError(Exception):
    pass

def _resolve_recurs_item(dct, k, v):
    sp = v.split()
    for i in xrange(len(sp)):
        if sp[i][:7] == "alias:":
            new_key = sp[i][7:]
            if new_key == k:
                raise AliasRecursionError, "Infinite alias loop"
            else:
                sp[i] = dct[new_key]
                sp = work_out(dct, k, ' '.join(sp))
    return sp

def resolve_recurs(dct):
    for k, v in dct.items():
        dct[k] = ' '.join(_resolve_recurs_item(dct, k, v)) 
    return dct

