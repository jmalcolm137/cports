pkgname = "linux-halcyon-broadcom-wl-bin"
pkgver = "6.30.223.271.7.3.1"
_wlver = ".".join(pkgver.split(".")[0:4])
_kernver = pkgver[len(_wlver) + 1 :]
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = ["perl", "python", "ckms"]
makedepends = ["linux-halcyon-devel", "broadcom-wl-ckms"]
# provides the same thing as the ckms variant
depends = [f"linux-halcyon~{_kernver}", f"broadcom-wl~{_wlver}"]
pkgdesc = f"Broadcom-wl modules for linux-halcyon {_kernver}"
license = "custom:broadcom-wl"
url = "https://www.broadcom.com/support/download-search?pf=Wireless+LAN+Infrastructure"
options = ["!cross"]


def init_configure(self):
    from cbuild.util import linux

    self._linux_version = linux.get_version(self, _kernver)


def configure(self):
    from cbuild.util import linux

    linux.ckms_configure(self, "broadcom-wl", _wlver, self._linux_version)


def build(self):
    from cbuild.util import linux

    linux.ckms_build(self, "broadcom-wl", _wlver, self._linux_version)


def install(self):
    from cbuild.util import linux

    linux.ckms_install(self, "broadcom-wl", _wlver, self._linux_version)

    srcp = linux.get_modsrc(self, "broadcom-wl", _wlver)
    self.install_license(srcp / "LICENSE.txt")
