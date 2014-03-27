"""
Distutils script for building cython .c and .so files. Call it with:
python setup.py build_ext --inplace
"""

import sys
print "RUNNING SETUP.PY, PYTHON IS:"

print sys.executable

from distutils.core import setup
from Cython.Build import cythonize

#from Cython.Compiler.Options import directive_defaults
#directive_defaults['profile'] = True

compile_cy_py = True

cy_modules = [
    'kivy/pentai/board_strip.pyx',
    'kivy/pentai/length_lookup_table.pyx',
    ]
if compile_cy_py:
    cy_modules.extend([
        'priority_filter.py',
        'priority_filter_2.py',
        'utility_stats.py',
        'bit_reverse.py',
        'utility_calculator.py',
        'direction_strips.py',
        'alpha_beta.py',
        'ab_state.py',
        'game_state.py',
        'board.py',
    ])

setup(
        #name = "PentAI",
        #name = "pente_ext",
        ext_modules = cythonize(
            cy_modules
        ),
        #packages=[ 'pente_ext' ]
    )
'''
setup(name='board_strip',
    version='1.0',
    ext_modules = cythonize(
        'board_strip.pyx',
    ),
    #packages=[ 'board_strip' ]
)
'''
    #ext_modules=[Extension('board_strip', ["board_strip.)],
