pkgname = "herdr"
pkgver = "0.9.5"
pkgrel = 0
archs = ["x86_64", "aarch64"]
build_style = "cargo"
hostmakedepends = ["cargo-auditable", "git"]
makedepends = ["rust-std"]
depends = ["ca-certificates", "curl", "git"]
pkgdesc = "Terminal workspace manager for AI coding agents"
license = "Apache-2.0"
url = "https://herdr.dev"
source = [
    f"{url}/archive/refs/tags/v{pkgver}.tar.gz",
]
source_paths = [".", "zig016"]
sha256 = [
    "a2486b09a8153630f6a19e72606ba1c961a6194bce13c09cba67ccce5e4252de",
]

# herdr's vendored libghostty-vt uses the Zig 0.16 build API; use the upstream
# static toolchain rather than the newer in-tree zig package
_zigver = "0.16.0"

match self.profile.arch:
    case "x86_64":
        source += [
            f"https://ziglang.org/download/{_zigver}/zig-x86_64-linux-{_zigver}.tar.xz"
        ]
        sha256 += [
            "70e49664a74374b48b51e6f3fdfbf437f6395d42509050588bd49abe52ba3d00"
        ]
    case "aarch64":
        source += [
            f"https://ziglang.org/download/{_zigver}/zig-aarch64-linux-{_zigver}.tar.xz"
        ]
        sha256 += [
            "ea4b09bfb22ec6f6c6ceac57ab63efb6b46e17ab08d21f69f3a48b38e1534f17"
        ]

# upstream runs the test suite under cargo-nextest, which isolates every test
# in its own process; several tests also require a normal host environment
# (root-owned sticky /tmp, ACL support), which the cbuild sandbox lacks
#
# the completions are generated with the target binary
options = ["!check", "!cross"]


def _set_zig_env(self):
    self.make_env["ZIG"] = str(self.chroot_cwd / "zig016" / "zig")
    self.make_env["ZIG_GLOBAL_CACHE_DIR"] = str(self.chroot_cwd / ".zig-cache")


def init_build(self):
    _set_zig_env(self)


def init_check(self):
    _set_zig_env(self)


def init_install(self):
    _set_zig_env(self)


def prepare(self):
    # herdr pins its own libghostty-vt commit and carries API patches for it,
    # so the system libghostty-vt package cannot be used; build the vendored
    # copy with zig instead
    #
    # the project already has a vendor/ directory for its path dependencies,
    # so keep the registry crates separate
    self.cargo.vendor(args=["cargo-vendor"])

    # Herdr vendors libghostty-vt and builds it with Zig; fetch its package
    # dependencies up front so the offline cargo build can reuse the cache
    _set_zig_env(self)
    self.do(
        self.make_env["ZIG"],
        "build",
        "--fetch=all",
        wrksrc="vendor/libghostty-vt",
        env={"ZIG_GLOBAL_CACHE_DIR": self.make_env["ZIG_GLOBAL_CACHE_DIR"]},
        allow_network=True,
    )


def post_build(self):
    from cbuild.util import cargo

    for shell in ["bash", "fish", "zsh"]:
        with open(self.cwd / f"herdr.{shell}", "w") as f:
            self.do(
                cargo.target_path(self, "herdr"),
                "completion",
                shell,
                stdout=f,
            )


def post_install(self):
    for shell in ["bash", "fish", "zsh"]:
        self.install_completion(f"herdr.{shell}", shell, "herdr")

    self.install_license("LICENSE")
