# (c) Simplistix Ltd 2009, all rights reserved.

import logging
import os,time

from mock import Mock
from functools import partial
from process import main
from setuplogging.tests import EnvironmentModule
from testfixtures import compare,Comparison as C,TempDirectory,Replacer,LogCapture,test_datetime
from unittest import TestCase

j = os.path.join

class runCommand:

    def __init__(self,var):
        self.responses = {}
        self.effects = {}
        self.command_to_tag = {}
        self.called=[]
        self.var = var

    def add(self,command,response='',effect=None):
        self.responses[command]=response
        if effect:
            self.effects[command]=effect
        return command
            
    def __call__(self,command,log=True):
        r = self.responses.get(command,'')
        e = self.effects.get(command)
        if e: e()
        self.called.append((command,log))
        return r

    # helpers

    def write_files(self,*sets):
        for path,content in sets:
            dirpath = path[:-1]
            if dirpath:
                dirpath = os.path.join(*dirpath)
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
            f = open(os.path.join(*path),'wb')
            f.write(content)
            f.close()
            
    def wget(self,day,user,passwd,url,*sets):
        
        wget = (
            'wget -m -k -K -a '+j(self.var.path,'wget-'+user+'-'+day+'.log')+
            ' -nv -x -E --http-user=%s --http-passwd=%s %s'
            )%(user,passwd,url)

        self.add(wget,effect=partial(self.write_files,*sets))

        return wget
    
    def unzip(self,date,user,passwd,*sets):
        # sets should be the same as those passed to wget!
        basepath = (self.var.path,'www','static',user)
        unzip = (
            'unzip -q -o -P %s -d '+j(*basepath)+' '+
            j(self.var.path,'www',user,date+'.zip')
            ) % (passwd,)

        nsets = []
        for path,content in sets:
            nsets.append((basepath+path[1:],content))
                         
        self.add(unzip,effect=partial(self.write_files,*nsets))
        
        return unzip

    def diff(self,user,path,response=''):
        diff = (
            'diff -q '+j(self.var.path,'www','static',user,*path)+' '
            +j(self.var.path,'create',user,'premier.screendigest.com',*path)
            )
        self.add(diff,response=response)
        return diff

    def print_cwd(self,name):
        print name,':',os.getcwd()
        
    def cwd(self,name,command):
        # handy for debugging!
        self.add(command,effect=partial(self.print_cwd,name))
        
logger = logging.getLogger()

class BaseTestCase(TestCase):

    def setUp(self):        
        self.e = EnvironmentModule(False)
        self.e.install()
        self.var = TempDirectory()
        self.r = Replacer(replace_returns=True)
        self.setuplogging_setup = self.r.replace('setuplogging.setup',Mock())
        self.handlers = self.r.replace('tests.base.logger.handlers',[])
        self.command = r = runCommand(self.var)
        self.r.replace('handlers.runCommand',r)
        self.r.replace('steps.runCommand',r)
        self.r.replace('process.datetime',test_datetime())
        self.log = LogCapture()
        self.e.var_path = self.var.path
        self.e.lockfile_path = os.path.join(self.var.path,'staticsite.lock')
        self.e.full_copy_path=os.path.join(self.var.path,'fullcopy.txt')
        self.e.site_domain = 'premier.screendigest.com'
        self.e.site_url = 'http://'+self.e.site_domain
        self.e.bad_phrases = ('a bad phrase',)
        self.e.dry_run = False

        self.day = time.strftime('%a')
        self.date = time.strftime('%Y%m%d')

    def tearDown(self):
        LogCapture.uninstall_all()
        self.r.restore()
        TempDirectory.cleanup_all()
        try:
            self.e.uninstall()
        except KeyError:
            # already uninstalled!
            pass
        
    def do_run(self,raise_on_critical=True):
        # we do it this way to make sure that the
        # default is correct!
        args = []
        if raise_on_critical:
            args.append(True)
        
        main(*args)
            
        compare(self.handlers,
                [C('testfixtures.LogCapture'),
                 C('errorhandler.ErrorHandler',
                   logger='',
                   level=logging.ERROR,
                   strict=False)])
        
        compare(self.setuplogging_setup.call_args,((),{},))