pkgname = "vmaf"
pkgver = "3.2.1"
pkgrel = 0
build_style = "meson"
configure_args = [
    "-Denable_avx512=false",
    "-Denable_docs=false",
]
meson_dir = "libvmaf"
hostmakedepends = [
    "meson",
    "nasm",
    "pkgconf",
    "vim-xxd",
]
pkgdesc = "Perceptual video quality assessment based on multi-method fusion"
license = "BSD-2-Clause-Patent"
url = "https://github.com/Netflix/vmaf"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "5df7386911bc15fd1ca783132528748d219768ae4fc5f8e0b61184f041648092"


def post_install(self):
    self.install_files("model", "usr/share/vmaf")
    self.install_license("LICENSE")


@subpackage("vmaf-devel")
def _(self):
    return self.default_devel()
