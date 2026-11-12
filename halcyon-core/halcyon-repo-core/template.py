pkgname = "halcyon-repo-core"
pkgver = "0.1.0"
pkgrel = 0
archs = ["x86_64"]
build_style = "meta"
depends = ["apk-tools"]
pkgdesc = "Halcyon core APK repository configuration"
license = "custom:meta"
url = "https://halcyon-linux.org"
# Configuration-only package; no tests to run.
options = ["etcfiles", "!check"]


def install(self):
    self.install_file(
        self.files_path / "20-halcyon-core.list",
        "etc/apk/repositories.d",
    )
    self.install_file(
        self.files_path / "halcyon-linux.rsa.pub",
        "etc/apk/keys",
    )
