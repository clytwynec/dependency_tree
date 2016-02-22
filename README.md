# DependencyTree nose plugin
[![Build Status](https://travis-ci.org/clytwynec/dependency_tree.svg?branch=master)](https://travis-ci.org/clytwynec/dependency_tree)

This nose plugin is intended to allow running tests based on a changeset.

Currently, the changeset must be passed in as an option (`diff-files`), which means it is also possible to run based on any particular file.


## Requires

* [snakefood](http://furius.ca/snakefood/) for generating the dependency tree as a .dot file
* [pygraphviz](https://pygraphviz.github.io/) to interpret the dependency tree from the .dot file
* [nose](http://nose.readthedocs.org/), because this is a nose plugin.


## How it works

The plugin uses snakefood to generate a dependency tree as a `.dot` file if the specified file doesn't already exist. To figure out which files contain tests that maybe related to the changeset, ...

Sidenote: Because this creates the tree in a `.dot`, you can convert it to another file format to visually inspect the graph of internal dependencies.

