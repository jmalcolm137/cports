pkgname = "uutils-findutils"
pkgver = "0.11.0"
pkgrel = 1
build_style = "cargo"
hostmakedepends = ["cargo-auditable", "pkgconf"]
# cbuild links the onig crate against the system oniguruma
makedepends = ["oniguruma-devel", "rust-std"]
pkgdesc = "GNU findutils in Rust"
license = "MIT"
url = "https://github.com/uutils/findutils"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "43d1fbb69a0e67e708435bd104966d1dd61357755452b733db9dabfd66cbf974"
# the binaries go into the uutils overlay, not /usr/bin
skip_providers = ["usr/gnubin"]
# the test suite covers the whole GNU behaviour matrix and is very slow
options = ["!check"]


def install(self):
    from cbuild.util import cargo

    for name in ["find", "locate", "updatedb", "xargs"]:
        self.install_file(
            cargo.target_path(self, name),
            "usr/gnubin",
            name=name,
            mode=0o755,
        )

    self.install_license("LICENSE")
