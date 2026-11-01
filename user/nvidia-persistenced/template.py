pkgname = "nvidia-persistenced"
pkgver = "595.112.07"
pkgrel = 0
build_style = "makefile"
make_install_args = ["DO_STRIP="]
make_use_env = True
hostmakedepends = ["pkgconf"]
makedepends = ["libtirpc-devel"]
pkgdesc = "NVIDIA driver persistence daemon"
license = "MIT"
url = "https://www.nvidia.com/en-us/drivers/unix"
source = f"https://github.com/NVIDIA/nvidia-persistenced/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "3333e30da22916e3e9271cb99ed8cc8f9f9576deeb4fa61822fc871736a5cd3d"
# no test suite
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
