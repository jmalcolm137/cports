pkgname = "torrhunt"
pkgver = "2.2.0"
pkgrel = 0
archs = ["x86_64", "aarch64"]
hostmakedepends = [
    "clang",
    "patchelf",
    "pkgconf",
    "squashfs-tools",
]
makedepends = [
    "libgcc-chimera",
    "qt6-qtbase-devel",
    "qt6-qtwebengine-devel",
]
depends = ["gcompat"]
ignore_shlibs = ["libc.so.6", "ld-linux-aarch64.so.1"]
pkgdesc = "Torrent search engine and browser"
license = "custom:torrhunt"
url = "https://ktechpit.com/USS/public/product.php?slug=torrhunt"
_snap_id = "SkflXvnUfQ4KFuN0nAos1ykmgwZf0Ujl"
_snap_rev = {"x86_64": "34", "aarch64": "35"}
_snap_sha = {
    "x86_64": "3fbd013c84d4f9a24cf336225230b39ffcd12b5923165f4ebb66e2a9dafdb118",
    "aarch64": "dc5271a0e1521c06fb61b9d74dff3efd242ea1524ca1fd3536ce4ce019a18b23",
}
source = (
    "!https://api.snapcraft.io/api/v1/snaps/download/"
    f"{_snap_id}_{_snap_rev.get(self.profile.arch, '34')}.snap>torrhunt.snap"
)
sha256 = _snap_sha.get(self.profile.arch, _snap_sha["x86_64"])
# prebuilt binary, no test suite, no license file, not cross-compilable
options = ["!check", "!cross", "!distlicense", "!strip"]


def post_patch(self):
    self.do(
        "unsquashfs",
        "-no-progress",
        "-f",
        "-d",
        "squashfs-root",
        f"/sources/{self.pkgname}-{self.pkgver}/torrhunt.snap",
    )
    (self.cwd / "torrhunt-abi.cpp").write_bytes(
        (self.files_path / "torrhunt-abi.cpp").read_bytes()
    )


def build(self):
    # The binary is linked against libstdc++, while our Qt is built with
    # libc++. Most symbols are unaffected, but the few Qt APIs using std::
    # types need a small forwarding shim. See files/torrhunt-abi.cpp.
    self.do(
        "sh",
        "-c",
        "c++ -std=c++20 -O2 -fPIC -shared -o libtorrhunt-abi.so "
        "torrhunt-abi.cpp $(pkg-config --cflags --libs "
        "Qt6WebEngineWidgets Qt6WebEngineCore Qt6Core)",
    )
    self.do(
        "patchelf",
        "--replace-needed",
        "libstdc++.so.6",
        "libc++abi.so.1",
        "squashfs-root/usr/bin/torrhunt",
    )


def install(self):
    self.install_file(
        "squashfs-root/usr/bin/torrhunt", "usr/lib/torrhunt", mode=0o755
    )
    self.install_file("libtorrhunt-abi.so", "usr/lib/torrhunt", mode=0o755)
    self.install_file(self.files_path / "torrhunt", "usr/bin", mode=0o755)
    self.install_file(
        "squashfs-root/usr/share/applications/torrhunt.desktop",
        "usr/share/applications",
    )
    self.install_file(
        "squashfs-root/usr/share/metainfo/com.ktechpit.torrhunt.metainfo.xml",
        "usr/share/metainfo",
    )
    for size in (16, 32, 64, 128, 256, 512):
        self.install_file(
            "squashfs-root/usr/share/icons/hicolor/"
            f"{size}x{size}/apps/com.ktechpit.torrhunt.png",
            f"usr/share/icons/hicolor/{size}x{size}/apps",
        )
    # the snap desktop file points at ${SNAP}/meta/gui/icon.png
    desktop = self.destdir / "usr/share/applications/torrhunt.desktop"
    desktop.write_text(
        desktop.read_text().replace(
            "Icon=${SNAP}/meta/gui/icon.png", "Icon=com.ktechpit.torrhunt"
        )
    )
