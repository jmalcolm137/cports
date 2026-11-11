pkgname = "bun"
pkgver = "1.4.4"
pkgrel = 0
archs = ["x86_64"]

hostmakedepends = ["patchelf"]
makedepends = ["libcxxabi-devel"]
depends = ["ca-certificates", "libcxxabi"]

pkgdesc = "Fast JavaScript runtime, bundler, test runner and package manager"
license = "MIT AND LGPL-2.0-or-later"
url = "https://bun.sh"

# The prebuilt binary is stripped and its ABI shim is intentionally kept
# outside the scan paths; dependencies are declared explicitly.
options = [
    "!check",
    "!cross",
    "!debug",
    "!lto",
    "!scanrundeps",
    "!scanshlibs",
    "!strip",
]

source = [
    f"https://github.com/oven-sh/bun/releases/download/bun-v{pkgver}/bun-linux-x64-musl.zip",
]
sha256 = ["a5a8ccc5e74dcb883fe974f125a7bdb3b41e5195ed1b870e73f17effd3eb2b2d"]


def build(self):
    # Bun's musl build imports a small subset of the libstdc++ ABI. Provide a
    # self-contained shim for those symbols instead of depending on GCC's
    # libstdc++ package.
    self.cp(self.files_path / "libstdcxx_compat.c", ".")
    self.do(
        "clang",
        "-shared",
        "-fPIC",
        "-O2",
        "-o",
        "libstdc++.so.6",
        "libstdcxx_compat.c",
        "-Wl,--no-as-needed",
        "-lc++abi",
    )

    # The shim lives in a private prefix next to the executable's sibling lib
    # directory.
    self.do("patchelf", "--set-rpath", "$ORIGIN/../lib/bun", "bun")

    for shell in ["bash", "fish", "zsh"]:
        self.do(
            "sh",
            "-c",
            f"SHELL=/bin/{shell} LD_LIBRARY_PATH=. ./bun completions {shell} > bun.{shell}",
        )


def install(self):
    self.install_bin("bun")
    self.install_link("usr/bin/bunx", "bun")

    self.install_dir("usr/lib/bun")
    self.install_file("libstdc++.so.6", "usr/lib/bun", mode=0o755)

    self.install_file(
        "bun.bash", "usr/share/bash-completion/completions", name="bun"
    )
    self.install_file(
        "bun.fish", "usr/share/fish/vendor_completions.d", name="bun.fish"
    )
    self.install_file("bun.zsh", "usr/share/zsh/site-functions", name="_bun")

    self.install_license(self.files_path / "LICENSE.md")
