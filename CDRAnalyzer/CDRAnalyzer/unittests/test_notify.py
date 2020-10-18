import run
from CDRAnalyzer.monitor import worker,pool
from threading import local
from CDRAnalyzer.settings import global_conf as conf
import unittest

class test_conf(unittest.TestCase):

    def test_run_thread(self):
        p=pool.Pool()

    def test_notify(self):
        self.w=worker.Worker()
        fl=self.w._start()
        l=worker.Listener()
        l.Listener()

if __name__ == '__main__':
    unittest.main()
