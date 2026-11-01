pkgname = "nvidia-modprobe"
pkgver = "615.78.08"
pkgrel = 0
build_style = "makefile"
make_install_args = ["DO_STRIP="]
make_use_env = True
hostmakedepends = ["pkgconf"]
makedepends = ["linux-headers"]
pkgdesc = "NVIDIA modprobe helper"
license = "GPL-2.0-or-later"
url = "https://www.nvidia.com/en-us/drivers/unix"
source = f"https://github.com/NVIDIA/nvidia-modprobe/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "9849cdef0162a3d54f82cf5eeaaab7498c30586de1121077276b0fb0c9ea920e"
file_modes = {"usr/bin/nvidia-modprobe": ("root", "root", 0o4755)}
# no test suite
options = ["!check"]
