"""
Tests for the DependencyTree plugin
"""
import re

from nose.config import Config
from nose.plugins import PluginTester
from unittest import TestCase

from plugin import DependencyTree


class DependecyTreePluginTestCase(TestCase):
    """
    Unit tests for the DependencyTree plugin.
    """
    def test_get_diff_dependent_tests(self):
        """
        The related tests are chosen correctly from the dependency tree.
        """
        plugin = DependencyTree()
        plugin.diff_files = 'plugin/plugin.py'
        plugin.dep_tree = 'plugin/mock_tests/test_deptree.dot'
        plugin.conf = Config()
        tests = plugin.get_diff_dependent_tests()
        self.assertEqual(1, len(tests))
        self.assertIn('plugin/mock_tests/related_tests.py', tests.pop())

    def test_get_diff_dependent_tests_cyclycal_import(self):
        """
        The related tests are chosen correctly from the dependency tree.
        """
        plugin = DependencyTree()
        plugin.diff_files = 'plugin/not_plugin.py'
        plugin.dep_tree = 'plugin/mock_tests/test_deptree.dot'
        plugin.conf = Config()
        tests = plugin.get_diff_dependent_tests()
        self.assertEqual(1, len(tests))
        self.assertIn('plugin/mock_tests/unrelated_tests.py', tests.pop())


class PluginIntegrationTestCase(PluginTester, TestCase):
    """
    Tests the plugins integration.
    """
    activate = '-v'
    env = {
        'NOSE_DIFF_FILES': 'plugin/plugin.py',
        'NOSE_DEP_TREE': 'plugin/mock_tests/test_deptree.dot',
        'NOSE_WITH_DEPENDENCY_TREE': '1',
    }
    plugins = [DependencyTree()]
    suitepath = 'plugin/mock_tests'

    def test_results(self):
        """
        Only the related test is run when the plugin is active.
        """
        output = str(self.output)
        expected_output = [
            "runTest (plugin.mock_tests.related_tests.RelatedTestCase) ... ok",
            "Ran 1 test in",
        ]
        self.assertIn(expected_output[0], output)
        self.assertIn(expected_output[1], output)
