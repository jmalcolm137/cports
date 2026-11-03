pkgname = "ladybird-sde"
pkgver = "0.1.0_git20261102"
pkgrel = 0
archs = ["x86_64"]
hostmakedepends = [
    "autoconf",
    "autoconf-archive",
    "automake",
    "bash",
    "bison",
    "cargo-auditable",
    "clang",
    "cmake",
    "curl",
    "findutils",
    "flex",
    "git",
    "gn",
    "gperf",
    "libtool",
    "lld",
    "nasm",
    "ninja",
    "patchelf",
    "perl",
    "pkgconf",
    "python",
    "unzip",
    "zip",
]
makedepends = [
    "curl-devel",
    "fontconfig-devel",
    "freetype-devel",
    "glib-devel",
    "glslang",
    "harfbuzz-devel",
    "icu-devel",
    "libavif-devel",
    "libdrm-devel",
    "libedit-devel",
    "libjpeg-turbo-devel",
    "libpng-devel",
    "libpsl-devel",
    "libtommath-devel",
    "libucontext-devel",
    "libwebp-devel",
    "libxcb-devel",
    "libxml2-devel",
    "linux-headers",
    "mesa-devel",
    "openssl3-devel",
    "qt6-qtbase-devel",
    "qt6-qtbase-private-devel",
    "qt6-qtpositioning-devel",
    "qt6-qtwayland-devel",
    "rust-std",
    "sdl3-devel",
    "serenity-lagom-devel",
    "sqlite-devel",
    "vulkan-headers",
    "vulkan-loader-devel",
    "wayland-devel",
    "wayland-protocols",
    "woff2-devel",
    "xcb-util-wm-devel",
    "zlib-ng-compat-devel",
]
depends = ["serenity-lagom>=0.1.0-r1"]
# libwindowserver.so has no SONAME, so it cannot provide a versioned symbol
ignore_shlibs = ["libwindowserver.so"]
pkgdesc = "LibGUI Ladybird browser for the Serenity Desktop Environment"
license = "BSD-2-Clause"
url = "https://github.com/jmalcolm137/ladybird"
_commit = "b775a1928ee26bd45dfe3176c8457b96d2c44dab"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "651ede5c93152a2cccd0db9cb5d210b230755c7aa0c8165bb870a08110208d5c"
# these are private, bundled copies and must not provide the system sonames
skip_providers = ["usr/lib/sde/lib/ladybird/*"]
# vcpkg and the SDE framework make cross builds impractical
options = ["!check", "!cross", "!debug"]


def _env(self, offline=False):
    renv = {
        "LADYBIRD_SOURCE_DIR": str(self.chroot_cwd),
        "LADYBIRD_MAIN_SOURCE_DIR": str(self.chroot_cwd),
        "VCPKG_ROOT": str(self.chroot_cwd / "Build/vcpkg-release"),
        "VCPKG_DISABLE_METRICS": "true",
        "CARGO_HOME": str(self.chroot_cwd / ".cargo-home"),
        "VCPKG_MAX_CONCURRENCY": str(self.make_jobs),
        "CFLAGS": "",
        "CXXFLAGS": "",
        "LDFLAGS": "",
    }
    if offline:
        renv["CARGO_NET_OFFLINE"] = "true"
    return renv


def prepare(self):
    (self.cwd / "REVISION").write_text(f"{_commit}\n")

    env = _env(self)
    self.do(
        "python3",
        "Meta/ladybird.py",
        "vcpkg",
        "--preset",
        "Release",
        "--jobs",
        str(self.make_jobs),
        env=env,
        allow_network=True,
    )
    self.do(
        "cargo",
        "fetch",
        "--locked",
        env=env,
        allow_network=True,
    )

    # vcpkg downloads a glibc-only gn; use the distribution's musl build
    gnport = (
        self.cwd
        / "Meta/CMake/vcpkg/overlay-ports/vcpkg-tool-gn"
    )
    gnport.mkdir(parents=True, exist_ok=True)
    (gnport / "vcpkg.json").write_text(
        """{
  "name": "vcpkg-tool-gn",
  "version-date": "2025-08-05",
  "port-version": 2,
  "description": "GN build system",
  "homepage": "https://gn.googlesource.com/gn/",
  "license": null,
  "supports": "native"
}
"""
    )
    (gnport / "portfile.cmake").write_text(
        """set(VCPKG_POLICY_EMPTY_PACKAGE enabled)

file(MAKE_DIRECTORY "${CURRENT_PACKAGES_DIR}/tools/gn")
file(COPY "/usr/bin/gn" DESTINATION "${CURRENT_PACKAGES_DIR}/tools/gn")
file(MAKE_DIRECTORY "${CURRENT_PACKAGES_DIR}/share/gn")
file(WRITE "${CURRENT_PACKAGES_DIR}/share/gn/version.txt" "system")
"""
    )

    self.do(
        "cmake",
        "--preset",
        "Release",
        "-S",
        ".",
        "-B",
        "Build/release",
        f"-DCMAKE_C_COMPILER={self.get_tool('CC')}",
        f"-DCMAKE_CXX_COMPILER={self.get_tool('CXX')}",
        "-DCMAKE_MAKE_PROGRAM=/usr/bin/ninja",
        "-DCMAKE_INSTALL_PREFIX=/usr/lib/sde",
        "-DCMAKE_INSTALL_BINDIR=bin",
        "-DCMAKE_INSTALL_LIBDIR=lib/ladybird",
        "-DCMAKE_INSTALL_LIBEXECDIR=libexec",
        "-DCMAKE_INSTALL_DATADIR=share",
        "-DENABLE_CI_BASELINE_CPU=ON",
        "-DENABLE_CLANG_PLUGINS=OFF",
        "-DENABLE_INSTALL_FREEDESKTOP_FILES=OFF",
        "-DENABLE_INSTALL_HEADERS=OFF",
        "-DENABLE_LTO_FOR_RELEASE=OFF",
        "-DENABLE_NETWORK_DOWNLOADS=ON",
        "-DBUILD_TESTING=OFF",
        env=env,
        allow_network=True,
    )


def build(self):
    env = _env(self, offline=True)
    self.do(
        "cmake",
        "--build",
        "Build/release",
        "--target",
        "LadybirdEngine",
        "ladybird",
        "WebDriver",
        f"-j{self.make_jobs}",
        env=env,
    )

    lagom = self.chroot_cwd / "build/lagom"
    self.do("mkdir", "-p", str(lagom))
    for entry in ["AK", "Userland", "libwm", "serenity", "src"]:
        self.do(
            "ln",
            "-sfn",
            f"/usr/lib/sde/framework/{entry}",
            str(lagom / entry),
        )
    self.do("ln", "-sfn", "/usr/lib/sde/lib", str(lagom / "lib"))

    self.do(
        "env",
        "-u",
        "CFLAGS",
        "-u",
        "CXXFLAGS",
        "-u",
        "LDFLAGS",
        "make",
        "-C",
        "UI/LibGUI",
        f"-j{self.make_jobs}",
        "LIBGUI_WAYLAND_ROOT=/usr/lib/sde/framework",
        f"LAGOM={lagom}",
        "SERENITY=/usr/lib/sde/framework/serenity",
        f"CXX={self.get_tool('CXX')}",
    )


def install(self):
    self.install_license("LICENSE")

    self.do(
        "cmake",
        "--install",
        "Build/release",
        "--component",
        "ladybird_Runtime",
        env={"DESTDIR": str(self.chroot_destdir)},
    )

    # the Qt frontend is not part of the SDE build
    self.uninstall("usr/lib/sde/bin/Ladybird", missing_ok=True)
    self.uninstall("usr/lib/sde/bin/WebDriver", missing_ok=True)

    self.install_file(
        "build/chrome/Ladybird",
        "usr/lib/sde/bin",
        name="Ladybird.real",
        mode=0o755,
    )
    self.install_file(
        self.files_path / "Ladybird", "usr/lib/sde/bin", mode=0o755
    )
    self.install_file(
        self.files_path / "Ladybird.af", "usr/lib/sde/share/res/apps"
    )
    self.install_file(
        self.files_path / "ladybird.desktop",
        "usr/lib/sde/share/applications",
    )
    self.install_dir("usr/bin")
    self.install_link("usr/bin/ladybird-sde", "../lib/sde/bin/Ladybird")

    self.install_dir("usr/lib/sde/lib/ladybird")
    self.do(
        "cp",
        "-a",
        f"{self.chroot_cwd}/Build/release/vcpkg_installed/"
        "x64-linux-dynamic/lib/.",
        f"{self.chroot_destdir}/usr/lib/sde/lib/ladybird/",
    )
    self.uninstall(
        "usr/lib/sde/lib/ladybird/*.a", glob=True, missing_ok=True
    )
    self.uninstall(
        "usr/lib/sde/lib/ladybird/pkgconfig", missing_ok=True
    )


def post_install(self):
    # make the installed binaries find their bundled libraries
    frontend = self.chroot_destdir / "usr/lib/sde/bin/Ladybird.real"
    self.do(
        "patchelf",
        "--force-rpath",
        "--set-rpath",
        "$ORIGIN/../lib",
        str(frontend),
    )

    libexec = self.destdir / "usr/lib/sde/libexec"
    if libexec.is_dir():
        for entry in libexec.iterdir():
            if entry.is_file() and not entry.is_symlink():
                self.do(
                    "patchelf",
                    "--force-rpath",
                    "--set-rpath",
                    "$ORIGIN/../lib/ladybird",
                    str(
                        self.chroot_destdir
                        / entry.relative_to(self.destdir)
                    ),
                )

    libdir = self.destdir / "usr/lib/sde/lib/ladybird"
    if libdir.is_dir():
        for entry in libdir.rglob("*.so*"):
            if entry.is_file() and not entry.is_symlink():
                self.do(
                    "patchelf",
                    "--force-rpath",
                    "--set-rpath",
                    "$ORIGIN",
                    str(
                        self.chroot_destdir
                        / entry.relative_to(self.destdir)
                    ),
                )
