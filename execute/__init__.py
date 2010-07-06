# Copyright (c) 2010 Simplistix Ltd
#
# See license.txt for more details.

from subprocess import Popen,PIPE,STDOUT

def simple(command,cwd=None):
    """Execute the command specified in a sub-process.

    This command must take no input. Any output to either
    the standard or error streams will be collected and
    returned as a string.

    :param command:
      A string containing the command to be executed.

    :param cwd:
      An optional current working directory in which to
      run the command. If not specified, the current working
      directory will be left as-is.
     
    :returns:
      A string containing anything written to the standard
      or error streams by the command as it runs.
    
    """
    return Popen(
        command,
        stderr=STDOUT,
        stdout=PIPE,
        universal_newlines=True,
        cwd=cwd,
        shell=True,
        ).communicate()[0]
