"""The site's layers, its tree, breadcrumbs, search and the Teacher/Student view.

Since 10 November 2026 the atlas has three layers and a shelf, so a teacher holds three things in mind, not eight:
Steps (the route, in order, with the marks), Words (look up a word: its walk and its sum) and Parts (prefixes,
suffixes, roots and joins, each with its words; parts.py). Everything a teacher prints, presents or checks is on the
For teachers shelf. From 8 to 10 November there were eight doors named as one -ion family (Progressions, Notations,
Explorations, Constructions, Derivations, Instructions, Connections, Explanations); their pages keep their addresses
and now sit inside a layer or on the shelf (HEADS). PAGES is the one place that says which page sits where: the
header, the breadcrumbs, the site map and the search's page records all come from it.

The Details/Board switch (named Teacher/Student until 10 November 2026, and still "teacher" and "student" in the
code) shows the same pages two ways, as Bright/Night shows them in two colourings. The site is a teacher's, used with
learners, so the second view is the board: it draws the words big and hides the teacher's notes and the build's under-construction notes. A
link ending ?view=student opens a page that way, and the pick is kept in this browser. Without script, a page shows
the teacher view.

Search runs in the reader's browser over search.json, which the build writes: every word, part, step, mark, term and
page. Nothing typed leaves the device. Without script the box stays hidden, and the header's Site map link stands in."""
import html, json, re

DOORS = [   # slug, name, (unused), in plain words, the short word in student view (None: for teachers only)
    ("progressions", "Steps", "", "Lessons in reading and spelling, in order: the legomorphic route through English spelling. Start here to learn the notation.", "Steps"),
    ("walk", "Words", "", "Look up a word and walk through it: its marks, a move at a time, and its parts.", "Words"),
    ("parts", "Parts", "", "Prefixes, suffixes, roots and joins, each with every word that has it.", "Parts"),
    ("teachers", "For teachers", "", "To print and present, how the route lines up with programs, and the reasons and sources.", None),
]
DOOR = {d[0]: d for d in DOORS}

# The pages that were doors until 10 November 2026, and now sit inside a layer or on the teachers' shelf: slug ->
# (heading, in plain words, the heading in student view or None).
HEADS = {
    "progressions": ("Steps", DOORS[0][3], "Steps"),
    "notations": ("The marks", "The marks, and what each one shows.", "Marks"),
    "explorations": ("Explorations", "Words to take apart and build: a family, contractions, and ablaut.", "Words"),
    "constructions": ("Sentences", "How sentences are built: actors, operators and actions, and the flip from claim to question.", "Sentences"),
    "derivations": ("Roots and their sources", "Where words come from, and the sources the roots cite.", "Roots"),
    "instructions": ("To print and present", "Presentations, word cards and affix tent cards.", None),
    "connections": ("Programs and word lists", "How the route lines up with UFLI Foundations and with the word lists schools already use.", None),
    "explanations": ("Reasons and sources", "Definitions, the notation and its name, and credits.", None),
    "teachers": ("For teachers", DOORS[3][3], None),
}

# The tree: (path, layer, title, one-line summary). Steps join it in tree().
PAGES = [
    ("index.html", None, "Home", "Legomorphic Notation and the three layers of the site."),
    ("progressions.html", "progressions", "Steps", "The legomorphic route through English spelling: the steps in their bands."),
    ("letters.html", "progressions", "Letters, names and sounds", "Before step 1: the alphabet in the song's units, as tiles to reveal, with a sound circle under each letter."),
    ("notations.html", "progressions", "The marks", "The marks of Legomorphic Notation, each drawn alone on one word."),
    ("walk.html", "walk", "Words", "Look up a word and walk through it, a move at a time, with its parts."),
    ("explorations.html", "walk", "Explorations", "Words to take apart and build: note, notate, notation; contractions; write, wrote, written."),
    ("contractions.html", "walk", "Squeezed into oblivion", "Contractions: the vowel squeezed out, the apostrophe in its place: the apostrophe catastrophe."),
    ("ablaut.html", "walk", "What's that ablaut?", "write, wrote, written: the vowel changes to mark time, and the spelling around it does its usual jobs."),
    ("parts.html", "parts", "Parts", "Prefixes, suffixes, roots and joins, each with every word that has it."),
    ("roots/leg.html", "parts", "*leg-: to gather", "The first root family: Greek and Latin words for gathering, choosing, reading and saying."),
    ("roots/deuk.html", "parts", "*deuk-: to lead", "A root family: produce, reduce, conduct, educate, duke and tug, with a lesson on stress."),
    ("roots/sem.html", "parts", "*sem-: one, same", "A root family: similar, simple, assemble and same, with a lesson on doubles at the front of a word."),
    ("roots/med.html", "parts", "*med-: to measure", "A root family: mode, model, modern, medicine, must and accommodate."),
    ("roots/leuk.html", "parts", "*leuk-: light", "A root family: illustrate, illuminate, lucid, lunar, light and lynx."),
    ("roots/hap.html", "parts", "hap: chance, luck", "A base family: happy, happen, mishap and haphazard, and why happy has two p's and mishap one."),
    ("derivations.html", "parts", "Roots and their sources", "Where words come from, and the sources the roots cite."),
    ("teachers.html", "teachers", "For teachers", "To print and present, connections to programs, and the reasons and sources."),
    ("constructions.html", "walk", "Sentences", "How sentences are built, and the flip from claim to question."),
    ("instructions.html", "teachers", "To print and present", "Presentations, word cards and affix tent cards."),
    ("presentations.html", "teachers", "Presentations", "The staff series and decks on single concepts, with their handouts."),
    ("tents.html", "teachers", "Affix tent cards", "Prefixes, roots and suffixes on cards that stand up: swap the root, keep the affixes. Extension work with the families."),
    ("cards.html", "teachers", "Word cards", "Printable cards: the Early Literacy Profile (Central Okanagan) and Dolch words, and grade 3 word sums."),
    ("connections.html", "teachers", "Programs and word lists", "How the route lines up with the word lists and programs schools already use."),
    ("word-lists.html", "teachers", "Early Literacy Profile and Dolch", "Where the Early Literacy Profile (Central Okanagan) words come from in Dolch's lists."),
    ("ufli.html", "teachers", "UFLI Foundations", "For schools that run UFLI: where its lessons meet the route, the mark to draw alongside each part of UFLI, and why the two orders differ."),
    ("explanations.html", "teachers", "Reasons and sources", "Definitions, the notation and its name, and credits."),
    ("definitions.html", "teachers", "Definitions", "What the notation's words mean, and where they come from."),
    ("about.html", "teachers", "About the notation", "The notation, its name, and how it came about."),
    ("credits.html", "teachers", "Credits and contact", "The writers the notation draws on, and how to get in touch."),
    ("sitemap.html", None, "Site map", "Every page, layer by layer."),
]
import lists as _lists
PAGES[-1:-1] = _lists.PAGES                 # the spelling lists, on the teachers' shelf
# The page each shelf page sits behind, for its breadcrumb: the four teachers' doors (13 November 2026).
SHELF_PARENT = {"ufli.html": "connections.html", "word-lists.html": "connections.html",
                "presentations.html": "instructions.html", "cards.html": "instructions.html", "tents.html": "instructions.html",
                "definitions.html": "explanations.html", "about.html": "explanations.html", "credits.html": "explanations.html"}
WORDS_PARENT = {"contractions.html": "explorations.html", "ablaut.html": "explorations.html"}
# Pages on the teachers' shelf that the board view still shows.
BOARD_OK = {"constructions.html"}
TEACHERS = {s for s, *_, w in DOORS if w is None}
NUMBER = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


def tree(STEPS, plain):
    steps = [(f"steps/{s['n']:02d}.html", "progressions", f"Step {s['n']}: {plain(s['title'])}", f"The words of step {s['n']}, marked.")
             for s in STEPS]
    i = next(k for k, p in enumerate(PAGES) if p[0] == "progressions.html")
    return PAGES[:i + 1] + steps + PAGES[i + 1:]


# ------------------------------------------------------------------ the header's pieces
VIEW_HEAD = ("<script>(() => { const r = document.documentElement; let v = null;"
             " try { v = new URLSearchParams(location.search).get('view'); if (v === 'board') v = 'student'; if (v === 'details') v = 'teacher'; } catch (e) {}"
             " try { if (v === 'student' || v === 'teacher') localStorage.setItem('view', v); else v = localStorage.getItem('view'); } catch (e) {}"
             " if (v === 'student') r.dataset.view = 'student'; })();</script>")

VIEW_SWITCH = ('<div class="view" role="group" aria-label="View" hidden>'
               '<button type="button" data-v="teacher">Details</button><button type="button" data-v="student">Board</button></div>')


def header_parts(up):
    """The search box, the site map link, the view switch, the menu button and the doors, for header()."""
    search = (f'<div class="search" data-up="{up}" role="search" hidden><label class="sr" for="q">Search the site</label>'
              f'<input id="q" type="search" placeholder="Search words, steps, marks" autocomplete="off" spellcheck="false" '
              f'aria-describedby="q-count"><span class="sr" id="q-count" aria-live="polite"></span><div class="results" hidden></div></div>')
    smap = f'<a class="smap" href="{up}sitemap.html">Site map</a>'
    menu = '<button class="menu" type="button" aria-expanded="false" aria-controls="doors" hidden>Menu</button>'
    links = "".join(f'<a class="door{" t-only" if sw is None else ""}" href="{up}{slug}.html" data-door="{slug}">'
                    f'<span class="dn">{name}</span>{f"<span class=sn>{sw}</span>" if sw else ""}</a>' for slug, name, _, _, sw in DOORS)
    doors = f'<nav class="doors" id="doors" aria-label="Doors">{links}</nav>'
    return search, smap, VIEW_SWITCH, menu, doors


VIEW_JS = """<script>(() => {
  const root = document.documentElement, sw = document.querySelector('.view');
  if (!sw) return;
  const now = () => root.dataset.view === 'student' ? 'student' : 'teacher';
  const show = () => sw.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === now())));
  sw.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.v === 'student') root.dataset.view = 'student'; else delete root.dataset.view;
    try { localStorage.setItem('view', b.dataset.v); } catch (err) {}
    show();
  });
  sw.hidden = false; show();
})();</script>"""

# On a narrow screen the doors fold into one Menu button. Without script they stay open.
MENU_JS = """<script>(() => {
  const head = document.querySelector('header.site'), b = head && head.querySelector('.menu');
  if (!b) return;
  document.documentElement.classList.add('js-menu'); b.hidden = false;
  b.addEventListener('click', () => { const open = head.classList.toggle('open'); b.setAttribute('aria-expanded', String(open)); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && head.classList.contains('open')) { head.classList.remove('open'); b.setAttribute('aria-expanded', 'false'); b.focus(); } });
})();</script>"""

# Scrolled past, the header pins to the top in a compact form: the logo, the breadcrumb trail, search and Menu. On the
# board too, since 11 November 2026, though the trail stays hidden there. head-hold keeps the header's height while
# it's pinned, so nothing on the page moves.
PIN_JS = """<script>(() => {
  const head = document.querySelector('header.site'), hold = head && head.parentElement, root = document.documentElement;
  if (!head || !hold.classList.contains('head-hold')) return;
  let pinned = false, H = 0;
  const set = on => {
    if (on === pinned) return; pinned = on;
    if (on) { H = head.offsetHeight; hold.style.height = H + 'px'; head.classList.add('pinned'); }
    else { head.classList.remove('pinned', 'open'); hold.style.height = '';
      const m = head.querySelector('.menu'); if (m) m.setAttribute('aria-expanded', 'false'); }
  };
  // pin once the header has gone; unpin only once there's room for it again, so it can't flicker at the line
  const check = () => set(pinned ? scrollY > H - head.offsetHeight : scrollY > head.offsetHeight);
  let ticking = false;
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; check(); }); } }, {passive: true});
  // a phone's address bar showing and hiding is a resize too: only a change of width means the header needs measuring
  let W = innerWidth;
  addEventListener('resize', () => { if (innerWidth === W) return; W = innerWidth; set(false); check(); });
  new MutationObserver(() => { set(false); check(); }).observe(root, {attributes: true, attributeFilter: ['data-view']});   // the board's header is a different height
  check();
})();</script>"""

SEARCH_JS = """<script>(() => {
  const box = document.querySelector('.search');
  if (!box || !window.fetch) return;
  const up = box.dataset.up || '', q = box.querySelector('input'), out = box.querySelector('.results'), count = box.querySelector('#q-count');
  box.hidden = false; document.documentElement.classList.add('js-search');
  let data = null, loading = null;
  const load = () => loading || (loading = fetch(up + 'search.json').then(r => r.json()).then(j => { data = j; render(); }).catch(() => { data = []; }));
  const KINDS = [['word', 'Words'], ['part', 'Parts'], ['step', 'Steps'], ['mark', 'Marks'], ['term', 'Terms'], ['page', 'Pages']], CAP = 6;
  const norm = s => s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/[’']/g, '');
  const esc = s => s.replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const student = () => document.documentElement.dataset.view === 'student';
  function render() {
    const said = q.value.trim(), t = norm(said);
    if (!t) { out.hidden = true; out.innerHTML = ''; count.textContent = ''; return; }
    if (!data) { load(); return; }
    // several words are also looked up one at a time, in the order typed: she could go
    const terms = [...new Set(t.split(/[^a-z0-9-]+/).filter(Boolean))], many = terms.length > 1;
    const hits = {}, found = new Set();
    for (const r of data) {
      if (r.x && student()) continue;
      const l = norm(r.l), k = r.k ? norm(r.k) : '';
      let s = l === t ? 0 : l.startsWith(t) ? 1 : l.includes(t) ? 2 : (' ' + k).includes(' ' + t) ? 3 : k.includes(t) ? 4 : -1;
      if (many && r.t === 'word' && terms.includes(l)) { s = 0.5 + terms.indexOf(l) / 1000; found.add(l); }
      else if (s < 0 && many && terms.every(w => (l + ' ' + k).includes(w))) s = 5;   // every word typed, in any order: short vowel
      if (s >= 0) (hits[r.t] = hits[r.t] || []).push([s, r]);
    }
    let h = '', n = 0;
    for (const [kind, label] of KINDS) {
      const list = (hits[kind] || []).sort((a, b) => a[0] - b[0] || a[1].l.length - b[1].l.length || a[1].l.localeCompare(b[1].l));
      if (!list.length) continue;
      const more = list.length > CAP;
      h += '<p class="rk">' + label + (more ? ' (' + list.length + ')' : '') + '</p><ul>'
         + list.map(([, r], i) => '<li' + (i >= CAP ? ' hidden' : '') + '><a href="' + esc(up + r.u) + '">' + esc(r.l) + (r.s ? '<span>' + esc(r.s) + '</span>' : '') + '</a></li>').join('')
         + '</ul>' + (more ? '<button type="button" class="more">Show all ' + list.length + '</button>' : '');
      n += list.length;
    }
    const missing = many && found.size ? terms.filter(w => !found.has(w) && (w.length > 1 || w === 'a' || w === 'i')) : [];
    if (n && missing.length) h += '<p class="rk none">Not on the site yet: ' + missing.map(esc).join(', ') + '</p>';
    out.innerHTML = n ? h : '<p class="rk none">Nothing found for \\u201c' + esc(said) + '\\u201d. The <a href="' + up + 'sitemap.html">site map</a> lists every page.</p>';
    out.hidden = false;
    count.textContent = n ? n + (n === 1 ? ' result' : ' results') : 'No results';
  }
  const links = () => [...out.querySelectorAll('a, button.more')].filter(e => !e.hidden && !e.closest('[hidden]'));
  const close = () => { out.hidden = true; };
  out.addEventListener('click', e => {             // Show all: the rest of that group, and focus on the first of them
    const b = e.target.closest('button.more'); if (!b) return;
    const ul = b.previousElementSibling, first = ul.querySelector('li[hidden] a');
    ul.querySelectorAll('li[hidden]').forEach(li => { li.hidden = false; });
    b.hidden = true; if (first) first.focus();
  });
  q.addEventListener('focus', load);
  q.addEventListener('input', render);
  q.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown') { const a = links()[0]; if (a) { e.preventDefault(); a.focus(); } }
    else if (e.key === 'Escape') { q.value = ''; render(); }
    else if (e.key === 'Enter') { const a = out.querySelector('a'); if (a && !out.hidden) { e.preventDefault(); location.href = a.href; } }
  });
  out.addEventListener('keydown', e => {
    const ls = links(), i = ls.indexOf(document.activeElement);
    if (e.key === 'ArrowDown' && i < ls.length - 1) { e.preventDefault(); ls[i + 1].focus(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); (i > 0 ? ls[i - 1] : q).focus(); }
    else if (e.key === 'Escape') { close(); q.focus(); }
  });
  document.addEventListener('click', e => { if (!box.contains(e.target)) close(); });
  q.addEventListener('focus', () => { if (q.value.trim()) render(); });
})();</script>"""


# ------------------------------------------------------------------ the pages
def door_head(slug, extra=""):
    name, plain_words, sw = HEADS[slug]
    student = f'<h1 class="s-only">{sw}</h1>' if sw else ""
    board = '<p class="board t-only"><a href="?view=board">Open this page on the board</a>: the words big, the notes hidden.</p>' if sw else ""
    return (f'<section class="hero door-hero"><div class="wrap">'
            f'<h1 class="t-only">{name}</h1>{student}'
            f'<p class="lead t-only">{plain_words}</p>{extra}{board}'
            f'</div></section>')


def write(OUT, page, header, footer, X):
    """The door pages and the site map. X carries what they need from build_site: the route, the legend, the
    drawing tools and the helpers."""
    uc, md = X["uc"], X["md"]

    def door_page(slug, title, desc, inner):
        body = f"""{header(0)}
<main class="door-page">
{inner}
</main>
{footer(0)}"""
        (OUT / f"{slug}.html").write_text(page(title, body, 0, desc), encoding="utf-8")

    # Progressions: the route, moved from the home page.
    door_page("progressions", "Progressions · A Legend for English Words", "The legomorphic route through English spelling, step by step.", f"""{door_head("progressions")}
<section class="route" id="route" aria-labelledby="route-h"><div class="wrap">
<h2 id="route-h" class="t-only">The legomorphic route at a glance</h2>
<p class="lead t-only">{X["route_lead"]} Open a step to see its words marked, the marks it brings in, and the pages in Carney's survey that back it.</p>
<p class="sub t-only">Each word is shown with its letters in colour: red for vowel letters, green for <em>sh</em>, <em>th</em> and <em>ch</em>, black for the rest.</p>
<div class="door-tiles route-tiles"><a class="dtile" href="letters.html"><b>Before step 1: letters</b><span class="t-only">Letters, names and sounds: the alphabet in the song&rsquo;s units, with a sound circle under each letter.</span></a><a class="dtile" href="notations.html"><b>The marks</b><span class="t-only">The twelve marks, each drawn alone on one word.</span></a></div>
{X["bands_html"]}
{uc(X["draft_note"])}
</div></section>""")

    import letters                                        # the alphabet before step 1 (13 November 2026)
    letters.write(door_page, door_head)

    # Notations: the legend, moved from the home page.
    note_word = X["svg_of"]("notation", 58, label="notation, marked")
    door_page("notations", "Notations · A Legend for English Words", "The marks of Legomorphic Notation, each drawn alone on one word.", f"""{door_head("notations", f'<div class="door-word">{note_word}</div>')}
<section class="marks" id="marks" aria-labelledby="marks-h"><div class="wrap">
<h2 id="marks-h">Reading the marks</h2>
<p class="sub t-only">Twelve marks, each drawn alone on one word. A step page shows a word with all its marks at once, and <a href="definitions.html#marks">Definitions</a> says where each name comes from.</p>
<div class="key">{X["key_html"]}</div>
{uc("next, a page for each mark, with its rule, the contrasts that teach it, and an animation of the mark at work.")}
</div></section>""")

    # Explorations: the first family on the site, note to notation; hop and hope come next.
    LW, svg_of = X["LW"], X["svg_of"]
    fam = "".join(f'<figure class="word" id="{word_id(w)}">{svg_of(w, 58, label=f"{w}, marked")}<figcaption><span class="ws">{s}</span><span class="t-only">{c}</span></figcaption></figure>'
                  for w, s, c in X["morph"])
    door_page("explorations", "Explorations · A Legend for English Words", "Words to take apart and build: families and contrasts.", f"""{door_head("explorations")}
<section class="about"><div class="wrap"><div class="door-tiles"><a class="dtile" href="#note-family"><b>A family: <i>note</i>, <i>notate</i>, <i>notation</i></b><span class="t-only">A word built in three moves, each from the one before.</span></a><a class="dtile" href="contractions.html"><b>Squeezed into oblivion</b><span class="t-only">Contractions: the vowel squeezed out and the apostrophe in its place.</span></a><a class="dtile" href="ablaut.html"><b>What&rsquo;s that ablaut?</b><span class="t-only"><i>write</i>, <i>wrote</i>, <i>written</i>: the vowel changes to mark time, and the spelling around it does its usual jobs.</span></a></div></div></section>
<section class="about" id="note-family" aria-labelledby="nf-h"><div class="wrap">
<h2 id="nf-h">A family: <i>note</i>, <i>notate</i>, <i>notation</i></h2>
<p class="sub t-only">Each word is built from the one before it. At each seam the <i>e</i> drops, and its job, making the <i>o</i> spell its name, passes to the next vowel.</p>
<div class="words fam">{fam}</div>
</div></section>
<section class="about" aria-labelledby="next-h"><div class="wrap">
<h2 id="next-h" class="t-only">Coming next</h2>
{uc("next, the first contrast, <i>hop</i> and <i>hope</i>, built in full: their families marked, cards to print, a presentation for teachers and an exercise for students. Then more families and contrasts, and a page for every word.")}
<p class="t-only">For word sums now, the <a href="cards.html#word-sums">grade 3 word sum cards</a> take high-frequency words apart at their seams.</p>
<p class="s-only s-soon">More words to take apart are coming soon.</p>
<p><a href="parts.html">Every word that&rsquo;s taken apart, by its parts</a>.</p>
</div></section>""")

    import ablaut, contractions
    X["ablaut_words"] = ablaut.write(OUT, door_page, X) + contractions.write(OUT, door_page, X)

    # Constructions: the Dialogue Team and the sentence cards.
    import characters, sessions
    team = characters.team(LW)
    hand = []
    for d in sessions.DECKS:
        for name, title, what in d.get("handouts", []):
            if any(k in name for k in ("operator", "modal", "sentence", "verb", "action", "actor")) and (OUT / "sessions" / "handouts" / f"{name}.pdf").exists():
                hand.append(f'<li><a href="sessions/handouts/{name}.pdf">{html.escape(title)}</a><span class="what">{what}</span></li>')
    hands = f'<ul class="handouts">{"".join(hand)}</ul>' if hand else ""
    import builder                                        # build a sentence (13 November 2026)
    sb = builder.section(X, lambda w: LW.W.get(w) or X["auto_codes"].get(w))
    door_page("constructions", "Constructions · A Legend for English Words", "How sentences are built, and the flip from claim to question.", f"""{door_head("constructions")}
{sb}
<section class="about" id="flip" aria-labelledby="flip-h"><div class="wrap">
<h2 id="flip-h">From a claim to a question</h2>
<p class="sub t-only">An actor, an operator and an action make a claim. When the operator moves to the front, the claim becomes a question. The Dialogue Team acts it out with their faces: their words with the letters lifted out.</p>
{team}
</div></section>
<section class="about t-only" id="sentence-cards" aria-labelledby="sc-h"><div class="wrap">
<h2 id="sc-h">Cards for building sentences</h2>
<p class="sub">From the first session of the staff series, on <a href="presentations.html">Presentations</a>. Print them in colour on card stock.</p>
{hands}
{uc("next, each sentence pattern as a concept of its own, with cards, a presentation for teachers and an exercise for students.")}
</div></section>""")

    # Derivations: the plan for the roots, and what's here now.
    import roots
    X["roots"] = roots.write(OUT, page, header, footer, X)
    door_page("derivations", "Derivations · A Legend for English Words", "Where words come from, and the sources the roots will cite.", f"""{door_head("derivations")}
<section class="about"><div class="wrap"><div class="door-tiles"><a class="dtile" href="roots/leg.html"><b>*leg-<span class="t-only">: to gather</span></b><span class="t-only">The first root family: <i>logic</i>, <i>collect</i>, <i>legend</i>, <i>lesson</i>, <i>loyal</i>, and the notation&rsquo;s own name.</span><span class="s-only">gather</span></a><a class="dtile" href="roots/hap.html"><b>hap<span class="t-only">: chance, luck</span></b><span class="t-only">A base family: <i>happy</i>, <i>happen</i>, <i>mishap</i>, <i>hapless</i>, <i>haphazard</i>, <i>perhaps</i>, and why <i>happy</i> has two p&rsquo;s.</span><span class="s-only">luck</span></a></div></div></section>
<section class="about t-only" aria-labelledby="dv-h"><div class="wrap prose">
<h2 id="dv-h">Roots, and the meanings of parts</h2>
<p>A word can be read as it is used now, or traced back through time: <a href="definitions.html#study">synchronic and diachronic</a>, a snapshot and a time-lapse. This page is for the time-lapse. <i>Before</i> is an example: Old English <i>beforan</i>, from <i>be-</i> &lsquo;by&rsquo; and <i>foran</i> &lsquo;in front&rsquo;, and <i>for</i> and <i>fore</i> grow from the same root.</p>
<p>The roots will follow Calvert Watkins&rsquo;s <i>American Heritage Dictionary of Indo-European Roots</i> (3rd ed., 2011), which is built root first and lists the English words from each root, with links to the <a href="https://lrc.la.utexas.edu/lex">Indo-European Lexicon</a> of the Linguistics Research Center at the University of Texas at Austin. Not every word has a known root. <i>Hop</i> and <i>hope</i> go back through Old English to early Germanic, and no further that anyone can show, and their pages will say so.</p>
{uc("next, a root page for every root behind the route's words, each citing its source, and a plain meaning for every part of a word.")}
</div></section>""")

    # Instructions and Explanations: teachers' doors, leading to the pages that are already here.
    def tiles(items):
        return '<div class="door-tiles">' + "".join(
            f'<a class="dtile" href="{p}"><b>{t}</b><span>{s}</span></a>' for p, t, s in items) + "</div>"
    pick = lambda door: [(p, t, s) for p, d, t, s in PAGES if d == door and p != f"{door}.html"]
    door_page("instructions", "To print and present · A Legend for English Words", "Presentations, word cards and affix tent cards.", f"""{door_head("instructions")}
<section class="about"><div class="wrap">
{tiles([x for x in pick("teachers") if x[0] in ("presentations.html", "cards.html", "tents.html")])}
{uc("next, the routines: the learning loop, marking a word by hand, flips from claim to question, and word sums at the seam.")}
</div></section>""")
    door_page("explanations", "Reasons and sources · A Legend for English Words", "Definitions, the notation and its name, and credits.", f"""{door_head("explanations")}
<section class="about"><div class="wrap">
{tiles([x for x in pick("teachers") if x[0] in ("definitions.html", "about.html", "credits.html")])}
{uc("next, pages of ideas: the primary terms from phone to sememe, grapheme two ways, why English spells the way it does, and what the name claims.")}
</div></section>""")

    # The teachers' shelf: everything a teacher prints, presents or checks, on one page.
    import lists
    lists.write(OUT, page, header, footer, X)
    import tents
    tents.write(OUT, page, header, footer, X)
    # Four doors, never more (ruled 13 November 2026): each opens on a page of three or four.
    shelf = [("lists/index.html", "Spelling", "Spelling lists by step and by family, words with a heart, words spelled apart, and lists for UFLI lessons."),
             ("connections.html", "Programs and word lists", "UFLI Foundations lesson by lesson, and the Early Literacy Profile (Central Okanagan) and Dolch lists."),
             ("instructions.html", "To print and present", "Presentations, word cards and affix tent cards."),
             ("explanations.html", "Reasons and sources", "About the notation, definitions, and credits.")]
    door_page("teachers", "For teachers · A Legend for English Words", DOOR["teachers"][3], f"""{door_head("teachers")}
<section class="about"><div class="wrap">{tiles(shelf)}</div></section>""")

    # The Parts layer (parts.py), then the Words layer (walk.py), which shows each word's sum.
    import parts
    X["parts"] = parts.write(OUT, door_page, X)
    import walk
    X["walk"] = walk.write(OUT, door_page, X)

    # Connections: the crosswalks (connections.py).
    import connections
    connections.write(OUT, door_page, door_head, uc, X)

    # The site map: the tree, written out.
    items = []
    for slug, name, _, plain_words, sw in DOORS:
        sub = [(p, t_, s) for p, d, t_, s in X["pages"] if d == slug and p != f"{slug}.html" and not p.startswith("steps/") and (not p.startswith("lists/") or p == "lists/index.html")]
        kids = "".join(f'<li><a href="{p}">{t_}</a> <span>{html.escape(s)}</span></li>' for p, t_, s in sub)
        steps = "".join(f'<li><a href="steps/{s["n"]:02d}.html">Step {s["n"]}: {md(s["title"])}</a></li>' for s in X["STEPS"]) if slug == "progressions" else ""
        items.append(f'<li{" class=t-only" if sw is None else ""}><a href="{slug}.html"><b>{name}</b></a> <span>{plain_words}</span>'
                     + (f'<ol class="kids">{steps}</ol>' if steps else "") + (f'<ul class="kids">{kids}</ul>' if kids else "") + "</li>")
    door_page("sitemap", "Site map · A Legend for English Words", "Every page of A Legend for English Words, layer by layer.", f"""<section class="hero"><div class="wrap">
<h1>Site map</h1>
<p class="lead">Every page. Three layers hold the site: the steps in order, the words one at a time, and the parts words are built from. The rest is on the teachers&rsquo; shelf.</p>
</div></section>
<section class="about"><div class="wrap"><ul class="smap-tree"><li><a href="index.html"><b>Home</b></a></li>{"".join(items)}</ul></div></section>""")


def doors_section():
    """The way in on the home page: the three layers, then the teachers' shelf."""
    out = []
    for n, (slug, name, _, plain_words, sw) in enumerate(DOORS, 1):
        num = f'<span class="ln">{n}</span>' if sw else ""
        out.append(f'<a class="door-tile{" t-only shelf" if sw is None else ""}" href="{slug}.html">{num}<span class="dn">{name}</span>{f"<span class=sn>{sw}</span>" if sw else ""}'
                   f'<span class="pw t-only">{plain_words}</span></a>')
    return f"""<section class="doors-home" id="doors-home" aria-labelledby="doors-h"><div class="wrap">
<h2 id="doors-h"><span class="t-only">Three layers</span><span class="s-only">Pick one</span></h2>
<p class="sub t-only">Legomorphic Notation is a language for teaching spelling and reading, for a teacher to use with learners. Learn it in order in Steps, look up any word in Words, and see what words share in Parts.</p>
<div class="door-grid">{"".join(out)}</div>
</div></section>"""


# ------------------------------------------------------------------ search
def write_search(OUT, X):
    recs, seen = [], set()
    def add(t, l, u, s="", k="", teacher=False):
        key = (t, l.lower(), u)
        if key in seen: return
        seen.add(key)
        r = {"t": t, "l": l, "u": u}
        if s: r["s"] = s
        if k: r["k"] = k
        if teacher: r["x"] = 1
        recs.append(r)
    strip = lambda s: re.sub(r"<[^>]+>", "", html.unescape(s))
    # words on the route, at the first step that has them
    where = {}
    for st in X["STEPS"]:
        for g in X["groups_of"](st["words_md"]):
            for w in g: where.setdefault(w, []).append(st["n"])
    for w, ns in sorted(where.items()):
        add("word", w, f"steps/{ns[0]:02d}.html#{word_id(w)}", "Step " + ", ".join(str(n) for n in ns[:3]) + ("…" if len(ns) > 3 else ""))
    for st in X["STEPS"]:                    # contrast words that are on no step's own list
        for item in (st.get("contrast_md") or "").replace("*", "").split(","):
            for w in (x.strip() for x in item.split("/")):
                if w and w not in where: add("word", w, f"steps/{st['n']:02d}.html", f"Step {st['n']}, contrast")
    # Words on the lists but not the route land on their place in the word lists' table, which holds every ELP word and
    # Dolch's 220, or, for Dolch's nouns, on the coded side of their card in the noun set: ten cards a sheet, each sheet a
    # plain page and then its coded page (build_dolch_cards.py)
    elp_of, dolch_of = {}, {w: "Dolch " + l["name"].lower() for l in X["dolch"]["levels"] for w in l["words"]}
    for n, L in X["elp"]["lists"].items():
        for w in L["words"]: elp_of.setdefault(w, f"ELP list {n}")
    nouns = X["dolch"]["nouns"]
    from pypdf import PdfReader
    cards = OUT / "cards" / "dolch-word-cards-nouns.pdf"
    assert len(PdfReader(str(cards)).pages) == 2 * -(-len(nouns) // 10), "the noun cards' pages have changed"
    for w in sorted(X["list_words"]):
        if w in where: continue
        if w in elp_of or w in dolch_of:
            add("word", w, f"word-lists.html#{word_id(w)}", ", ".join(x for x in (elp_of.get(w), dolch_of.get(w)) if x), teacher=True)
        else:
            add("word", w, f"cards/dolch-word-cards-nouns.pdf#page={2 * (nouns.index(w) // 10) + 2}", "Dolch noun, word cards", teacher=True)
    for w, *_ in X["morph"]:   # the family on Explorations
        if w not in where: add("word", w, f"explorations.html#{word_id(w)}", "Explorations")
    for w, u, label in X.get("roots", []):   # the families' words
        if w not in where: add("word", w, u, label)
    P = X.get("parts")
    if P:
        for w, d in P["sums"].items():           # every other analysed word: its walk if it's marked, else its place in Parts
            if P["marked"](w): add("word", w, "walk.html?w=" + w, "Words")
        seen_words = {r["l"] for r in recs if r["t"] == "word"}
        for w in X.get("auto_codes", {}):        # words marked by rule (auto_mark.py): their walk
            if w not in seen_words: add("word", w, "walk.html?w=" + w, "Words, marked by rule")
        for k, u, s in P["search"]: add("part", k, u, s)
    for st in X["STEPS"]:
        words = " ".join(w for g in X["groups_of"](st["words_md"]) for w in g)
        add("step", f"Step {st['n']}: {X['plain'](st['title'])}", f"steps/{st['n']:02d}.html", st["band"],
            k=words + " " + X["plain"](st.get("marks", "")) + " " + X["plain"](st.get("contrast_md", "") or ""))
    for name, what, w, m in X["KEY"]:
        add("mark", name, "notations.html#" + mark_id(name), f"drawn on {w}", k=strip(what))
    for term, anchor in X["terms"]:
        add("term", term, "definitions.html#" + anchor, "Definitions", teacher=True)
    for p, d, t, s in X["pages"]:
        if p.startswith("steps/"): continue
        add("page", t, p, DOOR[d][1] if d and p != f"{d}.html" else "", k=s, teacher=d in TEACHERS and p not in BOARD_OK)
    (OUT / "search.json").write_text(json.dumps(recs, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return len(recs)


def mark_id(name): return "mark-" + re.sub(r"[^a-z]+", "-", name.lower()).strip("-")


def word_id(w):
    """The id a word's figure or entry carries, so a search lands on the word itself: w-dont for don't, w-i for I."""
    return "w-" + re.sub(r"[^a-z0-9]+", "-", w.lower().replace("’", "").replace("'", "")).strip("-")


# ------------------------------------------------------------------ breadcrumbs, the current door, and teachers' pages
def door_label(d):
    """A door's name, with its short word beside it for student view (a teachers' door has none)."""
    return DOOR[d][1]


def finish(OUT, pages):
    """Every page built: put its breadcrumb where header() left <!--crumbs-->, mark its door as the current one, and
    tell a student who lands on a teachers' page that it's for teachers."""
    done = 0
    for p, d, t, s in pages:
        f = OUT / p
        if not f.exists(): continue
        src = f.read_text(encoding="utf-8")
        if "<!--crumbs-->" not in src: continue
        up = "../" * p.count("/")
        trail = []
        if p != "index.html":
            trail.append(f'<li><a href="{up}index.html">Home</a></li>')
            if d and p != f"{d}.html":
                trail.append(f'<li><a href="{up}{d}.html">{door_label(d)}</a></li>')
            if p in SHELF_PARENT:                                  # a page behind one of the four teachers' doors
                pp = SHELF_PARENT[p]; pt = next(t2 for p2, _, t2, _ in pages if p2 == pp)
                trail.append(f'<li><a href="{up}{pp}">{html.escape(pt)}</a></li>')
            elif p in WORDS_PARENT:
                trail.append(f'<li><a href="{up}{WORDS_PARENT[p]}">Explorations</a></li>')
            if p.startswith("lists/ufli-"):
                trail.append(f'<li><a href="{up}connections.html">Programs and word lists</a></li><li><a href="{up}ufli.html">UFLI Foundations</a></li>')
            elif p.startswith("lists/") and p != "lists/index.html":
                trail.append(f'<li><a href="{up}lists/index.html">Legomorphic spelling</a></li>')
            here = door_label(d) if d and p == f"{d}.html" else html.escape(t.split(":")[0] if p.startswith("steps/") else t)
            if p.startswith("lists/") and t.startswith("Spelling list: "):
                here = t[len("Spelling list: "):].split(":")[0]
            if p.startswith("lists/") and p.endswith("-check.html"):
                lt = next((t2 for p2, _, t2, _ in pages if p2 == p[:-11] + ".html"), "")
                trail.append(f'<li><a href="{up}{p[:-11]}.html">{lt[len("Spelling list: "):].split(":")[0]}</a></li>')
                here = "Check"
            trail.append(f'<li aria-current="page">{here}</li>')
        crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(trail)}</ol></nav>' if trail else ""
        notice = ""
        if d in TEACHERS and p not in BOARD_OK:
            notice = (f'<div class="for-teachers s-only"><div class="wrap"><p>This page is all details, so the board has nothing to show. To read it, pick Details at the top '
                       f'of the page, or go <a href="{up}index.html">back to the start</a>.</p></div></div>')
        src = src.replace("<!--crumbs-->", crumbs, 1).replace("<!--after-head-->", notice, 1)
        if d:
            src = src.replace(f'data-door="{d}">', f'data-door="{d}" aria-current="{"page" if p == f"{d}.html" else "true"}">', 1)
        f.write_text(src, encoding="utf-8")
        done += 1
    return done
