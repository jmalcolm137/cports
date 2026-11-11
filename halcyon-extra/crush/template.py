pkgname = "crush"
pkgver = "0.100.0"
pkgrel = 0
archs = ["x86_64"]
depends = ["ca-certificates"]
pkgdesc = "Glamorous AI coding agent for the terminal"
license = "custom:crush"
url = "https://github.com/charmbracelet/crush"
source = f"{url}/releases/download/v{pkgver}/crush_{pkgver}_Linux_x86_64.tar.gz"
sha256 = "122d4afe0e3bb0fc4c571f58b0c08d485c8733f272e962a02064c2150cd7a152"
# Prebuilt Go release binary; there is no test suite in the archive and the
# binary is already stripped.
options = ["!check", "!strip"]


def build(self):
    pass


def install(self):
    self.install_file("crush", "usr/bin", mode=0o755)
    self.install_file(
        "completions/crush.bash",
        "usr/share/bash-completion/completions",
        name="crush",
        mode=0o644,
    )
    self.install_file(
        "completions/crush.fish",
        "usr/share/fish/vendor_completions.d",
        name="crush.fish",
        mode=0o644,
    )
    self.install_file(
        "completions/crush.zsh",
        "usr/share/zsh/site-functions",
        name="_crush",
        mode=0o644,
    )
    self.install_file(
        "manpages/crush.1.gz",
        "usr/share/man/man1",
        mode=0o644,
    )
    self.install_license("LICENSE.md")
