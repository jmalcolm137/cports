# upstream tags releases as bun-vX.Y.Z; the generic git forge pattern accepts
# only bare vX.Y.Z or bun-X.Y.Z, so it finds no tags at all
url = "https://github.com/oven-sh/bun"
pattern_style = "git_forge"
pattern = r"refs/tags/bun-v([\d.]+)"
