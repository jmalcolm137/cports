# halcyon-core packages

This category builds the packages for the `halcyon-core` APK repository:

```text
https://repo.halcyon-linux.org/halcyon-core
```

The repository is served from Cloudflare R2 behind that custom domain. APK
clients use the `v3` index (`Packages.adb`), so no `APKINDEX.tar.gz` cache
entry is involved.

## Prerequisites

- a working cbuild setup and signing key (`etc/config.ini` `[signing] key`)
- an rclone remote for the R2 bucket, by default `halcyon:halcyon-repo`
- network access to `repo.halcyon-linux.org`

The publish script is at the cports checkout root:

```sh
./publish-repo.sh
```

It reindexes the category with `cbuild index`, verifies the signed index,
uploads the `.apk` files first, and uploads `Packages.adb` and
`APKINDEX.tar.gz` last. It also uploads the public key. Package files are
uploaded with a one-year immutable cache header; the index is uploaded with
`Cache-Control: no-store`.

## Build and publish

Build one package:

```sh
./cbuild halcyon-core/<package>
```

Build a batch:

```sh
./cbuild -t bulk-pkg halcyon-core/<package> halcyon-core/<package>
```

Publish the category:

```sh
./publish-repo.sh halcyon-core
```

Dry run:

```sh
./publish-repo.sh -n halcyon-core
```

Useful environment variables:

```sh
ARCH=x86_64                 # default is apk --print-arch
REMOTE=halcyon:halcyon-repo # rclone remote and bucket
FORCE=1                     # re-upload packages even if rclone thinks they match
VERIFY=0                    # skip apk signature verification of the index
PURGE=1 CF_ZONE_ID=... CF_API_TOKEN=...  # purge the two index URLs
```

Debug sub-repository, if needed:

```sh
./publish-repo.sh halcyon-core/debug
```

## Important rules

- Never publish a different file under an existing `.apk` name. The CDN caches
  package filenames as immutable for a year. Bump `pkgrel` when rebuilding.
- Keep the signing key stable. Existing clients must already trust it.
- The index must stay uncached. The live/target repository configuration uses
  `v3` URLs and the script uploads the index with `no-store`; keep the
  Cloudflare cache rule that bypasses `/Packages.adb` and `/APKINDEX.tar.gz`.
- `publish-repo.sh` uses `rclone copy`, not `sync`; it does not delete old
  package versions from R2.

## Client configuration

The target repository configuration is packaged as:

```text
halcyon-repo-core      -> /etc/apk/repositories.d/20-halcyon-core.list
halcyon-repo-extra     -> /etc/apk/repositories.d/21-halcyon-extra.list
```

Both templates live in `halcyon-core`. The `halcyon-repo-core` package also
installs the Halcyon public key as
`/etc/apk/keys/halcyon-linux.rsa.pub`.
