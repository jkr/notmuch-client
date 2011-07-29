from subprocess import Popen, PIPE

def _run_command_locally (nmconfig, command, args):
    connection_commands = [nmconfig.notmuch_bin]
    command_list = connection_commands + [command] + args
    command = Popen(command_list, 
                    stdin = PIPE, stdout = PIPE, stderr = PIPE)
    return command.communicate()

def _run_command_over_ssh (nmconfig, command, args):
    connection_commands = [nmconfig.ssh_bin, 
                           nmconfig.user + "@" + nmconfig.server, 
                           nmconfig.notmuch_bin]
    command_list = connection_commands + [command] + args
    command = Popen(command_list, 
                    stdin = PIPE, stdout = PIPE, stderr = PIPE)
    return command.communicate()

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

