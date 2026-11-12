#!/bin/sh

# Only exported symbols matter; hidden globals are fine (they are not part of
# the libc ABI). Use readelf so we can distinguish default and hidden
# visibility, unlike `nm` which shows both as uppercase.
symbols=$(
    readelf -sW "$1" |
        awk '$4 == "FUNC" || $4 == "OBJECT" {
            if ($5 == "GLOBAL" && $6 == "DEFAULT") print $8
        }'
)

bad=0
for name in $symbols; do
    case "$name" in
        # glue symbols
        __libc_*|__malloc_*) ;;
        # compiler-generated
        .L*) ;;
        # directly provided api
        aligned_alloc|malloc_usable_size) ;;
        # mimalloc heaps
        _mi_theap_empty|_mi_theap_main|_mi_heap_empty|_mi_heap_main) ;;
        *)
            echo "unexpected symbol $name"
            bad=1
            ;;
    esac
done

exit $bad
