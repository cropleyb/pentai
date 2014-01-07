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
            'priority_filter.py',
            ]
if False:
    cy_modules.extend([
        'budget_searcher.py',
        'utility_calculator.py',
        'utility_stats.py',
        'direction_strips.py',
        'alpha_beta.py',
        'ab_state.py',
        'game_state.py',
        'board.py',
        'ai_player.py',
    ])

setup(
        name = "Pentacular",
        ext_modules = cythonize(
            cy_modules
            # extra_compile_args=["-O3"], # Is this doing anything?
        )
    )
