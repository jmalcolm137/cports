pkgname = "halcyon-setup"
pkgver = "0.1.0"
pkgrel = 15
# Update this to the release commit when publishing the package. The r11
# patches were merged into the source tree, so the package now builds directly
# from the commit below.
_commit = "2308b5569d55c8cc51370df4117e34a70f5009f3"
hostmakedepends = ["gmake"]
makedepends = [
    "serenity-lagom-devel",
]
depends = [
    "bcachefs-tools",
    "btrfs-progs",
    "chimera-install-scripts",
    "dosfstools",
    "e2fsprogs",
    "exfatprogs",
    "f2fs-tools",
    "kmod",
    "ntfs-3g",
    "parted",
    "polkit",
    "serenity-lagom",
    "shadow",
    "sparted",
    "tzdb",
    "util-linux",
    "xfsprogs",
]
match self.profile.arch:
    case "x86_64":
        depends += [
            "grub-i386-pc",
            "grub-x86_64-efi",
            "limine",
            "firmware-apple",
        ]
    case "aarch64":
        depends += ["grub-arm64-efi", "limine", "firmware-apple"]
    case "riscv64":
        depends += ["grub-riscv64-efi", "limine"]
    case "ppc" | "ppc64" | "ppc64le":
        depends += ["grub-powerpc-ieee1275"]
# libwindowserver.so is installed as part of the SDE prefix and does not carry
# a SONAME.
ignore_shlibs = ["libwindowserver.so"]
pkgdesc = "Windows 95-style installation wizard for Halcyon Linux"
license = "BSD-2-Clause"
url = "https://github.com/jmalcolm137/halcyon-setup"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = ["d639c58f279a1e6c36b84f518570af00abb3d0025195de6321b5ced099f65d4e"]
# The GUI has no automated test suite; cross builds are not supported.
options = ["!check", "!cross", "etcfiles"]
# The project needs C++26 and is built without exceptions.
tool_flags = {
    "CXXFLAGS": ["-std=c++26", "-fno-exceptions", "-Wno-literal-suffix"],
}


def build(self):
    self.do(
        "make",
        f"-j{self.make_jobs}",
        "LAGOM=/usr/lib/sde",
        "SERENITY=/usr/lib/sde/framework/serenity",
        env={
            "CPPFLAGS": (
                "-I/usr/lib/sde/framework "
                "-I/usr/lib/sde/framework/Userland/Libraries "
                "-I/usr/lib/sde/framework/Userland/Services"
            ),
        },
    )


def install(self):
    self.install_license("LICENSE")

    self.install_file(
        "build/halcyon-setup",
        "usr/lib/sde/bin",
        name="halcyon-setup.real",
        mode=0o755,
    )
    self.install_file(
        "res/halcyon-setup", "usr/bin", name="halcyon-setup", mode=0o755
    )

    self.install_file(
        "res/halcyon-setup.desktop", "usr/share/applications", mode=0o644
    )
    self.install_file(
        "res/HalcyonSetup.desktop", "usr/share/applications", mode=0o644
    )
    self.install_file(
        self.files_path / "desktop-launcher",
        "etc/skel/Desktop",
        name="Install Halcyon Linux",
        mode=0o755,
    )

    self.install_file(
        "res/world-map.png", "usr/share/halcyon-setup", mode=0o644
    )
    self.install_file(
        "res/world-map.README",
        "usr/share/doc/halcyon-setup",
        name="world-map.README",
        mode=0o644,
    )

    for size in (16, 24, 32, 48, 64, 128, 256):
        self.install_file(
            f"res/icons/hicolor/{size}x{size}/apps/halcyon-setup.png",
            f"usr/share/icons/hicolor/{size}x{size}/apps",
            mode=0o644,
        )
