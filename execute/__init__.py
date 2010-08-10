# Copyright (c) 2010 Simplistix Ltd
#
# See license.txt for more details.

from subprocess import Popen,PIPE,STDOUT

def _popen(command,cwd):
    return Popen(
        command,
        stderr=STDOUT,
        stdout=PIPE,
        universal_newlines=True,
        cwd=cwd,
        shell=True,
        )

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
    return _popen(command,cwd).communicate()[0]

def returncode(command,cwd=None):
    """Execute the command specified in a sub-process.

    This command must take no input. The exit code set
    by the command will be returned. Any output from the
    command to either the standard or error streams will
    be discarded.

    :param command:
      A string containing the command to be executed.

    :param cwd:
      An optional current working directory in which to
      run the command. If not specified, the current working
      directory will be left as-is.
     
    :returns:
      The exit code set by the command that was run.
    
    """
    p = _popen(command,cwd)
    p.communicate()
    return p.returncode

def both(command,cwd=None):
    """Execute the command specified in a sub-process.

    This command must take no input.
    A 2-tuple will be returned. Any output to either
    the standard or error streams will be collected and
    returned as the first element of the tuple.The exit code set
    by the command will be returned as the second element of the
    tuple.

    :param command:
      A string containing the command to be executed.

    :param cwd:
      An optional current working directory in which to
      run the command. If not specified, the current working
      directory will be left as-is.
     
    :returns:
      The output and exit code of the command that was run.
    
    """
    p = _popen(command,cwd)
    output = p.communicate()[0]
    return output,p.returncode
