# Copyright (c) 2010 Simplistix Ltd
#
# See license.txt for more details.
from __future__ import with_statement

import os,sys

from execute import returncode
from testfixtures import tempdir,compare
from unittest import TestSuite,TestCase,makeSuite

class TestReturnCode(TestCase):

    @tempdir()
    def test_okay(self,d):
        path = d.write('test.py','\n'.join((
                "import sys",
                "sys.stdout.write('stdout\\n')",
                "sys.stderr.write('stderr\\n')",
                "sys.exit(0)",
                )),path=True)
        compare(0,returncode(sys.executable+' '+path))
    
    @tempdir()
    def test_error(self,d):
        path = d.write('test.py','\n'.join((
                "import sys",
                "sys.stdout.write('stdout\\n')",
                "sys.stderr.write('stderr\\n')",
                "sys.exit(1)",
                )),path=True)
        compare(1,returncode(sys.executable+' '+path))
        
    @tempdir()
    def test_working_directory(self,d):
        dir = d.makedir('a_dir',path=True)
        
        # tempdirs on Mac OS X give a different path
        # after you've os.chdir's into them!
        cur = os.getcwd()
        try:
            os.chdir(dir)
            expected = os.getcwd()
        finally:
            os.chdir(cur)
            
        path = d.write('test.py','\n'.join((
                "import os,sys",
                "dir = os.getcwd()",
                "if dir==%r:"% expected,
                "  sys.exit(3)",
                "else:",
                "  sys.exit(2)",
                )),path=True)

        compare(3,returncode(sys.executable+' '+path,cwd=dir))
    
    
def test_suite():
    return TestSuite((
        makeSuite(TestReturnCode),
        ))
