#!/bin/bash
LIBX11HASH_VERSION="ecdf417847601ae74a3ed1a2b787c80a22264a3d"
# ^ tag v1.4.1

set -e

. $(dirname "$0")/build_tools_util.sh || (echo "Could not source build_tools_util.sh" && exit 1)

here="$(dirname "$(realpath "$0" 2> /dev/null || grealpath "$0")")"
CONTRIB="$here"
PROJECT_ROOT="$CONTRIB/.."

pkgname="libx11hash"
info "Building $pkgname..."

(
    cd "$CONTRIB"
    if [ ! -d libx11hash2 ]; then
        git clone https://github.com/zebra-lucky/x11_hash.git libx11hash2
    fi
    cd libx11hash2
    if ! $(git cat-file -e ${LIBX11HASH_VERSION}) ; then
        info "Could not find requested version $LIBX11HASH_VERSION in local clone; fetching..."
        git init
        git fetch --depth 1 origin $LIBX11HASH_VERSION
    fi
    git reset --hard
    git clean -dfxq
    git checkout "${LIBX11HASH_VERSION}^{commit}"

    # add reproducible randomness.
    echo -e "\nconst char *kiiro_electrum_tag" \
            " = \"tagged by Kiiro-Electrum@$LIBX11HASH_VERSION\";" \
            >> ./x11hash.c
    autoreconf -fi || fail "Could not run autoreconf."
    make "-j$CPU_COUNT" || fail "Could not build $pkgname"
    make install || warn "Could not install $pkgname"
    . "$here/$pkgname/libx11hash/.libs/libx11hash-1.0.la"
    host_strip "$here/$pkgname/libx11hash/.libs/$dlname"
    TARGET_NAME="$dlname"
    if [ $(uname) == "Darwin" ]; then  # on mac, dlname is "libx11hash-1.0.0.dylib"
        TARGET_NAME="libx11hash-1.0.dylib"
    fi
    cp -fpv "$here/$pkgname/libx11hash/.libs/$dlname" "$PROJECT_ROOT/electrum/$TARGET_NAME" || fail "Could not copy the $pkgname binary to its destination"
    info "$TARGET_NAME has been placed in the inner 'electrum' folder."
    if [ -n "$DLL_TARGET_DIR" ] ; then
        cp -fpv "$here/$pkgname/libx11hash/.libs/$dlname" "$DLL_TARGET_DIR/$TARGET_NAME" || fail "Could not copy the $pkgname binary to DLL_TARGET_DIR"
    fi
)
