pkgname = "antigravity-cli"
pkgver = "1.5.16"
pkgrel = 0
archs = ["x86_64", "aarch64"]
# upstream ships glibc and musl builds; Chimera uses musl
_arch = {"x86_64": "x64", "aarch64": "arm64"}.get(self.profile.arch)
pkgdesc = "Google Antigravity CLI"
license = "custom:antigravity-cli"
url = "https://github.com/google-antigravity/antigravity-cli"
source = f"{url}/releases/download/{pkgver}/agy_cli_linux_{_arch}_musl.tar.gz"
match self.profile.arch:
    case "aarch64":
        sha256 = (
            "79e2477421b1146ff2e45c4540f19715f20bd61550368508b9072157842560e8"
        )
    case "x86_64":
        sha256 = (
            "7edd47e18176d0c2ed2e12c57c3fd674b2823df4a46a0c5bfc7130e72431e122"
        )
    case _:
        broken = f"not packaged for {self.profile.arch}"
# prebuilt statically linked binary, and upstream ships no license file
options = ["!strip", "!distlicense"]


def install(self):
    # upstream's installer installs the binary as agy
    self.install_bin("antigravity", name="agy")
