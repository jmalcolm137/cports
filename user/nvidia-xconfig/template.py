pkgname = "nvidia-xconfig"
pkgver = "595.112.07"
pkgrel = 0
build_style = "makefile"
make_install_args = ["DO_STRIP="]
make_use_env = True
hostmakedepends = ["pkgconf"]
makedepends = ["libpciaccess-devel"]
pkgdesc = "NVIDIA xorg.conf configurator"
license = "GPL-2.0-or-later"
url = "https://www.nvidia.com/en-us/drivers/unix"
source = f"https://github.com/NVIDIA/nvidia-xconfig/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "c3c34920e1111fbfdecc202e694ef01b6a5965e81d2c7c47b8ad9a16446168dc"
# no test suite
options = ["!check"]
