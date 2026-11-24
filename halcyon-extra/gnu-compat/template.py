pkgname = "gnu-compat"
pkgver = "0.1.0"
pkgrel = 0
build_style = "meta"
# The GNU tools that uutils does not implement are linked into /usr/gnulib
# below. GNU findutils is deliberately absent: uutils-findutils provides find,
# locate, updatedb and xargs in the overlay.
depends = [
    "bash",
    "diffutils",
    "gawk",
    "ggrep",
    "gm4",
    "gsed",
    "gtar",
    "uutils-coreutils",
    "uutils-findutils",
]
pkgdesc = "GNU userland for the uutils /usr/gnulib overlay"
license = "custom:meta"
url = "https://halcyon-linux.org"
broken_symlinks = [
    "usr/gnulib/awk",
    "usr/gnulib/cmp",
    "usr/gnulib/diff",
    "usr/gnulib/grep",
    "usr/gnulib/m4",
    "usr/gnulib/sed",
    "usr/gnulib/tar",
]
# no tests; the linked utilities come from the dependencies
options = ["!check"]


def install(self):
    self.install_dir("usr/gnulib")

    # uutils implements most of coreutils, but not these; link the GNU
    # implementations into the overlay so they are found before /usr/bin
    for name, target in {
        "awk": "gawk",
        "cmp": "gcmp",
        "diff": "gdiff",
        "grep": "ggrep",
        "m4": "gm4",
        "sed": "gsed",
        "tar": "gtar",
    }.items():
        self.install_link(f"usr/gnulib/{name}", f"../bin/{target}")
