#coding:utf-8

import sys

sys.path.append('/Users/alexliu/projects/Python-TDD')

import utest
import unittest

loader = utest.BetterLoader()

testsuites = loader.loadTestsFromName('main')

if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(testsuites)
