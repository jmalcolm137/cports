pkgname = "sparted"
pkgver = "0.1.0"
pkgrel = 1
_commit = "ddcf069b8aa9bc9aeb59d9fd1306697e1a076410"
hostmakedepends = ["gmake"]
makedepends = [
    "parted-devel",
    "serenity-lagom-devel",
]
depends = [
    "btrfs-progs",
    "dosfstools",
    "e2fsprogs",
    "exfatprogs",
    "f2fs-tools",
    "hfsutils",
    "jfsutils",
    "lvm2",
    "ntfs-3g",
    "polkit",
    "serenity-lagom",
    "util-linux",
    "xfsprogs",
]
# libwindowserver.so does not carry a SONAME
ignore_shlibs = ["libwindowserver.so"]
pkgdesc = "LibGUI/GParted port for the Serenity Desktop Environment"
license = "GPL-2.0-or-later"
url = "https://github.com/jmalcolm137/sparted"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "9db2ef074333f8995d9fe10b220bc026c6054fdd838a5a1be0c5d6d0c8c0ffce"
# the project requires C++26 and is built without exceptions
tool_flags = {
    "CXXFLAGS": ["-std=c++26", "-fno-exceptions", "-Wno-literal-suffix"],
}
# the UI tests need a compositor and the backend tests expect a full userland
options = ["!check"]


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
        "build/sparted",
        "usr/lib/sde/bin",
        name="PartitionEditor.real",
        mode=0o755,
    )
    self.install_file(
        self.files_path / "PartitionEditor", "usr/lib/sde/bin", mode=0o755
    )
    self.install_dir("usr/bin")
    self.install_link(
        "usr/bin/PartitionEditor", "../lib/sde/bin/PartitionEditor"
    )
    self.install_link("usr/bin/sparted", "../lib/sde/bin/PartitionEditor")

    self.install_file(
        "res/PartitionEditor.desktop", "usr/share/applications", mode=0o644
    )
    for size in (16, 32, 64, 128, 256):
        self.install_file(
            f"res/icons/hicolor/{size}x{size}/apps/sparted.png",
            f"usr/share/icons/hicolor/{size}x{size}/apps",
            name="PartitionEditor.png",
            mode=0o644,
        )
