"""
Distutils script for building cython .c and .so files. Call it with:
python setup.py build_ext --inplace
"""

from distutils.core import setup
from Cython.Build import cythonize

#from Cython.Compiler.Options import directive_defaults
#directive_defaults['profile'] = True


setup(
        name = "Pentacular",
        ext_modules = cythonize(
            [
            'board_strip.pyx',
            'length_lookup_table.pyx',
            'priority_filter.py',
            'budget_searcher.py',
            'utility_calculator.py',
            'utility_stats.py',
            'direction_strips.py',
            'alpha_beta.py',
            'ab_state.py',
            'ab_game.py',
            'game_state.py',
            'board.py',
            'ai_player.py',
            ],
            extra_compile_args=["-O3"],
        )
    )
