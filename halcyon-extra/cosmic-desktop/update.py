# release tags are "epoch-X.Y.Z"; the generic git forge pattern only accepts
# bare vX.Y.Z or cosmic-desktop-X.Y.Z, so it never finds an update, and the
# commit-pinned component tarballs must not be treated as versions
url = "https://github.com/pop-os/cosmic-epoch"
pattern_style = "git_forge"
pattern = r"refs/tags/epoch-([\d.]+)"
