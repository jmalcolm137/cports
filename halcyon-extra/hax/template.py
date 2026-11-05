pkgname = "hax"
pkgver = "0.6.1"
pkgrel = 0
build_style = "meson"
hostmakedepends = ["meson", "pkgconf"]
makedepends = ["curl-devel", "jansson-devel"]
checkdepends = ["python", "tmux"]
depends = ["ca-certificates"]
pkgdesc = "Minimalist terminal-native coding agent"
license = "MIT"
url = "https://github.com/OleksandrChekhovskyi/hax"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "de63efaadb9b71879b9a084a9e8aa863eb98e893b83c0a4ab8a465f97c8594e6"


def post_install(self):
    self.install_license("LICENSE")
