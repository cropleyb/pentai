"""
Distutils script for building cython .c and .so files. Call it with:
python setup.py build_ext --inplace
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
        name = "Pentacular",
        ext_modules = cythonize([
            'board_strip.pyx',
            'length_lookup_table.py',
            'priority_filter.py',
            'utility_calculator.py',
            'utility_stats.py',
            'direction_strips.py',
            'alpha_beta.py',
        ])
    )
