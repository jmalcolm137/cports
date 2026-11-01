pkgname = "nvidia-settings"
pkgver = "615.78.08"
pkgrel = 0
build_style = "makefile"
make_install_args = ["-j1", "DO_STRIP="]
make_use_env = True
hostmakedepends = ["pkgconf"]
makedepends = [
    "gtk+3-devel",
    "libglvnd-devel",
    "libvdpau-devel",
    "libx11-devel",
    "libxv-devel",
    "libxxf86vm-devel",
    "vulkan-loader-devel",
]
pkgdesc = "NVIDIA settings utility"
license = "GPL-2.0-or-later"
url = "https://www.nvidia.com/en-us/drivers/unix"
source = f"https://github.com/NVIDIA/nvidia-settings/archive/refs/tags/{pkgver}.tar.gz"
sha256 = "121ddd3ef54c2eeefe97fba2739d25b24cdaaa01793c67af63f23fb3fae9f693"
tool_flags = {"CFLAGS": ["-Wno-single-bit-bitfield-constant-conversion"]}
# no test suite
options = ["!check"]


def post_install(self):
    self.install_file(
        "doc/nvidia-settings.png", "usr/share/icons/hicolor/128x128/apps"
    )
    self.install_file("doc/nvidia-settings.desktop", "usr/share/applications")
