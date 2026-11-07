pkgname = "bore"
pkgver = "0.6.0"
pkgrel = 0
build_style = "cargo"
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
pkgdesc = "Simple TCP tunnel that exposes local ports to a remote server"
license = "MIT"
url = "https://github.com/ekzhang/bore"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "ab3175a6f304c7efdcacd0f6a0e4950f49eb31cb2a3ae9b4928c97ed8d03861c"


def post_install(self):
    self.install_license("LICENSE")
