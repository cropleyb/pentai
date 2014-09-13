#
# Kivy - Crossplatform NUI toolkit
# http://kivy.org/
#

from distutils.core import setup
from os.path import sep
from os import environ
import sys

platform = sys.platform
kivy_ios_root = environ.get('KIVYIOSROOT', None)
if kivy_ios_root is not None:
    platform = 'ios'

# -----------------------------------------------------------------------------

def get_modulename_from_file(filepath):
    filepath = filepath.replace(sep, '/')
    pyx = '.'.join(filepath.split('.')[:-1])
    pyxl = pyx.split('/')

    try:
        while pyxl[0] != 'pente':
            pyxl.pop(0)
        if pyxl[1] == 'pente':
            pyxl.pop(0)
    except:
        print "Couldn't get_modulename_from_file from %s" % filepath
        pyxl = pyx.split('/')[1:] # Strip off the leading "./"
    r = '.'.join(pyxl)
    return r

if platform != 'ios':
    # OS X
    from Cython.Build import cythonize
    ext_modules = cythonize(["pentai/*/*.pyx"])
else:
    from distutils.extension import Extension
    import glob

    ext_modules = []
    c_files = glob.glob("pentai/*/*.c")
    for filepath in c_files:
        ext_name = get_modulename_from_file(filepath)
        ext_modules.append(Extension(ext_name, [filepath]))

setup(
    name='pentai',
    author='Bruce Cropley',
    packages=[
        'pentai',
        'pentai.base',
        'pentai.ai',
        # TODO: Why is db missing (openings book)
        ],
    ext_modules=ext_modules,
    )

