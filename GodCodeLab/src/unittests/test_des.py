import unittest
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
from lib.des import Des

class TestDes(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_des1_gcsum(self):
        text = "Orange"
        des = Des.get_instance(Des.DES1,
            text)
        expected = 60
        actual = des.gc_sum()
        self.assertEqual(actual, expected)
    
    def test_des8_str(self):
        text = "Orange"
        expected = "604|10|1"
        des = Des.get_instance(Des.DES8 ,
            text)
        actual = str(des)
        self.assertEqual(actual, expected)

