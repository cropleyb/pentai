#!/bin/bash -x

. $(dirname $0)/environment.sh

cd $TMPROOT

mkdir -p bciosbuild bcinst

PKGS="transaction BTrees persistent zc.lockfile ZConfig zdaemon zope.event zope.interface zope.proxy zope.testing six zodb zc.zlibstorage"

# Download (build, install, clean)
# bypass download
#for p in 
for p in $PKGS
do
    # Hack due to lack of openssl in $HOSTPYTHON:
    # Use easy_install to download and build all ZODB dependencies, then clean
    # them so they can be built for iOS
    #echo "Processing $p"
    python ./setuptools-3.4.4/easy_install.py --build-directory ./bciosbuild --always-copy --install-dir ./bcinst $p 
    pushd bciosbuild/$p
    python ./setup.py clean
    popd
done

# Ignore errors from patches
patch -d $TMPROOT/bciosbuild/btrees/BTrees -p1 < $KIVYIOSROOT/tools/patches/btree.patch || true
patch -d $TMPROOT/bciosbuild/persistent -p0 < $KIVYIOSROOT/tools/patches/persistent.patch || true

# build 
OLD_CC="$CC"
OLD_CFLAGS="$CFLAGS"
OLD_LDFLAGS="$LDFLAGS"
OLD_LDSHARED="$LDSHARED"
export CC="$ARM_CC -I$BUILDROOT/include -I$BUILDROOT/include/freetype"
export CFLAGS="$ARM_CFLAGS"
export LDFLAGS="$ARM_LDFLAGS"
export LDSHARED="$KIVYIOSROOT/tools/liblink"

for p in $PKGS
do
	pushd bciosbuild/$p
    try $HOSTPYTHON ./setup.py clean
    try $HOSTPYTHON ./setup.py build_ext -g
    try $HOSTPYTHON setup.py install -O2 --root iosbuild
    #find iosbuild | grep -E '.*\.(py|pyc|so\.o|so\.a|so\.libs|.pth|.egg-info)$$' | xargs rm
    try cp -a iosbuild/usr/local/lib/python2.7/site-packages/* "$BUILDROOT/python/lib/python2.7/site-packages"
    cd $BUILDROOT/python/lib/python2.7/site-packages
	p_path=`echo $p | sed 's/\./\//g'`
    zip -r ../../python27.zip $p_path
	popd
done


export CC="$OLD_CC"
export CFLAGS="$OLD_CFLAGS"
export LDFLAGS="$OLD_LDFLAGS"
export LDSHARED="$OLD_LDSHARED"


#bd=$TMPROOT/$ZDB/build/lib.macosx-*
bds=$TMPROOT/bciosbuild/*/build/lib.macosx-*/*/
try $KIVYIOSROOT/tools/biglink $BUILDROOT/lib/libzodb.a $bds
deduplicate $BUILDROOT/lib/libzodb.a
