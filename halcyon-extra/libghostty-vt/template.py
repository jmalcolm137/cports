pkgname = "libghostty-vt"
pkgver = "1.0.0"
pkgrel = 0
hostmakedepends = ["zig"]
pkgdesc = "Portable C library for terminal emulation"
license = "MIT AND Apache-2.0 AND Unicode-3.0"
url = "https://github.com/ghostty-org/ghostty"
source = [
    f"https://release.files.ghostty.org/libghostty-vt/{pkgver}/"
    f"libghostty-vt-{pkgver}.tar.gz",
    f"https://release.files.ghostty.org/libghostty-vt/{pkgver}/"
    f"libghostty-vt-{pkgver}-deps.tar.gz",
]
source_paths = [".", "deps"]
sha256 = [
    "4a6ef758be721923e1969e7b81b443dcc92d8dd3fb5a39600c03a8817a753676",
    "4d5ea5e448e4c7ea8fb55ccbaa8668f2a97d44f438cee831e2b7ecd162d85c29",
]
# the git checkout does not build the library; the release tarballs do
options = ["!cross"]

_targets = {
    "x86_64": "x86_64-linux-musl",
    "aarch64": "aarch64-linux-musl",
    "ppc64le": "powerpc64le-linux-musl",
    "ppc64": "powerpc64-linux-musl",
    "ppc": "powerpc-linux-musl",
    "riscv64": "riscv64-linux-musl",
    "loongarch64": "loongarch64-linux-musl",
    "armv7": "arm-linux-musleabihf",
    "armhf": "arm-linux-musleabihf",
}
_target = _targets.get(self.profile.arch)
if _target is None:
    broken = f"unknown zig target for {self.profile.arch}"

_zig_build_args = [
    "--prefix",
    "/usr",
    "--system",
    "deps",
    "-Doptimize=ReleaseFast",
    "-Dcpu=baseline",
    f"-Dtarget={_target}",
]


def build(self):
    self.do(
        "zig",
        "build",
        *_zig_build_args,
        env={
            # stage the install into the build directory
            "DESTDIR": str(self.chroot_cwd / ".stage"),
            "ZIG_GLOBAL_CACHE_DIR": ".zig-cache-global-build",
        },
    )


def check(self):
    # the upstream suite only compiles with the debug-only slow runtime
    # safety checks, which makes it take hours; smoke test the C API instead
    self.cp(self.files_path / "smoke.c", ".")
    self.do(
        "cc",
        "smoke.c",
        "-o",
        "smoke",
        "-I",
        ".stage/usr/include",
        "-L",
        ".stage/usr/lib",
        "-lghostty-vt",
    )
    self.do("./smoke", env={"LD_LIBRARY_PATH": ".stage/usr/lib"})


def install(self):
    self.install_dir("usr")
    for ent in sorted((self.cwd / ".stage/usr").iterdir()):
        self.install_files(f".stage/usr/{ent.name}", "usr")


def post_install(self):
    self.install_license("LICENSE")
    # the release statically links a few dependencies; ship their licenses
    for dep in (self.cwd / "deps").iterdir():
        if not dep.is_dir():
            continue
        for lic in dep.glob("LICENSE*"):
            self.install_file(
                lic,
                "usr/share/licenses/libghostty-vt",
                name=f"{dep.name}-{lic.name}",
            )


@subpackage("libghostty-vt-devel")
def _(self):
    return self.default_devel()
