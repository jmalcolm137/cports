pkgname = "sparted"
pkgver = "0.1.0"
pkgrel = 0
pkgdesc = "LibGUI/GParted port for the Serenity Desktop Environment"
license = "GPL-2.0-or-later"
url = "https://github.com/jmalcolm137/sparted"

_commit = "56ca30e39a3508a6e4fcf62c330179e1f19ee3da"

hostmakedepends = ["gmake"]
makedepends = [
    "parted-devel",
    "serenity-lagom-devel",
]
depends = [
    "serenity-lagom",
    "polkit",
    "util-linux",
    "e2fsprogs",
    "dosfstools",
    "exfatprogs",
    "ntfs-3g",
    "btrfs-progs",
    "xfsprogs",
    "f2fs-tools",
    "jfsutils",
    "lvm2",
    "hfsutils",
]

# libwindowserver.so does not carry a SONAME
ignore_shlibs = ["libwindowserver.so"]

# the project requires C++26 and is built without exceptions
tool_flags = {
    "CXXFLAGS": ["-std=c++26", "-fno-exceptions", "-Wno-literal-suffix"],
}

# the UI tests need a compositor and the backend tests expect a full userland
options = ["!check"]

source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "951cfdf0c604833c60f6c7f398ea74eb686de6e40eab5adc37498f8707015a42"


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
        "build/sparted", "usr/lib/sde/bin", name="sparted.real", mode=0o755
    )
    self.install_file(self.files_path / "sparted", "usr/lib/sde/bin", mode=0o755)
    self.install_dir("usr/bin")
    self.install_link("usr/bin/sparted", "../lib/sde/bin/sparted")

    self.install_file(
        "res/sparted.desktop", "usr/share/applications", mode=0o644
    )
    for size in (16, 32, 64, 128, 256):
        self.install_file(
            f"res/icons/hicolor/{size}x{size}/apps/sparted.png",
            f"usr/share/icons/hicolor/{size}x{size}/apps",
            mode=0o644,
        )
