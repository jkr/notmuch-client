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


