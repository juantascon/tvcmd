#! /bin/bash

clean() {
    rm -rf MANIFEST $(find -name "__pycache__") dist distros/arch/{tvcmd*,pkg,src}
}

case "$1" in
    "-c") clean;;
    *) VER="$1";;
esac

if [ -z "$VER" ]; then
    exit
fi

echo "configuring for version: $VER"
pushd $(dirname $0)/..

clean

sed -i "s/version=.*/version=\"$VER\",/g" setup.py

# distribute to sf.net
./setup.py sdist
scp ./dist/tvcmd-$VER.tar.gz juantascon,tvcmd@frs.sourceforge.net:/home/frs/project/t/tv/tvcmd/
scp ./TODO juantascon,tvcmd@frs.sourceforge.net:/home/frs/project/t/tv/tvcmd/README

# arch dist
pushd distros/arch
sed -i "s/pkgver=.*/pkgver=$VER/g" PKGBUILD
sed -i "s/^md5sums=.*//g" PKGBUILD
makepkg -g >> PKGBUILD
sed -i '$!N; /^\(.*\)\n\1$/!P; D' ./PKGBUILD # similar to uniq
makepkg --source
aurup ./tvcmd-$VER-1.src.tar.gz multimedia
popd

clean

popd

