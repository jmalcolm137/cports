pkgname = "serenity-lagom"
pkgver = "0.1.0"
pkgrel = 6
# The SDE release is built from these exact revisions; do not update one
# without the other (see the upstream PKGBUILDs in Meta/packaging/aur).
_libgui_commit = "bdcfc26451f95713a5f1f154062c1313f149427f"
_serenity_commit = "584ceca57dbaca5f3b304915c6b449a69100ba78"
_sde_commit = "2562d7fe5f647280a29c5e6fedc45fe96ae56dfa"
hostmakedepends = [
    "bash",
    "bison",
    "cmake",
    "findutils",
    "flex",
    "gperf",
    "ninja",
    "perl",
    "pkgconf",
    "python",
    "unzip",
    "wayland-progs",
    "zip",
]
makedepends = [
    "dbus-devel",
    "elfutils-devel",
    "elogind-devel",
    "freetype-devel",
    "glib-devel",
    "libdisplay-info-devel",
    "libdrm-devel",
    "libei-devel",
    "libinput-devel",
    "libpulse-devel",
    "libucontext-devel",
    "libunwind-nongnu-devel",
    "libxcb-devel",
    "libxkbcommon-devel",
    "mesa-devel",
    "mesa-gbm-devel",
    "pipewire-devel",
    "pixman-devel",
    "wayland-devel",
    "wayland-protocols",
    "xcb-util-wm-devel",
]
depends = [
    "dbus-libs",
    "elfutils-libs",
    "elogind-libs",
    "fontconfig",
    "freetype",
    "glib",
    "libdisplay-info",
    "libdrm",
    "libei",
    "libglvnd",
    "libinput",
    "libpulse",
    "libucontext",
    "libunwind-nongnu",
    "libxcb",
    "libxkbcommon",
    "pipewire",
    "pipewire-libs",
    "pixman",
    "wayland",
    "xcb-util-wm",
]
pkgdesc = "SerenityOS userland framework, applications and resources for SDE"
license = "BSD-2-Clause"
url = "https://github.com/jmalcolm137/libgui-wayland"
source = [
    f"https://github.com/jmalcolm137/libgui-wayland/archive/{_libgui_commit}.tar.gz",
    f"https://github.com/jmalcolm137/serenity/archive/{_serenity_commit}.tar.gz",
    f"https://github.com/jmalcolm137/serenity-desktop-environment/archive/{_sde_commit}.tar.gz",
]
source_paths = [
    "libgui-wayland",
    "libgui-wayland/serenity",
    "serenity-desktop-environment",
]
sha256 = [
    "db2c6bcf8bf98c814ebfa8f89d740402f835a7037f7a27956a48da631387a607",
    "bfd19922cdc4f75e6f42123721496baec551e91078f294adfe52342169fa5d49",
    "951c4bffd66801f8021e3b8f4377bf9aeb764b6f95d309fede808accf04a7aac",
]
hardening = ["!int"]
# Everything under usr/lib/sde is a self-contained prefix and is not meant to
# be fed through the distribution's usual soname/dependency mapping.
# 0008 keeps a disabled cursor highlight disabled when Mouse Settings applies
# the other tabs, and uses the SerenityOS red/110 defaults when first enabled.
options = ["!check", "!cross", "!debug", "!lto"]

# Lagom targets needed before the SDE shim can be compiled. These are the
# targets upstream's scripts/build-libgui.sh builds in its first phase.
_generated = [
    "generate_AudioClientEndpoint.h",
    "generate_AudioManagerClientEndpoint.h",
    "generate_AudioManagerServerEndpoint.h",
    "generate_AudioServerEndpoint.h",
    "generate_ClipboardClientEndpoint.h",
    "generate_ClipboardServerEndpoint.h",
    "generate_ConfigClientEndpoint.h",
    "generate_ConfigServerEndpoint.h",
    "generate_FileSystemAccessClientEndpoint.h",
    "generate_FileSystemAccessServerEndpoint.h",
    "generate_LaunchClientEndpoint.h",
    "generate_LaunchServerEndpoint.h",
    "generate_NotificationClientEndpoint.h",
    "generate_NotificationServerEndpoint.h",
    "generate_WindowClientEndpoint.h",
    "generate_WindowManagerClientEndpoint.h",
    "generate_WindowManagerServerEndpoint.h",
    "generate_WindowServerEndpoint.h",
]

# Targets from the SDE's scripts/lagom-libraries.sh.
_libs = [
    "AK",
    "LibAudio",
    "LibCompress",
    "LibConfig",
    "LibCore",
    "LibCoreBasic",
    "LibCoreMinimal",
    "LibCrypto",
    "LibDesktop",
    "LibFileSystem",
    "LibGUI",
    "LibGemini",
    "LibGfx",
    "LibHTTP",
    "LibIPC",
    "LibImageDecoderClient",
    "LibJS",
    "LibKeyboard",
    "LibLaunch",
    "LibLocale",
    "LibMain",
    "LibRIFF",
    "LibSQL",
    "LibTLS",
    "LibTextCodec",
    "LibThreading",
    "LibURL",
    "LibUnicode",
    "LibWeb",
    "LibWebSocket",
    "LibWebView",
]

# Applications added to Lagom by the SDE patches (plus a few present in the
# release package but not listed by the v0.1.0 patch).
_apps = [
    "2048",
    "3DFileViewer",
    "About",
    "AnalogClock",
    "Assistant",
    "Browser",
    "BrowserSettings",
    "Calculator",
    "Calendar",
    "CalendarSettings",
    "CatDog",
    "CertificateSettings",
    "CharacterMap",
    "Chess",
    "ChessEngine",
    "ClockSettings",
    "ColorLines",
    "CrashReporter",
    "Debugger",
    "DisplaySettings",
    "Escalator",
    "Eyes",
    "FileManager",
    "FlappyBug",
    "Flood",
    "FontEditor",
    "GameOfLife",
    "GamesSettings",
    "GMLPlayground",
    "Gradient",
    "HackStudio",
    "Hearts",
    "Help",
    "HexEditor",
    "ImageViewer",
    "KeyboardMapper",
    "KeyboardSettings",
    "LibGfxDemo",
    "LibGfxScaleDemo",
    "Magnifier",
    "Mail",
    "MailSettings",
    "Mandelbrot",
    "Maps",
    "MapsSettings",
    "MasterWord",
    "Minesweeper",
    "ModelGallery",
    "MouseSettings",
    "NetworkSettings",
    "PDFViewer",
    "Piano",
    "PixelPaint",
    "Presenter",
    "Profiler",
    "Run",
    "Screenshot",
    "Screensaver",
    "Settings",
    "Snake",
    "Solitaire",
    "SoundPlayer",
    "SpaceAnalyzer",
    "Spider",
    "Spreadsheet",
    "SQLStudio",
    "Starfield",
    "Sudoku",
    "SystemMonitor",
    "Taskbar",
    "Terminal",
    "TerminalSettings",
    "TextEditor",
    "ThemeEditor",
    "Tubes",
    "UsersSettings",
    "VideoPlayer",
    "Weather",
    "Welcome",
    "WidgetGallery",
]


def prepare(self):
    lg = self.chroot_cwd / "libgui-wayland"
    serenity = lg / "serenity"
    lagom = lg / "build/lagom"
    cache = lg / "caches"

    # Clang 23's -Wunused flags the profiler's write-only pid; the SDE builds
    # with -Werror.
    prof = self.srcdir / (
        "serenity-desktop-environment/Libraries/LibSerenitySystem/Profiling.cpp"
    )
    prof.write_text(
        prof.read_text().replace(
            "static pid_t s_pid { -1 };",
            "[[maybe_unused]] static pid_t s_pid { -1 };",
        )
    )

    # SerenityOS downloads Unicode, CLDR, tzdata, CA certificates and other
    # data at configure time. cports only permits network access during the
    # fetch/extract/prepare/patch phases, so populate the cache here; the
    # build phase then configures with ENABLE_NETWORK_DOWNLOADS=OFF.
    self.do(
        "cmake",
        "-S",
        serenity / "Meta/Lagom",
        "-B",
        lagom,
        "-GNinja",
        "-DBUILD_LAGOM=ON",
        "-DENABLE_LAGOM_LIBWEB=ON",
        "-DENABLE_LAGOM_LADYBIRD=OFF",
        "-DENABLE_CLANG_PLUGINS=OFF",
        "-DENABLE_LAGOM_CCACHE=OFF",
        "-DCMAKE_BUILD_TYPE=Release",
        f"-DSERENITY_CACHE_DIR={cache}",
        f"-DSDE_ROOT={self.chroot_srcdir}/serenity-desktop-environment",
        allow_network=True,
    )


def patch(self):
    from cbuild.util import patch

    lg = self.srcdir / "libgui-wayland"
    sde = self.srcdir / "serenity-desktop-environment"

    patch.patch(
        self,
        sorted((lg / "patches").rglob("*.patch"), key=lambda p: p.name),
        wrksrc="libgui-wayland/serenity",
        apply_args=["--recount", "-C1"],
    )
    patch.patch(
        self,
        sorted((sde / "patches").glob("*.patch"))
        + sorted(self.patches_path.glob("*.patch")),
        wrksrc="libgui-wayland/serenity",
        apply_args=["--recount", "-C1"],
    )

    lg_patches = sorted((self.template_path / "patches-libgui").glob("*.patch"))
    if lg_patches:
        patch.patch(
            self,
            lg_patches,
            wrksrc="libgui-wayland",
            apply_args=["--recount", "-C1"],
        )


def build(self):
    lg = self.chroot_cwd / "libgui-wayland"
    serenity = lg / "serenity"
    lagom = lg / "build/lagom"
    sde = self.chroot_cwd / "serenity-desktop-environment"
    jobs = f"-j{self.make_jobs}"

    self.do(
        "cmake",
        "-S",
        serenity / "Meta/Lagom",
        "-B",
        lagom,
        "-GNinja",
        "-DBUILD_LAGOM=ON",
        "-DENABLE_LAGOM_LIBWEB=ON",
        "-DENABLE_LAGOM_LADYBIRD=OFF",
        "-DENABLE_CLANG_PLUGINS=OFF",
        "-DENABLE_LAGOM_CCACHE=OFF",
        "-DCMAKE_BUILD_TYPE=Release",
        f"-DSDE_ROOT={sde}",
        f"-DSERENITY_CACHE_DIR={lg}/caches",
        "-DENABLE_NETWORK_DOWNLOADS=OFF",
    )

    self.do("ninja", "-C", lagom, jobs, *_generated)
    self.do("ninja", "-C", lagom, jobs, *_libs)
    self.do("ninja", "-C", lagom, jobs, "windowserver", "eglgpu")
    self.do("ninja", "-C", lagom, jobs, *_apps)


def install(self):
    lg = self.chroot_cwd / "libgui-wayland"
    lagom = lg / "build/lagom"
    sde = self.chroot_cwd / "serenity-desktop-environment"

    self.do(
        "bash",
        sde / "scripts/install-framework.sh",
        "--destdir",
        self.chroot_destdir,
        "--prefix",
        "/usr/lib/sde",
        "--build",
        lagom,
        env={
            "LIBGUI_WAYLAND_ROOT": str(lg),
            "SERENITY": str(lg / "serenity"),
            "BUILD": str(lagom),
        },
    )
    # PartitionEditor is packaged separately as partition-editor.
    self.uninstall("usr/lib/sde/share/res/apps/PartitionEditor.af")
    self.install_license("serenity-desktop-environment/LICENSE")
    self.install_license(
        "libgui-wayland/LICENSE", name="LICENSE.libgui-wayland"
    )


@subpackage("serenity-lagom-devel")
def _(self):
    self.subdesc = "development files and framework sources"
    self.depends += [self.parent]
    # The installed SerenityOS source tree contains prebuilt toolchain stubs.
    self.options = [
        "execstack",
        "foreignelf",
        "!scancmd",
        "!scanpkgconf",
        "!scanrundeps",
        "!scanshlibs",
        "!scantrigdeps",
    ]

    return ["usr/lib/sde/framework"]
