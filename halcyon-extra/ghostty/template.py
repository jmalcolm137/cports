pkgname = "ghostty"
pkgver = "1.4.0"
pkgrel = 0
hostmakedepends = [
    "blueprint-compiler",
    "git",
    "glib-devel",
    "ncurses",
    "pkgconf",
    "zig",
]
makedepends = [
    "bzip2-devel",
    "fontconfig-devel",
    "freetype-devel",
    "glib-devel",
    "gtk4-devel",
    "gtk4-layer-shell-devel",
    "harfbuzz-devel",
    "libadwaita-devel",
    "libpng-devel",
    "libx11-devel",
    "mesa-devel",
    "oniguruma-devel",
    "wayland-devel",
    "zlib-ng-compat-devel",
]
pkgdesc = "Fast, native, feature-rich terminal emulator"
license = "MIT"
url = "https://ghostty.org"
source = f"https://release.files.ghostty.org/{pkgver}/ghostty-{pkgver}.tar.gz"
sha256 = "cb188ac6c3a8278d5fd7bfef15d8c017104c87f638b5560eb38024a71ae0f005"
# the app is a native GTK desktop application
options = ["!cross"]


def prepare(self):
    self.do(
        "sh",
        "nix/build-support/fetch-zig-cache.sh",
        env={
            "ZIG_GLOBAL_CACHE_DIR": str(
                self.chroot_cwd / ".zig-cache-fetch"
            )
        },
        allow_network=True,
    )
    self.cp(self.files_path / "extract-zig-cache.sh", ".")
    self.do("sh", "extract-zig-cache.sh", ".zig-cache-fetch/p")


_zig_args = [
    "--prefix",
    "/usr",
    "--system",
    ".zig-cache-fetch/p",
    "-Doptimize=ReleaseFast",
    "-Dcpu=baseline",
    "-Dapp-runtime=gtk",
    "-Demit-docs=false",
    "-Dinstalled-exe-path=/usr/bin/ghostty",
]


def build(self):
    self.do(
        "zig",
        "build",
        *_zig_args,
        env={
            "DESTDIR": str(self.chroot_cwd / ".stage"),
            "ZIG_GLOBAL_CACHE_DIR": ".zig-cache-global-build",
        },
    )


def check(self):
    self.do(".stage/usr/bin/ghostty", "--version")


def install(self):
    self.install_dir("usr")
    for ent in sorted((self.cwd / ".stage/usr").iterdir()):
        self.install_files(f".stage/usr/{ent.name}", "usr")


def post_install(self):
    self.install_license("LICENSE")
    # the app build also stages the embeddable C library; the separate
    # libghostty-vt package owns those files
    self.uninstall("usr/include/ghostty", missing_ok=True)
    self.uninstall("usr/lib/libghostty-vt*", glob=True, missing_ok=True)
    self.uninstall("usr/share/pkgconfig/libghostty-vt*", glob=True, missing_ok=True)
    # Chimera uses dinit; the systemd user unit is not useful here
    self.uninstall("usr/lib/systemd", missing_ok=True)
