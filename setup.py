"""
Distutils script for building cython .c and .so files. Call it with:
python setup.py build_ext --inplace
"""

from distutils.core import setup
from Cython.Build import cythonize

#from Cython.Compiler.Options import directive_defaults
#directive_defaults['profile'] = True

cy_modules = [
            'board_strip.pyx',
            'length_lookup_table.pyx',
            ]
if True:
    cy_modules.extend([
            'priority_filter.py',
            'priority_filter_2.py',
            'utility_stats.py',
            'bit_reverse.py',
    ])
if True:
    cy_modules.extend([
        'utility_calculator.py',
        'direction_strips.py',
        'alpha_beta.py',
        'ab_state.py',
        'game_state.py',
        'board.py',
    ])

setup(
        name = "PentAI",
        ext_modules = cythonize(
            cy_modules
        )
    )
