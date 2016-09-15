"""
Package script
"""
__author__ = 'Tom Yan'

from distutils.core import setup
import sys, py2exe

sys.argv.append('py2exe')

py2exe_options = {'includes': ['sip']}

setup(
    options = {'py2exe': py2exe_options},
    windows = ['main.py'],
)
