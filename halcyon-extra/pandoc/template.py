pkgname = "pandoc"
pkgver = "3.14"
pkgrel = 0
archs = ["x86_64"]
pkgdesc = "Universal markup converter"
license = "GPL-2.0-or-later"
url = "https://pandoc.org"
source = f"https://github.com/jgm/pandoc/releases/download/{pkgver}/pandoc-{pkgver}-linux-amd64.tar.gz"
sha256 = "c5f4720cdefb3f7bdc5d07202ef579feef0d1370773c873804dd8fdaa8c4f1b8"
# prebuilt static upstream binary
options = ["!check", "!debug", "!strip"]


def install(self):
    self.install_bin("bin/pandoc")
    self.install_link("usr/bin/pandoc-lua", "pandoc")
    self.install_link("usr/bin/pandoc-server", "pandoc")
    for page in ["pandoc.1.gz", "pandoc-lua.1.gz", "pandoc-server.1.gz"]:
        self.install_file(f"share/man/man1/{page}", "usr/share/man/man1")
