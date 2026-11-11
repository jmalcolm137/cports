pkgname = "cosmic"
pkgver = "1.11.0"
pkgrel = 0
archs = ["x86_64", "aarch64"]
prepare_after_patch = True
hostmakedepends = [
    "cargo-auditable",
    "git",
    "gmake",
    "just",
    "pkgconf",
    "python",
]
makedepends = [
    "alsa-lib-devel",
    "dbus-devel",
    "elogind-devel",
    "flatpak-devel",
    "glib-devel",
    "libdisplay-info-devel",
    "libdrm-devel",
    "libinput-devel",
    "libseat-devel",
    "libxcb-devel",
    "libxkbcommon-devel",
    "mesa-devel",
    "mesa-gbm-devel",
    "pipewire-devel",
    "pixman-devel",
    "rust-std",
    "udev-devel",
    "wayland-devel",
    "wayland-protocols",
    "xcb-util-wm-devel",
]
depends = [
    "accountsservice",
    "bluez",
    "dbus",
    "elogind",
    "flatpak",
    "fontconfig",
    "freetype",
    "glib",
    "hicolor-icon-theme",
    "iso-codes",
    "libdisplay-info",
    "libdrm",
    "libinput",
    "libseat-seatd",
    "libxkbcommon",
    "mesa-egl-libs",
    "mesa-gbm-libs",
    "mesa-gl-libs",
    "networkmanager",
    "pipewire",
    "pipewire-libs",
    "pixman",
    "polkit",
    "shared-mime-info",
    "upower",
    "wayland",
    "xdg-desktop-portal",
    "xdg-user-dirs",
    "xdg-utils",
    "xwayland",
]
pkgdesc = "COSMIC desktop environment"
license = "GPL-3.0-only AND MPL-2.0 AND CC-BY-SA-4.0"
url = "https://github.com/pop-os/cosmic-epoch"
source = [
    "https://github.com/pop-os/cosmic-epoch/archive/refs/tags/epoch-1.11.0.tar.gz",
    "https://github.com/pop-os/cosmic-session/archive/4b0a0a24e98b9e755b6a7146e4cb29539cacda0a.tar.gz",
    "https://github.com/pop-os/cosmic-comp/archive/8cb1802caada438bb5cc7670dfabdaca5fad0502.tar.gz",
    "https://github.com/pop-os/cosmic-panel/archive/ca20ce3185b3b4404f429d59d429c40b58a2ddef.tar.gz",
    "https://github.com/pop-os/cosmic-applets/archive/328d142faac17c9cc3e00d434d05060411c007ea.tar.gz",
    "https://github.com/pop-os/cosmic-applibrary/archive/3651caff79bcf36f7c16ba5ed4f41de530c7b1a7.tar.gz",
    "https://github.com/pop-os/cosmic-launcher/archive/b6c2ed7d1224a94568b083162ea6b79409ef111b.tar.gz",
    "https://github.com/pop-os/cosmic-settings/archive/f1d00fc06e18203e880771617657067c10c43321.tar.gz",
    "https://github.com/pop-os/cosmic-settings-daemon/archive/655b14fb9572dd7f7231ec6c343c63984e99741a.tar.gz",
    "https://github.com/pop-os/xdg-desktop-portal-cosmic/archive/f448ddfb296bf7bb23517b24b2f532559a334a1c.tar.gz",
    "https://github.com/pop-os/cosmic-osd/archive/4f96e98981712f02b98f704a6f19c4c6a58b378b.tar.gz",
    "https://github.com/pop-os/cosmic-bg/archive/9520e16758693bc2f6845d52680f236d548edda2.tar.gz",
    "https://github.com/pop-os/cosmic-workspaces-epoch/archive/cb953ea0e6fb45ac8f62f9c52f1347c971388e03.tar.gz",
    "https://github.com/pop-os/cosmic-notifications/archive/382927dc48964f3b098429ad6b836cc4b7e7ecf2.tar.gz",
    "https://github.com/pop-os/cosmic-icons/archive/f1a282a0822aed1f0083dd2ab2e6c65bd5b401eb.tar.gz",
    "https://github.com/pop-os/cosmic-greeter/archive/80e8a104b75a01ab8df52bca7b8bde6dbcdb8133.tar.gz",
    "https://github.com/pop-os/cosmic-screenshot/archive/45549f7e940d495ecee9268f58824668814e970c.tar.gz",
    "https://github.com/pop-os/cosmic-edit/archive/4ac1cc84f784d4f89327f3d3459af2633ceb4f12.tar.gz",
    "https://github.com/pop-os/cosmic-term/archive/699ac42384b917029082d45a01a9261a4ba75c45.tar.gz",
    "https://github.com/pop-os/cosmic-randr/archive/f1a97655c97e8799bf4a37a8f5103a8ab5e5068d.tar.gz",
    "https://github.com/pop-os/cosmic-files/archive/3cc4b8003e8d08349c7ced8a9cdd10cdfa45d38c.tar.gz",
    "https://github.com/pop-os/cosmic-store/archive/16b1667e43c634318a99995c8eb77c23603ae560.tar.gz",
    "https://github.com/pop-os/cosmic-wallpapers/archive/da595bba495cb8fc57f26505621fc25000218349.tar.gz",
    "https://github.com/pop-os/cosmic-idle/archive/6d6f07af60bb307882cdcbd0bda0a6fc76bd0df3.tar.gz",
    "https://github.com/pop-os/cosmic-player/archive/34a41f247a37eb681dd5c27c832e2d1f3c1dc1e4.tar.gz",
    "https://github.com/pop-os/cosmic-initial-setup/archive/653a4db1841e70ef8e36d3c6f0a14b7fce335697.tar.gz",
    "https://github.com/pop-os/launcher/archive/86c2639ba82f4d846c801abe84fcea8ae8e7d716.tar.gz",
    "https://github.com/pop-os/cosmic-monitor/archive/d79ff440dfa899ea6e9a3019dcfd9f9e8a44448d.tar.gz",
    "https://github.com/pop-os/cosmic-sound-theme/archive/bf5335fe1af0cb3bee83e1ad2371410ee434658d.tar.gz",
    "https://github.com/pop-os/cosmic-osk/archive/6b146a2b0a23d88ae84223ad06c6813bda5a9386.tar.gz",
    "https://github.com/pop-os/cosmic-viewer/archive/300210f1c7d86ba14a43602e40dd5fe1deb16703.tar.gz",
]
source_paths = [
    ".",
    "+cosmic-session",
    "+cosmic-comp",
    "+cosmic-panel",
    "+cosmic-applets",
    "+cosmic-app-library",
    "+cosmic-launcher",
    "+cosmic-settings",
    "+cosmic-settings-daemon",
    "+xdg-desktop-portal-cosmic",
    "+cosmic-osd",
    "+cosmic-bg",
    "+cosmic-workspaces-epoch",
    "+cosmic-notifications",
    "+cosmic-icons",
    "+cosmic-greeter",
    "+cosmic-screenshot",
    "+cosmic-edit",
    "+cosmic-term",
    "+cosmic-randr",
    "+cosmic-files",
    "+cosmic-store",
    "+cosmic-wallpapers",
    "+cosmic-idle",
    "+cosmic-player",
    "+cosmic-initial-setup",
    "+pop-launcher",
    "+cosmic-monitor",
    "+cosmic-sound-theme",
    "+cosmic-osk",
    "+cosmic-viewer",
]
sha256 = [
    "1829da06de86afebec2bb97b2e8e823847e81ebf2abdd410f22768724035ec5d",
    "8ad562ea4fc7c0536dd65f0755a70435f2aff6e34425c86cc2f939f77595fc01",
    "17e6cfccb612d4e9fcb2c9d44617a700ca91a9db922bf30f60fb8fadbb6b19be",
    "27854c7d3fc54cb29bc866b8421a078aa6b396ea73e2d88fe4ec0cf4fdd55704",
    "d53fa086da4af36e75cc84534e3a798173e9ac2a540af5ea182b5aeb93b29312",
    "c555779bd9d3d992695a6a25fe84256e0234b57990d5242ce924535dab55d294",
    "ff7c5e03757a68a109967573a0c88d04ffa3515f00f88c4a5d3946f0f1965af3",
    "f662118d69abe86fa51d1c5827ebeafb8f37dd37911daab008571e4f9f53070e",
    "6e13e95652c2d03c83e8ad323a19645b240f161113058dabcff2345a3e8b9c74",
    "f0f0a737f4a1d74c88b294de25dc26981f027cd504fb3325116c0b1af5e963b5",
    "af1e79a5c525bd4926ad32b5403fcac3c681520beb592c404668ad58b702470d",
    "b8081dadcbac28d2891bbd0712a88bf3cbc454006cd3b4f7d10eb1a01fdd5dd8",
    "811d9ba537c450409f3b4cdbebaf3e37df03ddde651699a3654689fc1d484f05",
    "67e2c0d8ddab507965832a1989e25f519f7598d2e23784d61f3ff9ec4874d558",
    "c53f0ba50d43ee0de4abba6140dedf6540008917553c2df765363aeef24966e4",
    "f458f7d8e7db183ddce696b4b8da045329f62d65615e7120aa7c84c3e70dd935",
    "94a7328ac5d41259487eb0ac30f34a41605dc9630d7192295e77ef3107fa2d69",
    "1166cd449332e70b17974bc78a5e8e6fb57bb2a0a89c657253ca0560a78bbeb0",
    "864051f89d7f046162b1cecc2b22c2108181106f6ce61db927be02a023f3b4de",
    "24677e8387151fdc0c9dee089a92378e07b7cb22f6d8282d724d9b7d735e601d",
    "d047c1cb0d0abb400aa378dffc1a96ad5a6d5f8f412d5319a7ee79d03ea405ad",
    "2344b4bd2f8a0572a8b845b0b72b103b6af6e349404a7c74e5c37b632fb75594",
    "4f9bf51d6622aeeaa9c4ee4980924b303089bfa7478c2f497987ce05e7eccbdc",
    "1d4d28ba36bbe77172d06fefae943eb05ea3662823930adcbf73ed3dd2c1952e",
    "2636946edd071f4d774600dd114bdd7b84444eab9b8af4f41481da50932750d7",
    "101c01263874b2bdfa49693ea04153ac8920efbbb43d7991999cd64c2c20597b",
    "f63836cb58458294fe0782c66f9e05e8daafe2a22d38d2dac53b24fff7fec9d0",
    "7af6f3abe9b306252bcf860dc5ba6ccfd90ad919d98f831aa8c6d0ae498a0633",
    "d4c8e95d7fcafdad1146803b4810aa48f609074d00a19e9b588f4ccf99339f33",
    "187a787f05deba4db974414e786f9080ecbdc945141ed44aad433990404c7fce",
    "8cbd3d4db79295cbc374aa6331b6e68e0f131615e996cefffb404a3b401bee92",
]
# The epoch components default to systemd integration. Build the
# systemd-free variants and install dinit-compatible session helpers instead.
tool_flags = {"RUSTFLAGS": ["-Clink-arg=-fuse-ld=lld"]}
hardening = ["!int"]
# Checks are disabled because this is a multi-component meta build.
options = ["!check", "!cross", "!debug", "!lto"]

_rust_components = [
    "cosmic-app-library",
    "cosmic-applets",
    "cosmic-bg",
    "cosmic-comp",
    "cosmic-edit",
    "cosmic-files",
    "cosmic-greeter",
    "cosmic-idle",
    "cosmic-initial-setup",
    "cosmic-launcher",
    "cosmic-monitor",
    "cosmic-notifications",
    "cosmic-osd",
    "cosmic-osk",
    "cosmic-panel",
    "cosmic-player",
    "cosmic-randr",
    "cosmic-screenshot",
    "cosmic-session",
    "cosmic-settings",
    "cosmic-settings-daemon",
    "cosmic-store",
    "cosmic-term",
    "cosmic-viewer",
    "cosmic-workspaces-epoch",
    "pop-launcher",
    "xdg-desktop-portal-cosmic",
]


def _cargo_env(self, offline=True):
    return {
        "CARGO_HOME": str(self.chroot_cwd / ".cargo-home"),
        "CARGO_BUILD_JOBS": str(self.make_jobs),
        "CARGO_NET_OFFLINE": "true" if offline else "false",
        "VERGEN_GIT_COMMIT_DATE": "1970-01-01",
        "VERGEN_GIT_SHA": "unknown",
    }


def patch(self):
    from cbuild.util import patch

    patch.patch(
        self,
        sorted((self.template_path / "patches").glob("*.patch")),
        apply_args=["--recount", "-C1"],
    )


def prepare(self):
    env = _cargo_env(self, offline=False)
    for component in _rust_components:
        self.do(
            "cargo",
            "fetch",
            "--locked",
            wrksrc=component,
            env=env,
            allow_network=True,
        )


def build(self):
    self.do("just", "build", env=_cargo_env(self))


def install(self):
    self.do(
        "just",
        f"rootdir={self.chroot_destdir}",
        "prefix=/usr",
        "install",
        env=_cargo_env(self),
    )

    # COSMIC installs systemd units and a systemd session target; dinit does
    # not consume them. Remove them and install the dinit service helper.
    self.uninstall("usr/lib/systemd", missing_ok=True)
    self.uninstall("usr/lib/sysusers.d/cosmic-greeter.conf", missing_ok=True)
    self.uninstall("usr/lib/tmpfiles.d/cosmic-greeter.conf", missing_ok=True)
    self.install_file(
        self.files_path / "cosmic-dinit-service", "usr/libexec", mode=0o755
    )
    self.install_file(
        self.files_path / "50-cosmic-dinit.rules",
        "usr/share/polkit-1/rules.d",
        mode=0o644,
    )
    self.install_license("cosmic-session/LICENSE")
