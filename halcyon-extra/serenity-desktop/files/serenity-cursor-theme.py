#!/usr/bin/env python3
"""Build Xcursor themes from the SerenityOS PNG cursor themes.

The SerenityOS cursor assets are plain PNGs described by Config.ini. Wayland
compositors (including the SDE's wlroots-based WindowServer) only understand
Xcursor files, so translate both shipped themes into that format without
changing the artwork.
"""

import argparse
import configparser
import struct
import sys
from pathlib import Path

from PIL import Image

# Canonical SerenityOS Config.ini key -> Xcursor names. Every alias contains
# the same images so both the standard names (ew-resize) and the legacy names
# used by wlroots and older toolkits resolve to the SerenityOS artwork.
ALIASES = {
    "Arrow": [
        "default",
        "left_ptr",
        "arrow",
        "top_left_arrow",
        "context-menu",
        "alias",
        "left_side",
        "right_side",
    ],
    "Crosshair": [
        "crosshair",
        "cross",
        "cross_reverse",
        "tcross",
        "cell",
    ],
    "IBeam": [
        "text",
        "xterm",
        "vertical-text",
    ],
    "ResizeH": [
        "ew-resize",
        "e-resize",
        "w-resize",
        "sb_h_double_arrow",
        "size_hor",
        "h_double_arrow",
    ],
    "ResizeV": [
        "ns-resize",
        "n-resize",
        "s-resize",
        "sb_v_double_arrow",
        "size_ver",
        "v_double_arrow",
        "top_side",
        "bottom_side",
    ],
    "ResizeDTLBR": [
        "nwse-resize",
        "nw-resize",
        "se-resize",
        "fd_double_arrow",
        "size_fdiag",
        "top_left_corner",
        "bottom_right_corner",
    ],
    "ResizeDBLTR": [
        "nesw-resize",
        "ne-resize",
        "sw-resize",
        "bd_double_arrow",
        "size_bdiag",
        "top_right_corner",
        "bottom_left_corner",
    ],
    "ResizeColumn": [
        "col-resize",
        "split_h",
    ],
    "ResizeRow": [
        "row-resize",
        "split_v",
    ],
    "Hand": [
        "pointer",
        "hand1",
        "hand2",
        "pointing_hand",
    ],
    "Help": [
        "help",
        "question_arrow",
        "whats_this",
        "left_ptr_help",
    ],
    "Drag": [
        "dnd-move",
        "drag",
        "dnd-none",
        "grab",
    ],
    "DragCopy": [
        "dnd-copy",
        "copy",
    ],
    "Move": [
        "move",
        "fleur",
        "all-scroll",
        "size_all",
    ],
    "Wait": [
        "wait",
        "watch",
        "progress",
        "left_ptr_watch",
        "half-busy",
    ],
    "Disallowed": [
        "not-allowed",
        "no-drop",
        "forbidden",
        "crossed_circle",
        "circle",
    ],
    "Eyedropper": [
        "color-picker",
        "eyedropper",
        "picker",
    ],
    "Zoom": [
        "zoom-in",
        "zoom",
        "magnifier",
    ],
    "Hidden": [
        "hidden",
        "none",
        "transparent",
    ],
}

# (image scale, nominal Xcursor size). The SerenityOS assets are 21px and
# 42px; 24/48 are the conventional nominal sizes and match the SDE's default
# cursor size of 24.
SCALES = ((1, 24), (2, 48))

XCURSOR_MAGIC = 0x72756358
XCURSOR_IMAGE_TYPE = 0xFFFD0002


def parse_params(filename):
    """Match Gfx::CursorParams::parse_from_filename from SerenityOS."""
    title = Path(filename).stem
    dot = title.rfind(".")
    hotspot = None
    frames = 1
    frame_ms = 0
    if dot > 0:
        params = title[dot + 1 :]
        i = 0
        have_hotspot = False
        hx = hy = 0
        while i + 1 < len(params):
            prop = params[i]
            i += 1
            if prop == "-":
                break
            start = i
            while i < len(params) and params[i].isdigit():
                i += 1
            if start == i:
                break
            value = int(params[start:i])
            if prop == "x":
                hx = value
                have_hotspot = True
            elif prop == "y":
                hy = value
                have_hotspot = True
            elif prop == "f":
                if value > 1:
                    frames = value
            elif prop == "t":
                if 100 <= value <= 1000:
                    frame_ms = value
        if have_hotspot:
            hotspot = (hx, hy)
    return hotspot, frames, frame_ms


def scaled_name(filename, scale):
    if scale == 1:
        return filename
    return f"{Path(filename).stem}-2x.png"


def premultiplied_argb(image):
    """Return Xcursor's premultiplied ARGB32 pixel data."""
    rgba = image.convert("RGBA").tobytes()
    out = bytearray(len(rgba))
    for i in range(0, len(rgba), 4):
        r, g, b, a = rgba[i], rgba[i + 1], rgba[i + 2], rgba[i + 3]
        # Same rounding as libXcursor's xcursorgen.
        pr = (r * a + 0x80 + ((r * a + 0x80) >> 8)) >> 8
        pg = (g * a + 0x80 + ((g * a + 0x80) >> 8)) >> 8
        pb = (b * a + 0x80 + ((b * a + 0x80) >> 8)) >> 8
        out[i] = pb
        out[i + 1] = pg
        out[i + 2] = pr
        out[i + 3] = a
    return bytes(out)


def load_frames(source, filename, scale, nominal):
    path = source / scaled_name(filename, scale)
    if path.exists():
        image = Image.open(path).convert("RGBA")
    elif scale != 1 and (source / filename).exists():
        # A few Dark cursors only ship a 1x image. Scale it up with
        # nearest-neighbour to keep the pixel art crisp.
        image = Image.open(source / filename).convert("RGBA")
        image = image.resize((image.width * 2, image.height * 2), Image.NEAREST)
    else:
        return []

    hotspot, frames, frame_ms = parse_params(filename)
    if frames > 1 and image.width % frames != 0:
        frames = 1
    frame_width = image.width // frames
    if hotspot is None:
        hotspot = (frame_width // 2, image.height // 2)
    else:
        hotspot = (hotspot[0] * scale, hotspot[1] * scale)
    hotspot = (
        min(max(hotspot[0], 0), frame_width - 1),
        min(max(hotspot[1], 0), image.height - 1),
    )

    images = []
    for frame in range(frames):
        crop = image.crop(
            (frame * frame_width, 0, (frame + 1) * frame_width, image.height)
        )
        images.append(
            {
                "width": crop.width,
                "height": crop.height,
                "xhot": hotspot[0],
                "yhot": hotspot[1],
                "delay": frame_ms,
                "size": nominal,
                "pixels": premultiplied_argb(crop),
            }
        )
    return images


def write_xcursor(path, images):
    toc_size = 12 * len(images)
    offset = 16 + toc_size
    toc = bytearray()
    chunks = bytearray()
    for image in images:
        toc += struct.pack(
            "<III", XCURSOR_IMAGE_TYPE, image["size"], offset + len(chunks)
        )
        chunks += struct.pack(
            "<IIIIIIIII",
            36,
            XCURSOR_IMAGE_TYPE,
            image["size"],
            1,
            image["width"],
            image["height"],
            image["xhot"],
            image["yhot"],
            image["delay"],
        )
        chunks += image["pixels"]
    path.write_bytes(
        struct.pack("<IIII", XCURSOR_MAGIC, 16, 0x00010000, len(images))
        + toc
        + chunks
    )


def build_theme(source, dest, name):
    config = configparser.ConfigParser()
    config.read(source / "Config.ini")
    cursor_dir = dest / "cursors"
    cursor_dir.mkdir(parents=True, exist_ok=True)

    for key, filenames in ALIASES.items():
        if not config.has_option("Cursor", key):
            continue
        filename = config.get("Cursor", key)
        images = []
        for scale, nominal in SCALES:
            images += load_frames(source, filename, scale, nominal)
        if not images:
            continue
        for alias in filenames:
            write_xcursor(cursor_dir / alias, images)

    (dest / "index.theme").write_text(
        f"[Icon Theme]\nName={name}\nComment=SerenityOS cursor theme\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source", type=Path, help="directory containing Default/ and Dark/"
    )
    parser.add_argument(
        "destdir", type=Path, help="staging root (writes usr/share/icons/...)"
    )
    args = parser.parse_args()

    for source_name, target_name, name in (
        ("Default", "SerenityOS", "SerenityOS Default"),
        ("Dark", "SerenityOS-Dark", "SerenityOS Dark"),
    ):
        source = args.source / source_name
        if not source.is_dir():
            print(f"missing cursor theme: {source}", file=sys.stderr)
            return 1
        target = args.destdir / "usr/share/icons" / target_name
        build_theme(source, target, name)
        print(f"generated {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
