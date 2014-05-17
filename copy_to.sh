#!/bin/bash

try () {
	"$@" || exit -1
}

DESTDIR=$1

mkdir -p $DESTDIR
rsync -ra pentai* setup.py main.py $DESTDIR


