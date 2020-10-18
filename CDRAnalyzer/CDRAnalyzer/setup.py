"""
Run this module first time to setup the environment.
It creates databases, tables and environment variables.

"""

from distutils.core import setup

setup(
    name='CDRAnalyzer',
    version='0.1dev',
    packages=['database','loader','logic','monitor','MQ','settings','unittests','util'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
)
