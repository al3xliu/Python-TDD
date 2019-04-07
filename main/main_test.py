#coding:utf-8

import sys
import unittest

sys.path.append('/Users/alexliu/projects/Python-TDD')

import utest

def add(x):
    return lambda y : x+y

class MainTestCase(utest.Test):

    def test_add(self):
        self.assert_equal(5, add(2)(3))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MainTestCase))
    return suite
