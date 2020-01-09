#!/bin/sh

# Usage: ./make-git-snapshot.sh [COMMIT]
#
# to make a snapshot of the given tag/branch.  Defaults to HEAD.
# Point env var REF to a local mesa repo to reduce clone time.

DIRNAME=mesa-$( date +%Y%m%d )

if [ -x /usr/bin/pxz ]; then
    XZ=/usr/bin/pxz
else
    XZ=/usr/bin/xz
fi

echo REF ${REF:+--reference $REF}
echo DIRNAME $DIRNAME
echo HEAD ${1:-HEAD}

rm -rf $DIRNAME

git clone ${REF:+--reference $REF} \
	git://git.freedesktop.org/git/mesa/mesa $DIRNAME

GIT_DIR=$DIRNAME/.git git archive --format=tar --prefix=$DIRNAME/ ${1:-HEAD} \
	| $XZ > $DIRNAME.tar.xz

# rm -rf $DIRNAME
