#coding:utf-8

import unittest
import sys
from werkzeug.utils import import_string, find_modules

sys.path.append('/Users/alexliu/projects/Python-TDD')

def iter_suites():
    """Yields all testsuites."""
    for module in find_modules('main'):
        mod = import_string(module)
        if hasattr(mod, 'suite'):
            yield mod.suite()

def suite():
    """A testsuite that has all the Flask tests.  You can use this
    function to integrate the Flask tests into your own testsuite
    in case you want to test that monkeypatches to Flask do not
    break it.
    """
    suite = unittest.TestSuite()
    for other_suite in iter_suites():
        suite.addTest(other_suite)
    return suite

def find_all_tests(suite):
    """Yields all the tests and their names from a given suite."""
    suites = [suite]
    while suites:
        s = suites.pop()
        try:
            suites.extend(s)
        except TypeError:
            yield s, '%s.%s.%s' % (
                s.__class__.__module__,
                s.__class__.__name__,
                s._testMethodName
            )


class Test(unittest.TestCase):

    """Baseclass for all the tests cases.  Use these methods
    for testing.
    """

    def setup(self):
        pass

    def teardown(self):
        pass

    def assert_equal(self, x, y):
        self.assertEqual(x, y)

    def assert_true(self, x, msg=None):
        self.assertTrue(x, msg)

    def assert_false(self, x, msg=None):
        self.assertTrue(x, msg)

    def assert_in(self, x, y):
        self.assertIn(x, y)

    def assert_not_in(self, x, y):
        self.assertNotIn(x, y)


class BetterLoader(unittest.TestLoader):
    """A nicer loader that solves two problems.  First of all we are setting
    up tests from different sources and we're doing this programmatically
    which breaks the default loading logic so this is required anyways.
    Secondly this loader has a nicer interpolation for test names than the
    default one so you can just do ``run-tests.py ViewTestCase`` and it
    will work.
    """

    def getRootSuite(self):
        return suite()

    def loadTestsFromName(self, name, module=None):
        root = self.getRootSuite()
        if name == 'suite':
            return root

        all_tests = []
        for testcase, testname in find_all_tests(root):
            print(testname)
            if testname == name or \
               testname.endswith('.' + name) or \
               ('.' + name + '.') in testname or \
               testname.startswith(name + '.'):
                all_tests.append(testcase)

        if not all_tests:
            raise LookupError('could not find test case for "%s"' % name)

        if len(all_tests) == 1:
            return all_tests[0]

        rv = unittest.TestSuite()
        for test in all_tests:
            rv.addTest(test)
        return rv
