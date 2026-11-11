"""The word walk (walk.html), made 8 November 2026: type a word that is marked on the site, then tap through it.

Two walks over the same drawing, each bringing in the marks a step at a time:
- Read it starts from the graphemes (the letters, and the bars where letters work together), then decodes: a circle for
  each sound, the vowel marks, the jobs letters do for one another, the syllables, and the parts that carry meaning.
- Spell it starts from the syllables (a band stands in for the letters while only sounds show), then the sounds, then the
  graphemes that spell them, then the marks.

The words are every marked word on the route, the ELP and Dolch lists (nouns too) and the word families. Each is drawn
here once with legomorphic_words.py's layer classes (nz1 to nz9, and the wt band) and saved as docs/walk/<id>.json, which
the page fetches when the word is asked for; docs/walk/index.json lists them. A word with two markings (read, the present
and the past) carries both. Words the site still shows in plain letters aren't in the walk until they're marked.

Any other word would need an automatic first pass from a pronunciation dictionary, which would get some words wrong, so
the walk takes only words that are marked and ruled here."""
import html, json, re, pathlib
import doors

KIND_JOBS = {"vault": "vowel vault", "blockedvault": "block box", "nudge": "nice-nudge", "cone": "cone of silence", "block": "block box"}
PAIRS = {"Santa Claus": ("Santa", "Claus")}
HYPHENED = {"good-bye": ("good", "bye")}


def drawn(LW, word, F=80.0):
    """(markup, width, height) with layer classes; swoops and vaults get pathLength so the page can draw them in."""
    parts = PAIRS.get(word) or HYPHENED.get(word)
    if parts:
        g1, w1, H = LW.svg_word(parts[0], F, 0.0, cls=True)
        g2, w2, _ = LW.svg_word(parts[1], F, w1, cls=True)
        y = 1.44 * F - 0.28 * F
        hy = (f'<line class="nz5" x1="{w1 - 0.12 * F:.1f}" y1="{y:.1f}" x2="{w1 + 0.12 * F:.1f}" y2="{y:.1f}" stroke="var(--ink)" '
              f'stroke-width="{0.07 * F:.1f}" stroke-linecap="round"/>') if word in HYPHENED else ""
        g, w = g1 + hy + g2, w1 + w2
    else:
        g, w, H = LW.svg_word(word, F, 0.0, cls=True)
    for layer in ("3", "8"):
        g = g.replace(f'<path class="nz{layer}"', f'<path pathLength="1" class="nz{layer} dr"')
    return g, w, H


def facts(LW, word):
    """What the captions name: the units, the bars, the sounds, the syllables, the vowel marks, the jobs and the parts."""
    words = PAIRS.get(word) or HYPHENED.get(word) or (word,)
    out = {"units": [], "bars": [], "sounds": 0, "sylls": [], "short": [], "long": [], "jobs": [], "parts": []}
    for w in words:
        p = LW.parse(w)
        L = [l["ch"] for l in p["letters"]]
        out["units"] += [u["text"] for u in p["units"]]
        out["bars"] += [u["text"] for u in p["units"] if u["kind"] in ("k", "q", "g", "t", "r", "le") or (u["kind"] == "x" and len(u["text"]) > 1)]
        out["sounds"] += p["sounds"]
        out["sylls"] += ["".join(L[a:b + 1]) for a, b in p["syllables"]]
        out["short"] += [L[m["col"]] for m in p["marks"] if m["type"] == "breve"]
        out["long"] += [L[m["col"]] for m in p["marks"] if m["type"] == "macron"]
        for m in p["marks"]:
            t = m["type"]
            if t == "vault" and m.get("cone", True): jobs = ["cone of silence", "vowel vault"]
            elif t in KIND_JOBS: jobs = [KIND_JOBS[t]]
            else: jobs = []
            for j in jobs:
                if j not in out["jobs"]: out["jobs"].append(j)
        seams = sorted(m["after"] for m in p["marks"] if m["type"] == "seam")
        cuts = [0] + [s + 1 for s in seams] + [len(L)]
        out["parts"] += ["".join(L[a:b]) for a, b in zip(cuts, cuts[1:])]
    if len(out["parts"]) == len(words): out["parts"] = [word]     # no seams: the word is one part (Santa Claus too)
    return out


def write(OUT, door_page, X):
    LW, SC, with_code = X["LW"], X["SC"], X["with_code"]
    from noun_codes import NOUN_CODES
    # every word the site shows, and where each is taught
    where = {}
    for st in X["STEPS"]:
        for g in X["groups_of"](st["words_md"]):
            for w in g:
                where.setdefault(w, []).append({"t": f"Step {st['n']}", "u": f"steps/{st['n']:02d}.html#{doors.word_id(w)}"})
    for st in X["STEPS"]:                    # the steps' contrast words, after the steps' own words
        for item in (st.get("contrast_md") or "").replace("*", "").split(","):
            for w in item.split("/"):
                w = w.strip()
                if w and not any(l["t"] == f"Step {st['n']}" for l in where.get(w, [])):
                    where.setdefault(w, []).append({"t": f"Step {st['n']}, contrast", "u": f"steps/{st['n']:02d}.html"})
    fam = {}
    for w, u, label in X.get("roots", []):   # the families behind Derivations, for their words that are drawn
        fam.setdefault(w, []).append({"t": label, "u": u})
    P = X.get("parts") or {"sums": {}}
    words = set(where) | set(X["list_words"]) | {w for w, *_ in X["morph"]} | {"legomorphic"} | {w for w in fam if w in LW.W} | set(P["sums"])
    elp = {w for L in X["elp"]["lists"].values() for w in L["words"]}
    d220 = {w for l in X["dolch"]["levels"] for w in l["words"]}
    nouns = X["dolch"]["nouns"]
    (OUT / "walk").mkdir(exist_ok=True)
    for f in (OUT / "walk").glob("*.json"): f.unlink()
    index, skipped = [], []
    for w in sorted(words, key=lambda x: (x.lower(), x)):
        sum_ = P["sums"].get(w)
        wid = doors.word_id(w)
        def sum_only():
            """A word that's taken apart but not marked yet: its sum and where its family is, with no drawing."""
            links = [{"t": sum_["home"][1], "u": sum_["home"][0]}] if sum_["home"] else []
            (OUT / "walk" / f"{wid}.json").write_text(json.dumps({"w": w, "forms": [], "where": links, "sum": sum_["parts"], "mean": sum_["mean"]}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            index.append([w, wid])
        if w in SC.UNMARKED:
            if sum_: sum_only()
            else: skipped.append(w)
            continue
        forms = SC.VARIANTS.get(w) or [(None, "")]
        undo = []
        try:
            for part in (PAIRS.get(w) or HYPHENED.get(w) or (w,)):          # the nouns' codes, only while they're drawn
                if part not in LW.W and part in NOUN_CODES: undo.append(with_code(part, NOUN_CODES[part]))
            if not all(p in LW.W for p in (PAIRS.get(w) or HYPHENED.get(w) or (w,))) and not SC.VARIANTS.get(w):
                if sum_: sum_only()
                else: skipped.append(w)
                continue
            out = []
            for code, gloss in forms:
                u2 = with_code(w, code) if code else None
                try:
                    g, wd, H = drawn(LW, w)
                    out.append({"gloss": gloss, "svg": g, "W": round(wd, 1), "H": round(H, 1), **facts(LW, w)})
                finally:
                    if u2: u2()
        finally:
            for u in reversed(undo): u()
        links = list(where.get(w, []))
        if w in elp or w in d220: links.append({"t": "Word lists", "u": f"word-lists.html#{doors.word_id(w)}", "x": 1})
        if w in nouns: links.append({"t": "Noun cards", "u": f"cards/dolch-word-cards-nouns.pdf#page={2 * (nouns.index(w) // 10) + 2}", "x": 1})
        if w in {m for m, *_ in X["morph"]}: links.append({"t": "Explorations", "u": f"explorations.html#{doors.word_id(w)}"})
        links += fam.get(w, [])
        rec = {"w": w, "forms": out, "where": links}
        if sum_: rec["sum"], rec["mean"] = sum_["parts"], sum_["mean"]
        (OUT / "walk" / f"{wid}.json").write_text(json.dumps(rec, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        index.append([w, wid])
    (OUT / "walk" / "index.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    body = f"""<section class="hero walk-hero"><div class="wrap">
<h1><span class="t-only">Words</span><span class="s-only">Pick a word</span></h1>
<p class="lead t-only">Look up a word, then tap or swipe through it. <b>Read it</b> starts from the word in plain letters and decodes; <b>Spell it</b> starts from the syllables, then the sounds, then the letters. Under the word is its sum: tap a part to see every word that shares it.</p>
</div></section>
{section(note=X["uc"]("a word is either marked, so it can be walked, or shown as a word sum only. Next: the word built from left to right, a unit at a swipe; and draft marks for more words, labelled as drafts, for teachers to check."))}
<section class="about t-only"><div class="wrap"><p><a href="explorations.html">A family built in three moves: <i>note</i>, <i>notate</i>, <i>notation</i></a>. Every analysed word, by its parts, is in <a href="parts.html">Parts</a>.</p></div></section>"""
    door_page("walk", "Words · Sound and Word Atlas", "Look up a word and walk through it: its marks, a move at a time, and its parts.", body)
    return len(index), skipped


PICKS = ("which", "make", "little", "squirrel", "notation")


def section(note="", head="", lazy=False, url=True, default="which"):
    """The walk: the word field, the try-one chips, the two walks, the stage and its controls, and the script. walk.html
    has it whole; the home page has a copy (head, lazy, and no ?w= in its address), since 9 November 2026."""
    chips = "".join(f'<button type="button" class="chip" data-w="{html.escape(w)}">{html.escape(w)}</button>' for w in PICKS)
    return f"""<section class="walk" aria-label="Word walk" data-default="{default}"{' data-lazy="1"' if lazy else ''}{' data-url="off"' if not url else ''}><div class="wrap">
{head}<div class="walk-bar">
<form class="walk-form" role="search" autocomplete="off">
<label class="sr" for="walk-q">A word</label>
<input id="walk-q" type="text" list="walk-words" placeholder="Type a word" spellcheck="false" autocapitalize="off">
<datalist id="walk-words"></datalist>
<button type="submit" class="btn">Show it</button>
</form>
<div class="walk-modes" role="group" aria-label="Walk"><button type="button" data-mode="read" aria-pressed="true">Read it</button><button type="button" data-mode="spell" aria-pressed="false">Spell it</button></div>
</div>
<div class="chips" aria-label="Try one">{chips}</div>
<div class="walk-forms" hidden></div>
<p class="walk-msg" role="status"></p>
<div class="walk-stage" tabindex="0" aria-label="The word. Tap, swipe left, or press the right arrow, for the next step."></div>
<p class="walk-cap" aria-live="polite"></p>
<div class="walk-nav"><button type="button" class="walk-back">Back</button><span class="walk-dots" aria-hidden="true"></span><button type="button" class="walk-next">Next</button><button type="button" class="walk-all">Show it all</button></div>
<p class="walk-sum"></p>
<div class="pcard walk-pop" hidden aria-live="polite"></div>
<p class="walk-where"></p>
<noscript><p>The word walk needs script. Each word is also on its step page.</p></noscript>
{note}
</div></section>
{WALK_JS}"""


WALK_JS = r"""<script>(() => {
  const root = document.querySelector('.walk'); if (!root || !window.fetch) return;
  const $ = s => root.querySelector(s);
  const form = $('.walk-form'), input = $('#walk-q'), list = $('#walk-words'), stage = $('.walk-stage'), cap = $('.walk-cap'),
        dots = $('.walk-dots'), msg = $('.walk-msg'), where = $('.walk-where'), formsBox = $('.walk-forms'), sumBox = $('.walk-sum');
  const student = () => document.documentElement.dataset.view === 'student';
  const norm = s => s.trim().toLowerCase().replace(/[’']/g, '').replace(/\s+/g, ' ');
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const it = s => '<i>' + esc(s) + '</i>';
  const and = a => a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  let index = [], word = null, form_ = 0, mode = 'read', step = 0, steps = [];
  const params = new URLSearchParams(location.search);
  if (params.get('m') === 'spell') mode = 'spell';

  function plan(f) {
    const S = [], beats = n => '<span class="t-only">' + n + (n === 1 ? ' syllable' : ' syllables') + '</span><span class="s-only">' + n + (n === 1 ? ' beat' : ' beats') + '</span>';
    const vowels = () => [f.short.length ? 'a cup for short ' + and(f.short.map(it)) : '', f.long.length ? 'a bar for long ' + and(f.long.map(it)) : ''].filter(Boolean).join('; ');
    const marks = [];
    if (f.short.length || f.long.length) marks.push({show: [6], cap: 'The vowels: ' + vowels() + '.'});
    if (f.jobs.length) marks.push({show: [7, 8], cap: 'Letters doing jobs: ' + and(f.jobs) + '.'});
    if (f.parts.length > 1) marks.push({show: [9], cap: 'The parts: ' + f.parts.map(it).join(' + ') + '.'});
    if (mode === 'read') {
      S.push({show: [5], plain: true, cap: 'The word as it’s written.'});
      S.push({show: [5, 4], cap: f.bars.length ? 'The letters. A bar joins letters that work together: ' + and(f.bars.map(it)) + '.' : 'The letters, each on its own.'});
      S.push({show: [1, 2], cap: 'A circle for each sound: ' + f.sounds + '. Red is a vowel sound.'});
      S.push(...marks.filter(m => m.show[0] !== 9));
      S.push({show: [3], cap: 'Put the sounds together: ' + beats(f.sylls.length) + ', ' + f.sylls.map(it).join(' · ') + '.'});
      S.push(...marks.filter(m => m.show[0] === 9));
    } else {
      S.push({show: [3], band: true, cap: 'Say it and count: ' + beats(f.sylls.length) + '.'});
      S.push({show: [1, 2], band: true, cap: 'Say each sound: ' + f.sounds + '. Red is a vowel sound.'});
      S.push({show: [5, 4], cap: 'Spell each sound: ' + f.units.map(it).join(' · ') + '.'});
      S.push(...marks);
    }
    return S;
  }
  function apply() {
    const shown = new Set(); let band = false;
    steps.slice(0, step + 1).forEach(s => { s.show.forEach(n => shown.add(n)); band = !!s.band; });
    stage.querySelectorAll('[class*="nz"]').forEach(el => {
      const n = +((el.getAttribute('class') || '').match(/nz(\d)/) || [])[1];
      el.classList.toggle('on', shown.has(n));
    });
    stage.classList.toggle('plain', !!(steps[step] && steps[step].plain));   // the first move: every letter in ink, no marks
    const wt = stage.querySelector('.wt'); if (wt) wt.classList.toggle('on', band && !shown.has(5));
    cap.innerHTML = steps[step] ? steps[step].cap : '';
    dots.innerHTML = steps.map((_, i) => '<i class="' + (i === step ? 'now' : i < step ? 'done' : '') + '"></i>').join('');
    $('.walk-back').disabled = step === 0; $('.walk-next').disabled = step >= steps.length - 1;
  }
  function draw() {
    if (!word) return;
    root.classList.toggle('sum-only', !word.forms.length);
    if (!word.forms.length) {      // taken apart, not marked yet: the word in plain letters
      stage.innerHTML = '<span class="walk-plain">' + esc(word.w) + '</span>'; steps = []; step = 0;
      cap.innerHTML = 'This word isn’t marked yet. Its parts are below.'; dots.innerHTML = ''; return;
    }
    const f = word.forms[form_];
    stage.innerHTML = '<svg viewBox="0 0 ' + f.W + ' ' + f.H + '" role="img" aria-label="' + esc(word.w) + ', marked">' + f.svg + '</svg>';
    steps = plan(f); step = 0; stage.getBoundingClientRect(); requestAnimationFrame(apply);
    root.querySelectorAll('[data-mode]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
  }
  function show(w) {
    const n = norm(w), hit = index.find(([x]) => norm(x) === n);
    msg.textContent = '';
    if (!hit) { msg.innerHTML = it(w.trim()) + ' isn’t marked on this site yet.<span class="t-only"> The walk takes words from the route, the ELP and Dolch lists and the word families.</span>'; return; }
    fetch('walk/' + hit[1] + '.json').then(r => r.json()).then(j => {
      word = j; form_ = 0; input.value = j.w;
      formsBox.hidden = j.forms.length < 2;
      formsBox.innerHTML = j.forms.length < 2 ? '' : j.forms.map((f, i) => '<button type="button" data-form="' + i + '" aria-pressed="' + (i === 0) + '">' + esc(f.gloss) + '</button>').join('');
      const allT = j.where.length && j.where.every(l => l.x);   // only teachers' links: student view shows no line at all
      where.innerHTML = j.where.length ? '<span' + (allT ? ' class="t-only"' : '') + '>On the site: ' + j.where.map(l => '<a' + (l.x ? ' class="t-only"' : '') + ' href="' + esc(l.u) + '">' + esc(l.t) + '</a>').join(' · ') + '</span>' : '';
      pop.hidden = true;
      sumBox.innerHTML = j.sum ? '<span class="ws-l">Word sum</span> ' + j.sum.map(p => '<button type="button" class="part' + (p.r ? ' root' : '') + '" data-p="' + esc(p.k) + '">' + p.s + '</button>').join(' + ') + ' &rarr; <i>' + esc(j.w) + '</i>'
        + (j.mean ? '<span class="ws-m t-only">' + esc(j.mean) + '</span>' : '') : '';
      draw();
      if (root.dataset.url !== 'off') { const u = new URL(location.href); u.searchParams.set('w', j.w); history.replaceState(null, '', u); }
    });
  }
  const go = d => { const s = Math.max(0, Math.min(steps.length - 1, step + d)); if (s !== step) { step = s; apply(); } };
  form.addEventListener('submit', e => { e.preventDefault(); show(input.value); });
  root.querySelectorAll('.chip').forEach(b => b.addEventListener('click', () => show(b.dataset.w)));
  root.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => { mode = b.dataset.mode; draw(); }));
  formsBox.addEventListener('click', e => { const b = e.target.closest('[data-form]'); if (!b) return; form_ = +b.dataset.form;
    formsBox.querySelectorAll('[data-form]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); draw(); });
  stage.addEventListener('click', () => { if (swiped) { swiped = false; return; } go(1); });
  stage.addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); } });
  // tap a part of the sum: what it means, and the other words that have it (as on the family pages)
  const pop = $('.walk-pop'); let partsData = null;
  const closePop = () => { pop.hidden = true; sumBox.querySelectorAll('.part.sel').forEach(b => b.classList.remove('sel')); };
  sumBox.addEventListener('click', async e => {
    const b = e.target.closest('.part'); if (!b) return;
    if (b.classList.contains('sel')) { closePop(); return; }
    if (!partsData) { try { partsData = await (await fetch('parts.json')).json(); } catch (err) { partsData = {}; } }
    const k = b.dataset.p, d = partsData[k]; closePop(); if (!d) return;
    const others = d.w.filter(w => w !== word.w), few = others.slice(0, 14);
    pop.innerHTML = '<p><b>' + esc(k) + '</b>' + (d.m ? ' ' + d.m + '.' : '') + '</p>'
      + (others.length ? '<p class="pin">Also in ' + few.map(w => '<a href="walk.html?w=' + encodeURIComponent(w) + '" data-w="' + esc(w) + '">' + esc(w) + '</a>').join(', ')
        + (others.length > few.length ? ', and ' + (others.length - few.length) + ' more' : '') + '.</p>' : '<p class="pin">No other word here has it yet.</p>')
      + '<p class="pin"><a href="' + esc(d.u) + '">See it in Parts</a></p>';
    pop.hidden = false; b.classList.add('sel');
  });
  pop.addEventListener('click', e => { const a = e.target.closest('a[data-w]'); if (a) { e.preventDefault(); input.value = a.dataset.w; show(a.dataset.w); } });
  // swipe left for the next move, right to go back, as a page turns
  // the first few pixels decide the direction: sideways locks the page so it can't scroll, up or down scrolls as usual
  let sx = null, sy = null, lx = null, swiped = false, axis = null;
  stage.addEventListener('touchstart', e => { if (e.touches.length > 1) { sx = null; return; } const t = e.touches[0]; sx = lx = t.clientX; sy = t.clientY; swiped = false; axis = null; }, {passive: true});
  stage.addEventListener('touchmove', e => { if (sx === null) return; if (e.touches.length > 1) { sx = null; axis = null; return; }
    const t = e.touches[0], dx = t.clientX - sx, dy = t.clientY - sy; lx = t.clientX;
    if (!axis && Math.max(Math.abs(dx), Math.abs(dy)) > 8) axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
    if (axis === 'x' && e.cancelable) e.preventDefault(); }, {passive: false});
  const endSwipe = e => { if (sx === null) return; const t = e.changedTouches[0], dx = (t ? t.clientX : lx) - sx; sx = null;
    if (axis === 'x' && Math.abs(dx) > 40) { swiped = true; go(dx < 0 ? 1 : -1); } axis = null; };
  stage.addEventListener('touchend', endSwipe);
  stage.addEventListener('touchcancel', () => { sx = null; axis = null; });
  $('.walk-next').addEventListener('click', () => go(1));
  $('.walk-back').addEventListener('click', () => go(-1));
  $('.walk-all').addEventListener('click', () => { step = steps.length - 1; apply(); });
  const start = () => fetch('walk/index.json').then(r => r.json()).then(j => {
    index = j; list.innerHTML = j.map(([w]) => '<option value="' + esc(w) + '">').join('');
    show((root.dataset.url !== 'off' && params.get('w')) || root.dataset.default);
  });
  // on the home page the walk waits until it scrolls into view
  if (root.dataset.lazy === '1' && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); start(); } }, {rootMargin: '200px'});
    io.observe(root);
  } else start();
})();</script>"""
