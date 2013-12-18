"""
Distutils script for building cython .c and .so files. Call it with:
python setup.py build_ext --inplace
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
        name = "My hello app",
        ext_modules = cythonize(
            'board_strip.pyx',
        )
    )
'''
# TODO Something broken in distutils? Doesn't like multiple files
            'take_counter.py',
            'priority_filter.py',
            'threat_counter.py'
'''
