pkgname = "serenity-desktop"
pkgver = "0.1.0"
pkgrel = 1
pkgdesc = "SerenityOS desktop environment on Wayland"
license = "BSD-2-Clause"
url = "https://github.com/jmalcolm137/serenity-desktop-environment"

# Used only as the source of the wlroots protocol XMLs. The library and public
# headers come from the distribution's wlroots0.20 packages.
_wlroots_ver = "0.20.2"

hostmakedepends = [
    "bash",
    "cmake",
    "ninja",
    "patchelf",
    "pkgconf",
    "python",
    "wayland-progs",
]
makedepends = [
    "dbus-devel",
    "elogind-devel",
    "freetype-devel",
    "glib-devel",
    "libdisplay-info-devel",
    "libdrm-devel",
    "libei-devel",
    "libinput-devel",
    "libliftoff-devel",
    "libpulse-devel",
    "libxcb-devel",
    "libxkbcommon-devel",
    "linux-pam-devel",
    "mesa-devel",
    "mesa-gbm-devel",
    "pipewire-devel",
    "pixman-devel",
    "serenity-lagom-devel",
    "wayland-devel",
    "wayland-protocols",
    "wlroots0.20-devel",
    "xcb-util-wm-devel",
]
depends = [
    "dbus",
    "dbus-libs",
    "elogind-libs",
    "fontconfig",
    "freetype",
    "glib",
    "libdisplay-info",
    "libdrm",
    "libei",
    "libinput",
    "libliftoff",
    "libpulse",
    "libseat-seatd",
    "libunwind-nongnu",
    "libxcb",
    "libxkbcommon",
    "linux-pam-libs",
    "mesa-egl-libs",
    "mesa-gbm-libs",
    "mesa-gl-libs",
    "pipewire",
    "pipewire-libs",
    "pixman",
    "polkit",
    "python-gobject",
    "serenity-lagom>=0.1.0-r1",
    "wayland",
    "wlroots0.20",
    "xcb-util-wm",
    "xdg-desktop-portal",
    "xwayland",
]
# Provided by serenity-lagom; the shlib name is unversioned and not in a
# standard libdir, so the scanner cannot infer the provider.
ignore_shlibs = ["libwindowserver.so"]
options = ["!check", "!cross", "!debug", "!lto"]
hardening = ["!int"]

source = [
    f"https://github.com/jmalcolm137/serenity-desktop-environment/archive/refs/tags/v{pkgver}.tar.gz",
    f"https://gitlab.freedesktop.org/wlroots/wlroots/-/releases/{_wlroots_ver}/downloads/wlroots-{_wlroots_ver}.tar.gz",
]
sha256 = [
    "abec19a8c4637218c30cb0667a3e97b29533d5dd4b3ea6dc6aaf7d1b49f67438",
    "80c567d2ed4efb2cfa6b077f22c7a710d9c78ba4e185a75e8694001114af0733",
]
source_paths = [
    "serenity-desktop-environment",
    "serenity-desktop-environment/third_party/wlroots",
]


def prepare(self):
    sde = self.chroot_cwd / "serenity-desktop-environment"
    wlr = sde / "third_party/wlroots"
    inc = wlr / "patched-include"
    proto = wlr / "build/protocol"

    # wlroots' public headers are C and use constructs C++ cannot parse.
    def strip_static(text):
        pos = 0
        while True:
            start = text.find("[static", pos)
            if start < 0:
                break
            end = text.find("]", start)
            if end < 0:
                break
            fields = text[start + 1 : end].split()
            fields = [f for f in fields[1:] if f != "restrict"]
            text = text[:start] + "[" + " ".join(fields) + "]" + text[end + 1 :]
            pos = start + 1
        return text

    # Rename the layer-shell namespace argument so the generated protocol
    # header is valid C++ too.
    x = self.srcdir / (
        "serenity-desktop-environment/third_party/wlroots/"
        "protocol/wlr-layer-shell-unstable-v1.xml"
    )
    x.write_text(x.read_text().replace('name="namespace"', 'name="layer_namespace"'))

    # The distro does not install generated protocol headers, and its C
    # headers need the same C++ compatibility edits the SDE's build script
    # normally applies. Keep a private patched header tree.
    self.do("rm", "-rf", inc, proto)
    self.do("mkdir", "-p", inc, proto)
    self.do("cp", "-a", "/usr/include/wlroots-0.20/.", inc)

    # The SDE build script looks for this file and otherwise tries to clone
    # wlroots. Point it at the distro package instead.
    pcdir = wlr / "install/lib/pkgconfig"
    self.do("mkdir", "-p", pcdir)
    self.do("cp", "/usr/lib/pkgconfig/wlroots-0.20.pc", pcdir / "wlroots-0.20.pc")

    patched = self.srcdir / (
        "serenity-desktop-environment/third_party/wlroots/patched-include"
    )
    for p in patched.rglob("*.h"):
        p.write_text(strip_static(p.read_text()))

    p = patched / "wlr/types/wlr_layer_shell_v1.h"
    p.write_text(p.read_text().replace("char *namespace;", "char *layer_namespace;"))

    # Generate the server-side protocol headers the public wlroots headers
    # include (layer-shell and output-power-management).
    xml_dir = self.srcdir / (
        "serenity-desktop-environment/third_party/wlroots/protocol"
    )
    for xml in sorted(xml_dir.glob("*.xml")):
        self.do(
            "wayland-scanner",
            "server-header",
            wlr / "protocol" / xml.name,
            proto / f"{xml.stem}-protocol.h",
        )


def patch(self):
    from cbuild.util import patch

    plist = sorted((self.template_path / "patches-sde").glob("*.patch"))
    if plist:
        patch.patch(
            self,
            plist,
            wrksrc="serenity-desktop-environment",
            apply_args=["--recount", "-C1"],
        )


def build(self):
    sde = self.chroot_cwd / "serenity-desktop-environment"
    wlr = sde / "third_party/wlroots"

    self.do(
        "bash",
        sde / "scripts/build-full-sde.sh",
        env={
            "SDE_PREBUILT_FRAMEWORK": "ON",
            "LIBGUI_WAYLAND_ROOT": "/usr/lib/sde/framework",
            "SDE_LIBGUI_WAYLAND_ROOT": "/usr/lib/sde/framework",
            "SDE_LAGOM_BUILD_DIR": "/usr/lib/sde",
            "SDE_SERENITY_BUILD_DIR": "/usr/lib/sde/framework",
            "SDE_SERENITY_SRC": "/usr/lib/sde/framework/serenity",
            "SERENITY_SRC": "/usr/lib/sde/framework/serenity",
            "BUILD": "/usr/lib/sde",
            "LD_LIBRARY_PATH": "/usr/lib/sde/lib",
            "WLROOTS_SRC": str(wlr),
            "JOBS": str(self.make_jobs),
        },
    )


def install(self):
    sde = self.chroot_cwd / "serenity-desktop-environment"

    self.do(
        "bash",
        sde / "scripts/install-sde.sh",
        "--destdir",
        self.chroot_destdir,
        "--prefix",
        "/usr/lib/sde",
        "--without-framework",
        env={
            "BUILD": "/usr/lib/sde",
            "SERENITY": "/usr/lib/sde/framework/serenity",
        },
    )
    # WindowServer links the private lagom libraries from /usr/lib/sde/lib;
    # libwlroots itself comes from the system wlroots0.20 package.
    self.do(
        "patchelf",
        "--set-rpath",
        "/usr/lib/sde/lib",
        self.chroot_destdir / "usr/lib/sde/bin/WindowServer",
    )
    self.install_license("serenity-desktop-environment/LICENSE")
