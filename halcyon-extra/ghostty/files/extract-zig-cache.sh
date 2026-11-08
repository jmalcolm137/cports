#!/bin/sh
set -e

cache="${1:-.zig-cache-fetch/p}"

for f in "$cache"/*.tar.gz; do
    [ -e "$f" ] || continue

    hash="$(basename "$f" .tar.gz)"
    tmp="$(mktemp -d)"

    tar -xzf "$f" -C "$tmp"

    top="$tmp/$hash"
    if [ ! -d "$top" ]; then
        echo "missing top-level directory for $hash" >&2
        exit 1
    fi

    # The cached archive wraps the package in a directory named after its
    # hash. Zig strips a single top-level directory when unpacking a package,
    # so do the same here; otherwise keep the archive root.
    set -- "$top"/*
    if [ "$#" -eq 1 ] && [ -d "$1" ]; then
        root="$1"
    else
        root="$top"
    fi

    rm -rf "$cache/$hash"
    mkdir -p "$cache/$hash"
    cp -a "$root"/. "$cache/$hash"/
    rm -rf "$tmp"
    rm -f "$f"
done
