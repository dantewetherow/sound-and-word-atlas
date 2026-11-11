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
    if len(words) == 1:      # Try it: the marks letter by letter, for a learner's attempt to sit beside
        COL = {"vowel": "v", "team": "t"}
        out["try"] = {"L": "".join(L), "sy": [a for a, b in p["syllables"]][1:],
                      "d": [[m["cols"][0], m["cols"][-1], 1 if m.get("color") == "vowel" else 0] for m in p["marks"] if m["type"] == "dot"],
                      "b": [[m["from"], m["to"], COL.get(m.get("color"), "c")] for m in p["marks"] if m["type"] == "blendbar"],
                      "sh": [m["col"] for m in p["marks"] if m["type"] == "breve"], "lg": [m["col"] for m in p["marks"] if m["type"] == "macron"],
                      "sm": [m["after"] + 1 for m in p["marks"] if m["type"] == "seam"]}
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
<p class="lead t-only">Look up a word, then tap or swipe through it, or try marking it first. <b>Read it</b> starts from the word in plain letters and decodes; <b>Spell it</b> starts from the syllables, then the sounds, then the letters. <b>Try it</b> puts the marks in the learner’s hands: pick sound circles, bond bars, syllable swoops, breves, macrons or seams, then tap or swipe them onto the word, or write its word sum. <b>Show ours</b> sets the site’s marks underneath to talk about; nothing is scored. Under the word is its sum: tap a part to see every word that shares it.</p>
</div></section>
{section(note=X["uc"]("a word is either marked, so it can be walked, or shown as a word sum only. Next: the word built from left to right, a unit at a swipe; and draft marks for more words, labelled as drafts, for teachers to check."))}
<section class="about t-only"><div class="wrap"><p><a href="explorations.html">A family built in three moves: <i>note</i>, <i>notate</i>, <i>notation</i></a>. Every analysed word, by its parts, is in <a href="parts.html">Parts</a>.</p></div></section>"""
    door_page("walk", "Words · Sound and Word Atlas", "Look up a word and walk through it: its marks, a move at a time, and its parts.", body)
    return len(index), skipped




def section(note="", head="", lazy=False, url=True, default="which"):
    """The walk: the word field and its suggestions, the three walks, the stage and its controls, and the script. walk.html
    has it whole; the home page has a copy (head, lazy, and no ?w= in its address), since 9 November 2026."""
    return f"""<section class="walk" aria-label="Word walk" data-default="{default}"{' data-lazy="1"' if lazy else ''}{' data-url="off"' if not url else ''}><div class="wrap">
{head}<div class="walk-bar">
<form class="walk-form" role="search" autocomplete="off">
<label class="sr" for="walk-q">A word</label>
<div class="walk-field"><input id="walk-q" type="search" placeholder="Type a word" spellcheck="false" autocapitalize="off" autocorrect="off" enterkeyhint="go" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="walk-sug">
<div class="walk-sug" id="walk-sug" role="listbox" aria-label="Words on the site" hidden></div></div>
<button type="submit" class="btn">Show it</button>
</form>
<div class="walk-modes" role="group" aria-label="Walk"><button type="button" data-mode="read" aria-pressed="true">Read it</button><button type="button" data-mode="spell" aria-pressed="false">Spell it</button><button type="button" data-mode="try" aria-pressed="false">Try it</button></div>
</div>
<div class="walk-forms" hidden></div>
<p class="walk-msg" role="status"></p>
<div class="walk-board"><div class="try-tools" role="group" aria-label="What to mark" hidden></div>
<div class="walk-stage" tabindex="0" aria-label="The word. Tap, swipe left, or press the right arrow, for the next step."></div></div>
<p class="walk-cap" aria-live="polite"></p>
<div class="walk-nav"><button type="button" class="walk-back">Back</button><span class="walk-dots" aria-hidden="true"></span><button type="button" class="walk-next">Next</button><button type="button" class="walk-all">Show it all</button></div>
<div class="walk-try" hidden>
<p class="try-say"></p>
<div class="try-text"></div>
<div class="try-row try-ours" hidden><span class="try-lab">Ours</span><div class="try-board"></div></div>
<p class="try-count" aria-live="polite"></p>
<div class="try-acts"><button type="button" class="try-undo">Undo</button><button type="button" class="try-clear">Clear</button><button type="button" class="try-show" aria-pressed="false">Show ours</button></div>
</div>
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
  const form = $('.walk-form'), input = $('#walk-q'), sug = $('.walk-sug'), stage = $('.walk-stage'), cap = $('.walk-cap'),
        dots = $('.walk-dots'), msg = $('.walk-msg'), where = $('.walk-where'), formsBox = $('.walk-forms'), sumBox = $('.walk-sum');
  const student = () => document.documentElement.dataset.view === 'student';
  const norm = s => s.trim().toLowerCase().replace(/[’']/g, '').replace(/\s+/g, ' ');
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
  const it = s => '<i>' + esc(s) + '</i>';
  const and = a => a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1];
  let index = [], word = null, form_ = 0, mode = 'read', step = 0, steps = [];
  const params = new URLSearchParams(location.search);
  if (params.get('m') === 'spell' || params.get('m') === 'try') mode = params.get('m');

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
      S.push({show: [5, 4], spell: true, cap: f.bars.length ? 'Spell each sound. A bar first where a sound takes more than one letter, then the letters: ' + f.units.map(it).join(' · ') + '.' : 'Spell each sound: ' + f.units.map(it).join(' · ') + '.'});
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
    stage.classList.toggle('plain', !!(steps[step] && steps[step].plain));
    stage.classList.toggle('spelling', mode === 'spell');   // reading: letters, then the bar joins them; spelling: the bar, then the letters fill it   // the first move: every letter in ink, no marks
    const wt = stage.querySelector('.wt'); if (wt) wt.classList.toggle('on', band && !shown.has(5));
    cap.innerHTML = steps[step] ? steps[step].cap : '';
    dots.innerHTML = steps.map((_, i) => '<i class="' + (i === step ? 'now' : i < step ? 'done' : '') + '"></i>').join('');
    $('.walk-back').disabled = step === 0; $('.walk-next').disabled = step >= steps.length - 1;
  }
  function draw() {
    if (!word) return;
    const trying = mode === 'try';
    root.classList.toggle('trying', trying); tryBox.hidden = toolsBox.hidden = !trying; if (!trying) root.classList.remove('texting');
    root.querySelectorAll('[data-mode]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
    root.classList.toggle('sum-only', !word.forms.length);
    if (!word.forms.length) {      // taken apart, not marked yet: the word in plain letters
      stage.innerHTML = '<span class="walk-plain">' + esc(word.w) + '</span>'; steps = []; step = 0;
      cap.innerHTML = 'This word isn’t marked yet. Its parts are below.'; dots.innerHTML = '';
      if (trying) tryOpen(); return;
    }
    const f = word.forms[form_];
    stage.innerHTML = '<svg viewBox="0 0 ' + f.W + ' ' + f.H + '" role="img" aria-label="' + esc(word.w) + (trying ? ', to mark' : ', marked') + '">' + f.svg + '</svg>';
    if (trying) { steps = []; step = 0; tryOpen(); return; }
    stage.classList.remove('plain');
    stage.querySelectorAll('line.nz4').forEach(l => { l.setAttribute('pathLength', '1'); l.classList.add('dr'); });   // a bar draws across, left to right
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
  form.addEventListener('submit', e => { e.preventDefault(); sugClose(); input.blur(); show(input.value); });
  // the word field: the site's own suggestions, which leave the cursor in the field (a browser's list took it away on a
  // tablet, a tap for every letter deleted), and a tap in the field selects the word that's there, so typing replaces it
  let sugs = [], sugAt = -1;
  const sugClose = () => { sug.hidden = true; sug.innerHTML = ''; sugs = []; sugAt = -1; input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant'); };
  const sugMark = () => { sug.querySelectorAll('[role="option"]').forEach((o, i) => o.setAttribute('aria-selected', String(i === sugAt)));
    if (sugAt >= 0) { input.setAttribute('aria-activedescendant', 'walk-sug-' + sugAt); sug.children[sugAt].scrollIntoView({block: 'nearest'}); } else input.removeAttribute('aria-activedescendant'); };
  function sugShow() {
    const t = norm(input.value); if (!t || !index.length) { sugClose(); return; }
    const words = index.map(([w]) => w), first = words.filter(w => norm(w).startsWith(t)), more = words.filter(w => !norm(w).startsWith(t) && norm(w).includes(t));
    sugs = first.concat(more).slice(0, 10); sugAt = -1;
    if (!sugs.length || (sugs.length === 1 && norm(sugs[0]) === t && word && norm(word.w) === t)) { sugClose(); return; }
    sug.innerHTML = sugs.map((w, i) => '<div role="option" id="walk-sug-' + i + '" data-w="' + esc(w) + '" aria-selected="false">' + esc(w) + '</div>').join('');
    sug.hidden = false; input.setAttribute('aria-expanded', 'true');
  }
  const pick = w => { sugClose(); input.blur(); show(w); };
  input.addEventListener('input', sugShow);
  input.addEventListener('focus', () => { setTimeout(() => { if (document.activeElement === input) input.setSelectionRange(0, input.value.length); }, 0); });
  input.addEventListener('blur', () => setTimeout(sugClose, 150));
  input.addEventListener('keydown', e => {
    if (e.key === 'ArrowDown' && sugs.length) { e.preventDefault(); sugAt = Math.min(sugs.length - 1, sugAt + 1); sugMark(); }
    else if (e.key === 'ArrowUp' && sugs.length) { e.preventDefault(); sugAt = Math.max(-1, sugAt - 1); sugMark(); }
    else if (e.key === 'Escape') sugClose();
    else if (e.key === 'Enter' && sugAt >= 0) { e.preventDefault(); pick(sugs[sugAt]); }
  });
  sug.addEventListener('pointerdown', e => e.preventDefault());      // keep the field's focus until the pick is made
  sug.addEventListener('click', e => { const o = e.target.closest('[data-w]'); if (o) pick(o.dataset.w); });
  root.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => { mode = b.dataset.mode; draw(); }));
  formsBox.addEventListener('click', e => { const b = e.target.closest('[data-form]'); if (!b) return; form_ = +b.dataset.form;
    formsBox.querySelectorAll('[data-form]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); draw(); });
  stage.addEventListener('click', () => { if (mode === 'try') return; if (swiped) { swiped = false; return; } go(1); });
  stage.addEventListener('keydown', e => { if (mode === 'try') return; if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); } });
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
  // Try it: the learner marks the word on the stage itself, picking a mark first so a tap or a swipe means one thing,
  // and the site's marks can be set underneath to compare. Nothing is scored.
  const tryBox = $('.walk-try'), toolsBox = $('.try-tools'), say = $('.try-say'), countBox = $('.try-count'), textBox = $('.try-text'),
        oursRow = $('.try-ours'), oursB = $('.try-ours .try-board'), showB = $('.try-show');
  const NS = 'http://www.w3.org/2000/svg';
  const ICON = {
    circ: '<circle cx="11" cy="11" r="4.5" fill="currentColor"/>',
    bond: '<line x1="3" y1="11" x2="19" y2="11" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>',
    swoop: '<path d="M3 8 Q11 18 19 8" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
    breve: '<path d="M5 7 Q11 17 17 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
    macron: '<line x1="5" y1="11" x2="17" y2="11" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
    seam: '<line x1="11" y1="3" x2="11" y2="19" stroke="currentColor" stroke-width="2.2" stroke-dasharray="3 3"/>',
    sum: '<path d="M11 5V17M5 11H17" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>',
    join: '<path d="M4 11H17M12 6l5 5-5 5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
  };
  const TOOLS = {
    circ: ['Sound circles', 'Tap a letter for each sound you say. Where two or more letters spell one sound, swipe across them for one circle.', 'sound circle'],
    bond: ['Bond bars', 'Swipe across letters that work together to bond them with a bar.', 'bond bar'],
    swoop: ['Syllable swoops', 'Swipe under each syllable, from its first letter to its last. Tap a letter for a syllable of one letter.', 'syllable swoop'],
    breve: ['Breves', 'Tap a vowel with a short sound to give it a breve.', 'breve'],
    macron: ['Macrons', 'Tap a vowel with a long sound to give it a macron.', 'macron'],
    seam: ['Seams', 'Tap between two letters where one part ends and the next begins.', 'seam'],
    sum: ['Word sum', 'Write the word sum. Put + between the parts and brackets round a letter that drops or changes: <i>hop(e) + ing</i>.'],
    join: ['Put together', 'Here are the parts. Write the word they make.']
  };
  const MARKS = ['circ', 'bond', 'swoop', 'breve', 'macron', 'seam'], LAYERS = {circ: [1, 2], bond: [4], swoop: [3], breve: [6], macron: [6], seam: [9]};
  let T = null, G = null, Y = null, tool = 'circ', showing = false, undo = [];
  const fresh = () => ({circ: [], bond: [], swoop: [], breve: [], macron: [], seam: [], sum: '', join: ''});
  const plainSum = () => word.sum.map(p => p.s.replace(/\(([^)&]*)&rarr;[^)]*\)/g, '$1').replace(/[()]/g, '')).join(' + ');
  const sumText = () => word.sum.map(p => p.s.replace(/&rarr;/g, '→')).join(' + ');
  const svgOf = () => stage.querySelector('svg');
  function tryOpen() {
    const f = word.forms[form_];
    if (!Y || Y.w !== word.w || Y.f !== form_) { Y = Object.assign(fresh(), {w: word.w, f: form_}); undo = []; showing = false; }
    T = f && f.try || null; G = null;
    const svg = svgOf();
    if (T && svg) {          // the letters' places, read off the drawing: the marks go where the site's would
      const ts = [...svg.querySelectorAll('g.nz5 text')];
      if (ts.length === T.L.length) {
        const x = ts.map(t => +t.getAttribute('x')), base = +ts[0].getAttribute('y');
        G = {x, base, gaps: x.slice(1).map((v, i) => (v + x[i]) / 2)};
        stage.classList.add('plain');
        svg.querySelectorAll('[class*="nz"]').forEach(el => el.classList.toggle('on', /\bnz5\b/.test(el.getAttribute('class'))));
        svg.insertAdjacentHTML('beforeend', '<g class="yours"></g><g class="ghost"></g>');
      }
    }
    const tools = (G ? MARKS : []).concat(word.sum && word.sum.length > 1 ? ['sum', 'join'] : []);
    if (!tools.includes(tool)) tool = tools[0];
    toolsBox.innerHTML = tools.map(k => '<button type="button" data-tool="' + k + '" aria-pressed="' + (k === tool) + '"><svg viewBox="0 0 22 22" aria-hidden="true">' + ICON[k] + '</svg><span>' + TOOLS[k][0] + '</span></button>').join('');
    toolsBox.hidden = !tools.length;
    if (!tools.length) { say.textContent = 'This word has nothing to mark yet.'; return; }
    tryDraw();
  }
  const isText = () => tool === 'sum' || tool === 'join';
  function tryDraw() {
    root.classList.toggle('texting', isText());
    say.innerHTML = TOOLS[tool][1];
    showB.textContent = showing ? 'Hide ours' : 'Show ours'; showB.setAttribute('aria-pressed', String(showing));
    $('.try-undo').hidden = isText(); $('.try-undo').disabled = !undo.length;
    oursRow.hidden = !showing;
    if (isText()) {
      const k = tool;
      textBox.innerHTML = (k === 'join' ? '<p class="try-given">' + esc(plainSum()) + ' &rarr;</p>' : '<p class="try-given"><i>' + esc(word.w) + '</i> &rarr;</p>')
        + '<input class="try-in" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="' + (k === 'join' ? 'The word' : 'The word sum') + '" value="' + esc(Y[k]) + '">';
      const inp = textBox.querySelector('input'); inp.addEventListener('input', () => { Y[k] = inp.value; });
      inp.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); showing = true; tryDraw(); } });
      oursB.innerHTML = '<p class="try-given">' + (k === 'join' ? esc(sumText()) + ' &rarr; <i>' + esc(word.w) + '</i>' : '<i>' + esc(word.w) + '</i> &rarr; ' + esc(sumText())) + '</p>';
      countBox.textContent = ''; return;
    }
    textBox.innerHTML = '';
    ink(svgOf().querySelector('g.yours'), Y);
    if (showing) ours();
    countBox.innerHTML = counts();
  }
  // the learner's marks, drawn as the site draws them (legomorphic_words.py, at 80 units a letter's height)
  function ink(g, m, ghost) {
    if (!g || !G) return;
    const x = G.x, B = G.base, line = (x1, y1, x2, y2, c, w, d) => '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="' + c + '" stroke-width="' + w + '" stroke-linecap="round"' + (d ? ' stroke-dasharray="4.6 4.6"' : '') + '/>';
    let o = '';
    m.seam.forEach(k => { o += line(G.gaps[k - 1], B - 76, G.gaps[k - 1], B + 36.8, 'var(--modal)', 2.4, 1); });
    m.breve.forEach(i => { o += '<path d="M' + (x[i] - 20.6) + ' ' + (B - 78) + ' Q' + x[i] + ' ' + (B - 62) + ' ' + (x[i] + 20.6) + ' ' + (B - 78) + '" fill="none" stroke="var(--verb)" stroke-width="4" stroke-linecap="round"/>'; });
    m.macron.forEach(i => { o += line(x[i] - 22.3, B - 72.8, x[i] + 22.3, B - 72.8, 'var(--verb)', 4); });
    m.bond.forEach(([a, b]) => { o += line(x[a] - 20.6, B + 26.4, x[b] + 20.6, B + 26.4, 'var(--ink)', 4); });
    m.circ.forEach(([a, b]) => { o += '<circle cx="' + (x[a] + x[b]) / 2 + '" cy="' + (B + 44.8) + '" r="5.8" fill="var(--ink)"/>'; });
    m.swoop.forEach(([a, b]) => { o += '<path d="M' + (x[a] - 8.6) + ' ' + (B + 68) + ' Q' + (x[a] + x[b]) / 2 + ' ' + (B + 84) + ' ' + (x[b] + 8.6) + ' ' + (B + 68) + '" fill="none" stroke="var(--modal)" stroke-width="3.7" stroke-linecap="round"/>'; });
    g.innerHTML = o; g.style.opacity = ghost ? 0.35 : '';
  }
  const used = () => MARKS.filter(k => k === tool || Y[k].length);
  function ours() {
    const f = word.forms[form_], show = new Set([5]); used().forEach(k => LAYERS[k].forEach(n => show.add(n)));
    oursB.innerHTML = '<svg viewBox="0 0 ' + f.W + ' ' + f.H + '" role="img" aria-label="' + esc(word.w) + ', as the site marks it">' + f.svg + '</svg>';
    oursB.querySelectorAll('[class*="nz"]').forEach(el => { const n = +((el.getAttribute('class') || '').match(/nz(\d)/) || [])[1]; el.classList.toggle('on', show.has(n)); });
  }
  function counts() {
    const mine = {circ: Y.circ.length, bond: Y.bond.length, swoop: Y.swoop.length, breve: Y.breve.length, macron: Y.macron.length, seam: Y.seam.length},
          site = {circ: T.d.length, bond: T.b.length, swoop: T.sy.length + 1, breve: T.sh.length, macron: T.lg.length, seam: T.sm.length};
    const ks = used().filter(k => mine[k] || showing); if (!ks.length) return '';
    const say_ = c => ks.map(k => c[k] + ' ' + TOOLS[k][2] + (c[k] === 1 ? '' : 's')).join(', ');
    return 'Yours: ' + say_(mine) + '.' + (showing ? '<br>Ours: ' + say_(site) + '.' : '');
  }
  // a tap or a swipe on the stage, read for the mark that's picked
  const span = (a, b, list) => list.filter(([p, q]) => !(q < a || p > b));
  function act(t, x0, x1, tap) {
    const n = G.x.length, near = v => G.x.reduce((k, c, i) => Math.abs(c - v) < Math.abs(G.x[k] - v) ? i : k, 0);
    const gap = v => G.gaps.reduce((k, c, i) => Math.abs(c - v) < Math.abs(G.gaps[k - 1] - v) ? i + 1 : k, 1);
    const lo = Math.min(x0, x1), hi = Math.max(x0, x1), pad = 14;
    let a = G.x.findIndex(c => c >= lo - pad), b = n - 1 - [...G.x].reverse().findIndex(c => c <= hi + pad);
    if (tap || a < 0 || b < a || a >= n) a = b = near(tap ? x0 : (x0 + x1) / 2);
    const m = JSON.parse(JSON.stringify(Y));
    if (t === 'seam') { if (n < 2) return null; const k = gap(tap ? x0 : (x0 + x1) / 2), i = m.seam.indexOf(k); i < 0 ? m.seam.push(k) : m.seam.splice(i, 1); }
    else if (t === 'breve' || t === 'macron') { const o = t === 'breve' ? 'macron' : 'breve', i = near(x0);
      m[o] = m[o].filter(v => v !== i); m[t].includes(i) ? m[t] = m[t].filter(v => v !== i) : m[t].push(i); }
    else {
      const hit = span(a, b, m[t]);
      if (tap) { if (hit.length) m[t] = m[t].filter(r => !hit.includes(r)); else if (t !== 'bond') m[t].push([a, a]); }
      else { if (t === 'bond' && a === b) return null; m[t] = m[t].filter(r => !hit.includes(r)); m[t].push([a, b]); }
      m[t].sort((p, q) => p[0] - q[0]);
    }
    return m;
  }
  let px = null, py = null, pid = null;
  const toSvg = e => { const svg = svgOf(), pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY; return pt.matrixTransform(svg.getScreenCTM().inverse()); };
  stage.addEventListener('pointerdown', e => { if (mode !== 'try' || !G || isText() || !svgOf()) return; e.preventDefault();
    const p = toSvg(e); px = p.x; py = p.y; pid = e.pointerId; try { stage.setPointerCapture(pid); } catch (err) {} });
  stage.addEventListener('pointermove', e => { if (px === null || e.pointerId !== pid) return; const p = toSvg(e);
    if (Math.abs(p.x - px) < 10) { svgOf().querySelector('g.ghost').innerHTML = ''; return; }
    const m = act(tool, px, p.x, false); if (m) ink(svgOf().querySelector('g.ghost'), Object.fromEntries(MARKS.map(k => [k, k === tool ? m[k].filter(r => !JSON.stringify(Y[k]).includes(JSON.stringify(r))) : []])), true); });
  const lift = e => { if (px === null || e.pointerId !== pid) return; const p = toSvg(e), tap = Math.abs(p.x - px) < 10 && Math.abs(p.y - py) < 30;
    const m = e.type === 'pointerup' ? act(tool, px, p.x, tap) : null; px = null; svgOf().querySelector('g.ghost').innerHTML = '';
    if (m) { undo.push(JSON.stringify(Y)); Y = m; tryDraw(); } };
  stage.addEventListener('pointerup', lift); stage.addEventListener('pointercancel', lift);
  toolsBox.addEventListener('click', e => { const b = e.target.closest('[data-tool]'); if (!b) return; tool = b.dataset.tool;
    toolsBox.querySelectorAll('[data-tool]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); tryDraw(); });
  showB.addEventListener('click', () => { showing = !showing; tryDraw(); });
  $('.try-undo').addEventListener('click', () => { if (undo.length) { Y = JSON.parse(undo.pop()); tryDraw(); } });
  $('.try-clear').addEventListener('click', () => { if (!Y) return; undo.push(JSON.stringify(Y));
    if (isText()) Y[tool] = ''; else MARKS.forEach(k => { Y[k] = []; }); showing = false; tryDraw(); });
  // swipe left for the next move, right to go back, as a page turns
  // the first few pixels decide the direction: sideways locks the page so it can't scroll, up or down scrolls as usual
  let sx = null, sy = null, lx = null, swiped = false, axis = null;
  stage.addEventListener('touchstart', e => { if (mode === 'try' || e.touches.length > 1) { sx = null; return; } const t = e.touches[0]; sx = lx = t.clientX; sy = t.clientY; swiped = false; axis = null; }, {passive: true});
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
    index = j;
    show((root.dataset.url !== 'off' && params.get('w')) || root.dataset.default);
  });
  // on the home page the walk waits until it scrolls into view
  if (root.dataset.lazy === '1' && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); start(); } }, {rootMargin: '200px'});
    io.observe(root);
  } else start();
})();</script>"""
