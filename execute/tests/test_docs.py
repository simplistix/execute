# Copyright (c) 2010 Simplistix Ltd
#
# See license.txt for more details.

import sys

from doctest import REPORT_NDIFF,ELLIPSIS
from glob import glob
from manuel import doctest,codeblock,capture
from manuel.testing import TestSuite
from os.path import dirname,join,pardir
from testfixtures import TempDirectory

def setUp(test):
    test.globs['temp_dir']=TempDirectory()
    test.globs['python']=sys.executable

def tearDown(test):
    TempDirectory.cleanup_all()
    
def test_suite():
    m =  doctest.Manuel(optionflags=REPORT_NDIFF|ELLIPSIS)
    m += codeblock.Manuel()
    m += capture.Manuel()

    return TestSuite(
        m,
        setUp=setUp,
        tearDown=tearDown,
        *glob(join(dirname(__file__),pardir,pardir,'docs','*.txt'))
        )
