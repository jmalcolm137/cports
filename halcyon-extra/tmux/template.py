pkgname = "tmux"
pkgver = "3.8"
pkgrel = 0
build_style = "gnu_configure"
configure_args = ["--enable-sixel"]
hostmakedepends = ["automake", "byacc", "pkgconf"]
makedepends = ["libevent-devel", "ncurses-devel"]
pkgdesc = "Terminal multiplexer"
license = "ISC"
url = "https://tmux.github.io"
source = f"https://github.com/tmux/tmux/releases/download/{pkgver}/tmux-{pkgver}.tar.gz"
sha256 = "e79c699c7e949dccd0a4a125e17b8d1261e311b16979dbc8eb34542f3966d82e"
hardening = ["vis", "cfi"]

# cports builds with clang against musl by default. tmux is C-only, so no C++
# runtime (libc++) is required or linked.


def post_install(self):
    self.install_license("COPYING")
