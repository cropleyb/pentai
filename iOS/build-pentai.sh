#!/bin/bash -x

. $(dirname $0)/environment.sh

PROJ=pente
EXTSRC=$KIVYIOSROOT/src/$PROJ
mkdir -p $EXTSRC
pushd ~/Dropbox/$PROJ
try ./copy_to.sh $EXTSRC
popd
pushd $EXTSRC

# TODO: cp other py files

OLD_CC="$CC"
OLD_CFLAGS="$CFLAGS"
OLD_LDFLAGS="$LDFLAGS"
OLD_LDSHARED="$LDSHARED"
export CC="$ARM_CC -I$BUILDROOT/include"
export CFLAGS="$ARM_CFLAGS"
export LDFLAGS="$ARM_LDFLAGS"
export LDSHARED="$KIVYIOSROOT/tools/liblink"

# iOS cythonize
echo "PRE-CYTHONIXE"
# TODO specified .py
find . -name "*.pyx" -exec $KIVYIOSROOT/tools/cythonize.py {} \;
echo "POST-CYTHONIXE"

# Build cython module
#HOSTPYTHON=$TMPROOT/Python-$IOS_PYTHON_VERSION/hostpython
echo "BEFORE BUILD1"
try $HOSTPYTHON ./setup.py build_ext -g
echo "BETWEEN BUILDS"
try $HOSTPYTHON ./setup.py install -O2 --root iosbuild
echo "AFTER BUILDS"

# Look for built targets
try find iosbuild | grep -E '.*\.(py|pyc|so\.o|so\.a|so\.libs)$$' | xargs rm
try rm -rdf "$BUILDROOT/python/lib/python2.7/site-packages/$PROJ*"

# Copy to python for iOS installation
#try cp -R "iosbuild/usr/local/lib/python2.7/site-packages/" "$BUILDROOT/python/lib/python2.7/site-packages"
#try find "iosbuild/usr/local/lib/python2.7/site-packages/" -name "*.so" | xargs cp "$BUILDROOT/python/lib/python2.7/site-packages"
try cp -R "iosbuild/usr/local/lib/python2.7/site-packages/pentai" "$BUILDROOT/python/lib/python2.7/site-packages"
popd

export CC="$OLD_CC"
export CFLAGS="$OLD_CFLAGS"
export LDFLAGS="$OLD_LDFLAGS"
export LDSHARED="$OLD_LDSHARED"

bd=$EXTSRC/build/lib.macosx-*
#try $KIVYIOSROOT/tools/biglink $BUILDROOT/lib/libpente.a $bd
try $KIVYIOSROOT/tools/biglink $BUILDROOT/lib/libpente.a $bd $bd/pentai/base $bd/pentai/ai
deduplicate $BUILDROOT/lib/libpente.a
