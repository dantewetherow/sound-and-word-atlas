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
    words = set(where) | set(X["list_words"]) | {w for w, *_ in X["morph"]} | {"legomorphic"}
    elp = {w for L in X["elp"]["lists"].values() for w in L["words"]}
    d220 = {w for l in X["dolch"]["levels"] for w in l["words"]}
    nouns = X["dolch"]["nouns"]
    (OUT / "walk").mkdir(exist_ok=True)
    for f in (OUT / "walk").glob("*.json"): f.unlink()
    index, skipped = [], []
    for w in sorted(words, key=lambda x: (x.lower(), x)):
        if w in SC.UNMARKED: skipped.append(w); continue
        forms = SC.VARIANTS.get(w) or [(None, "")]
        undo = []
        try:
            for part in (PAIRS.get(w) or HYPHENED.get(w) or (w,)):          # the nouns' codes, only while they're drawn
                if part not in LW.W and part in NOUN_CODES: undo.append(with_code(part, NOUN_CODES[part]))
            if not all(p in LW.W for p in (PAIRS.get(w) or HYPHENED.get(w) or (w,))) and not SC.VARIANTS.get(w):
                skipped.append(w); continue
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
        wid = doors.word_id(w)
        (OUT / "walk" / f"{wid}.json").write_text(json.dumps({"w": w, "forms": out, "where": links}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        index.append([w, wid])
    (OUT / "walk" / "index.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    picks = [w for w in ("which", "make", "little", "squirrel", "notation") if any(w == i[0] for i in index)]
    chips = "".join(f'<button type="button" class="chip" data-w="{html.escape(w)}">{html.escape(w)}</button>' for w in picks)
    body = f"""<section class="hero walk-hero"><div class="wrap">
<h1><span class="t-only">Word walk</span><span class="s-only">Pick a word</span></h1>
<p class="lead t-only">Type a word, then tap through it. <b>Read it</b> starts from the letters and decodes; <b>Spell it</b> starts from the syllables, then the sounds, then the letters.</p>
</div></section>
<section class="walk" aria-label="Word walk" data-default="which"><div class="wrap">
<div class="walk-bar">
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
<div class="walk-stage" tabindex="0" aria-label="The word. Tap, or press the right arrow, for the next step."></div>
<p class="walk-cap" aria-live="polite"></p>
<div class="walk-nav"><button type="button" class="walk-back">Back</button><span class="walk-dots" aria-hidden="true"></span><button type="button" class="walk-next">Next</button><button type="button" class="walk-all">Show it all</button></div>
<p class="walk-where"></p>
<noscript><p>The word walk needs script. Each word is also on its step page.</p></noscript>
{X["uc"]("the walk takes the words marked on this site. Any other word would need an automatic first pass from a pronunciation dictionary, which would get some wrong. Next: a draft for other words, for teachers to check.")}
</div></section>
{WALK_JS}"""
    door_page("walk", "Word walk · Sound and Word Atlas", "Type a word and walk through it: reading from its letters, spelling from its sounds.", body)
    return len(index), skipped


WALK_JS = r"""<script>(() => {
  const root = document.querySelector('.walk'); if (!root || !window.fetch) return;
  const $ = s => root.querySelector(s);
  const form = $('.walk-form'), input = $('#walk-q'), list = $('#walk-words'), stage = $('.walk-stage'), cap = $('.walk-cap'),
        dots = $('.walk-dots'), msg = $('.walk-msg'), where = $('.walk-where'), formsBox = $('.walk-forms');
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
    const wt = stage.querySelector('.wt'); if (wt) wt.classList.toggle('on', band && !shown.has(5));
    cap.innerHTML = steps[step] ? steps[step].cap : '';
    dots.innerHTML = steps.map((_, i) => '<i class="' + (i === step ? 'now' : i < step ? 'done' : '') + '"></i>').join('');
    $('.walk-back').disabled = step === 0; $('.walk-next').disabled = step >= steps.length - 1;
  }
  function draw() {
    if (!word) return;
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
      where.innerHTML = j.where.length ? 'On the site: ' + j.where.map(l => '<a' + (l.x ? ' class="t-only"' : '') + ' href="' + esc(l.u) + '">' + esc(l.t) + '</a>').join(' · ') : '';
      draw();
      const u = new URL(location.href); u.searchParams.set('w', j.w); history.replaceState(null, '', u);
    });
  }
  const go = d => { const s = Math.max(0, Math.min(steps.length - 1, step + d)); if (s !== step) { step = s; apply(); } };
  form.addEventListener('submit', e => { e.preventDefault(); show(input.value); });
  root.querySelectorAll('.chip').forEach(b => b.addEventListener('click', () => show(b.dataset.w)));
  root.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => { mode = b.dataset.mode; draw(); }));
  formsBox.addEventListener('click', e => { const b = e.target.closest('[data-form]'); if (!b) return; form_ = +b.dataset.form;
    formsBox.querySelectorAll('[data-form]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); draw(); });
  stage.addEventListener('click', () => go(1));
  stage.addEventListener('keydown', e => { if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); } });
  $('.walk-next').addEventListener('click', () => go(1));
  $('.walk-back').addEventListener('click', () => go(-1));
  $('.walk-all').addEventListener('click', () => { step = steps.length - 1; apply(); });
  fetch('walk/index.json').then(r => r.json()).then(j => {
    index = j; list.innerHTML = j.map(([w]) => '<option value="' + esc(w) + '">').join('');
    show(params.get('w') || root.dataset.default);
  });
})();</script>"""
