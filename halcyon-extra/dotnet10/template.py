pkgname = "dotnet10"
pkgver = "10.0.113"
pkgrel = 0
archs = ["x86_64"]

_bootstrap = "10.0.113-r0"
_gccver = "15.2.0-r9"

hostmakedepends = [
    "bash",
    "cmake",
    "file",
    "findutils",
    "ggrep",
    "git",
    "gtar",
    "grpc",
    "jq",
    "ninja",
    "nodejs",
    "patchelf",
    "pigz",
    "protobuf-protoc",
    "rsync",
    "unzip",
    "xz",
    "zip",
]
makedepends = [
    "brotli-devel",
    "heimdal-devel",
    "icu-devel",
    "libgit2-devel",
    "libucontext-devel",
    "libunwind-devel",
    "libxml2-devel",
    "openssl3-devel",
    "rapidjson",
    "zlib-ng-compat-devel",
]
depends = ["ca-certificates", "heimdal-gssapi-libs", "icu-libs"]
pkgdesc = ".NET SDK and runtime"
license = "MIT"
url = "https://dotnet.microsoft.com"

options = ["!check", "!cross", "!lto", "etcfiles"]
hardening = ["!int"]

source = [
    f"https://github.com/dotnet/dotnet/archive/refs/tags/v{pkgver}.tar.gz",
    f"https://dl-cdn.alpinelinux.org/alpine/edge/community/x86_64/dotnet10-stage0-bootstrap-{_bootstrap}.apk>bootstrap.tar.gz",
    f"https://dl-cdn.alpinelinux.org/alpine/edge/community/x86_64/dotnet10-stage0-artifacts-{_bootstrap}.apk>artifacts.tar.gz",
    f"https://dl-cdn.alpinelinux.org/alpine/edge/main/x86_64/libstdc%2B%2B-{_gccver}.apk>libstdcxx.tar.gz",
    f"https://dl-cdn.alpinelinux.org/alpine/edge/main/x86_64/libgcc-{_gccver}.apk>libgcc.tar.gz",
]
source_paths = [
    ".",
    "bootstrap-pkg",
    "artifacts-pkg",
    "libstdcxx-pkg",
    "libgcc-pkg",
]
sha256 = [
    "5c3a5dcc776c94d314853ccf24d3a2b5627f2249c7defb8a8f0cbade8ecd4631",
    "d16544ef7527bbbd1a653e00bac8d115250874446feea2b5a07e725107b169d5",
    "82f2fccdd3c1faa7f0331c52a5ede15262c43539bf3a25b405d7817ed45fd506",
    "adfebfc0c4b80c293be8cc802a7fb73d7f5854f01b47ff1f40282d18f255b357",
    "01c9609197de10519ceb204a09d1efa54baad145f65bf00ba0908086692ca3fe",
]

_sdkver = "10.0.113"
_sdkroot = "/usr/lib/dotnet"


def _fix_modes(self, root):
    exec_names = {
        "apphost",
        "createdump",
        "dnx",
        "dotnet",
        "ilc",
        "singlefilehost",
    }
    data_suffixes = {
        ".a",
        ".c",
        ".cmake",
        ".cpp",
        ".def",
        ".dll",
        ".h",
        ".in",
        ".json",
        ".m",
        ".o",
        ".orig",
        ".pdb",
        ".props",
        ".pubxml",
        ".targets",
        ".txt",
        ".xml",
    }

    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue

        mode = path.stat().st_mode
        name = path.name

        if name in exec_names or (name.startswith("lib") and ".so" in name):
            path.chmod(mode | 0o111)
        elif name.endswith(".sh"):
            path.chmod(mode | 0o111)
        elif path.suffix in data_suffixes:
            path.chmod(mode & ~0o111)


def _check_no_gcc(self, root):
    script = f'''
bad=
for f in $(find "{root}" -type f); do
    if readelf -d "$f" 2>/dev/null | grep -qE 'libstdc\\+\\+\\.so\\.6|libgcc_s\\.so\\.1'; then
        bad="$bad $f"
    fi
done
if [ -n "$bad" ]; then
    echo "GCC runtime dependency found:$bad" >&2
    exit 1
fi
'''
    self.do("sh", "-c", script)


def _sdk_archive(self):
    matches = sorted(
        (self.cwd / "artifacts/assets/Release").glob("dotnet-sdk-*.tar.gz")
    )
    if not matches:
        self.error("source build produced no dotnet SDK archive", bt=True)
    return str(
        self.chroot_cwd / "artifacts/assets/Release" / matches[0].name
    )


def post_patch(self):
    # Keep all private build state outside the VMR tree. The source-build
    # binary scanner walks the tree and would otherwise block on the .NET
    # diagnostic FIFOs/sockets created under TMPDIR.
    aux = self.statedir / "aux"
    auxc = self.chroot_statedir / "aux"

    for d in [
        "bootstrap",
        "artifacts",
        "gcc-libs",
        "tools",
        "dotnet-home",
        "tmp",
        "nuget",
        "smoke",
    ]:
        path = aux / d
        self.rm(path, recursive=True, force=True)
        self.mkdir(path, parents=True)

    # The Alpine stage0 SDK is only used to bootstrap the build. It links
    # against GCC's libstdc++/libgcc, so provide those privately.
    self.do(
        "cp",
        "-a",
        "bootstrap-pkg/usr/lib/dotnet/bootstrap/10.0.113/.",
        str(auxc / "bootstrap") + "/",
    )

    # The stage0 bootstrap and artifacts packages both contribute NuGet
    # packages to the previously-source-built package directory.
    self.do(
        "sh",
        "-c",
        f"cp -al artifacts-pkg/usr/lib/dotnet/artifacts/10.0.113/. {auxc}/artifacts/ && "
        f"cp -al bootstrap-pkg/usr/lib/dotnet/artifacts/10.0.113/. {auxc}/artifacts/",
    )

    self.do(
        "sh",
        "-c",
        f"cp -a libstdcxx-pkg/usr/lib/libstdc++.so.6* {auxc}/gcc-libs/ && "
        f"cp -a libgcc-pkg/usr/lib/libgcc_s.so.1 {auxc}/gcc-libs/",
    )

    # The source archives are only needed to populate the directories above.
    # The merged artifacts directory uses hardlinks, so these can be dropped.
    for d in ["bootstrap-pkg", "artifacts-pkg", "libstdcxx-pkg", "libgcc-pkg"]:
        self.rm(d, recursive=True, force=True)

    # The build scripts use GNU grep and GNU tar options that the base
    # BSD userland versions lack.
    self.ln_s("/usr/bin/ggrep", aux / "tools" / "grep")
    self.ln_s("/usr/bin/gtar", aux / "tools" / "tar")

    manifest = f"""\
{{
  "release": "10.0.13",
  "channel": "10.0",
  "tag": "v{pkgver}",
  "sdkVersion": "{_sdkver}",
  "runtimeVersion": "10.0.13",
  "aspNetCoreVersion": "10.0.13",
  "sourceRepository": "https://github.com/dotnet/dotnet",
  "sourceVersion": "4099f83977f4d29604a9aeb971fb0a7bc1d5f699",
  "officialBuildId": "20261004.4"
}}
"""
    with open(aux / "release.json", "w") as f:
        f.write(manifest)


def build(self):
    aux = self.statedir / "aux"
    auxc = self.chroot_statedir / "aux"

    cflags = self.get_cflags(hardening=[], shell=True)
    cxxflags = self.get_cxxflags(hardening=[], shell=True)
    cflags += ' -D_GNU_SOURCE -DLIBC_SO=\\"libc.musl-x86_64.so.1\\"'
    cxxflags += ' -D_GNU_SOURCE -DLIBC_SO=\\"libc.musl-x86_64.so.1\\"'

    env = {
        "CC": "/usr/bin/clang",
        "CXX": "/usr/bin/clang++",
        "CLR_CC": "/usr/bin/clang",
        "CLR_CXX": "/usr/bin/clang++",
        "CFLAGS": cflags,
        "CXXFLAGS": cxxflags,
        "LDFLAGS": self.get_ldflags(hardening=[], shell=True),
        "DOTNET_ROOT": str(auxc / "bootstrap"),
        "DOTNET_CLI_HOME": str(auxc / "dotnet-home"),
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
        "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
        "DOTNET_NOLOGO": "1",
        "DOTNET_SYSTEM_NET_DISABLEIPV6": "1",
        "DOTNET_LTTng": "0",
        "DOTNET_BUNDLE_EXTRACT_BASE_DIR": str(auxc / "tmp"),
        "HOME": str(auxc / "dotnet-home"),
        "NUGET_PACKAGES": str(auxc / "nuget"),
        "TMPDIR": str(auxc / "tmp"),
        "LD_LIBRARY_PATH": str(auxc / "gcc-libs"),
        "PATH": ":".join(
            [
                str(auxc / "tools"),
                str(auxc / "bootstrap"),
                "/usr/lib/llvm22/bin",
                "/usr/bin",
                "/bin",
            ]
        ),
        "LANG": "C.UTF-8",
        "CI": "",
    }

    args = [
        "/v:minimal",
        "/p:LogVerbosity=minimal",
        "/p:MinimalConsoleLogOutput=true",
        "/p:CleanWhileBuilding=true",
        "/p:OfficialBuilder=Alpine",
        "/p:ContinueOnPrebuiltBaselineError=true",
        "/p:TargetRid=linux-musl-x64",
        "/p:DefaultSubsets=clr+libs+tools+host+packs+tasks",
        "/p:CMakeArgs=-DHeimdalGssApi=ON",
        "/p:FeatureXplatEventSource=false",
        "/p:UseSystemLibs=+brotli+zlib+rapidjson+libunwind-lttng",
    ]

    self.do(
        "./build.sh",
        "--with-sdk",
        str(auxc / "bootstrap"),
        "--with-packages",
        str(auxc / "artifacts"),
        "--release-manifest",
        str(auxc / "release.json"),
        "--source-only",
        "--",
        *args,
        env=env,
        allow_network=True,
    )

    # Smoke test the produced SDK and verify it does not pull in GCC runtime
    # libraries.
    archive = _sdk_archive(self)
    self.do("tar", "xzf", archive, "-C", str(auxc / "smoke"), "--no-same-owner")
    self.do(
        str(auxc / "smoke" / "dotnet"),
        "--info",
        env={
            "DOTNET_ROOT": str(auxc / "smoke"),
            "DOTNET_CLI_HOME": str(auxc / "dotnet-home"),
            "HOME": str(auxc / "dotnet-home"),
            "TMPDIR": str(auxc / "tmp"),
            "PATH": "/usr/bin:/bin",
            "LANG": "C.UTF-8",
        },
    )
    _check_no_gcc(self, str(auxc / "smoke"))


def install(self):
    archive = _sdk_archive(self)

    self.install_dir("usr/lib/dotnet")
    self.do(
        "tar",
        "xzf",
        archive,
        "-C",
        str(self.chroot_destdir / "usr/lib/dotnet"),
        "--no-same-owner",
    )

    root = self.destdir / "usr/lib/dotnet"

    for path in root.glob(
        "shared/Microsoft.NETCore.App/*/libcoreclrtraceptprovider.so"
    ):
        path.unlink()

    _fix_modes(self, root)

    # libmscordbi needs to find libmscordaccore in the same directory.
    for path in root.rglob("libmscordbi.so"):
        rel = path.relative_to(self.destdir)
        self.do(
            "patchelf",
            "--set-rpath",
            "$ORIGIN",
            str(self.chroot_destdir / rel),
        )

    _check_no_gcc(self, str(self.chroot_destdir / "usr/lib/dotnet"))

    self.install_dir("usr/bin")
    self.install_link("usr/bin/dotnet", "../lib/dotnet/dotnet")
    if (root / "dnx").is_file():
        self.install_link("usr/bin/dnx", "../lib/dotnet/dnx")

    self.install_file(self.files_path / "dotnet.sh", "etc/profile.d")
    self.install_file(self.files_path / "install_location", "etc/dotnet")
    self.install_file(
        self.files_path / "install_location_x64", "etc/dotnet"
    )

    self.install_completion(
        "src/sdk/scripts/register-completions.bash", "bash", "dotnet"
    )
    self.install_completion(
        "src/sdk/scripts/register-completions.zsh", "zsh", "dotnet"
    )

    self.install_license("LICENSE.TXT")
