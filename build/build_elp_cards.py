"""High-frequency word cards from the SD23 Early Literacy Profile (ELP) lists, in three sets: Kindergarten, Grade 1, Grade 2.

Each set is one PDF for double-sided printing, flipping on the long edge. Each odd page holds plain words, and the even
page after it holds the same words coded, each one behind its plain card (the columns are mirrored on the back).
Kindergarten is 8 cards to a page, since its 12 words take two sheets either way and its letters can be bigger;
grades 1 and 2 are 10 to a page. Every coded word is drawn by legomorphic_words.py, so the cards and the decks
cannot drift apart. The name of the notation is left off the cards, as it is on the handouts.

Run:  python3 build/build_elp_cards.py <node_modules with @fontsource-variable/lexend> docs/cards <work folder>
      (npm install @fontsource-variable/lexend gives the node_modules folder; the font is under the SIL Open Font License.)
"""
import asyncio, base64, html, json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import legomorphic_words as LW
from known_codes import all_codes
from playwright.async_api import async_playwright

FONTS, OUT, WORK = (pathlib.Path(a) for a in sys.argv[1:4])
codes, _ = all_codes(); LW.W.clear(); LW.W.update(codes)
esc = html.escape
ELP = json.loads((HERE / "data" / "elp_hfw.json").read_text(encoding="utf-8"))

# (file name, set title, grade key in elp_hfw.json, columns, rows, card width and height in inches)
SETS = [("elp-word-cards-kindergarten", "Kindergarten", "K", 2, 4, 3.9, 2.5),
        ("elp-word-cards-grade-1", "Grade 1", "1", 2, 5, 3.9, 2.0),
        ("elp-word-cards-grade-2", "Grade 2", "2", 2, 5, 3.9, 2.0)]
PAGE_W, PAGE_H = 8.5, 11.0
PAD_X, PAD_TOP, PAD_BOTTOM = 0.20, 0.15, 0.25   # the word stays this far inside its card, so a back printed a little off still holds it
PLAIN_CAP = 1.10                                # the largest letter size on the plain side, in inches
PLAIN_HEIGHT = 1.30                             # a plain word's height, ascenders to descenders, as a share of its letter size
TAG = "#8d8577"
SOURCE = ("Words from the Early Literacy Profile (ELP) Assessment &amp; Instructional Guide, Central Okanagan Public Schools (2025), pp.&nbsp;16&ndash;17.")
HOW = "Print in colour and double-sided, flipping on the long edge, so each coded word lands behind its plain one. Cut on the grey lines."

def cards_for(grade):
    out = []
    for k, v in sorted(ELP["lists"].items(), key=lambda kv: int(kv[0])):
        if v["grade"] != grade: continue
        name = v["label"].replace("'e'", "‘e’")       # the guide prints Silent ‘e’ with curly quotes
        label = "Kindergarten · List 1" if grade == "K" else f"Grade {grade} · List {k} · {name}"
        out += [(w, label) for w in v["words"]]
    return out

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
.head,.foot{position:absolute;font-size:7pt;color:""" + TAG + """;letter-spacing:.02em;}
.head{display:flex;justify-content:space-between;}
.foot p{margin:0 0 .03in;}
"""

def coded(word, F):
    g, w, H = LW.svg_word(word, 100.0, 0.0, cls=False)
    return (f'<svg viewBox="0 0 {w:.1f} {H:.1f}" style="width:{w / 100 * F:.3f}in;height:{H / 100 * F:.3f}in" '
            f'role="img" aria-label="{esc(word)}, coded">{g}</svg>')

def layout(cols, rows, cw, ch):
    x0, y0 = (PAGE_W - cols * cw) / 2, (PAGE_H - rows * ch) / 2
    return x0, y0

def sheet_pages(title, cards, cols, rows, cw, ch, F_plain, F_coded, sheet, n_sheets):
    x0, y0 = layout(cols, rows, cw, ch)
    gw, gh = cols * cw, rows * ch
    area = f"left:{PAD_X}in;right:{PAD_X}in;top:{PAD_TOP}in;bottom:{PAD_BOTTOM}in"
    def head(side):
        return (f'<div class="head" style="left:{x0}in;width:{gw}in;top:{y0 - .32:.2f}in">'
                f'<span>ELP high-frequency words · {esc(title)}</span><span>Sheet {sheet} of {n_sheets} · {side}</span></div>')
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
                     f'<div class="word" style="{area}"><span class="plain" style="font-size:{F_plain:.3f}in">{esc(word)}</span></div>'
                     f'<div class="tag">{esc(label)}</div></div>')
        back.append(f'<div class="card" data-word="{esc(word)}" data-slot="{r},{cols - 1 - c}" style="left:{xb:.3f}in;top:{y:.3f}in;{box}">'
                    f'<div class="word" style="{area}">{coded(word, F_coded)}</div>'
                    f'<div class="tag">{esc(label)}</div></div>')
    over = .15                                                   # cut lines run a little into the margin, for a paper cutter
    cuts = "".join(f'<div class="cut" style="left:{x0 + c * cw - .0035:.4f}in;top:{y0 - over}in;width:.007in;height:{gh + 2 * over}in"></div>' for c in range(cols + 1))
    cuts += "".join(f'<div class="cut" style="top:{y0 + r * ch - .0035:.4f}in;left:{x0 - over}in;height:.007in;width:{gw + 2 * over}in"></div>' for r in range(rows + 1))
    foot = (f'<div class="foot" style="left:{x0}in;width:{gw}in;top:{y0 + gh + .2:.2f}in"><p>{HOW}</p><p>{SOURCE}</p></div>')
    return (f'<section class="page front">{head("plain side")}{cuts}{"".join(front)}{foot}</section>'
            f'<section class="page back">{head("coded side")}{"".join(back)}</section>')

MEASURE_JS = """(words) => { const s = document.createElement('span'); s.className = 'plain'; s.style.fontSize = '100px'; document.body.appendChild(s);
  const out = {}; for (const w of words) { s.textContent = w; out[w] = s.getBoundingClientRect().width / 100; } s.remove(); return out; }"""

# Run in the page before printing: every word sits inside its card's word area, every back card sits behind its front.
CHECK_JS = """() => { const bad = [], pages = [...document.querySelectorAll('.page')];
  pages.forEach((pg, i) => { if (pg.scrollHeight > pg.clientHeight + 1 || pg.scrollWidth > pg.clientWidth + 1) bad.push('page ' + (i + 1) + ' overflows');
    pg.querySelectorAll('.card').forEach(card => { const a = card.querySelector('.word').getBoundingClientRect(), el = card.querySelector('.word > *').getBoundingClientRect();
      if (el.left < a.left - .5 || el.right > a.right + .5 || el.top < a.top - .5 || el.bottom > a.bottom + .5) bad.push('p' + (i + 1) + ' ' + card.dataset.word + ' leaves its space');
      const t = card.querySelector('.tag').getBoundingClientRect(), c = card.getBoundingClientRect();
      if (t.right > c.right - 4) bad.push('p' + (i + 1) + ' label too long on ' + card.dataset.word); }); });
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
        for name, title, grade, cols, rows, cw, ch in SETS:
            cards = cards_for(grade)
            aw, ah = cw - 2 * PAD_X, ch - PAD_TOP - PAD_BOTTOM
            plain_w = await page.evaluate(MEASURE_JS, [w for w, _ in cards])
            F_plain = min(PLAIN_CAP, ah / PLAIN_HEIGHT, aw / max(plain_w.values()))
            F_coded = min(ah / 2.36, aw / max(LW.svg_word(w, 1.0, 0, cls=False)[1] for w, _ in cards))
            per = cols * rows
            slots = cards + [None] * ((-len(cards)) % per)
            n_sheets = len(slots) // per
            body = "".join(sheet_pages(title, slots[s * per:(s + 1) * per], cols, rows, cw, ch, F_plain, F_coded, s + 1, n_sheets) for s in range(n_sheets))
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

asyncio.run(main())
