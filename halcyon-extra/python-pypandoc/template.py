pkgname = "python-pypandoc"
pkgver = "1.17"
pkgrel = 0
build_style = "python_pep517"
hostmakedepends = [
    "python-build",
    "python-hatchling",
    "python-installer",
]
depends = ["pandoc", "python"]
pkgdesc = "Thin wrapper for pandoc"
license = "MIT"
url = "https://github.com/JessicaTegner/pypandoc"
source = f"$(PYPI_SITE)/p/pypandoc/pypandoc-{pkgver}.tar.gz"
sha256 = "51179abfd6e582a25ed03477541b48836b5bba5a4c3b282a547630793934d799"
# tests require network access and optional converters
options = ["!check"]


def post_install(self):
    self.install_license("LICENSE")
