#configure test monitor class

import run
from CDRAnalyzer.monitor import worker,pool
from threading import local
from CDRAnalyzer.settings import global_conf as conf
import unittest

class test_conf(unittest.TestCase):

    #def test_file_path(self):
    #    res = conf.MON_PATH
    #    self.assertIsNotNone(res)

    #def test_file_check(self):
    #    self.w=worker.Worker()
    #    self.assertIsNotNone(self.w.before_path) or self.assertIsNotNone(self.w.dir)

    def test_file_validate(self):
        self.w=worker.Worker()
        self._p= worker._parser()
        fl=self.w._start()
        for f in fl:
            #print ("this is testmon %s" % f)
            self._p._parse(fp=f,tb="cdr_main",db="cdr_portal")

if __name__ == '__main__':
    unittest.main()
