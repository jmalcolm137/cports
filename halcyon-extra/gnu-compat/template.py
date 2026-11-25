pkgname = "gnu-compat"
pkgver = "0.1.0"
pkgrel = 2
build_style = "meta"
# The GNU tools that uutils does not implement are linked into /usr/gnubin
# below. GNU findutils is deliberately absent: uutils-findutils provides find,
# locate, updatedb and xargs in the /usr/gnubin overlay.
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
pkgdesc = "GNU userland for the uutils /usr/gnubin overlay"
license = "custom:meta"
url = "https://halcyon-linux.org"
broken_symlinks = [
    "usr/gnubin/awk",
    "usr/gnubin/cmp",
    "usr/gnubin/diff",
    "usr/gnubin/grep",
    "usr/gnubin/m4",
    "usr/gnubin/sed",
    "usr/gnubin/tar",
]
# no tests; the linked utilities come from the dependencies
options = ["!check"]


def install(self):
    self.install_dir("usr/gnubin")

    # uutils implements most of coreutils, but not these; link the GNU
    # implementations into the compatibility directory
    for name, target in {
        "awk": "gawk",
        "cmp": "gcmp",
        "diff": "gdiff",
        "grep": "ggrep",
        "m4": "gm4",
        "sed": "gsed",
        "tar": "gtar",
    }.items():
        self.install_link(f"usr/gnubin/{name}", f"../bin/{target}")
