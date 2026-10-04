"""Cover Instagram dyal Saispress (1080x1350): tswira + titre + logo, b l alwan dyal l brand.

Jouj d les formes:
  A: tswira l fo9 katdoub f navy, titre kbir ta7tha (l forme l 3adiya, katkhdem m3a ay tswira).
  D: tswira 3amra l post kamel, cadre gold, titre f boîte navy (ghir ila tswira twila w HD).
"""
import re
from io import BytesIO
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFilter, ImageFont, features

ASSETS = Path(__file__).resolve().parent / "assets"
W, H = 1080, 1350
NAVY, NAVY2 = (11, 31, 77), (22, 53, 122)
GOLD, GOLD_L, WHITE = (201, 162, 39), (230, 198, 92), (255, 255, 255)
SITE = "saispress.com"
RAQM = features.check("raqm")

Crop = Callable[[Image.Image, tuple[int, int]], Image.Image]


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    engine = ImageFont.Layout.RAQM if RAQM else ImageFont.Layout.BASIC
    return ImageFont.truetype(str(ASSETS / "fonts" / name), size, layout_engine=engine)


def _shape(text: str) -> tuple[str, dict]:
    if not RAQM:  # bla libraqm/fribidi l 7rouf l 3arbiya kayjiw mfer9in
        raise RuntimeError("Pillow bla raqm (khass libfribidi0)")
    return text, {"direction": "rtl"}


def _width(text: str, fnt: ImageFont.FreeTypeFont) -> float:
    t, kw = _shape(text)
    return fnt.getlength(t, **kw)


def _text(dr: ImageDraw.ImageDraw, xy, text: str, fnt, fill, anchor: str) -> None:
    t, kw = _shape(text)
    dr.text(xy, t, font=fnt, fill=fill, anchor=anchor, **kw)


def clean_title(title: str) -> str:
    """N7ayydo emoji w rmouz ma kaybanouch f l font."""
    t = re.sub(r"[^\w\s؀-ۿ.,:;!?«»\"'()%\-–—،؛؟]", "", title)
    return re.sub(r"\s+", " ", t).strip(" -–—:")


def _wrap(text: str, fnt, maxw: int) -> list[str]:
    lines, cur = [], ""
    for w in text.split():
        t = f"{cur} {w}".strip()
        if not cur or _width(t, fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def _fit(text: str, name: str, maxw: int, max_lines: int, hi: int, lo: int):
    """Akbar taille fiha titre kaydkhel f max_lines stoura."""
    for size in range(hi, lo - 1, -2):
        fnt = _font(name, size)
        lines = _wrap(text, fnt, maxw)
        if len(lines) <= max_lines:
            return fnt, lines
    return fnt, lines


def _fit_title(text: str, name: str, maxw: int, steps):
    """steps = [(max_lines, hi, lo), ...]: 2 stoura ila kaydkhel b taille mzyana, sinon 3, sinon 4."""
    for max_lines, hi, lo in steps:
        fnt, lines = _fit(text, name, maxw, max_lines, hi, lo)
        if len(lines) <= max_lines:
            return fnt, lines
    return fnt, lines


# tailles mn 9bel kanet 112/104: titre kan kaykbar 7tta y3ammer 3 stoura
STEPS_A = [(2, 84, 70), (3, 76, 58), (4, 64, 50)]
STEPS_D = [(2, 80, 66), (3, 72, 56)]


def _vgrad(w: int, h: int, color, a0: int, a1: int, power: float = 1.0) -> Image.Image:
    mask = Image.new("L", (1, h))
    for y in range(h):
        mask.putpixel((0, y), int(a0 + (a1 - a0) * (y / max(1, h - 1)) ** power))
    layer = Image.new("RGBA", (w, h), (*color, 255))
    layer.putalpha(mask.resize((w, h)))
    return layer


def _pill(dr, right: int, top: int, text: str, fnt, padx: int = 22, pady: int = 10) -> None:
    tw = _width(text, fnt)
    asc, desc = fnt.getmetrics()
    h = asc + desc + pady
    dr.rounded_rectangle((right - tw - 2 * padx, top, right, top + h), radius=h // 2, fill=GOLD)
    _text(dr, (right - padx, top + h / 2), text, fnt, NAVY, "rm")


def _logo(height: int) -> Image.Image:
    lg = Image.open(ASSETS / "logo.png").convert("RGBA")
    return lg.resize((round(lg.width * height / lg.height), height), Image.LANCZOS)


def _stock_label(dr, xy) -> None:
    _text(dr, xy, "صورة تعبيرية", _font("Tajawal-Bold.ttf", 26), WHITE, "lm")


def _lines(dr, lines, fnt, right: int, top: int, lh: int) -> None:
    for i, ln in enumerate(lines):
        _text(dr, (right, top + i * lh), ln, fnt, WHITE, "ra")


def layout_a(img: Image.Image, title: str, category: str, crop: Crop, stock: bool) -> Image.Image:
    fnt, lines = _fit_title(title, "Tajawal-Black.ttf", 900, STEPS_A)
    lh = int(fnt.size * 1.18)
    block = lh * len(lines)
    text_top = 1255 - block
    # tswira katkbar/katsghar 3la 7sab toul d titre
    ph_h = min(940, text_top - 90 + 260)
    im = Image.new("RGBA", (W, H), (*NAVY, 255))
    im.paste(crop(img, (W, ph_h)), (0, 0))
    fade = min(420, ph_h // 2)
    im.alpha_composite(_vgrad(W, fade, NAVY, 0, 255, 1.6), (0, ph_h - fade))
    im.alpha_composite(_vgrad(W, 200, (0, 0, 0), 90, 0), (0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((-200, text_top - 60, 1300, H + 150), fill=(*NAVY2, 140))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))
    dr = ImageDraw.Draw(im)
    if category:
        _pill(dr, 1010, text_top - 78, category, _font("Tajawal-Bold.ttf", 34))
    dr.rectangle((1022, text_top + 14, 1032, text_top + block - 22), fill=GOLD)
    _lines(dr, lines, fnt, 1000, text_top, lh)
    dr.rectangle((0, H - 8, W, H), fill=GOLD)
    _text(dr, (70, H - 44), SITE, _font("Tajawal-Bold.ttf", 28), GOLD_L, "lm")
    lg = _logo(70)
    im.alpha_composite(lg, (W - lg.width - 50, 48))
    if stock:
        _stock_label(dr, (50, 83))
    return im


def layout_d(img: Image.Image, title: str, category: str, crop: Crop, stock: bool) -> Image.Image:
    im = crop(img, (W, H)).convert("RGBA")
    im.alpha_composite(_vgrad(W, 700, NAVY, 0, 235, 1.2), (0, H - 700))
    im.alpha_composite(_vgrad(W, 220, (0, 0, 0), 100, 0), (0, 0))
    fnt, lines = _fit_title(title, "Tajawal-ExtraBold.ttf", 860, STEPS_D)
    lh = int(fnt.size * 1.2)
    by1 = 1272
    by0 = by1 - lh * len(lines) - 105  # 105 = padding + str d site dakhel l boîte
    box = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(box).rectangle((60, by0, W - 60, by1), fill=(*NAVY, 235))
    im.alpha_composite(box)
    dr = ImageDraw.Draw(im)
    dr.rectangle((W - 72, by0, W - 60, by1), fill=GOLD)
    _lines(dr, lines, fnt, W - 110, by0 + 30, lh)
    if category:
        _pill(dr, W - 110, by0 - 62, category, _font("Tajawal-Bold.ttf", 32), padx=20, pady=8)
    dr.rectangle((28, 28, W - 28, H - 28), outline=GOLD, width=3)
    _text(dr, (95, by1 - 30), SITE, _font("Tajawal-Bold.ttf", 24), GOLD_L, "lm")
    lg = _logo(64)
    im.alpha_composite(lg, (W - lg.width - 65, 62))
    if stock:
        _stock_label(dr, (65, 94))
    return im


def choose_layout(native: tuple[int, int], upscaled: bool, n_lines: int) -> str:
    """D ghir ila tswira l asliya HD w machi 3rida bzaf (bach ma ytqt3ouch nas/tafasil f crop).

    - l asliya (qbel AI) khassha t3ammer 1080x1350 b zoom <= 1.15
    - w/h <= 1.35: tswira 3:2 wla 16:9 ila crop 4:5 kaydiy ktar mn 40% mnha -> A
    - titre 4 stoura -> A (fih blasa ktar)
    """
    w, h = native
    if upscaled or n_lines > 3:
        return "A"
    zoom = max(W / w, H / h)
    return "D" if w / h <= 1.35 and zoom <= 1.15 else "A"


def make_post(img: Image.Image, title: str, category: str, crop: Crop,
              native: tuple[int, int], upscaled: bool = False, stock: bool = False) -> tuple[bytes, str]:
    title = clean_title(title)
    category = clean_title(category)[:20]
    _, lines = _fit_title(title, "Tajawal-ExtraBold.ttf", 860, STEPS_D)
    kind = choose_layout(native, upscaled, len(lines))
    im = (layout_d if kind == "D" else layout_a)(img, title, category, crop, stock)
    out = BytesIO()
    im.convert("RGB").save(out, "JPEG", quality=95, optimize=True, subsampling=0)
    return out.getvalue(), kind
