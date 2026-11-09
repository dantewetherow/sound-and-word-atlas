"""Sight word cards for all 220 of E. W. Dolch's words, in five sets: Pre-primer, Primer, First, Second and Third grade,
and since 8 November 2026 a sixth set for his 95 nouns, which he kept off his sight vocabulary. Santa Claus and good-bye are
drawn as two marked words, as the actor cards draw them.

The sheets work the way the ELP cards do (build_elp_cards.py): one PDF per set for double-sided printing, flipping on
the long edge, with plain words on each odd page and the same words coded on the even page after it, each behind its
plain card. Every set is 10 cards to a page. Each card's tag names its Dolch level and, when the word is on one, the
ELP list that teaches it, so a teacher can see which cards a class has already met there.

Codes come from the deck tools and legomorphic_words.py, then site_codes.py, then dolch_codes.py for the 43 words that
had none, then noun_codes.py for the nouns. The words come from data/dolch.json.

Run:  python3 build/build_dolch_cards.py <node_modules with @fontsource-variable/lexend> docs/cards <work folder>
"""
import asyncio, base64, html, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import legomorphic_words as LW
from known_codes import all_codes
from site_codes import SITE_CODES
from dolch_codes import DOLCH_CODES
from noun_codes import NOUN_CODES
from playwright.async_api import async_playwright

FONTS, OUT, WORK = (pathlib.Path(a) for a in sys.argv[1:4])
codes, _ = all_codes()
for w, c in {**SITE_CODES, **DOLCH_CODES}.items(): codes.setdefault(w, c)
codes["live"] = DOLCH_CODES["live"]            # Dolch lists live with the verbs: the live of "we live here"
for w, c in NOUN_CODES.items(): codes.setdefault(w, c)
LW.W.clear(); LW.W.update(codes)
esc = html.escape
DOLCH = json.loads((HERE / "data" / "dolch.json").read_text(encoding="utf-8"))
ELP = json.loads((HERE / "data" / "elp_hfw.json").read_text(encoding="utf-8"))
ELP_LIST = {w: n for n, v in ELP["lists"].items() for w in v["words"]}

# (file name, set title, level key in dolch.json, columns, rows, card width and height in inches)
SETS = [(f"dolch-word-cards-{lv['key']}", lv["name"], lv["key"], 2, 5, 3.9, 2.0) for lv in DOLCH["levels"]] \
     + [("dolch-word-cards-nouns", "Nouns", "nouns", 2, 5, 3.9, 2.0)]
PAIRS = {"Santa Claus": ("Santa", "Claus")}        # two marked words, as on the actor cards
HYPHENED = {"good-bye": ("good", "bye")}
PAGE_W, PAGE_H = 8.5, 11.0
PAD_X, PAD_TOP, PAD_BOTTOM = 0.20, 0.15, 0.25
PLAIN_CAP = 1.10
PLAIN_HEIGHT = 1.30
TAG = "#8d8577"
# One footer line, a quarter inch clear of the bottom edge, where most printers can still print.
FOOT = ("Print in colour, double-sided, flipping on the long edge; cut on the grey lines. "
        "Words from E. W. Dolch (1936). Tags name the word&rsquo;s ELP list, if it has one.")

def cards_for(key):
    if key == "nouns":
        return [(w, "Dolch noun · " + (f"ELP list {ELP_LIST[w]}" if w in ELP_LIST else "not on the ELP lists")) for w in DOLCH["nouns"]]
    lv = next(l for l in DOLCH["levels"] if l["key"] == key)
    name = lv["name"][0].lower() + lv["name"][1:]
    return [(w, f"Dolch {name} · " + (f"ELP list {ELP_LIST[w]}" if w in ELP_LIST else "not on the ELP lists")) for w in lv["words"]]

def face(path):
    data = base64.b64encode((FONTS / path).read_bytes()).decode()
    return ('@font-face{font-family:"Lexend";font-style:normal;font-weight:100 900;'
            f'src:url(data:font/woff2;base64,{data}) format("woff2");}}')

CSS = face("@fontsource-variable/lexend/files/lexend-latin-wght-normal.woff2") + """
:root{--ink:#2b2b2b;--soft:#6b6256;--line:#d8d0c0;--verb:#b5402f;--subject:#3a7d44;--modal:#3f6488;}
*{box-sizing:border-box;}
@page{size:8.5in 11in;margin:0;}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:"Lexend",system-ui,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
.page{position:relative;width:8.5in;height:11in;overflow:hidden;break-after:page;}
.page:last-child{break-after:auto;}
.card{position:absolute;}
.word{position:absolute;display:flex;align-items:center;justify-content:center;}
.plain{font-weight:400;line-height:1;white-space:nowrap;color:var(--ink);}
.tag{position:absolute;left:.12in;bottom:.07in;font-size:6.4pt;letter-spacing:.03em;color:""" + TAG + """;white-space:nowrap;}
.cut{position:absolute;background:#b3aa9b;}
.head{position:absolute;font-size:7pt;color:""" + TAG + """;letter-spacing:.02em;}
.foot{position:absolute;font-size:6.6pt;color:""" + TAG + """;letter-spacing:.02em;white-space:nowrap;}
.head{display:flex;justify-content:space-between;}
.foot p{margin:0 0 .03in;}
"""

def drawn(word):
    """(markup, width, height) at a letter size of 100: one word, two words side by side, or two joined by a hyphen."""
    parts = PAIRS.get(word) or HYPHENED.get(word)
    if not parts: return LW.svg_word(word, 100.0, 0.0, cls=False)
    g1, w1, H = LW.svg_word(parts[0], 100.0, 0.0, cls=False)
    g2, w2, _ = LW.svg_word(parts[1], 100.0, w1, cls=False)
    hy = ""
    if word in HYPHENED:                         # a hyphen in the gap the two words' margins leave, at the middle of an x
        y = 1.44 * 100 - 28
        hy = f'<line x1="{w1 - 12:.1f}" y1="{y:.1f}" x2="{w1 + 12:.1f}" y2="{y:.1f}" stroke="var(--ink)" stroke-width="7" stroke-linecap="round"/>'
    return g1 + hy + g2, w1 + w2, H

def coded(word, F):
    g, w, H = drawn(word)
    return (f'<svg viewBox="0 0 {w:.1f} {H:.1f}" style="width:{w / 100 * F:.3f}in;height:{H / 100 * F:.3f}in" '
            f'role="img" aria-label="{esc(word)}, coded">{g}</svg>')

def sheet_pages(title, cards, cols, rows, cw, ch, F_plain, F_coded, sheet, n_sheets):
    x0, y0 = (PAGE_W - cols * cw) / 2, (PAGE_H - rows * ch) / 2
    gw, gh = cols * cw, rows * ch
    area = f"left:{PAD_X}in;right:{PAD_X}in;top:{PAD_TOP}in;bottom:{PAD_BOTTOM}in"
    def head(side):
        return (f'<div class="head" style="left:{x0}in;width:{gw}in;top:{y0 - .32:.2f}in">'
                f'<span>{"Dolch nouns" if title == "Nouns" else "Dolch sight words · " + esc(title)}</span><span>Sheet {sheet} of {n_sheets} · {side}</span></div>')
    front, back = [], []
    for i, card in enumerate(cards):
        r, c = divmod(i, cols)
        y = y0 + r * ch
        xf, xb = x0 + c * cw, x0 + (cols - 1 - c) * cw          # the back mirrors the columns for a long-edge flip
        if card is None:
            continue
        word, label = card
        box = f'width:{cw}in;height:{ch}in'
        front.append(f'<div class="card" data-word="{esc(word)}" data-slot="{r},{c}" style="left:{xf:.3f}in;top:{y:.3f}in;{box}">'
                     f'<div class="word" style="{area}"><span class="plain" style="font-size:{F_plain[word]:.3f}in">{esc(word)}</span></div>'
                     f'<div class="tag">{esc(label)}</div></div>')
        back.append(f'<div class="card" data-word="{esc(word)}" data-slot="{r},{cols - 1 - c}" style="left:{xb:.3f}in;top:{y:.3f}in;{box}">'
                    f'<div class="word" style="{area}">{coded(word, F_coded[word])}</div>'
                    f'<div class="tag">{esc(label)}</div></div>')
    over = .15
    cuts = "".join(f'<div class="cut" style="left:{x0 + c * cw - .0035:.4f}in;top:{y0 - over}in;width:.007in;height:{gh + 2 * over}in"></div>' for c in range(cols + 1))
    cuts += "".join(f'<div class="cut" style="top:{y0 + r * ch - .0035:.4f}in;left:{x0 - over}in;height:.007in;width:{gw + 2 * over}in"></div>' for r in range(rows + 1))
    foot = (f'<div class="foot" style="left:{x0}in;width:{gw}in;top:{y0 + gh + .12:.2f}in"><p>{FOOT}</p></div>')
    return (f'<section class="page front">{head("plain side")}{cuts}{"".join(front)}{foot}</section>'
            f'<section class="page back">{head("coded side")}{"".join(back)}</section>')

MEASURE_JS = """(words) => { const s = document.createElement('span'); s.className = 'plain'; s.style.fontSize = '100px'; document.body.appendChild(s);
  const out = {}; for (const w of words) { s.textContent = w; out[w] = s.getBoundingClientRect().width / 100; } s.remove(); return out; }"""

# The same check as the ELP cards: every word inside its card's word area, every back card behind its front.
CHECK_JS = """() => { const bad = [], pages = [...document.querySelectorAll('.page')];
  pages.forEach((pg, i) => { if (pg.scrollHeight > pg.clientHeight + 1 || pg.scrollWidth > pg.clientWidth + 1) bad.push('page ' + (i + 1) + ' overflows');
    pg.querySelectorAll('.card').forEach(card => { const a = card.querySelector('.word').getBoundingClientRect(), el = card.querySelector('.word > *').getBoundingClientRect();
      if (el.left < a.left - .5 || el.right > a.right + .5 || el.top < a.top - .5 || el.bottom > a.bottom + .5) bad.push('p' + (i + 1) + ' ' + card.dataset.word + ' leaves its space');
      const t = card.querySelector('.tag').getBoundingClientRect(), c = card.getBoundingClientRect();
      if (t.right > c.right - 4) bad.push('p' + (i + 1) + ' label too long on ' + card.dataset.word); });
    const f = pg.querySelector('.foot'); if (f && (f.getBoundingClientRect().bottom > pg.getBoundingClientRect().bottom - 19 || f.scrollWidth > f.clientWidth + 1)) bad.push('page ' + (i + 1) + ' footer too near the edge or too long'); });
  for (let i = 0; i + 1 < pages.length; i += 2) { const f = [...pages[i].querySelectorAll('.card')], b = [...pages[i + 1].querySelectorAll('.card')];
    if (f.length !== b.length) bad.push('sheet ' + (i / 2 + 1) + ' front and back differ');
    f.forEach((card, k) => { const fr = card.getBoundingClientRect(), br = b[k].getBoundingClientRect(), W = pages[i].getBoundingClientRect().width;
      const mirrored = Math.abs((W - fr.right) - (br.left - pages[i + 1].getBoundingClientRect().left)) < .5 && Math.abs(fr.top - pages[i].getBoundingClientRect().top - (br.top - pages[i + 1].getBoundingClientRect().top)) < .5;
      if (b[k].dataset.word !== card.dataset.word || !mirrored) bad.push('sheet ' + (i / 2 + 1) + ' ' + card.dataset.word + ' is not behind its front'); }); }
  return {bad, fonts: document.fonts.check('40px Lexend'), pages: pages.length}; }"""

async def main():
    OUT.mkdir(parents=True, exist_ok=True); WORK.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch()
        page = await br.new_page()
        await page.set_content(f"<!doctype html><html><head><style>{CSS}</style></head><body></body></html>")
        await page.evaluate("document.fonts.load('100px Lexend')"); await page.evaluate("document.fonts.ready")
        for name, title, key, cols, rows, cw, ch in SETS:
            cards = cards_for(key)
            aw, ah = cw - 2 * PAD_X, ch - PAD_TOP - PAD_BOTTOM
            plain_w = await page.evaluate(MEASURE_JS, [w for w, _ in cards])
            single = [w for w, _ in cards if w not in PAIRS and w not in HYPHENED]   # a two-word card shrinks alone
            F_plain = min(PLAIN_CAP, ah / PLAIN_HEIGHT, aw / max(plain_w[w] for w in single))
            F_coded = min(ah / LW.HEIGHT, aw / max(drawn(w)[1] / 100 for w in single))
            fp = {w: min(F_plain, aw / plain_w[w]) for w, _ in cards}
            fc = {w: min(F_coded, aw / (drawn(w)[1] / 100)) for w, _ in cards}
            per = cols * rows
            slots = cards + [None] * ((-len(cards)) % per)
            n_sheets = len(slots) // per
            body = "".join(sheet_pages(title, slots[s * per:(s + 1) * per], cols, rows, cw, ch, fp, fc, s + 1, n_sheets) for s in range(n_sheets))
            f = WORK / f"{name}.html"
            f.write_text(f'<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><title>{esc(name)}</title><style>{CSS}</style></head><body>{body}</body></html>', encoding="utf-8")
            await page.goto(f.as_uri()); await page.evaluate("document.fonts.ready")
            await page.emulate_media(media="print")
            r = await page.evaluate(CHECK_JS)
            assert r["fonts"] and not r["bad"], (name, r)
            await page.pdf(path=str(OUT / f"{name}.pdf"), width="8.5in", height="11in", print_background=True,
                           margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            print(f"wrote {name}.pdf | {len(cards)} cards on {n_sheets} sheets ({r['pages']} pages) | "
                  f"plain {F_plain * 72:.0f} pt, coded {F_coded * 72:.0f} pt | widest plain {max(plain_w, key=plain_w.get)}")
        await br.close()

if __name__ == "__main__":
    asyncio.run(main())
