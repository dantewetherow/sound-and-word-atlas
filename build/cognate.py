"""A cognate laid out part by part (25 November 2026): English information beside Ukrainian інформація, each part in
its colour, so learners see the same parts in the same order. Both words come from Latin informatio: English took it
through French; Wiktionary gives no route for the Ukrainian. Strictly they are parallel borrowings of one
Latin word rather than cognates inherited side by side; the site uses cognate in the plain sense, words with a shared
origin. Ukrainian forms and IPA: Wiktionary, інформація.

Used on the form family page (roots.py) and in the word study (studies.py)."""

ROWS = [("English", "en", ["in", "form", "ation", ""], "/&#716;&#618;nf&#601;r&#712;me&#618;&#643;&#601;n/", "information"),
        ("Ukrainian", "uk", ["&#1110;&#1085;", "&#1092;&#1086;&#1088;&#1084;", "&#1072;&#1094;&#1110;", "&#1103;"], "[inf&#596;r&#712;mat&#865;s&#690;ij&#592;]", "informatsiia")]
KINDS = ["pre", "base", "suf", "end"]
GLOSS = ["in, into", "shape", "the act of", "an ending that changes with the sentence"]


def block(steps=False):
    """steps: reveal one column at a time on a slide (data-s 1 to 4), then the sounds (5)."""
    s = (lambda k: f' data-s="{k}"') if steps else (lambda k: "")
    out = []
    for lab, lang, parts, say, latin in ROWS:
        cells = "".join(f'<span class="cg cg-{KINDS[i]}{" cg-none" if not p else ""}"{s(i + 1)}>{p}</span>' for i, p in enumerate(parts))
        out.append(f'<div class="cog-row" lang="{lang}"><span class="cog-lab">{lab}</span>{cells}'
                   f'<span class="cog-say"{s(5)}>{say} <i lang="en">{latin}</i></span></div>')
    gl = "".join(f'<span class="cog-g"{s(i + 1)}>{g}</span>' for i, g in enumerate(GLOSS))
    return f'<div class="cog">{"".join(out)}<div class="cog-row cog-gls"><span class="cog-lab"></span>{gl}<span></span></div></div>'


CSS = """
/* a cognate, part by part (25 November 2026) */
.cog { display: grid; gap: 10px; margin: 16px 0; overflow-x: auto; }
.cog-row { display: grid; grid-template-columns: 7.5em repeat(4, minmax(3.2em, auto)) 1fr; align-items: center; gap: 0 6px; }
.cog-lab { font-size: 0.85rem; color: var(--soft); }
.cg { display: inline-block; text-align: center; font-size: 1.6rem; padding: 4px 12px; border: 2px solid var(--kc); border-radius: 8px; color: var(--kc); background: var(--card); }
.cg-pre { --kc: var(--modal); } .cg-base { --kc: var(--ink); } .cg-suf { --kc: var(--verb); } .cg-end { --kc: var(--soft); border-style: dashed; }
.cg-none { border-color: transparent; background: transparent; }
.cog-say { font-size: 0.95rem; color: var(--soft); padding-left: 10px; }
.cog-gls .cog-g { font-size: 0.78rem; color: var(--soft); text-align: center; line-height: 1.2; }
"""
