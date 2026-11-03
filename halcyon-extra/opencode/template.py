pkgname = "opencode"
pkgver = "2.2.5"
pkgrel = 0
archs = ["x86_64"]

_bunver = "1.4.4"

hostmakedepends = ["bun", "patchelf"]
makedepends = ["libcxxabi-devel", "libgcc-chimera"]
depends = [
    "bash",
    "ca-certificates",
    "curl",
    "libarchive-progs",
    "libcxxabi",
    "libgcc-chimera",
    "ripgrep",
]

pkgdesc = "Open source AI coding agent"
license = "MIT"
url = "https://github.com/anomalyco/opencode"

# The prebuilt binary is produced by Bun and its ABI shim is intentionally
# kept outside the scan paths; dependencies are declared explicitly.
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
    f"{url}/archive/refs/tags/v{pkgver}.tar.gz",
    f"https://github.com/oven-sh/bun/releases/download/bun-v{_bunver}/bun-linux-x64-musl-baseline.zip",
]
source_paths = [".", "bun-baseline"]
sha256 = [
    "04621edf6c47c2c7a36982ef39914d482c16977708fbd7b779f49f928bdc4fba",
    "6e9c37098b293920aed28bfb51ab240e26d23bfdd9bbfecb3ad428ac166549bc",
]

_target = "linux-x64-baseline-musl"
_outdir = f"packages/cli/dist/cli-{_target}/bin/opencode"


def prepare(self):
    # The build needs the native musl variants of several optional
    # dependencies, including the web UI's lightningcss module.
    self.do(
        "bun",
        "install",
        "--os=*",
        "--cpu=*",
        "--libc=*",
        "--frozen-lockfile",
        "--ignore-scripts",
        f"--cache-dir={self.chroot_cwd / '.bun-cache'}",
        env={"HUSKY": "0"},
        allow_network=True,
    )


def build(self):
    # The compiled CLI and some native modules link against the libstdc++
    # ABI. Provide the small set of symbols the Bun runtime imports instead
    # of depending on GCC's libstdc++ package. Modules that need the wider
    # C++ ABI, such as @parcel/watcher, fall back to the fs.watch backend.
    self.cp(self.files_path / "libstdcxx_compat.c", ".")
    self.do(
        "clang",
        "-shared",
        "-fPIC",
        "-O2",
        "-Wl,-soname,libstdc++.so.6",
        "-o",
        "libstdc++.so.6",
        "libstdcxx_compat.c",
        "-Wl,--no-as-needed",
        "-lc++abi",
    )

    bun = self.chroot_cwd / "bun-baseline" / "bun"
    self.do("chmod", "755", str(bun))

    self.do(
        "bun",
        "run",
        "./script/build.ts",
        "--skip-install",
        wrksrc="packages/cli",
        env={
            "OPENCODE_VERSION": pkgver,
            "OPENCODE_TARGET": _target,
            "OPENCODE_BUN_EXECUTABLE": str(bun),
        },
    )

    for shell in ["bash", "fish", "zsh"]:
        self.do(
            "sh",
            "-c",
            f"LD_LIBRARY_PATH=. ./{_outdir} --completions {shell} > opencode.{shell}",
        )

    # The shim is installed in a private prefix next to the CLI.
    self.do("patchelf", "--set-rpath", "$ORIGIN/../lib/opencode", _outdir)


def install(self):
    self.install_bin(_outdir)
    self.install_file("libstdc++.so.6", "usr/lib/opencode", mode=0o755)

    self.install_file(
        "opencode.bash", "usr/share/bash-completion/completions", name="opencode"
    )
    self.install_file(
        "opencode.fish",
        "usr/share/fish/vendor_completions.d",
        name="opencode.fish",
    )
    self.install_file(
        "opencode.zsh", "usr/share/zsh/site-functions", name="_opencode"
    )

    self.install_license("LICENSE")
