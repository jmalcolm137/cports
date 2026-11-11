pkgname = "firmware-apple"
pkgver = "20221231"
pkgrel = 0
archs = ["x86_64", "aarch64"]
hostmakedepends = ["zstd-progs"]
pkgdesc = "Wi-Fi and Bluetooth firmware for Apple T2 and Apple Silicon Macs"
license = "custom:Apple-Firmware"
url = "https://github.com/mrheyday/Apple-Firmware"
_commit = "f7ebff75ae7299f7b9068b5d321f66744e6b687c"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "44bafb047086ad11514941fecb25970229a358d7f5be23a2a5932df5de218805"
options = ["!strip"]


def install(self):
    self.install_files(
        "lib/firmware/brcm",
        "usr/lib/firmware",
    )

    # the kernel firmware loader supports zstd compressed blobs
    for f in list((self.destdir / "usr/lib/firmware/brcm").rglob("*")):
        if f.is_symlink() or not f.is_file() or f.name.endswith(".zst"):
            continue
        self.do(
            "zstd",
            "--compress",
            "--quiet",
            "--rm",
            self.chroot_destdir / f.relative_to(self.destdir),
        )

    self.install_license("README.md")
