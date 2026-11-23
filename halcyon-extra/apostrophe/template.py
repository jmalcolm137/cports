pkgname = "apostrophe"
pkgver = "3.5"
pkgrel = 0
build_style = "meson"
hostmakedepends = [
    "desktop-file-utils",
    "gettext",
    "glib-devel",
    "gtk+3-update-icon-cache",
    "meson",
    "pkgconf",
    "python",
]
makedepends = [
    "glib-devel",
    "gobject-introspection",
    "gtk4-devel",
    "libadwaita-devel",
]
depends = [
    "gtk4",
    "gtksourceview",
    "libadwaita",
    "libspelling",
    "pandoc",
    "python-chardet",
    "python-gobject",
    "python-pypandoc",
    "python-regex",
    "typst",
    "webkitgtk4",
]
pkgdesc = "Distraction-free Markdown editor"
license = "GPL-3.0-or-later"
url = "https://gitlab.gnome.org/World/apostrophe"
source = f"{url}/-/archive/v{pkgver}/apostrophe-v{pkgver}.tar.gz"
sha256 = "67db4b783e0a69eb22cb393e92e91f53fb48d72598379a5829b7d05d95dc3149"
