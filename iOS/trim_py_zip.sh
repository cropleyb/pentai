#!/bin/bash -x

pushd ../build/python/lib/

PZ=python27.zip
if [ ! -e "$PZ" ];
then
	echo "No zipfile $PZ to operate on"
	exit 1
fi

if [ ! -e "$PZ.orig" ]; then
	echo "Copy $PZ to .orig"
	cp $PZ $PZ.orig
fi

zip -d python27.zip "*xml*" "*pydoc*" "*tarfile*" "*wininst*" "tarfile*" "mailbox*""plat-mac*" "decimal*" "distutils*"
zip -d python27.zip smtplib.pyo aifc.pyo rfc822.pyo ftplib.pyo mhlib.pyo 
zip -d python27.zip httplib.pyo 
zip -d python27.zip imaplib.pyo "compiler*" locale.pyo cookielib.pyo optparse.pyo difflib.pyo argparse.pyo
zip -d python27.zip "*sql*"
zip -d python27.zip "*plat-mac*" "*mail*" "*scripts*"
zip -d python27.zip "*test*" # This will be a problem when I want to run 
							 # the unittests

# ZODB 
zip -d python27.zip "*.rej" "*.py" "*.pyc" "*.c" "*.so.libs" "*.so.o"
zip -d python27.zip "*.txt" "*.h" "*.so"

popd
