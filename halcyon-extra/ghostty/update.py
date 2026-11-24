# the release tarballs live under release.files.ghostty.org, which has no
# directory index, and the repository also carries the separately versioned
# libghostty-vt "vt-*" tags, so only the application's vX.Y.Z tags count
url = "https://github.com/ghostty-org/ghostty"
pattern_style = "git_forge"
pattern = r"refs/tags/v([\d.]+)"
