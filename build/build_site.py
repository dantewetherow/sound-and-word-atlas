"""Build the Sound and Word Atlas site (version 1: the route and its steps) from the manual's route data.

usage: python3 build_site.py <route.json> <out dir> [--standalone]
The route.json comes from the manual (see ../README.md). Words are drawn with legomorphic_words.py and the
codes the deck tools already use, plus site_codes.py for route words that had none.
--standalone writes the home page as a full document, for a web host such as GitHub Pages. Without it the home
page has no doctype or head, because claude.ai adds those when it publishes the page as an artifact."""
import sys, json, re, html, pathlib, shutil
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
STANDALONE = "--standalone" in sys.argv[3:]
import legomorphic_words as LW
from known_codes import all_codes
import site_codes as SC

route = json.load(open(sys.argv[1], encoding="utf-8"))
OUT = pathlib.Path(sys.argv[2]); (OUT / "steps").mkdir(parents=True, exist_ok=True)
codes, _ = all_codes()
for w, c in SC.SITE_CODES.items(): codes.setdefault(w, c)
LW.W.clear(); LW.W.update(codes)
STEPS = route["steps"]; N = len(STEPS)
BUILT = "8 November 2026"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..600;1,9..144,400..600'
         '&family=Lexend:wght@300;400;500&display=swap">')

def md(s):
    """The manual's inline markdown (italics for cited words) to HTML."""
    s = html.escape(s.replace("**", ""), quote=False)
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)

def plain(s): return re.sub(r"\*", "", s)

def groups_of(words_md):
    """The step's words, kept in the groups the manual writes them in (be/bed is a pair)."""
    main = words_md.replace("**", "").split("; contrast")[0].replace("*", "")
    out = []
    for item in re.split(r"[;,]", main):
        for part in item.split("→"):
            g = [w.strip() for w in part.split("/") if w.strip()]
            if g: out.append(g)
    return out

def with_code(word, code):
    """Put a word's code in place for one drawing, and afterwards leave LW.W as it was (no stray empty code behind)."""
    had, old = word in LW.W, LW.W.get(word)
    LW.W[word] = code
    return lambda: LW.W.__setitem__(word, old) if had else LW.W.pop(word, None)

def svg_of(word, F, code=None, label=None):
    undo = with_code(word, code) if code else None
    try:
        svg, _, _ = LW.svg_strip([word], F=F, cls=False, label=label or f"{word}, marked")
    finally:
        if undo: undo()
    return svg

def coloured(word, code=None):
    """A word with its letters in their colours, as the orientation map shows them."""
    if word in SC.UNMARKED or (word not in LW.W and not code): return f'<span class="cw">{html.escape(word)}</span>'
    undo = with_code(word, code) if code else None
    try: letters = LW.parse(word)["letters"]
    finally:
        if undo: undo()
    cls = {"vowel": "v", "team": "g", "consonant": ""}
    return '<span class="cw">' + "".join(f'<span class="{cls[l["type"]]}">{html.escape(l["ch"])}</span>' if cls[l["type"]] else html.escape(l["ch"]) for l in letters) + "</span>"

def word_cells(group, F):
    cells = []
    for w in group:
        if w in SC.VARIANTS:
            for code, gloss in SC.VARIANTS[w]:
                cells.append(f'<figure class="word">{svg_of(w, F, code, f"{w}, as in {gloss}, marked")}<figcaption>{html.escape(gloss)}</figcaption></figure>')
        elif w in SC.UNMARKED or w not in LW.W:
            cells.append(f'<figure class="word unmarked"><span class="plain" style="font-size:{F:.0f}px">{html.escape(w)}</span>'
                         f'<figcaption>(under construction)</figcaption></figure>')
        else:
            cells.append(f'<figure class="word">{svg_of(w, F)}</figure>')
    return cells

def page(title, body, depth, desc):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
<title>{html.escape(title)}</title>
<link rel="icon" href="{up}favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">
<script>try {{ const t = localStorage.getItem('theme'); if (t === 'light' || t === 'dark') document.documentElement.dataset.theme = t; }} catch (e) {{}}</script>
{FONTS}
<link rel="stylesheet" href="{up}site.css">
</head>
<body>
{body}
{THEME_JS}
</body>
</html>
"""

# Bright and night. The page follows the device until a reader picks one; the pick is kept in this browser, and picking
# what the device already shows goes back to following the device. The script in the head sets the pick before the
# page paints, so it never flashes the other colours. Without script the switch stays hidden and the device decides.
THEME_JS = """<script>(() => {
  const root = document.documentElement, dark = matchMedia('(prefers-color-scheme: dark)'), sw = document.querySelector('.theme');
  if (!sw) return;
  const now = () => root.dataset.theme || (dark.matches ? 'dark' : 'light');
  const show = () => sw.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.pick === now())));
  sw.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    const pick = b.dataset.pick, device = dark.matches ? 'dark' : 'light';
    try { if (pick === device) { delete root.dataset.theme; localStorage.removeItem('theme'); }
          else { root.dataset.theme = pick; localStorage.setItem('theme', pick); } }
    catch (err) { root.dataset.theme = pick; }
    show();
  });
  if (dark.addEventListener) dark.addEventListener('change', show);
  sw.hidden = false; show();
})();</script>"""
# Note, the mascot, beside the site's name in the header (characters.py), in the site's colours so he follows bright and
# night. The brand link names the site, so the drawing is hidden from screen readers. Go, the logo (logo.py,
# build/logo.svg), stays the browser tab's icon, where Note's cone and vault are too fine to read.
import about_pages, characters
LOGO = characters.lifted(LW, "note", px_height=48, weight=1.7)

THEME_SWITCH = ('<div class="theme" role="group" aria-label="Page colours" hidden>'
                '<button type="button" data-pick="light">Bright</button><button type="button" data-pick="dark">Night</button></div>')

def header(depth):
    up = "../" * depth
    return (f'<header class="site"><div class="wrap"><a class="brand" href="{up}index.html"><span class="logo">{LOGO}</span><span class="name"><small>Legomorphic Notation</small>Sound and Word Atlas</span></a>'
            f'<div class="tools"><nav class="site" aria-label="Site"><a href="{up}index.html#route">The route</a><a href="{up}index.html#marks">Reading the marks</a>'
            f'<a href="{up}definitions.html">Definitions</a><a href="{up}cards.html">Word cards</a><a href="{up}word-lists.html">Word lists</a><a href="{up}presentations.html">Presentations</a><a href="{up}about.html">About</a></nav>'
            f'{THEME_SWITCH}</div></div></header>')

def footer(depth):
    up = "../" * depth
    return ('<footer class="site"><div class="wrap"><p>Page references are to Edward Carney, <i>A Survey of English Spelling</i> '
            '(Routledge, 1994). Updated ' + BUILT + '.</p>'
            '<p>&copy; 2026 Dante Wetherow, B.Ed., M.Ed. Shared under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>. '
            f'<a href="{up}credits.html">Credits and contact</a></p></div></footer>')

def fname(n): return f"{n:02d}.html"

def uc(text):
    """What's still being built, and what comes next, in the site's one form for it: (Under construction: ...). The
    text is HTML, starting in lower case."""
    return f'<p class="uc">(Under construction: {text})</p>'

# The manual's open items (route["open"]) as the step pages show them: what is still being decided on that step, and
# what comes next. Each item is found by its first words, and it must name the same steps it is shown on, so a new or
# changed item in the manual stops the build until its notes here are written.
UC_OPEN = {
 "Teams with two sounds": {
  22: "whether a team with two sounds, like the *oo* of *moon* and *book*, takes a mark to tell its sounds apart is still "
      "being decided. For now both sounds are marked alike. Next: decide, then redraw the words that change.",
  24: "*ow* joins the teams with two sounds here, as in *now* and *snow*. Whether those teams take a mark to tell their "
      "sounds apart is still being decided, and for now both sounds are marked alike. Next: decide, then redraw the words "
      "that change."},
 "Step 19 could move up": {
  19: "this step may move up to follow step 13. Its words turn up in reading from the start, and every unit it uses is in "
      "place by step 13, where the seam lets *does* be built as *do* + *es*. Next: decide where it sits in the route.",
  13: "step 19, a vowel that borrows a sound, may move up to follow this step, since every unit it uses is in place by "
      "here. Next: decide where it sits in the route."},
 "The black bond bar": {
  **{n: "the black bond bar, under letters that spell one consonant sound such as *qu*, *wh* and *ng*, is used from early "
        "in the route but isn't named as a new mark until step 25. Next: decide whether to name it at step 5." for n in (4, 5, 13)},
  25: "the black bond bar is named as a new mark here, but *qu*, *wh* and *ng* take it from earlier steps. Next: decide "
      "whether to name it at step 5 instead."},
 "The pointer pill": {
  28: "the pointer pill is a proposed mark, not a settled one. Next: decide whether it joins the legend."},
}
for item in route["open"]:
    key = next((k for k in UC_OPEN if item.startswith(k)), None)
    assert key, f"an open item in the manual has no under-construction note on the site yet: {item[:70]}"
    named = {int(x) for x in re.findall(r"\b(?:step|steps)\s+(\d+)", item, re.I)} | {int(x) for x in re.findall(r"\band\s+(\d+)\)", item)}
    assert named == set(UC_OPEN[key]), (key, sorted(named))

def open_items_for(n):
    return [UC_OPEN[k][n] for k in UC_OPEN if n in UC_OPEN[k] and any(i.startswith(k) for i in route["open"])]

DRAFT_FROM = 16                         # steps 16 to 32 were added as a first draft on 15 October 2026
DRAFT_NOTE = f"steps {DRAFT_FROM} to {N} are a first draft. Next: a second look at their order and their words."

def new_marks(m):
    """The step's new marks. The manual writes an undecided one as "open: ..." or "proposed: ...", and the step's
    under-construction note says what's being decided."""
    if m.lower() == "none": return "None: the step uses marks already met."
    if re.match(r"(open|proposed):", m, re.I): return "None settled yet."
    return md(m)

# ------------------------------------------------------------------ step pages
for i, s in enumerate(STEPS):
    n = s["n"]; band = s["band"]
    prev_s = STEPS[i - 1] if i else None; next_s = STEPS[i + 1] if i + 1 < N else None
    cells = []
    for g in groups_of(s["words_md"]):
        inner = word_cells(g, 58)
        cells.append(f'<div class="group{" pair" if len(inner) > 1 else ""}">' + "".join(inner) + "</div>")
    notes = []
    marks = s["marks"].strip()
    notes.append(f'<div class="note"><h2>New marks</h2><p>{new_marks(marks)}</p></div>')
    if s.get("contrast_md"):
        notes.append(f'<div class="note"><h2>Contrast</h2><p>{md(s["contrast_md"])}</p></div>')
    k = s["kernel_md"].strip()
    notes.append(f'<div class="note"><h2>Kernel words</h2><p>{md(k) if k.lower() != "none" else "None at this step."}</p></div>')
    notes.append(f'<div class="note"><h2>Carney (1994)</h2><p>{md(s.get("carney", ""))}</p></div>')
    for text in open_items_for(n):
        notes.append(f'<div class="note uc">{uc(md(text))}</div>')
    unmarked = sorted({SC.UNMARKED[w] for g in groups_of(s["words_md"]) for w in g if w in SC.UNMARKED})
    um = uc("the words in plain letters aren't marked here yet. " + " ".join(f"{md(why)} Next: {md(nxt)}" for why, nxt in unmarked)) if unmarked else ""
    draft = uc(DRAFT_NOTE) if n >= DRAFT_FROM else ""
    pn = '<nav class="pn" aria-label="Steps">'
    pn += (f'<a class="prev" href="{fname(prev_s["n"])}"><span>Step {prev_s["n"]}</span>{md(prev_s["title"])}</a>' if prev_s else '<span></span>')
    pn += (f'<a class="next" href="{fname(next_s["n"])}"><span>Step {next_s["n"]}</span>{md(next_s["title"])}</a>' if next_s else '<span></span>')
    pn += "</nav>"
    body = f"""{header(1)}
<main class="wrap">
<div class="step-head">
<p class="eyebrow"><a href="../index.html#band-{re.sub(r'[^a-z]+', '-', band.lower()).strip('-')}">{html.escape(band)}</a> · Step {n} of {N}</p>
<h1>{md(s['title'])}</h1>
{draft}
</div>
<div class="plate">
<section class="words" aria-label="The step's words, marked">
{''.join(cells)}
{um}
</section>
<aside class="notes">
{''.join(notes)}
</aside>
</div>
{pn}
</main>
{footer(1)}"""
    t = f"Step {n}: {plain(s['title'])}"
    (OUT / "steps" / fname(n)).write_text(page(t, body, 1, f"{t}, on the Sound and Word Atlas route."), encoding="utf-8")

# ------------------------------------------------------------------ home page (the artifact's own page: no doctype, the host adds it)
def tile(s):
    words = []
    for g in groups_of(s["words_md"]):
        for w in g:
            if w in SC.VARIANTS:
                words.append(coloured(w, SC.VARIANTS[w][0][0]))
            else:
                words.append(coloured(w))
    seen, uniq = set(), []
    for w in words:
        if w not in seen: seen.add(w); uniq.append(w)
    return (f'<a class="tile" href="steps/{fname(s["n"])}"><span class="num">{s["n"]}</span>'
            f'<span class="t">{md(s["title"])}</span><span class="w">{" ".join(uniq)}</span></a>')

bands_html = []
for b in route["bands"]:
    ss = [x for x in STEPS if x["n"] in b["steps"]]
    slug = re.sub(r"[^a-z]+", "-", b["name"].lower()).strip("-")
    draft = '<span class="badge">Under construction</span>' if min(b["steps"]) >= DRAFT_FROM else ""
    bands_html.append(f'<section class="band" id="band-{slug}"><div class="band-label"><h3>{html.escape(b["name"])}</h3>'
                      f'<p>Steps {min(b["steps"])} to {max(b["steps"])}</p>{draft}</div>'
                      f'<div class="tiles">{"".join(tile(x) for x in ss)}</div></section>')

KEY = [("Sound circle", "One circle under each sound: red for a vowel sound, black for a consonant, green for <em>sh</em>, <em>th</em>, <em>ch</em>", ["it", "she"]),
       ("Syllable swoop", "One swoop under each syllable", ["happy"]),
       ("Short mark", "A cup over a vowel that keeps its short sound", ["get"]),
       ("Long mark", "A bar over a vowel that says its name", ["go"]),
       ("Bond bar", "A bar under letters that spell one sound: black for consonant units and for doubled letters, boxed or not, green for <em>sh</em>, <em>th</em>, <em>ch</em>, red for vowel units", ["will", "she", "night"]),
       ("R-controlled unit", "A red bar under a vowel and its <em>r</em>, with the vowel red, the <em>r</em> black and one circle", ["car"]),
       ("Block box", "A box around the vowel protector at work: a pair or cluster with a vowel after it, which it stops from reaching back. A pair keeps its bond bar when the box comes; a cluster has none", ["hopping"]),
       ("Cone of silence", "A dotted ring around a silent <em>e</em>", ["have"]),
       ("Vowel vault", "An arc from an <em>e</em>, or a vowel after one consonant, back to the vowel it makes long", ["make"]),
       ("Nice-nudge", "A small arc under the letters from <em>e</em>, <em>i</em> or <em>y</em> to the <em>c</em> or <em>g</em> it softens", ["nice"]),
       ("Blocked vault", "A half-arc that ends in a red X where a box stops the vault", ["getting"]),
       ("Morpheme seam", "A dotted line between morphemes", ["going"])]
key_html = "".join(f'<figure class="mark"><div class="mw">{"".join(svg_of(w, 34) for w in ws)}</div>'
                   f'<figcaption><b>{name}</b>{what}</figcaption></figure>' for name, what, ws in KEY)

uniq = {w for s in STEPS for g in groups_of(s["words_md"]) for w in g}
n_words = len(uniq) + sum(len(v) - 1 for w, v in SC.VARIANTS.items() if w in uniq)
n_marked = n_words - len([w for w in uniq if w in SC.UNMARKED or (w not in LW.W and w not in SC.VARIANTS)])

home_head = f"""<title>Sound and Word Atlas</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<link rel="stylesheet" href="site.css">
"""
import landing
for w in ("legomorphic", "note", "notate", "notation"): assert w in LW.W, w
home_body = f"""{header(0)}
<main>
{landing.html_block(LW)}
<section class="route" id="route" aria-labelledby="route-h"><div class="wrap">
<h2 id="route-h">The route at a glance</h2>
<p class="lead">{md(route["intro"].split(" The orientation map")[0])} Open a step to see its words marked, the marks it brings in, and the pages in Carney's survey that back it.</p>
<p class="sub">Each word is shown with its letters in colour: red for vowels, green for <em>sh</em>, <em>th</em> and <em>ch</em>, black for the rest.</p>
{''.join(bands_html)}
</div></section>
<section class="marks" id="marks" aria-labelledby="marks-h"><div class="wrap">
<h2 id="marks-h">Reading the marks</h2>
<p class="sub">Twelve marks, each drawn on a word that uses it.</p>
<div class="key">{key_html}</div>
{uc("next, the legend in full, with the rule behind each mark.")}
</div></section>
<section class="about" id="about" aria-labelledby="about-h"><div class="wrap">
<h2 id="about-h">What&rsquo;s here</h2>
<div class="cols">
<div><h3>The route</h3><p>{N} steps in {len(route["bands"])} bands, with {n_words} different words, {n_marked} of them marked. Each step page has its words, the marks it brings in, and the pages in Carney&rsquo;s survey that back it.</p></div>
<div><h3>To print and present</h3><p>Printable cards for the ELP high-frequency words and all of Dolch&rsquo;s sight words are on the <a href="cards.html">Word cards</a> page, and <a href="word-lists.html">Word lists</a> shows where the ELP words come from. The first session of the staff series, with its handouts, is under <a href="presentations.html">Presentations</a>.</p></div>
<div><h3>The notation</h3><p><a href="about.html">About</a> explains the notation and its name, <a href="definitions.html">Definitions</a> has its words, and <a href="credits.html">Credits</a> names the writers it draws on.</p></div>
</div>
{uc(f"steps {DRAFT_FROM} to {N} are a first draft, and a few words show in plain letters until their marking is settled. Next: the legend in full, the word families and the teaching routines.")}
</div></section>
</main>
{footer(0)}"""
if STANDALONE:
    home = page("Sound and Word Atlas", home_body, 0,
                "A route through English spelling for teachers: 32 steps, with every word marked in Legomorphic Notation.")
else:
    home = home_head + home_body
(OUT / "index.html").write_text(home, encoding="utf-8")

# The word cards page, written when the card PDFs are in <out>/cards (build_elp_cards.py makes them).
CARD_SETS = [("elp-word-cards-kindergarten.pdf", "Kindergarten", "K", "List 1", 8),
             ("elp-word-cards-grade-1.pdf", "Grade 1", "1", "Lists 2 to 10", 10),
             ("elp-word-cards-grade-2.pdf", "Grade 2", "2", "Lists 11 to 13", 10)]
ELP_FILE = HERE / "data" / "elp_hfw.json"
if ELP_FILE.exists() and all((OUT / "cards" / f).exists() for f, *_ in CARD_SETS):
    ELP = json.loads(ELP_FILE.read_text(encoding="utf-8"))
    tiles = []
    for f, title, grade, lists, per in CARD_SETS:
        n = sum(len(v["words"]) for v in ELP["lists"].values() if v["grade"] == grade)
        kb = round((OUT / "cards" / f).stat().st_size / 1024)
        tiles.append(f'<div><h3>{title}</h3><p>{lists}: {n} cards on {-(-n // per)} sheets, {per} to a page.</p>'
                     f'<p><a href="cards/{f}" download>Download the PDF</a> ({kb} KB)</p></div>')
    sample = (f'<div class="words"><figure class="word"><span class="plain" style="font-size:58px">make</span><figcaption>front</figcaption></figure>'
              f'<figure class="word">{svg_of("make", 58)}<figcaption>back</figcaption></figure></div>')

    # The grade 3 word sum cards (build_word_sum_cards.py), shown when their PDF is there too.
    WS_FILE = "word-sum-cards-grade-3.pdf"
    ws_html = ""
    if (OUT / "cards" / WS_FILE).exists():
        import word_sum_codes as WS
        groups = []
        for short, title, rows in WS.SECTIONS:
            groups.append((title, len(rows)))
            if short == "Prefixes": groups.append(("Pairs that aren't word sums", len(WS.PAIRS)))
        sheet, ranges = 1, []
        for title, n in groups:
            k = -(-n // 10)
            ranges.append(f'<li>{"Sheets" if k > 1 else "Sheet"} {sheet}{f"&ndash;{sheet + k - 1}" if k > 1 else ""}: {html.escape(title[0].lower() + title[1:])} ({n} cards)</li>')
            sheet += k
        n_cards = sum(n for _, n in groups)
        kb = round((OUT / "cards" / WS_FILE).stat().st_size / 1024)
        ws_sample = (f'<div class="words"><figure class="word"><span class="plain" style="font-size:58px">making</span><figcaption>front</figcaption></figure>'
                     f'<figure class="word"><span style="font-size:15px;color:var(--soft)">make + ing &rarr; making</span>{svg_of("making", 58)}<figcaption>back</figcaption></figure></div>')
        ws_html = f"""
<section class="about" id="word-sums" aria-labelledby="ws-h"><div class="wrap">
<h2 id="ws-h">Grade 3 word sums</h2>
<p class="sub">An extension for students who have finished the ELP lists: {n_cards} cards built on the list words. The front has the whole word. The back has its word sum, such as make + ing &rarr; making, and the word coded with a seam at each join. Each group starts on a new sheet, so you can print just the rule you're teaching.</p>
<p><a href="cards/{WS_FILE}" download>Download the PDF</a> ({kb} KB, {sheet - 1} sheets, 10 to a page)</p>
<ul class="sub">{''.join(ranges)}</ul>
{ws_sample}
</div></section>"""
    # The Dolch sight word cards (build_dolch_cards.py), shown when all five PDFs are there.
    DOLCH = json.loads((HERE / "data" / "dolch.json").read_text(encoding="utf-8"))
    elp_words = {w for v in ELP["lists"].values() for w in v["words"]}
    dolch_sets = [(f'dolch-word-cards-{l["key"]}.pdf', l) for l in DOLCH["levels"]]
    dolch_html = ""
    if all((OUT / "cards" / f).exists() for f, _ in dolch_sets):
        dtiles = []
        for f, l in dolch_sets:
            n, on = len(l["words"]), sum(w in elp_words for w in l["words"])
            kb = round((OUT / "cards" / f).stat().st_size / 1024)
            dtiles.append(f'<div><h3>{html.escape(l["name"])}</h3><p>{n} cards on {-(-n // 10)} sheets, {on} of them on the ELP lists.</p>'
                          f'<p><a href="cards/{f}" download>Download the PDF</a> ({kb} KB)</p></div>')
        n_d = sum(len(l["words"]) for l in DOLCH["levels"])
        dolch_html = f"""
<section class="about" id="dolch" aria-labelledby="dolch-h"><div class="wrap">
<h2 id="dolch-h">Dolch sight words</h2>
<p class="sub">All {n_d} of E. W. Dolch&rsquo;s sight words (1936), one set for each of his levels, 10 to a page. Each card&rsquo;s tag names its level and the ELP list that teaches the word, if one does, so you can set aside the cards a class has already met. <a href="word-lists.html">Where the ELP words come from</a> shows how the two lists line up.</p>
<div class="cols">{''.join(dtiles)}</div>
</div></section>"""
    cards_body = f"""{header(0)}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Downloads</p>
<h1>Word cards</h1>
<p class="lead">Printable cards with the plain word on the front and the coded word on the back: high-frequency words from the SD23 Early Literacy Profile lists, all of Dolch&rsquo;s sight words, and word sums for students who have finished the ELP lists.</p>
</div></section>
<section class="about" id="elp" aria-labelledby="elp-h"><div class="wrap">
<h2 id="elp-h">ELP high-frequency words</h2>
<div class="cols">{''.join(tiles)}</div>
{sample}
</div></section>{dolch_html}{ws_html}
<section class="about" aria-label="Notes"><div class="wrap"><div class="cols">
<div><h3>Printing</h3><p>Print in colour and double-sided, flipping on the long edge, so each back lands behind its front. Print one sheet first and hold it up to a window to check that the backs line up, then cut on the grey lines. Spaces left over on a sheet are blank cards to write on.</p></div>
<div><h3>The coding</h3><p>The coded side shows the word in the notation, and <a href="index.html#marks">Reading the marks</a> says what each mark means.</p>{uc("a few markings are still being settled, most of the word sums and a few of the Dolch words among them. Next: settle them, then update the cards that change.")}</div>
<div><h3>Where the words come from</h3><p>The Early Literacy Profile (ELP) Assessment &amp; Instructional Guide, Central Okanagan Public Schools (2025), pp. 16&ndash;17. The guide doesn't name a source for its lists; it says they were aligned with a phonics scope and sequence, keeping one word for each pattern. All but three of its 148 words are E. W. Dolch&rsquo;s (1936), as <a href="word-lists.html">Word lists</a> shows. These cards aren't an SD23 publication. The district's own <a href="https://assessment.sd23.bc.ca/elp">ELP page</a> is the place for the assessment itself.</p></div>
<div><h3>Word sums</h3><p>Word sums and word matrices come from Melvyn Ramsden's Real Spelling, and Peter Bowers brought them into classrooms as structured word inquiry. The base words come from the ELP lists and E. W. Dolch's grade 3 list (Dolch, 1936).</p></div>
</div></div></section>
</main>
{footer(0)}"""
    (OUT / "cards.html").write_text(page("Word cards · Sound and Word Atlas", cards_body, 0,
                                         "Printable high-frequency word cards from the SD23 ELP lists, plain on the front and coded on the back."), encoding="utf-8")
    print("wrote cards.html |", ", ".join(t for _, t, *_ in CARD_SETS))

from dolch_codes import DOLCH_CODES
import word_lists
for w, c in DOLCH_CODES.items(): LW.W.setdefault(w, c)
word_lists.write(OUT, page, header, footer, coloured, LW)

import sessions
sessions.write(OUT, page, header, footer)

about_pages.write(OUT, page, header, footer, svg_of, LW)

import definitions
definitions.write(OUT, page, header, footer, svg_of, KEY, LW)

if (HERE / "site.css").exists():
    shutil.copy(HERE / "site.css", OUT / "site.css")
shutil.copy(HERE / "logo.svg", OUT / "favicon.svg")          # the tab icon: the logo's own colour rules, light or dark
for icon in ("favicon-32.png", "apple-touch-icon.png"):      # for browsers that can't use an SVG icon
    shutil.copy(HERE / icon, OUT / icon)
print("wrote", OUT, "| words", n_words, "marked", n_marked)
