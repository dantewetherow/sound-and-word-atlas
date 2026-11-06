"""Grade 3 word sum cards: an extension for students who have finished the ELP high-frequency lists.

One PDF for double-sided printing, flipping on the long edge, 10 cards to a page. The front of each card has the
whole word; the back has its word sum and the word coded, with a seam at each join. Each group of the manual's
Word analysis draft starts on a new sheet, so a teacher can print just the rule being taught. Markings come from
word_sum_codes.py and are drawn by legomorphic_words.py. The name of the notation is left off the cards.

Run:  python3 build/build_word_sum_cards.py <node_modules with @fontsource-variable/lexend> docs/cards <work folder>
"""
import asyncio, base64, html, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import legomorphic_words as LW
from known_codes import all_codes
import word_sum_codes as WS
from playwright.async_api import async_playwright

FONTS, OUT, WORK = (pathlib.Path(a) for a in sys.argv[1:4])
codes, _ = all_codes(); LW.W.clear(); LW.W.update(codes)
for _, _, rows in WS.SECTIONS:
    for _, w, code in rows: LW.W[w] = code
esc = html.escape

NAME, TITLE = "word-sum-cards-grade-3", "Grade 3 word sums"
COLS, ROWS, CW, CH = 2, 5, 3.9, 2.0
PAGE_W, PAGE_H = 8.5, 11.0
PAD_X, PAD_TOP, PAD_BOTTOM = 0.20, 0.15, 0.25
SUM_H = 0.30                 # the word sum line on the back, in inches
CODED_CAP = 0.55             # the largest letter size for a coded word; longer words shrink to fit
PLAIN_CAP, PLAIN_HEIGHT = 1.0, 1.30
TAG = "#8d8577"
CREDIT = ("Word sums after Melvyn Ramsden's Real Spelling and Peter Bowers's structured word inquiry. "
          "Base words from the SD23 ELP lists (pp.&nbsp;16&ndash;17) and Dolch grade 3.")
HOW = "Print in colour and double-sided, flipping on the long edge, so each back lands behind its front. Cut on the grey lines."

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
.stack{display:flex;flex-direction:column;align-items:center;justify-content:center;max-width:100%;}
.sum{font-size:12.5pt;line-height:1;color:var(--soft);white-space:nowrap;height:""" + f"{SUM_H}in" + """;display:flex;align-items:flex-start;}
.sum.note{font-size:10pt;}
.pair{display:flex;align-items:flex-end;gap:.25in;}
.tag{position:absolute;left:.12in;bottom:.07in;font-size:6.4pt;letter-spacing:.03em;color:""" + TAG + """;white-space:nowrap;}
.cut{position:absolute;background:#b3aa9b;}
.head,.foot{position:absolute;font-size:6.6pt;color:""" + TAG + """;letter-spacing:.02em;}
.head{display:flex;justify-content:space-between;}
.foot p{margin:0 0 .03in;}
"""

AW, AH = CW - 2 * PAD_X, CH - PAD_TOP - PAD_BOTTOM

def coded(word, F):
    g, w, H = LW.svg_word(word, 100.0, 0.0, cls=False)
    return (f'<svg viewBox="0 0 {w:.1f} {H:.1f}" style="width:{w / 100 * F:.3f}in;height:{H / 100 * F:.3f}in;display:block" '
            f'role="img" aria-label="{esc(word)}, coded">{g}</svg>')

def fit(*words, gap=0.0):
    """The coded letter size that fits these words side by side under the word sum line."""
    ratio = sum(LW.svg_word(w, 1.0, 0, cls=False)[1] for w in words)
    return min(CODED_CAP, (AH - SUM_H) / 2.36, (AW - gap) / ratio)

def cards():
    """(group label, front text, back html) for every card, with the group each starts."""
    out = []
    for short, title, rows in WS.SECTIONS:
        group = [(short, w, f'<div class="stack"><div class="sum">{esc(s)}</div>{coded(w, fit(w))}</div>') for s, w, _ in rows]
        out.append((short, group))
        if short == "Prefixes":   # the pairs come after prefixes in the manual's tab
            pairs = [("Not word sums", f"{a} / {b}",
                      f'<div class="stack"><div class="sum note">Not a word sum: {esc(note[0].lower() + note[1:])}</div>'
                      f'<div class="pair">{coded(a, fit(a, b, gap=.25))}{coded(b, fit(a, b, gap=.25))}</div></div>')
                     for a, b, note in WS.PAIRS]
            out.append(("Not word sums", pairs))
    return out

def sheet(label, slot_cards, sheet_no, n_sheets, F_plain):
    x0, y0 = (PAGE_W - COLS * CW) / 2, (PAGE_H - ROWS * CH) / 2
    gw, gh = COLS * CW, ROWS * CH
    area = f"left:{PAD_X}in;right:{PAD_X}in;top:{PAD_TOP}in;bottom:{PAD_BOTTOM}in"
    def head(side):
        return (f'<div class="head" style="left:{x0}in;width:{gw}in;top:{y0 - .32:.2f}in">'
                f'<span>{TITLE} · {esc(label)}</span><span>Sheet {sheet_no} of {n_sheets} · {side}</span></div>')
    front, back = [], []
    for i, card in enumerate(slot_cards):
        if card is None: continue
        group, front_text, back_html = card
        r, c = divmod(i, COLS)
        y, xf, xb = y0 + r * CH, x0 + c * CW, x0 + (COLS - 1 - c) * CW
        box, tag = f"width:{CW}in;height:{CH}in", f'<div class="tag">{TITLE} · {esc(group)}</div>'
        front.append(f'<div class="card" data-word="{esc(front_text)}" style="left:{xf:.3f}in;top:{y:.3f}in;{box}">'
                     f'<div class="word" style="{area}"><span class="plain" style="font-size:{F_plain[front_text]:.3f}in">{esc(front_text)}</span></div>{tag}</div>')
        back.append(f'<div class="card" data-word="{esc(front_text)}" style="left:{xb:.3f}in;top:{y:.3f}in;{box}">'
                    f'<div class="word" style="{area}">{back_html}</div>{tag}</div>')
    over = .15
    cuts = "".join(f'<div class="cut" style="left:{x0 + c * CW - .0035:.4f}in;top:{y0 - over}in;width:.007in;height:{gh + 2 * over}in"></div>' for c in range(COLS + 1))
    cuts += "".join(f'<div class="cut" style="top:{y0 + r * CH - .0035:.4f}in;left:{x0 - over}in;height:.007in;width:{gw + 2 * over}in"></div>' for r in range(ROWS + 1))
    foot = f'<div class="foot" style="left:{x0}in;width:{gw}in;top:{y0 + gh + .12:.2f}in"><p>{HOW}</p><p>{CREDIT}</p></div>'
    return (f'<section class="page front">{head("front")}{cuts}{"".join(front)}{foot}</section>'
            f'<section class="page back">{head("back")}{"".join(back)}</section>')

MEASURE_JS = """(words) => { const s = document.createElement('span'); s.className = 'plain'; s.style.fontSize = '100px'; document.body.appendChild(s);
  const out = {}; for (const w of words) { s.textContent = w; out[w] = s.getBoundingClientRect().width / 100; } s.remove(); return out; }"""

CHECK_JS = """() => { const bad = [], pages = [...document.querySelectorAll('.page')];
  pages.forEach((pg, i) => { if (pg.scrollHeight > pg.clientHeight + 1 || pg.scrollWidth > pg.clientWidth + 1) bad.push('page ' + (i + 1) + ' overflows');
    pg.querySelectorAll('.card').forEach(card => { const a = card.querySelector('.word').getBoundingClientRect();
      card.querySelectorAll('.word *').forEach(el => { const r = el.getBoundingClientRect(); if (!r.width) return;
        if (r.left < a.left - .5 || r.right > a.right + .5 || r.top < a.top - .5 || r.bottom > a.bottom + .5) bad.push('p' + (i + 1) + ' ' + card.dataset.word + ' leaves its space'); });
      const t = card.querySelector('.tag').getBoundingClientRect(), c = card.getBoundingClientRect();
      if (t.right > c.right - 4) bad.push('p' + (i + 1) + ' label too long on ' + card.dataset.word); }); });
  for (let i = 0; i + 1 < pages.length; i += 2) { const f = [...pages[i].querySelectorAll('.card')], b = [...pages[i + 1].querySelectorAll('.card')];
    if (f.length !== b.length) bad.push('sheet ' + (i / 2 + 1) + ' front and back differ');
    const P = pages[i].getBoundingClientRect(), Q = pages[i + 1].getBoundingClientRect();
    f.forEach((card, k) => { const fr = card.getBoundingClientRect(), brr = b[k].getBoundingClientRect();
      const ok = Math.abs((P.right - fr.right) - (brr.left - Q.left)) < .5 && Math.abs((fr.top - P.top) - (brr.top - Q.top)) < .5;
      if (b[k].dataset.word !== card.dataset.word || !ok) bad.push('sheet ' + (i / 2 + 1) + ' ' + card.dataset.word + ' is not behind its front'); }); }
  return {bad, fonts: document.fonts.check('40px Lexend'), pages: pages.length}; }"""

async def main():
    OUT.mkdir(parents=True, exist_ok=True); WORK.mkdir(parents=True, exist_ok=True)
    groups = cards()
    per = COLS * ROWS
    plan = []                                     # (group label, the cards on one sheet)
    for label, group in groups:
        for s in range(0, len(group), per):
            chunk = group[s:s + per]
            plan.append((label, chunk + [None] * (per - len(chunk))))
    async with async_playwright() as p:
        br = await p.chromium.launch()
        page = await br.new_page()
        await page.set_content(f"<!doctype html><html><head><style>{CSS}</style></head><body></body></html>")
        await page.evaluate("document.fonts.load('100px Lexend')"); await page.evaluate("document.fonts.ready")
        fronts = [c[1] for _, g in groups for c in g]
        widths = await page.evaluate(MEASURE_JS, fronts)
        singles = [w for w in widths if " / " not in w]
        F_single = min(PLAIN_CAP, AH / PLAIN_HEIGHT, AW / max(widths[w] for w in singles))
        F_plain = {w: (F_single if w in singles else min(F_single, AW / widths[w])) for w in widths}
        body = "".join(sheet(label, chunk, i + 1, len(plan), F_plain) for i, (label, chunk) in enumerate(plan))
        f = WORK / f"{NAME}.html"
        f.write_text(f'<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><title>{TITLE}</title><style>{CSS}</style></head><body>{body}</body></html>', encoding="utf-8")
        await page.goto(f.as_uri()); await page.evaluate("document.fonts.ready")
        await page.emulate_media(media="print")
        r = await page.evaluate(CHECK_JS)
        assert r["fonts"] and not r["bad"], r
        await page.pdf(path=str(OUT / f"{NAME}.pdf"), width="8.5in", height="11in", print_background=True,
                       margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        await br.close()
    first = {}
    for i, (label, _) in enumerate(plan): first.setdefault(label, []).append(i + 1)
    print(f"wrote {NAME}.pdf | {len(fronts)} cards on {len(plan)} sheets ({r['pages']} pages) | plain {F_single * 72:.0f} pt (pairs as small as {min(F_plain.values()) * 72:.0f} pt) | widest word {max(singles, key=widths.get)}")
    for label, sheets in first.items(): print(f"  {label}: " + (f"sheets {sheets[0]}-{sheets[-1]}" if len(sheets) > 1 else f"sheet {sheets[0]}"))

asyncio.run(main())
