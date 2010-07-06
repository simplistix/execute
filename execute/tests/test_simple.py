# Copyright (c) 2010 Simplistix Ltd
#
# See license.txt for more details.
from __future__ import with_statement

import os,sys

from execute import simple
from mock import Mock
from subprocess import PIPE,STDOUT
from testfixtures import tempdir,compare,Replacer
from unittest import TestSuite,TestCase,makeSuite

class TestSimple(TestCase):

    @tempdir()
    def test_out_and_err(self,d):
        # without the flushes, the order comes out wrong
        path = d.write('test.py','\n'.join((
                "import sys",
                "sys.stdout.write('stdout\\n')",
                "sys.stdout.flush()",
                "sys.stderr.write('stderr\\n')",
                "sys.stderr.flush()",
                "sys.stdout.write('stdout2\\n')",
                "sys.stdout.flush()",
                )),path=True)
        compare('stdout\nstderr\nstdout2\n',
                simple(sys.executable+' '+path))
    
    @tempdir()
    def test_args(self,d):
        path = d.write('test.py','\n'.join((
                "import sys",
                "print sys.argv",
                )),path=True)
        compare("[%r, 'x=1', '--y=2', 'a', 'b']\n" % path,
                simple(sys.executable+' '+path+' x=1 --y=2 a b'))
    
    @tempdir()
    def test_working_directory(self,d):
        dir = d.makedir('a_dir',path=True)
        path = d.write('test.py','\n'.join((
                "import os",
                "print os.getcwd()",
                )),path=True)

        # tempdirs on Mac OS X give a different path
        # after you've os.chdir's into them!
        cur = os.getcwd()
        try:
            os.chdir(dir)
            expected = os.getcwd()+'\n'
        finally:
            os.chdir(cur)
            
        compare(expected,
                simple(sys.executable+' '+path,cwd=dir))

    def test_popen_params(self):
        m = Mock()
        m.Popen.return_value = m.Popeni
        m.Popeni.communicate.return_value=('','')
        with Replacer() as r:
            r.replace('execute.Popen',m.Popen)
            simple('something')
        compare(m.method_calls,[
                ('Popen',
                 ('something',),
                 {'cwd': None,
                  'shell': True,
                  'stderr': STDOUT,
                  'stdout': PIPE,
                  'universal_newlines': True}),
                ('Popeni.communicate', (), {})
                ])
    
def test_suite():
    return TestSuite((
        makeSuite(TestSimple),
        ))
