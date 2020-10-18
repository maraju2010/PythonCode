import run
from CDRAnalyzer.monitor import worker,pool
from threading import local
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.logic import algo_1 as algo
from CDRAnalyzer.loader.report import Report
import unittest

class test_conf(unittest.TestCase):

    def test_file_validate(self):
        a=algo.auth_code_sn()
        a._analyse()

    def test_report(self):
        r=Report()
        
if __name__ == '__main__':
    unittest.main()
