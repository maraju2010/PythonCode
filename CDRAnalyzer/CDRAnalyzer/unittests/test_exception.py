import run
from CDRAnalyzer.monitor import worker,pool
from threading import local
from CDRAnalyzer.settings import global_conf as conf
from CDRAnalyzer.logic import algo_1 as algo
import unittest

class test_conf(unittest.TestCase):

    def test_algo_exception(self):
        a=algo.auth_code_sn()
        #a._handle_exception()
        start,end = a._get_chunk
        print (start)
        print(end)

if __name__ == '__main__':
    unittest.main()
