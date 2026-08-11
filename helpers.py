"""Shared helpers: paths, fonts, and symbol image loading."""

import os
import customtkinter as ctk
from PIL import Image, ImageDraw

from game_rules import SYMBOLS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIC_DIR = os.path.join(BASE_DIR, "images")


def F(size, weight="normal"):
    """Quick font builder."""
    return ctk.CTkFont(family="Segoe UI", size=size, weight=weight)


def placeholder_image(sym, size):
    """Fallback picture when a symbol image file is missing."""
    im = Image.new("RGB", size, "#2f7fe0")
    draw = ImageDraw.Draw(im)
    draw.rectangle((1, 1, size[0] - 2, size[1] - 2), outline="#ffffff", width=8)
    draw.text((size[0] // 2, size[1] // 2), sym[0].upper(),
              fill="#ffffff", anchor="mm")
    return im


def load_symbol_images(prefix, size):
    """Return {rock, paper, scissors} -> CTkImage for an image prefix."""
    out = {}
    for sym in SYMBOLS:
        path = os.path.join(PIC_DIR, f"{prefix}-{sym}.png")
        if os.path.exists(path):
            im = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
        else:
            im = placeholder_image(sym, size)
        out[sym] = ctk.CTkImage(light_image=im, dark_image=im, size=size)
    return out
