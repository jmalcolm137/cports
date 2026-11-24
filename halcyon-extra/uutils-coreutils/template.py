pkgname = "uutils-coreutils"
pkgver = "0.13.0"
pkgrel = 0
build_style = "cargo"
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
pkgdesc = "GNU coreutils in Rust"
license = "MIT"
url = "https://github.com/uutils/coreutils"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "5830c023555ea8e98505e8cfb09524d3097f427c5e58ef197a943e6cb73af9b0"
# the overlay directory is not a command
skip_providers = ["usr/gnulib"]
# the test suite expects a complete userland and takes a very long time
options = ["!check"]


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

    # Only the Rust utilities are installed, into the uutils overlay that
    # base-files puts on PATH. The GNU counterparts and the links for the
    # utilities uutils does not implement are provided by gnu-compat.
    self.do(
        "make",
        "install",
        "PROFILE=release",
        "MULTICALL=y",
        "LN=ln -sf",
        "PREFIX=/usr",
        "BINDIR=/usr/gnulib",
        # the binary looks for locales next to itself first
        "DATAROOTDIR=/usr/gnulib",
        "MANPAGES=n",
        "COMPLETIONS=n",
        "CARGOFLAGS=--locked",
        f"DESTDIR={self.chroot_destdir}",
        f"-j{self.make_jobs}",
        env=_make_env(self),
    )
