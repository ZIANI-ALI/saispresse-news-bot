"""Cover Instagram dyal Saispress (1080x1350): tswira + titre + logo, b l alwan dyal l brand.

Jouj d les formes:
  A: tswira l fo9 katdoub f navy, titre kbir ta7tha (l forme l 3adiya, katkhdem m3a ay tswira).
  D: tswira 3amra l post kamel, cadre gold, titre f boîte navy (ghir ila tswira twila w HD).
  match: natija d match: tswira l fo9, carte d score (l fer9an, l ahdaf, li sjlou), titre sghir.
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
RED = (204, 20, 38)  # akhbar 3ajila
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


def _pill(dr, right: int, top: int, text: str, fnt, padx: int = 22, pady: int = 10,
          fill=GOLD, color=NAVY) -> None:
    tw = _width(text, fnt)
    asc, desc = fnt.getmetrics()
    h = asc + desc + pady
    dr.rounded_rectangle((right - tw - 2 * padx, top, right, top + h), radius=h // 2, fill=fill)
    _text(dr, (right - padx, top + h / 2), text, fnt, color, "rm")


def _logo(height: int) -> Image.Image:
    lg = Image.open(ASSETS / "logo.png").convert("RGBA")
    return lg.resize((round(lg.width * height / lg.height), height), Image.LANCZOS)


def _stock_label(dr, xy) -> None:
    _text(dr, xy, "صورة تعبيرية", _font("Tajawal-Bold.ttf", 26), WHITE, "lm")


def _lines(dr, lines, fnt, right: int, top: int, lh: int) -> None:
    for i, ln in enumerate(lines):
        _text(dr, (right, top + i * lh), ln, fnt, WHITE, "ra")


def layout_a(img: Image.Image, title: str, category: str, crop: Crop, stock: bool,
             urgent: bool = False) -> Image.Image:
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
    accent = RED if urgent else GOLD
    if urgent:  # "عاجل" kbira 7amra blast catégorie
        _pill(dr, 1010, text_top - 96, "عاجل", _font("Tajawal-Black.ttf", 46), padx=30, pady=6,
              fill=RED, color=WHITE)
    elif category:
        _pill(dr, 1010, text_top - 78, category, _font("Tajawal-Bold.ttf", 34))
    dr.rectangle((1022, text_top + 14, 1032, text_top + block - 22), fill=accent)
    _lines(dr, lines, fnt, 1000, text_top, lh)
    dr.rectangle((0, H - (12 if urgent else 8), W, H), fill=accent)
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


def _fit_one(text: str, name: str, maxw: int, hi: int, lo: int) -> ImageFont.FreeTypeFont:
    """Akbar taille fiha l ktaba kadkhel f str wa7ed."""
    for size in range(hi, lo - 1, -2):
        fnt = _font(name, size)
        if _width(text, fnt) <= maxw:
            return fnt
    return fnt


def _cut(text: str, fnt, maxw: int) -> str:
    while text and _width(text, fnt) > maxw:
        text = text[:-2].rstrip(" ،,") + "…"
    return text


def layout_match(img: Image.Image, title: str, match: dict, crop: Crop, stock: bool,
                 urgent: bool = False) -> Image.Image:
    """Natija d match: l fari9 l awel (home) 3la limen, b7al l 9raya b l 3arbiya."""
    fnt, lines = _fit_title(title, "Tajawal-Black.ttf", 900, [(2, 64, 54), (3, 56, 46)])
    lh = int(fnt.size * 1.2)
    top = 1255 - lh * len(lines)  # titre l te7t, carte fo9o, tswira 3amra l ba9i
    cy1 = top - 45
    cy0 = cy1 - 230
    ph_h = cy0 + 140
    im = Image.new("RGBA", (W, H), (*NAVY, 255))
    im.paste(crop(img, (W, ph_h)), (0, 0))
    im.alpha_composite(_vgrad(W, 380, NAVY, 0, 255, 1.5), (0, ph_h - 380))
    im.alpha_composite(_vgrad(W, 200, (0, 0, 0), 90, 0), (0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((-200, cy0 - 40, 1300, H + 200), fill=(*NAVY2, 150))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))
    dr = ImageDraw.Draw(im)
    accent = RED if urgent else GOLD

    comp = clean_title(match.get("competition", ""))[:40]
    if urgent:
        _pill(dr, 1010, cy0 - 92, "عاجل", _font("Tajawal-Black.ttf", 42), padx=28, pady=6, fill=RED, color=WHITE)
    elif comp:
        _pill(dr, 1010, cy0 - 80, comp, _font("Tajawal-Bold.ttf", 32))

    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((60, cy0, 1020, cy1), radius=28, fill=(*NAVY, 235),
                                           outline=accent, width=3)
    im.alpha_composite(card)
    dr = ImageDraw.Draw(im)
    score_f = _font("Tajawal-Black.ttf", 120)
    for cx, sx, team, goals, scorers in (
            (830, 625, match["home"], match["home_score"], match.get("home_scorers", "")),
            (250, 455, match["away"], match["away_score"], match.get("away_scorers", ""))):
        team = clean_title(team)
        _text(dr, (cx, cy0 + 85), team, _fit_one(team, "Tajawal-ExtraBold.ttf", 290, 58, 32), WHITE, "mm")
        scorers = clean_title(scorers)
        if scorers:  # str wla jouj
            sf = _font("Tajawal-Bold.ttf", 25)
            rows = _wrap(scorers, sf, 300)
            rows = rows[:1] if len(rows) == 1 else [rows[0], _cut(" ".join(rows[1:]), sf, 300)]
            for i, row in enumerate(rows):
                _text(dr, (cx, cy0 + (168 if len(rows) == 1 else 155) + i * 32), row, sf, GOLD_L, "mm")
        dr.text((sx, cy0 + 100), str(goals), font=score_f, fill=GOLD_L, anchor="mm")
    dr.text((540, cy0 + 95), "-", font=_font("Tajawal-Black.ttf", 100), fill=GOLD_L, anchor="mm")

    dr.rectangle((1022, top + 12, 1032, top + lh * len(lines) - 18), fill=accent)
    _lines(dr, lines, fnt, 1000, top, lh)
    dr.rectangle((0, H - (12 if urgent else 8), W, H), fill=accent)
    _text(dr, (70, H - 44), SITE, _font("Tajawal-Bold.ttf", 28), GOLD_L, "lm")
    lg = _logo(70)
    im.alpha_composite(lg, (W - lg.width - 50, 48))
    if stock:
        _stock_label(dr, (50, 83))
    return im


def valid_match(m) -> dict | None:
    """Gemini kay3ti 'match' ghir ila kan l khabar natija d match sala; nt2akdo mn l 9yam."""
    if not isinstance(m, dict) or not str(m.get("home", "")).strip() or not str(m.get("away", "")).strip():
        return None
    try:
        hs, as_ = int(m["home_score"]), int(m["away_score"])
    except (KeyError, TypeError, ValueError):
        return None
    if not (0 <= hs <= 30 and 0 <= as_ <= 30):
        return None
    return {**m, "home_score": hs, "away_score": as_}


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
              native: tuple[int, int], upscaled: bool = False, stock: bool = False,
              urgent: bool = False, match: dict | None = None) -> tuple[bytes, str]:
    title = clean_title(title)
    match = valid_match(match)
    if match:  # natija d match: cover dyal score
        return _jpeg(layout_match(img, title, match, crop, stock, urgent)), "match"
    category = clean_title(category)[:20]
    _, lines = _fit_title(title, "Tajawal-ExtraBold.ttf", 860, STEPS_D)
    if urgent:  # 3ajil: dima A b l a7mar
        return _jpeg(layout_a(img, title, category, crop, stock, urgent=True)), "3ajil"
    kind = choose_layout(native, upscaled, len(lines))
    return _jpeg((layout_d if kind == "D" else layout_a)(img, title, category, crop, stock)), kind


def _jpeg(im: Image.Image) -> bytes:
    out = BytesIO()
    im.convert("RGB").save(out, "JPEG", quality=95, optimize=True, subsampling=0)
    return out.getvalue()
