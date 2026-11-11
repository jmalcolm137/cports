pkgname = "t2fanrd"
pkgver = "0.1.0"
pkgrel = 0
archs = ["x86_64"]
build_style = "cargo"
hostmakedepends = ["cargo-auditable"]
makedepends = ["dinit-chimera", "rust-std"]
pkgdesc = "Fan control daemon for Apple T2 Macs"
license = "GPL-3.0-or-later"
url = "https://github.com/GnomedDev/T2FanRD"
_commit = "48baf962697ec3d4d969c74cf601ee8e15b7aeaa"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "33cd1644bd7602587b0d486a4396de6bdaae3d704d91e1e762604980beaa6e84"
# no test suite
options = ["!check"]


def post_install(self):
    self.install_license("LICENCE")
    self.install_file(
        self.files_path / "t2fanrd-run", "usr/lib/t2fanrd", mode=0o755
    )
    self.install_service(self.files_path / "t2fanrd", enable=True)
