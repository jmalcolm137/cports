pkgname = "broadcom-wl"
pkgver = "6.30.223.271"
pkgrel = 2
# the shipped binary blob and the driver only support x86
archs = ["x86_64"]
makedepends = ["dinit-chimera"]
depends = ["kmod"]
pkgdesc = "Broadcom 802.11 Linux STA wireless driver"
license = "custom:broadcom-wl"
url = "https://www.broadcom.com/support/download-search?pf=Wireless+LAN+Infrastructure"
source = (
    "https://docs.broadcom.com/docs-and-downloads/docs/linux_sta/"
    f"hybrid-v35_64-nodebug-pcoem-{pkgver.replace('.', '_')}.tar.gz"
)
sha256 = "5f79774d5beec8f7636b59c0fb07a03108eef1e3fd3245638b20858c714144be"
# no tests; do not let the package stage strip the prebuilt proprietary object
options = ["!check", "!strip"]


# patch series from Arch Linux broadcom-wl-dkms 6.30.223.271-50
def patch(self):
    from cbuild.util import patch

    # the Arch series is applied with GNU patch fuzz; git apply needs a bit of
    # context reduction where patches insert includes next to each other
    patch.patch(
        self,
        sorted(self.patches_path.glob("*.patch")),
        apply_args=["-C1"],
        stamp=True,
    )


def post_patch(self):
    # change the default interface prefix from eth to wlan
    wlp = self.cwd / "src/wl/sys/wl_linux.c"
    wlp.write_text(
        wlp.read_text().replace(
            "#define BRCM_WLAN_IFNAME eth%d",
            "#define BRCM_WLAN_IFNAME wlan%d",
        )
    )

    # the proprietary object lives outside the CKMS source tree, and always
    # treat the compiler as new enough for -Wno-date-time
    mk = self.cwd / "Makefile"
    mkdata = mk.read_text().replace(
        "$(src)/lib/wlc_hybrid.o_shipped",
        "/usr/lib/broadcom-wl/wlc_hybrid.o_shipped",
    )
    mkdata = "".join(
        "GE_49 := 1\n" if line.startswith("GE_49 :=") else line
        for line in mkdata.splitlines(keepends=True)
    )
    mk.write_text(mkdata)


def install(self):
    self.install_license("lib/LICENSE.txt")
    self.install_file("lib/wlc_hybrid.o_shipped", "usr/lib/broadcom-wl")

    self.install_file(
        self.files_path / "halcyon-wifi-select",
        "usr/lib/halcyon",
        name="wifi-select",
        mode=0o755,
    )
    self.install_initramfs(self.files_path / "halcyon-wifi-hook", name="broadcom-wl")
    self.install_initramfs(
        self.files_path / "halcyon-wifi-init",
        "init-top",
        name="000-halcyon-wifi",
    )
    self.install_service(self.files_path / "halcyon-wifi", enable=True)

    srcp = f"usr/src/broadcom-wl-{pkgver}"
    self.install_file("Makefile", srcp)
    self.install_files("src", srcp)
    # the module package needs the license alongside the source tree
    self.install_file("lib/LICENSE.txt", srcp)
    self.install_file(
        self.files_path / "ckms.ini", srcp, template={"VERSION": pkgver}
    )


@subpackage("broadcom-wl-ckms")
def _(self):
    self.subdesc = "kernel module sources"
    self.install_if = [self.parent, "ckms"]
    self.depends = [
        self.parent,
        "ckms",
        "clang",
        "gmake",
        "lld",
    ]

    return ["usr/src"]
