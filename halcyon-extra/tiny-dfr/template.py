pkgname = "tiny-dfr"
pkgver = "0.3.8"
pkgrel = 0
archs = ["x86_64", "aarch64"]
build_style = "cargo"
hostmakedepends = ["cargo-auditable", "pkgconf"]
makedepends = [
    "cairo-devel",
    "dinit-chimera",
    "fontconfig-devel",
    "freetype-devel",
    "libdrm-devel",
    "libinput-devel",
    "librsvg-devel",
    "rust-std",
    "udev-devel",
]
pkgdesc = "Touch Bar daemon for Apple T2 and Apple Silicon Macs"
license = "MIT AND Apache-2.0"
url = "https://github.com/AsahiLinux/tiny-dfr"
_commit = "a79f2f43e6c6a9b855968e54eb243c20642ebc89"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "3f8f7f3889f3039b4c5e347b4481fcc5383d1655781050debcc9de623d2875f8"
# no test suite
options = ["!check"]


def post_install(self):
    self.install_license("LICENSE")
    self.install_license("LICENSE.material", name="LICENSE.material")
    self.install_files("share/tiny-dfr", "usr/share")
    self.install_file(
        "etc/udev/rules.d/99-touchbar-seat.rules",
        "usr/lib/udev/rules.d",
    )
    self.install_file(
        "etc/udev/rules.d/99-touchbar-tiny-dfr.rules",
        "usr/lib/udev/rules.d",
    )
    self.install_file(
        self.files_path / "tiny-dfr-run", "usr/lib/tiny-dfr", mode=0o755
    )
    self.install_service(self.files_path / "tiny-dfr", enable=True)
