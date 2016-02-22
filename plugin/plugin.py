"""
DependencyTree Plugin Implementation
"""
import logging
import os
import pygraphviz as pgv
import re
import subprocess
import sys

from nose.plugins import Plugin


log = logging.getLogger('nose.plugins.dependency_tree')


class DependencyTree(Plugin):
    """
    Example Usage:
        nosetests --with-dependency-tree --diff-files `git diff --name-only`
    """
    name = 'dependency-tree'

    def options(self, parser, env):
        super(DependencyTree, self).options(parser, env=env)

        parser.add_option(
            "--dep-tree",
            action="store",
            default=env.get('NOSE_DEP_TREE', "deptree.dot"),
            dest="dep_tree",
            metavar="FILE",
            help="File path for the dependency tree .dot file"
        )

        parser.add_option(
            "--diff-files",
            action="store",
            default=env.get('NOSE_DIFF_FILES', None),
            dest="diff_files",
            metavar="FILES",
            help="A list of files"
        )

    def configure(self, options, conf):
        super(DependencyTree, self).configure(options, conf)
        if not self.enabled:
            return

        self.dep_tree = options.dep_tree
        if not os.path.isfile(self.dep_tree):
            log.info("No dependency tree found, generating a new one...")

            # generate the dependency tree
            subprocess.check_call(
                "sfood . --internal -q | sfood-graph > {}".format(
                    self.dep_tree,
                ),
                shell=True
            )

        self.diff_files = options.diff_files
        self.diff_dependent_tests = self.get_diff_dependent_tests()

    def wantFile(self, file):
        """
        Return true for all source files in dependency tree
        """
        if file in self.diff_dependent_tests:
            return True
        return False

    def get_diff_dependent_tests(self):
        diff_files = re.split(' |,', self.diff_files)
        graph = pgv.AGraph(self.dep_tree).reverse()
        test_pattern = self.conf.testMatch

        def _get_test_files(node, visited=None, tests=None):
            if not tests:
                tests = set()
            if not visited:
                visited = []

            if node in visited:
                return
            else:
                visited += ['node']

            if graph.has_node(node) and test_pattern.search(node):
                tests.update([os.path.abspath(node)])
            if graph.out_degree(nbunch=node) == 0:
                return tests
            # TODO: cyclical imports?
            for _cur_node, next_node in graph.iteroutedges(nbunch=node):
                tests.update(_get_test_files(next_node, visited, tests))
            return tests

        test_files = set()
        for fp in diff_files:
            test_files.update(_get_test_files(fp.strip()))

        log.debug("Tests for {}:\n\t{}".format(
            diff_files, '\n\t'.join(test_files)))
        return test_files
