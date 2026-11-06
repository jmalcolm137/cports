pkgname = "uutils-coreutils"
pkgver = "0.12.0"
pkgrel = 2
build_style = "cargo"
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
depends = [
    "bash",
    "diffutils",
    "findutils",
    "gawk",
    "ggrep",
    "gm4",
    "gsed",
    "gtar",
]
pkgdesc = "GNU coreutils in Rust, with a GNU userland PATH overlay"
license = "MIT"
url = "https://github.com/uutils/coreutils"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "4fb327655cb4ffcbf2f16550cf9234079ffe839692f7aa1a6eda104af684e122"
# these links point at binaries provided by the packages above
broken_symlinks = [
    "usr/bin/gnu/awk",
    "usr/bin/gnu/cmp",
    "usr/bin/gnu/diff",
    "usr/bin/gnu/find",
    "usr/bin/gnu/grep",
    "usr/bin/gnu/m4",
    "usr/bin/gnu/sed",
    "usr/bin/gnu/tar",
    "usr/bin/gnu/xargs",
]
# the overlay directory is not a command
skip_providers = ["usr/bin/gnu"]
# the test suite expects a complete userland and takes a very long time
options = ["etcfiles", "!check"]


def _make_env(self):
    from cbuild.util import cargo

    env = cargo.get_environment(self, cache=False)
    env["CARGO_NET_OFFLINE"] = "true"
    return env


def build(self):
    # build the multicall binary with every utility enabled
    self.do(
        "make",
        "build-coreutils",
        "PROFILE=release",
        "MULTICALL=y",
        "CARGOFLAGS=--locked",
        f"-j{self.make_jobs}",
        env=_make_env(self),
    )


def install(self):
    self.install_license("LICENSE")

    self.do(
        "make",
        "install",
        "PROFILE=release",
        "MULTICALL=y",
        "LN=ln -sf",
        "PREFIX=/usr",
        "BINDIR=/usr/bin/gnu",
        # the binary looks for locales next to itself first
        "DATAROOTDIR=/usr/bin/gnu",
        "MANPAGES=n",
        "COMPLETIONS=n",
        "CARGOFLAGS=--locked",
        f"DESTDIR={self.chroot_destdir}",
        f"-j{self.make_jobs}",
        env=_make_env(self),
    )

    # GNU implementations of the utilities that collide with chimerautils
    for name, target in {
        "awk": "gawk",
        "cmp": "gcmp",
        "diff": "gdiff",
        "find": "gfind",
        "grep": "ggrep",
        "m4": "gm4",
        "sed": "gsed",
        "tar": "gtar",
        "xargs": "gxargs",
    }.items():
        self.install_link(f"usr/bin/gnu/{name}", f"../{target}")

    # prepend the overlay to PATH for regular (non-system) users
    self.install_file(
        self.files_path / "00-gnu-path.sh", "etc/profile.d", mode=0o644
    )
