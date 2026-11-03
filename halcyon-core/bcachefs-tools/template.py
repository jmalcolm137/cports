pkgname = "bcachefs-tools"
pkgver = "1.39.7"
pkgrel = 0
build_style = "makefile"
# the Makefile must be able to append its own flags to CFLAGS; passing the
# cbuild flags on the command line would make those appends no-ops
make_use_env = True
hostmakedepends = [
    "cargo-auditable",
    "findutils",
    "git",
    "pkgconf",
    "rust-bindgen",
]
makedepends = [
    "keyutils-devel",
    "libaio-devel",
    "libsodium-devel",
    # bcachefs needs the standalone libunwind with libunwind.pc, not LLVM's
    "libunwind-nongnu-devel",
    "linux-headers",
    "lz4-devel",
    "rust-std",
    "udev-devel",
    "userspace-rcu-devel",
    "util-linux-blkid-devel",
    "util-linux-uuid-devel",
    "zlib-ng-compat-devel",
    "zstd-devel",
]
pkgdesc = "Userspace tools for bcachefs"
license = (
    "GPL-2.0-only AND GPL-2.0-or-later AND LGPL-2.1-only AND BSD-2-Clause "
    "AND BSD-3-Clause AND Apache-2.0 AND MIT AND MPL-2.0 AND Unlicense"
)
url = "https://bcachefs.org"
source = f"https://github.com/koverstreet/bcachefs-tools/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "0d2d6f9689212cd1056137f932c6f786bc0c88ad569618b481ace52803c4e990"
# no upstream test target; testing needs loop devices and root
# upstream does not enable LTO for distribution builds yet
options = ["!check", "!lto"]

if self.profile.wordsize == 32:
    broken = "requires 64-bit atomics"

# force the version rather than having the Makefile run git describe or
# cargo metadata, and make sure binaries go to /usr/bin as we have no /sbin
_make_args = [
    f"VERSION={pkgver}",
    "PREFIX=/usr",
    "ROOT_SBINDIR=/usr/bin",
]
make_build_args = [*_make_args]
make_install_args = [*_make_args]


def prepare(self):
    from cbuild.util import cargo

    # the archive has no .git or .version, so without this the Makefile would
    # run cargo metadata (and potentially the network) even when VERSION is
    # passed on the command line
    (self.cwd / ".version").write_text(f"{pkgver}\n")

    cargo.Cargo(self).vendor()


def init_build(self):
    from cbuild.util import cargo

    renv = cargo.get_environment(self)
    renv["CARGO_NET_OFFLINE"] = "true"
    self.make_env.update(renv)

    # libc cannot detect Chimera's musl version through the Rust target spec,
    # so it hides statx even though musl is new enough; tell it otherwise
    self.make_env["RUSTFLAGS"] = (
        self.make_env.get("RUSTFLAGS", "")
        + " --cfg libc_unstable_musl_v1_2_3"
    ).strip()

    # make_use_env means the makefile build style no longer passes these on
    # the command line; put them in the environment instead so cross builds
    # still pick up the target binutils
    for tool in ["AR", "AS", "NM", "RANLIB", "OBJCOPY", "READELF"]:
        self.make_env[tool] = self.get_tool(tool)


def post_install(self):
    self.install_license("COPYING")

    # the DKMS source tree staged by the upstream Makefile is also what CKMS
    # consumes, it just needs a ckms.ini
    self.install_file(
        self.files_path / "ckms.ini",
        f"usr/src/bcachefs-{pkgver}",
        template={"VERSION": pkgver},
    )


@subpackage("bcachefs-ckms")
def _(self):
    self.subdesc = "kernel module sources"
    self.install_if = [self.parent, "ckms"]
    self.depends = [
        self.parent,
        "ckms",
        "clang",
        "gmake",
        "lld",
        "rust",
        "rust-bindgen",
        "rust-src",
    ]

    return ["usr/src"]
