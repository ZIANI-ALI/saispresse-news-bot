"""Cover Instagram dyal Saispress (1080x1350): tswira + titre + logo, b l alwan dyal l brand.

Jouj d les formes:
  A: tswira l fo9 katdoub f navy, titre kbir ta7tha (l forme l 3adiya, katkhdem m3a ay tswira).
  D: tswira 3amra l post kamel, cadre gold, titre f boîte navy (ghir ila tswira twila w HD).
  match: natija d match: tswira l fo9, carte d score (l fer9an, l ahdaf, li sjlou), titre sghir.
         Ila l9ina chi3arat: cover d chi3arat f blast tsawer 7orra (make_badges_post).
  story: 1080x1920 (make_story): tswira l fo9, panel navy, titre f l wost, logo, blasa khawya l sticker d lien.
"""
import itertools
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
    """Natija d match b7al Marca: tswira 3amra, score kbir, chi3arat d l fer9an, li sjlou. Bla titre.
    L fari9 l awel (home) 3la limen, b7al l 9raya b l 3arbiya."""
    im = crop(img, (W, H)).convert("RGBA")
    im.alpha_composite(_vgrad(W, 820, NAVY, 0, 252, 0.9), (0, H - 820))
    im.alpha_composite(_vgrad(W, 220, (0, 0, 0), 110, 0), (0, 0))
    dr = ImageDraw.Draw(im)
    accent = RED if urgent else GOLD

    comp = clean_title(match.get("competition", ""))[:40]
    if urgent:
        _pill(dr, 540 + _width("عاجل", _font("Tajawal-Black.ttf", 40)) / 2 + 26, 790, "عاجل",
              _font("Tajawal-Black.ttf", 40), padx=26, pady=6, fill=RED, color=WHITE)
    elif comp:
        cf = _font("Tajawal-Bold.ttf", 32)
        _pill(dr, 540 + _width(comp, cf) / 2 + 22, 800, comp, cf)

    sy = 1000  # wast d l score
    score_f = _font("Tajawal-Black.ttf", 230)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))  # dell bach l ar9am ybano fo9 ay tswira
    sd = ImageDraw.Draw(shadow)
    for x, goals in ((655, match["home_score"]), (425, match["away_score"])):
        sd.text((x + 4, sy + 6), str(goals), font=score_f, fill=(0, 0, 0, 170), anchor="mm")
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    dr = ImageDraw.Draw(im)
    dr.text((655, sy), str(match["home_score"]), font=score_f, fill=WHITE, anchor="mm")
    dr.text((425, sy), str(match["away_score"]), font=score_f, fill=WHITE, anchor="mm")
    dr.rectangle((537, sy - 55, 543, sy + 55), fill=accent)
    for cx, team, badge in ((900, match["home"], match.get("home_badge")),
                            (180, match["away"], match.get("away_badge"))):
        team = clean_title(team)
        if badge is not None:
            b = badge.copy()
            b.thumbnail((190, 190), Image.LANCZOS)
            im.alpha_composite(b, (cx - b.width // 2, sy - 20 - b.height // 2))
            dr = ImageDraw.Draw(im)
            _text(dr, (cx, sy + 110), team, _fit_one(team, "Tajawal-Bold.ttf", 280, 34, 24), GOLD_L, "mm")
        else:  # bla chi3ar: smiya kbira
            _text(dr, (cx, sy), team, _fit_one(team, "Tajawal-ExtraBold.ttf", 270, 64, 30), WHITE, "mm")

    # li sjlou: home 3la limen, away 3la lissar
    sf = _font("Tajawal-Bold.ttf", 30)
    for x, scorers, anchor in ((1010, match.get("home_scorers", ""), "ra"),
                               (70, match.get("away_scorers", ""), "la")):
        names = [clean_title(n) for n in re.split(r"[،,؛;]", scorers or "") if clean_title(n)]
        rows = []  # kol hadaf kaml f str wa7ed (ma ntferq smiya 3la d9i9a)
        for n in names:
            if rows and _width(f"{rows[-1]} • {n}", sf) <= 440:
                rows[-1] = f"{rows[-1]} • {n}"
            else:
                rows.append(n)
        rows = rows[:3]
        for i, row in enumerate(rows):
            _text(dr, (x, sy + 165 + i * 40), row, sf, GOLD_L, anchor)

    dr.rectangle((0, H - (12 if urgent else 8), W, H), fill=accent)
    _text(dr, (70, H - 44), SITE, _font("Tajawal-Bold.ttf", 28), GOLD_L, "lm")
    lg = _logo(70)
    im.alpha_composite(lg, (W - lg.width - 50, 48))
    if stock:
        _stock_label(dr, (50, 83))
    return im


_MINUTE_RE = re.compile(r"\d{1,3}(?:\s*\+\s*\d{1,2})?")


def clean_scorers(text, goals: int) -> str:
    """Li sjlou kif katbhom Gemini, b la9youd: bla latin/JSON (ma ytsrrbch "home_en"...), bla jomal,
    bla tikrar, w 3adad l ahdaf ma ydouzch l score (score 0 = walou)."""
    if goals <= 0:
        return ""
    text = re.split(r'[A-Za-z"{}\[\]:\\]', str(text or ""), maxsplit=1)[0]  # ay 7aja mor latin/JSON = ghalat
    out, seen, n = [], set(), 0
    for part in re.split(r"[،,؛;\n]", text):
        part = re.sub(r"\s+", " ", part).strip(" .-–")
        mins = _MINUTE_RE.findall(part)
        name = re.sub(r"\(.*?\)|[\d'’+\s]+", " ", part).split()
        if not name and mins and out and n + len(mins) <= goals:  # "الكعبي 12'، 55'": d9i9a dyal li 9bel
            out[-1] += " " + part
            n += len(mins)
            continue
        if not name or len(name) > 4 or " ".join(name) in seen:  # jomla machi smiya, wla mkerrer
            continue
        k = max(1, len(mins))
        if n + k > goals:
            break
        seen.add(" ".join(name))
        out.append(part)
        n += k
    return "، ".join(out)


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
    return {**m, "home_score": hs, "away_score": as_,
            "home_scorers": clean_scorers(m.get("home_scorers"), hs),
            "away_scorers": clean_scorers(m.get("away_scorers"), as_)}


def _badge_color(badge: Image.Image) -> tuple[int, int, int]:
    """Lon l ghaleb f chi3ar (bla byed/k7al/rmadi), bach nlewno bih jiht l fari9."""
    small = badge.convert("RGBA").resize((48, 48))
    px, count = small.load(), {}
    for x in range(48):
        for y in range(48):
            r, g, b, a = px[x, y]
            if a < 200 or max(r, g, b) < 40 or max(r, g, b) - min(r, g, b) < 40:
                continue
            key = (r // 32, g // 32, b // 32)
            count[key] = count.get(key, 0) + max(r, g, b) - min(r, g, b)  # lon m9awed kayghleb l bahet
    if not count:
        return NAVY2
    return tuple(v * 32 + 16 for v in max(count, key=count.get))


def _mix(c1, c2, t: float) -> tuple[int, int, int]:
    return tuple(round(a * (1 - t) + b * t) for a, b in zip(c1, c2))


def badges_bg(match: dict) -> Image.Image:
    """Khalfiya bla tswira l natija d match: kol fari9 b lon chi3aro f jihto (home limen), w chi3aro kbir l fo9."""
    hb, ab = match.get("home_badge"), match.get("away_badge")
    hc = _mix(_badge_color(hb) if hb is not None else NAVY2, NAVY, 0.45)
    ac = _mix(_badge_color(ab) if ab is not None else NAVY2, NAVY, 0.45)
    im = Image.new("RGBA", (W, H), ac + (255,))
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(600, 0), (W, 0), (W, H), (480, H)], fill=255)
    im.paste(Image.new("RGBA", (W, H), hc + (255,)), (0, 0), mask)
    ImageDraw.Draw(im).line([(600, 0), (480, H)], fill=GOLD, width=6)
    for badge, cx in ((hb, 810), (ab, 270)):
        if badge is None:
            continue
        big = badge.copy()
        big.thumbnail((400, 400), Image.LANCZOS)
        if big.width < 400 and big.height < 400:  # chi3ar sghir: nkebbroh
            r = 400 / max(big.size)
            big = big.resize((round(big.width * r), round(big.height * r)), Image.LANCZOS)
        x, y = cx - big.width // 2, 420 - big.height // 2
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shadow.paste((0, 0, 0, 150), (x + 8, y + 14), big.split()[3])
        im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
        im.alpha_composite(big, (x, y))
    return im


def make_badges_post(title: str, match: dict, urgent: bool = False) -> bytes:
    """Cover d natija bla tswira: chi3arat kbar l fo9, w ta7t score b smiyat l fer9an (bla chi3arat sghar)."""
    match = valid_match(match)
    bg = badges_bg(match)
    plain = {**match, "home_badge": None, "away_badge": None}
    return _jpeg(layout_match(bg, clean_title(title), plain, lambda im, size: im, False, urgent))


# Cover bla tswira (khabar bla source, bla chakhsiya w bla tswira 7orra mnasba): titre kbir howa l cover.
STEPS_TEXT = [(3, 118, 96), (4, 104, 84), (5, 90, 72), (6, 76, 62)]


def _text_bg(w: int, h: int, urgent: bool) -> Image.Image:
    """Navy (7mer f 3ajil) b glow, khtout mayla chfafa w logo kbir chfaf (filigrane)."""
    base, glow_c = ((150, 12, 26), RED) if urgent else (NAVY, NAVY2)
    im = Image.new("RGBA", (w, h), (*base, 255))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((-w * 0.3, -h * 0.25, w * 1.0, h * 0.75), fill=(*glow_c, 230))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(min(w, h) // 5)))
    lines = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lines)
    for x in range(-h, w, 46):
        ld.line([(x, h), (x + h, 0)], fill=(255, 255, 255, 9), width=2)
    im.alpha_composite(lines)
    mark = _logo(round(h * 0.62))
    mark.putalpha(mark.getchannel("A").point(lambda v: v * 14 // 255))
    im.alpha_composite(mark, (-round(mark.width * 0.28), h - round(mark.height * 0.78)))
    return im


def _fit_balanced(text: str, name: str, maxw: int, steps):
    """_fit_title + bla ster lakher fih klma wa7da (kanssghro 7tta 75% bach yn9as ster) + stoura mtwazniin."""
    fnt, lines = _fit_title(text, name, maxw, steps)
    n = len(lines)
    if n > 1 and len(lines[-1].split()) == 1:
        for size in range(fnt.size - 2, round(fnt.size * 0.75) - 1, -2):
            if len(_wrap(text, _font(name, size), maxw)) < n:
                fnt, n = _font(name, size), n - 1
                break
    words = text.split()
    best, best_key = None, None
    for cuts in itertools.combinations(range(1, len(words)), n - 1) if 1 < n < len(words) else ():
        b = (0, *cuts, len(words))
        ws = [_width(" ".join(words[b[i]:b[i + 1]]), fnt) for i in range(n)]
        if max(ws) > maxw:
            continue
        key = (sum(b[i + 1] - b[i] == 1 for i in range(n)), max(ws) - min(ws))
        if best_key is None or key < best_key:
            best, best_key = b, key
    return fnt, ([" ".join(words[best[i]:best[i + 1]]) for i in range(n)] if best else _wrap(text, fnt, maxw))


def _text_block(im: Image.Image, title: str, category: str, urgent: bool, right: int, maxw: int,
                top: int, bottom: int, steps, pill_size: int = 40) -> None:
    """Pill (rkn / عاجل) + titre kbir mcentri bin top w bottom, b khatt dahbi (7mer: byed) l imin."""
    dr = ImageDraw.Draw(im)
    accent = WHITE if urgent else GOLD
    pill_text = "عاجل" if urgent else category
    pill_fnt = _font("Tajawal-Black.ttf" if urgent else "Tajawal-Bold.ttf", pill_size)
    pill_h = (sum(pill_fnt.getmetrics()) + 10) if pill_text else 0
    fnt, lines = _fit_balanced(title, "Tajawal-Black.ttf", maxw, steps)
    lh = int(fnt.size * 1.24)
    block = (pill_h + 44 if pill_text else 0) + lh * len(lines)
    y = top + max(0, (bottom - top - block) // 2)
    if pill_text:
        _pill(dr, right, y, pill_text, pill_fnt, padx=28, pady=10, fill=accent, color=RED if urgent else NAVY)
        y += pill_h + 44
    dr.rectangle((right + 22, y + 18, right + 32, y + lh * len(lines) - 26), fill=accent)
    _lines(dr, lines, fnt, right, y, lh)


def make_text_post(title: str, category: str, urgent: bool = False) -> bytes:
    """Cover 1080x1350 bla tswira: titre kbir f l wost (b7al "quote card"), logo w saispress.com lta7t."""
    title, category = clean_title(title), clean_title(category)[:20]
    im = _text_bg(W, H, urgent)
    _text_block(im, title, category, urgent, 990, 880, 90, H - 200, STEPS_TEXT)
    dr = ImageDraw.Draw(im)
    dr.rectangle((0, H - (12 if urgent else 8), W, H), fill=WHITE if urgent else GOLD)
    lg = _logo(84)
    im.alpha_composite(lg, (W - lg.width - 70, H - 72 - lg.height))
    _text(dr, (70, H - 72 - lg.height // 2), SITE, _font("Tajawal-Bold.ttf", 30), WHITE if urgent else GOLD_L, "lm")
    return _jpeg(im)


def make_text_site(title: str, category: str, urgent: bool = False) -> bytes:
    """Tswira d site 1600x900 bla tswira (nefs design)."""
    title, category = clean_title(title), clean_title(category)[:20]
    w, h = 1600, 900
    im = _text_bg(w, h, urgent)
    _text_block(im, title, category, urgent, w - 130, w - 420, 60, h - 60,
                [(3, 104, 84), (4, 88, 70), (5, 74, 60)], 36)
    lg = _logo(96)
    im.alpha_composite(lg, (70, h - 70 - lg.height))
    return _jpeg(im)


def make_text_story(title: str, category: str, urgent: bool = False) -> bytes:
    """Story 1080x1920 bla tswira: titre kbir, logo, w blasa khawya l sticker d lien (b7al make_story)."""
    title, category = clean_title(title), clean_title(category)[:20]
    im = _text_bg(SW, SH, urgent)
    _text_block(im, title, category, urgent, 990, 880, 300, 1300, STEPS_TEXT, 44)
    dr = ImageDraw.Draw(im)
    accent = WHITE if urgent else GOLD
    lg = _logo(110)
    im.alpha_composite(lg, ((SW - lg.width) // 2, 1330))
    x0 = (SW - SLOT_W) // 2
    dr.rounded_rectangle((x0, SLOT_Y, x0 + SLOT_W, SLOT_Y + SLOT_H), radius=SLOT_R,
                         fill=(150, 12, 26) if urgent else NAVY2, outline=accent, width=4)
    _chevrons(dr, SW // 2, SLOT_Y - 58, 26, accent)
    return _jpeg(im)


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


SW, SH = 1080, 1920  # story 9:16
STORY_PH = 960       # tswira l fo9 (nos d story)
STEPS_STORY = [(3, 80, 64), (4, 68, 54), (5, 58, 48)]
STEPS_STORY_SMALL = [(4, 56, 46), (5, 50, 42)]  # titre twil: bach yb9a blasa l sticker
# Blasa khawya l sticker d lien (Instagram ma kaykhallich tkhbbih: kayrdo dima dakhel l cadre).
# Cadre f l wost lta7t b nefs proportion d sticker d Instagram (≈ 228x77 = 2.96:1, coins ≈ 23%):
# l user kaykbber sticker 7tta y3mmer l cadre. Fo9 l interface d Instagram (~250px lta7t).
SLOT_W, SLOT_H, SLOT_R = 380, 128, 30
SLOT_Y = 1550      # top d cadre (ila l contenu kaykhalli lih blasa)
SLOT_Y_MAX = 1580  # ma tnzelch ktar mn hna


def _chevrons(dr, cx: int, cy: int, size: int, fill) -> None:
    """Jouj flèches lta7t (kayweriw l cadre d sticker: l click, machi swipe up) bla ma n7tajo glyph f l font."""
    for k in (0, 1):
        y = cy + k * size * 0.62
        dr.line([(cx - size / 2, y), (cx, y + size / 2), (cx + size / 2, y)], fill=fill, width=6, joint="curve")


def make_story(img: Image.Image, title: str, category: str, crop: Crop, stock: bool = False,
               urgent: bool = False) -> bytes:
    """Story 1080x1920: tswira l fo9, panel navy ta7tha: catégorie, titre f l wost, logo, blasa khawya l sticker d lien.
    L contenu kollo bin safe zones d Instagram (fo9 ~250px w ta7t ~250px m3amrin b l interface)."""
    title = clean_title(title)
    category = clean_title(category)[:20]
    accent = RED if urgent else GOLD
    im = Image.new("RGBA", (SW, SH), (*NAVY, 255))
    im.paste(crop(img, (SW, STORY_PH)), (0, 0))
    im.alpha_composite(_vgrad(SW, 260, (0, 0, 0), 120, 0), (0, 0))  # profil d Instagram fo9 tswira
    im.alpha_composite(_vgrad(SW, 140, NAVY, 0, 200, 1.4), (0, STORY_PH - 140))
    glow = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((-260, STORY_PH + 80, SW + 260, SH + 260), fill=(*NAVY2, 170))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(140)))
    mark = _logo(820)  # logo kbir chfaf f l jnab (filigrane)
    mark.putalpha(mark.getchannel("A").point(lambda v: v * 11 // 255))
    im.alpha_composite(mark, (-250, SH - 640))
    dr = ImageDraw.Draw(im)
    dr.rectangle((0, STORY_PH, SW, STORY_PH + 8), fill=accent)
    if stock:
        _text(dr, (50, STORY_PH - 40), "صورة تعبيرية", _font("Tajawal-Bold.ttf", 28), WHITE, "lm")

    pill_fnt = _font("Tajawal-Black.ttf", 44) if urgent else _font("Tajawal-Bold.ttf", 36)
    pill_text = "عاجل" if urgent else category
    pill_h = (sum(pill_fnt.getmetrics()) + 10) if pill_text else 0
    lg = _logo(110)
    room = SLOT_Y - 90 - (STORY_PH + 8)  # contenu bin tswira w flèches d sticker
    for steps in (STEPS_STORY, STEPS_STORY_SMALL):
        fnt, lines = _fit_title(title, "Tajawal-Black.ttf", 920, steps)
        lh = int(fnt.size * 1.22)
        block = (pill_h + 36 if pill_text else 0) + lh * len(lines) + 48 + lg.height
        if block + 2 * 36 <= room:
            break
    top = STORY_PH + 8 + max(36, (room - block) // 2)
    if pill_text:
        tw = _width(pill_text, pill_fnt)
        padx = 30 if urgent else 24
        _pill(dr, round(SW / 2 + tw / 2 + padx), top, pill_text, pill_fnt, padx=padx, pady=10,
              fill=accent, color=WHITE if urgent else NAVY)
        top += pill_h + 36
    for i, ln in enumerate(lines):
        _text(dr, (SW // 2, top + i * lh), ln, fnt, WHITE, "ma")
    top += lh * len(lines) + 48
    im.alpha_composite(lg, ((SW - lg.width) // 2, top))
    # blasa d sticker d lien: flèches lta7t + cadre khawi (l user kay7ett fih sticker «التفاصيل» f Instagram)
    y0 = min(SLOT_Y_MAX, max(SLOT_Y, top + lg.height + 90))
    x0 = (SW - SLOT_W) // 2
    dr.rounded_rectangle((x0, y0, x0 + SLOT_W, y0 + SLOT_H), radius=SLOT_R, fill=NAVY2, outline=accent, width=4)
    if y0 - 58 >= top + lg.height + 16:  # titre twil: bla flèches bach ma ylsa9ouch f logo
        _chevrons(dr, SW // 2, y0 - 58, 26, accent)
    return _jpeg(im)


def _jpeg(im: Image.Image) -> bytes:
    out = BytesIO()
    im.convert("RGB").save(out, "JPEG", quality=95, optimize=True, subsampling=0)
    return out.getvalue()
