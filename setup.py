from setuptools import setup, find_packages

setup(
    name='dependency_tree',
    version = "0.1",
    packages = find_packages(),
    install_requires = [
        'nose',
        'pygraphviz>=1.1',
        'snakefood==1.4'
    ],
    py_modules = ['plugin'],
    entry_points = {
        'nose.plugins.0.10': [
            'dependency_tree = plugin:DependencyTree'
        ]
    },
    # metadata for upload to PyPI
    author = "Christine Lytwynec",
    author_email = "chris.lytwynec@gmail.com",
    description = "A nose plugin for running only tests affected by a changeset",
)
