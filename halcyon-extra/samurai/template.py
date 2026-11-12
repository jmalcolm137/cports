pkgname = "samurai"
pkgver = "1.3"
pkgrel = 0
build_style = "makefile"
pkgdesc = "Ninja-compatible build tool"
license = "ISC"
url = "https://github.com/michaelforney/samurai"
source = f"{url}/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "44ff119a27b343ec47a797fa8701c19b9e672230bc15f3c6a6cede9641ea6332"
# no test suite
options = ["!check"]


def post_install(self):
    self.install_license("LICENSE")
