pkgname = "ab-av1"
pkgver = "0.11.7"
pkgrel = 0
build_style = "cargo"
hostmakedepends = ["cargo-auditable", "pkgconf"]
makedepends = ["rust-std"]
depends = ["ffmpeg"]
pkgdesc = "AV1 encoding with fast VMAF sampling"
license = "MIT"
url = "https://github.com/alexheretic/ab-av1"
source = f"{url}/archive/refs/tags/v{pkgver}.tar.gz"
sha256 = "7c464cec24a40889ebb73ae22c86ff169678cd13f6e3e89293725043daf5b2d2"
# generates completions with the target binary
options = ["!cross"]


def post_build(self):
    from cbuild.util import cargo

    for shell in ["bash", "fish", "zsh"]:
        with open(self.cwd / f"ab-av1.{shell}", "w") as f:
            self.do(
                cargo.target_path(self, "ab-av1"),
                "print-completions",
                shell,
                stdout=f,
            )


def post_install(self):
    for shell in ["bash", "fish", "zsh"]:
        self.install_completion(f"ab-av1.{shell}", shell, "ab-av1")

    self.install_license("LICENSE")
