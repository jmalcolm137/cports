pkgname = "linux-halcyon-bcachefs-bin"
pkgver = "1.39.7.7.3.1"
_bcachefsver = ".".join(pkgver.split(".")[0:3])
_kernver = pkgver[len(_bcachefsver) + 1 :]
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["perl", "python", "ckms"]
makedepends = ["linux-halcyon-devel", "bcachefs-ckms"]
# provides the same thing as the ckms variant
depends = [f"linux-halcyon~{_kernver}", f"bcachefs-tools~{_bcachefsver}"]
pkgdesc = f"Bcachefs modules for linux-halcyon {_kernver}"
license = "GPL-2.0-only"
url = "https://bcachefs.org"
options = ["!cross"]


def init_configure(self):
    from cbuild.util import linux

    self._linux_version = linux.get_version(self, _kernver)


def configure(self):
    from cbuild.util import linux

    linux.ckms_configure(self, "bcachefs", _bcachefsver, self._linux_version)


def build(self):
    from cbuild.util import linux

    linux.ckms_build(self, "bcachefs", _bcachefsver, self._linux_version)


def install(self):
    from cbuild.util import linux

    linux.ckms_install(self, "bcachefs", _bcachefsver, self._linux_version)

    srcp = linux.get_modsrc(self, "bcachefs", _bcachefsver)
    self.install_license(srcp / "COPYING")
