pkgname = "xlib-wayland"
pkgver = "0.1.0"
pkgrel = 0
build_style = "meson"
configure_args = ["-Dtests=false", "-Dtools=false"]
hostmakedepends = [
    "meson",
    "ninja",
    "pkgconf",
    "wayland-progs",
]
makedepends = [
    "cairo-devel",
    "fontconfig-devel",
    "freetype-devel",
    "libx11-devel",
    "libxcb-devel",
    "libxcomposite-devel",
    "libxcursor-devel",
    "libxdamage-devel",
    "libxext-devel",
    "libxfixes-devel",
    "libxft-devel",
    "libxi-devel",
    "libxinerama-devel",
    "libxkbcommon-devel",
    "libxrandr-devel",
    "libxrender-devel",
    "pixman-devel",
    "wayland-devel",
    "wayland-protocols",
]
pkgdesc = "Wayland-native, ABI-compatible implementation of Xlib"
license = "MIT"
url = "https://github.com/jmalcolm137/xlib-wayland"

_commit = "bf07693e94479200e1cf93cdb7cbcc844aae281f"

source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "880ebc340b0e49ffd3fa184c235fda0997ea6852a69c6147d18922aeef190998"

# The shim installs the same sonames as the Xorg libraries so that it can take
# over from them at run time.
replaces = [
    "libx11",
    "libxext",
    "libxft",
    "libxfixes",
    "libxcursor",
    "libxrandr",
    "libxdamage",
    "libxcomposite",
    "libxinerama",
]
replaces_priority = 100

# The replaced Xorg packages stay installed and keep providing the sonames, so
# do not advertise them again from this package.
skip_providers = [
    "usr/lib/libX11.so.*",
    "usr/lib/libX11-xcb.so.*",
    "usr/lib/libXext.so.*",
    "usr/lib/libXft.so.*",
    "usr/lib/libXrandr.so.*",
    "usr/lib/libXfixes.so.*",
    "usr/lib/libXcursor.so.*",
    "usr/lib/libXdamage.so.*",
    "usr/lib/libXcomposite.so.*",
    "usr/lib/libXinerama.so.*",
]

# the test suite needs the bundled headless compositor and a full userland
options = ["!check"]

# strcasestr() and friends are only declared by musl with _GNU_SOURCE
tool_flags = {"CFLAGS": ["-D_GNU_SOURCE"]}


def post_install(self):
    self.install_license("LICENSE")

    # The shim installs no headers and is built against the system X headers,
    # so keep the pkg-config files and unversioned link symlinks from the
    # X development packages instead of conflicting with them.
    self.uninstall("usr/lib/pkgconfig")
    for lib in [
        "X11",
        "X11-xcb",
        "Xext",
        "Xft",
        "Xrandr",
        "Xfixes",
        "Xcursor",
        "Xdamage",
        "Xcomposite",
        "Xinerama",
    ]:
        self.uninstall(f"usr/lib/lib{lib}.so")
