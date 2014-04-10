#
# Kivy - Crossplatform NUI toolkit
# http://kivy.org/
#

import sys

from copy import deepcopy
import os
from os.path import join, dirname, sep, exists, basename
from os import walk, environ
from distutils.core import setup
from distutils.extension import Extension
from collections import OrderedDict

#from Cython.Compiler.Options import directive_defaults
#directive_defaults['profile'] = True

if sys.version > '3':
    PY3 = True
else:
    PY3 = False


def getoutput(cmd):
    import subprocess
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return p.communicate()[0]


def pkgconfig(*packages, **kw):
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    cmd = 'pkg-config --libs --cflags {}'.format(' '.join(packages))
    for token in getoutput(cmd).split():
        ext = token[:2].decode('utf-8')
        flag = flag_map.get(ext)
        if not flag:
            continue
        kw.setdefault(flag, []).append(token[2:].decode('utf-8'))
    return kw


# -----------------------------------------------------------------------------
# Determine on which platform we are

platform = sys.platform

# Detect 32/64bit for OSX (http://stackoverflow.com/a/1405971/798575)
if sys.platform == 'darwin':
    if sys.maxsize > 2 ** 32:
        osx_arch = 'x86_64'
    else:
        osx_arch = 'i386'

# Detect Python for android project (http://github.com/kivy/python-for-android)
ndkplatform = environ.get('NDKPLATFORM')
if ndkplatform is not None and environ.get('LIBLINK'):
    platform = 'android'
kivy_ios_root = environ.get('KIVYIOSROOT', None)
if kivy_ios_root is not None:
    platform = 'ios'
if exists('/opt/vc/include/bcm_host.h'):
    platform = 'rpi'

# -----------------------------------------------------------------------------
# Detect options
#
c_options = OrderedDict()
c_options['use_rpi'] = platform == 'rpi'
c_options['use_opengl_es2'] = True
c_options['use_opengl_debug'] = False
c_options['use_glew'] = False
c_options['use_sdl'] = False
c_options['use_ios'] = False
c_options['use_mesagl'] = False
c_options['use_x11'] = False
c_options['use_gstreamer'] = False
c_options['use_avfoundation'] = platform == 'darwin'

# now check if environ is changing the default values
for key in list(c_options.keys()):
    ukey = key.upper()
    if ukey in environ:
        value = bool(int(environ[ukey]))
        print('Environ change {0} -> {1}'.format(key, value))
        c_options[key] = value

# -----------------------------------------------------------------------------
# Cython check
# on python-for-android and kivy-ios, cython usage is external
have_cython = False
if platform in ('ios', 'android'):
    print('\nCython check avoided.')
else:
    try:
        # check for cython
        from Cython.Distutils import build_ext, Extension # No impact?
        from Cython.Build import cythonize
        have_cython = True
    except ImportError:
        print('\nCython is missing, its required for compiling kivy !\n\n')
        raise

if not have_cython:
    from distutils.command.build_ext import build_ext

# -----------------------------------------------------------------------------
# Setup classes


class KivyBuildExt(build_ext):

    def build_extensions(self):
        print('Build configuration is:')
        for opt, value in c_options.items():
            print(' * {0} = {1}'.format(opt, value))

        c = self.compiler.compiler_type
        print('Detected compiler is {}'.format(c))
        if c != 'msvc':
            for e in self.extensions:
                e.extra_link_args += ['-lm']

        build_ext.build_extensions(self)

    def update_if_changed(self, fn, content):
        need_update = True
        if exists(fn):
            with open(fn) as fd:
                need_update = fd.read() != content
        if need_update:
            with open(fn, 'w') as fd:
                fd.write(content)


# -----------------------------------------------------------------------------
# extract version (simulate doc generation, kivy will be not imported)
environ['KIVY_DOC_INCLUDE'] = '1'
import kivy

# extra build commands go in the cmdclass dict {'command-name': CommandClass}
# see tools.packaging.{platform}.build.py for custom build commands for
# portable packages.  also e.g. we use build_ext command from cython if its
# installed for c extensions.
from kivy.tools.packaging.factory import FactoryBuild
cmdclass = {
    'build_factory': FactoryBuild,
    'build_ext': KivyBuildExt}

try:
    # add build rules for portable packages to cmdclass
    if platform == 'win32':
        from kivy.tools.packaging.win32.build import WindowsPortableBuild
        cmdclass['build_portable'] = WindowsPortableBuild
    elif platform == 'darwin':
        from kivy.tools.packaging.osx.build import OSXPortableBuild
        cmdclass['build_portable'] = OSXPortableBuild
except ImportError:
    print('User distribution detected, avoid portable command.')

# Detect which opengl version headers to use
if platform in ('android', 'darwin', 'ios', 'rpi'):
    pass
elif platform == 'win32':
    print('Windows platform detected, force GLEW usage.')
    c_options['use_glew'] = True
else:
    # searching GLES headers
    default_header_dirs = ['/usr/include', '/usr/local/include']
    found = False
    for hdir in default_header_dirs:
        filename = join(hdir, 'GLES2', 'gl2.h')
        if exists(filename):
            found = True
            print('Found GLES 2.0 headers at {0}'.format(filename))
            break
    if not found:
        print('WARNING: GLES 2.0 headers are not found')
        print('Fallback to Desktop opengl headers.')
        c_options['use_opengl_es2'] = False

# check if we are in a kivy-ios build
if platform == 'ios':
    print('Kivy-IOS project environment detect, use it.')
    print('Kivy-IOS project located at {0}'.format(kivy_ios_root))
    c_options['use_ios'] = True

# detect gstreamer, only on desktop
if platform not in ('ios', 'android'):
    gst_flags = pkgconfig('gstreamer-1.0')
    if 'libraries' in gst_flags:
        c_options['use_gstreamer'] = True


# -----------------------------------------------------------------------------
# declare flags


def get_modulename_from_file(filename):
    filename = filename.replace(sep, '/')
    pyx = '.'.join(filename.split('.')[:-1])
    pyxl = pyx.split('/')
    return pyxl[-1]


def expand(*args):
    return join('pentai', dirname(__file__), *args)

class CythonExtension(Extension):

    def __init__(self, *args, **kwargs):
        Extension.__init__(self, *args, **kwargs)
        self.cython_directives = {
            'c_string_encoding': 'utf-8',
            'profile': 'USE_PROFILE' in environ,
            'embedsignature': 'USE_EMBEDSIGNATURE' in environ}
        # XXX with pip, setuptools is imported before distutils, and change
        # our pyx to c, then, cythonize doesn't happen. So force again our
        # sources
        self.sources = args[1]


def merge(d1, *args):
    d1 = deepcopy(d1)
    for d2 in args:
        for key, value in d2.items():
            value = deepcopy(value)
            if key in d1:
                d1[key].extend(value)
            else:
                d1[key] = value
    return d1


def determine_base_flags():
    flags = {
        'libraries': [],
        'include_dirs': [],
        'extra_link_args': [],
        'extra_compile_args': []}
    if c_options['use_ios']:
        sysroot = environ.get('IOSSDKROOT', environ.get('SDKROOT'))
        if not sysroot:
            raise Exception('IOSSDKROOT is not set')
        flags['include_dirs'] += [sysroot]
        flags['extra_compile_args'] += ['-isysroot', sysroot]
        flags['extra_link_args'] += ['-isysroot', sysroot]
    elif platform == 'darwin':
        v = os.uname()
        if v[2] >= '13.0.0':
            # use xcode-select to search on the right Xcode path
            # XXX use the best SDK available instead of a specific one
            import platform as _platform
            xcode_dev = getoutput('xcode-select -p').splitlines()[0]
            sdk_mac_ver = '.'.join(_platform.mac_ver()[0].split('.')[:2])
            print('Xcode detected at {}, and using MacOSX{} sdk'.format(
                    xcode_dev, sdk_mac_ver))
            sysroot = join(xcode_dev.decode('utf-8'),
                    'Platforms/MacOSX.platform/Developer/SDKs',
                    'MacOSX{}.sdk'.format(sdk_mac_ver),
                    'System/Library/Frameworks')
        else:
            sysroot = ('/System/Library/Frameworks/'
                       'ApplicationServices.framework/Frameworks')
        flags['extra_compile_args'] += ['-F%s' % sysroot]
        flags['extra_link_args'] += ['-F%s' % sysroot]
    return flags


def determine_gl_flags():
    flags = {'libraries': []}
    if platform == 'win32':
        flags['libraries'] = ['opengl32']
    elif platform == 'ios':
        flags['libraries'] = ['GLESv2']
        flags['extra_link_args'] = ['-framework', 'OpenGLES']
    elif platform == 'darwin':
        flags['extra_link_args'] = ['-framework', 'OpenGL', '-arch', osx_arch]
        flags['extra_compile_args'] = ['-arch', osx_arch]
    elif platform.startswith('freebsd'):
        flags['include_dirs'] = ['/usr/local/include']
        flags['extra_link_args'] = ['-L', '/usr/local/lib']
        flags['libraries'] = ['GL']
    elif platform.startswith('openbsd'):
        flags['include_dirs'] = ['/usr/X11R6/include']
        flags['extra_link_args'] = ['-L', '/usr/X11R6/lib']
        flags['libraries'] = ['GL']
    elif platform == 'android':
        flags['include_dirs'] = [join(ndkplatform, 'usr', 'include')]
        flags['extra_link_args'] = ['-L', join(ndkplatform, 'usr', 'lib')]
        flags['libraries'] = ['GLESv2']
    elif platform == 'rpi':
        flags['include_dirs'] = ['/opt/vc/include',
            '/opt/vc/include/interface/vcos/pthreads',
            '/opt/vc/include/interface/vmcs_host/linux']
        flags['extra_link_args'] = ['-L', '/opt/vc/lib']
        flags['libraries'] = ['GLESv2']
    else:
        flags['libraries'] = ['GL']
    if c_options['use_glew']:
        if platform == 'win32':
            flags['libraries'] += ['glew32']
        else:
            flags['libraries'] += ['GLEW']
    return flags


def determine_sdl():
    flags = {}
    if not c_options['use_sdl']:
        return flags

    flags['libraries'] = ['SDL', 'SDL_ttf', 'freetype', 'z', 'bz2']
    flags['include_dirs'] = []
    flags['extra_link_args'] = []
    flags['extra_compile_args'] = []

    # Paths as per homebrew (modified formula to use hg checkout)
    if c_options['use_ios']:
        # Note: on IOS, SDL is already loaded by the launcher/main.m
        # So if we add it here, it will just complain about duplicate
        # symbol, cause libSDL.a would be included in main.m binary +
        # text_sdlttf.so
        # At the result, we are linking without SDL explicitly, and add
        # -undefined dynamic_lookup
        # (/tito)
        flags['libraries'] = ['SDL_ttf', 'freetype', 'bz2']
        flags['include_dirs'] += [
            join(kivy_ios_root, 'build', 'include'),
            join(kivy_ios_root, 'build', 'include', 'SDL'),
            join(kivy_ios_root, 'build', 'include', 'freetype')]
        flags['extra_link_args'] += [
            '-L', join(kivy_ios_root, 'build', 'lib'),
            '-undefined', 'dynamic_lookup']
    else:
        flags['include_dirs'] = ['/usr/local/include/SDL']
        flags['extra_link_args'] += ['-L/usr/local/lib/']

    if platform == 'ios':
        flags['extra_link_args'] += [
            '-framework', 'Foundation',
            '-framework', 'UIKit',
            '-framework', 'AudioToolbox',
            '-framework', 'CoreGraphics',
            '-framework', 'QuartzCore',
            '-framework', 'MobileCoreServices',
            '-framework', 'ImageIO']
    elif platform == 'darwin':
        flags['extra_link_args'] += [
            '-framework', 'ApplicationServices']
    return flags


base_flags = determine_base_flags()
gl_flags = determine_gl_flags()

sources = {
    'base/board_strip.pyx': base_flags,
    'base/direction_strips.pyx': base_flags,
    'base/board.pyx': base_flags,
    'base/game_state.pyx': base_flags,
    'base/bit_reverse.pyx': base_flags,
    'ai/length_lookup_table.pyx': base_flags,
    'ai/priority_filter.pyx': base_flags,
    'ai/priority_filter_2.pyx': base_flags,
    'ai/utility_stats.pyx': base_flags,
    'ai/utility_calculator.pyx': base_flags,
    'ai/alpha_beta.pyx': base_flags,
    'ai/ab_state.pyx': base_flags,
    }

if c_options['use_sdl']:
    sdl_flags = determine_sdl()
    sources['core/window/sdl.pyx'] = merge(
        base_flags, gl_flags, sdl_flags)
    sources['core/text/text_sdlttf.pyx'] = merge(
        base_flags, gl_flags, sdl_flags)
    sources['core/audio/audio_sdl.pyx'] = merge(
        base_flags, sdl_flags)

if platform in ('darwin', 'ios'):
    # activate ImageIO provider for our core image
    if platform == 'ios':
        osx_flags = {'extra_link_args': [
            '-framework', 'Foundation',
            '-framework', 'UIKit',
            '-framework', 'AudioToolbox',
            '-framework', 'CoreGraphics',
            '-framework', 'QuartzCore',
            '-framework', 'ImageIO',
            '-framework', 'Accelerate']}
    else:
        osx_flags = {'extra_link_args': [
            '-framework', 'ApplicationServices']}

if c_options['use_rpi']:
    sources['lib/vidcore_lite/egl.pyx'] = merge(
            base_flags, gl_flags)
    sources['lib/vidcore_lite/bcm.pyx'] = merge(
            base_flags, gl_flags)

if c_options['use_x11']:
    sources['core/window/window_x11.pyx'] = merge(
        base_flags, gl_flags, {
            # FIXME add an option to depend on them but not compile them
            # cause keytab is included in core, and core is included in
            # window_x11
            #
            #'depends': [
            #    'core/window/window_x11_keytab.c',
            #    'core/window/window_x11_core.c'],
            'libraries': ['Xrender', 'X11']})

if c_options['use_gstreamer']:
    sources['lib/gstplayer/_gstplayer.pyx'] = merge(
        base_flags, gst_flags, {
            'depends': ['lib/gstplayer/_gstplayer.h']})


# -----------------------------------------------------------------------------
# extension modules

def get_dependencies(name, deps=None):
    if deps is None:
        deps = []
    return deps


def resolve_dependencies(fn, depends):
    fn = basename(fn)
    deps = []
    get_dependencies(fn, deps)
    get_dependencies(fn.replace('.pyx', '.pxd'), deps)
    return [expand('graphics', x) for x in deps]


def get_extensions_from_sources(sources):
    ext_modules = []
    if environ.get('KIVY_FAKE_BUILDEXT'):
        print('Fake build_ext asked, will generate only .h/.c')
        return ext_modules
    for pyx, flags in sources.items():
        is_graphics = pyx.startswith('graphics')
        pyx = expand(pyx)
        depends = [expand(x) for x in flags.pop('depends', [])]
        if not have_cython:
            #pyx = '%s.c' % pyx[:-4]
            print pyx
            pyx = "%s.c" % ".".join(pyx.split('.')[:-1])
            print " -> %s" % pyx
        if is_graphics:
            depends = resolve_dependencies(pyx, depends)
        f_depends = [x for x in depends if x.rsplit('.', 1)[-1] in (
            'c', 'cpp', 'm')]
        module_name = get_modulename_from_file(pyx)
        flags_clean = {'depends': depends}
        for key, value in flags.items():
            if len(value):
                flags_clean[key] = value
        ext_modules.append(CythonExtension(module_name,
            [pyx] + f_depends, **flags_clean))
    return ext_modules

ext_modules = get_extensions_from_sources(sources)

# -----------------------------------------------------------------------------
# automatically detect data files
data_file_prefix = 'share/kivy-'
examples = {}
#examples_allowed_ext = ('readme', 'py', 'wav', 'png', 'jpg', 'svg', 'json',
#                        'avi', 'gif', 'txt', 'ttf', 'obj', 'mtl', 'kv')
examples_allowed_ext = ('readme', 'wav', 'png', 'jpg', 'svg', 'json',
                        'avi', 'gif', 'txt', 'ttf', 'obj', 'mtl', 'kv')
for root, subFolders, files in walk('examples'):
    for fn in files:
        ext = fn.split('.')[-1].lower()
        if ext not in examples_allowed_ext:
            continue
        filename = join(root, fn)
        directory = '%s%s' % (data_file_prefix, dirname(filename))
        if not directory in examples:
            examples[directory] = []
        examples[directory].append(filename)

'''
import pdb
pdb.set_trace()
'''

# -----------------------------------------------------------------------------
# setup !
setup(
    name='pentai',
    #author='Bruce Cropley',
    package_dir={'pentai': 'pentai'},
    ext_modules=ext_modules,
    #ext_modules=cythonize(sources.keys()),
    )

