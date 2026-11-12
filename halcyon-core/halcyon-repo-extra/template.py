pkgname = "halcyon-repo-extra"
pkgver = "0.1.0"
pkgrel = 0
archs = ["x86_64"]
build_style = "meta"
depends = ["halcyon-repo-core"]
pkgdesc = "Halcyon extra APK repository configuration"
license = "custom:meta"
url = "https://halcyon-linux.org"
# Configuration-only package; no tests to run.
options = ["etcfiles", "!check"]


def install(self):
    self.install_file(
        self.files_path / "21-halcyon-extra.list",
        "etc/apk/repositories.d",
    )
