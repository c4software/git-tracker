#!/usr/bin/env python
from setuptools import setup

requires = ['jinja2','mistune']

try:
    import argparse  # NOQA
except ImportError:
    requires.append('argparse')

entry_points = {'console_scripts': [
                                    'git-tracker = git_tracker.git_tracker:main',
                                    'git-tracker-get-my-issue = git_tracker.get_my_issue:main'
                                   ]
                }

README = ""
CHANGELOG = ""

setup(
    name="Git-Tracker",
    version="0.2",
    url='http://blog.lesite.us',
    author='Valentin Brosseau',
    author_email='c4software@gmail.com',
    description="Simple issue tracker for Git based on Git.",
    long_description="",
    packages=['git_tracker'],
    include_package_data=True,
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[],
    test_suite='',
)
