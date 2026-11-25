"""Letter teams (24 November 2026): teams.html, beside Letters, names and sounds under Steps.

Dante asked for a page like the alphabet page for the common digraphs and trigraphs, built for quick, satisfying drills:
each team drawn in the notation's colours with its bond bar and sound circle, and a key word for each sound ("ow as in
snow", "ow as in cow"; th buzzy in this, th quiet in thin). Tap a team's circle for its key word. The Drill button runs
the chosen rows one key word at a time, big and fully marked: say the word, then the team's sound (the team
alone is ambiguous: ow in snow, ow in cow); in order or shuffled; say, then check, or fast; by tap or on a beat; with a
count and a time at the end. Nothing is saved but the drill's settings, in this browser.

Each team is (letters, code for the letters, key word, a note or ""). The code draws the team as it is drawn inside a
word; the key word is drawn from its checked code. The step is where the path brings the team in (coverage.UNITS)."""
import html

GROUPS = [
    ("green", "sh, ch, th", "Green: two or three letters, one sound", [
        ("sh", "g.sh", "ship", ""), ("ch", "g.ch", "chip", ""), ("th", "g.th", "this", "buzzy"), ("th", "g.th", "thin", "quiet"),
        ("tch", "g.tch", "catch", "after a short vowel")]),
    ("cons", "ck, ng, wh", "Black: consonant teams", [
        ("ck", "k.ck", "duck", "after a short vowel"), ("ng", "k.ng", "ring", ""), ("wh", "k.wh", "when", ""), ("ph", "k.ph", "phone", ""),
        ("kn", "k.kn", "knee", ""), ("wr", "k.wr", "write", ""), ("qu", "q.qu", "quick", "two sounds")]),
    ("long", "ai, ee, oa", "Red: vowel teams that spell a long sound", [
        ("ai", "t.ai", "rain", ""), ("ay", "t.ay", "day", ""), ("ee", "t.ee", "tree", ""), ("ea", "t.ea", "eat", ""),
        ("oa", "t.oa", "boat", ""), ("oe", "t.oe", "toe", ""), ("ow", "t.ow", "snow", ""), ("ie", "t.ie", "pie", ""),
        ("igh", "t.igh", "night", ""), ("ue", "t.ue", "blue", ""), ("ew", "t.ew", "new", "")]),
    ("other", "ow, oi, oo", "Red: vowel teams with other sounds", [
        ("ow", "t.ow", "cow", ""), ("ou", "t.ou", "out", ""), ("oi", "t.oi", "coin", ""), ("oy", "t.oy", "boy", ""),
        ("oo", "t.oo", "moon", ""), ("oo", "t.oo", "book", "short"), ("aw", "t.aw", "saw", ""), ("au", "t.au", "haul", ""),
        ("ea", "t.ea", "head", "short e")]),
    ("r", "ar, or, er", "Red and black: r-controlled units", [
        ("ar", "r.ar", "car", ""), ("or", "r.or", "for", ""), ("er", "r.er", "her", ""), ("ir", "r.ir", "bird", ""),
        ("ur", "r.ur", "turn", ""), ("air", "r.air", "hair", ""), ("ear", "r.ear", "hear", ""), ("are", "r.ar e0", "care", ""),
        ("ore", "r.or e0", "more", "")]),
]

SECOND = {"cow", "book", "head"}   # a team's second sound: no step shown until the path places it


def write(door_page, X):
    import json, gym, pathlib, coverage
    from noun_codes import NOUN_CODES
    here = pathlib.Path(__file__).resolve().parent
    LW, svg_of = X["LW"], X["svg_of"]
    pool = dict(X["auto_codes"]); pool.update(NOUN_CODES); pool.update(gym.codes())
    for fn in ("more_codes.json", "family_codes.json"): pool.update(json.loads((here / "data" / fn).read_text(encoding="utf-8")))
    import re
    key_svg = lambda w: re.sub(r' style="[^"]*"', "", svg_of(w, 40, code=None if w in LW.W else pool[w], label=f"{w}, marked"), count=1)
    step = lambda g: (coverage.UNITS.get(g) or (None,))[0]

    def team_svg(g, code):
        """The team alone: no syllable swoop (it isn't a syllable), cropped to the letters, bar and circle, sized by CSS."""
        import re
        out = svg_of(g, 58, code=code, label=g)
        out = re.sub(r'<path d="M[^"]*Q[^"]*" fill="none" stroke="var\(--modal\)"[^>]*/>', "", out)
        out = re.sub(r'viewBox="0 0 ([\d.]+) [\d.]+"', r'viewBox="0 26 \1 100"', out)
        return re.sub(r' style="[^"]*"', "", out, count=1)

    rows, chips = [], []
    for gid, short, head, teams in GROUPS:
        chips.append(f'<button type="button" class="tm-chip" data-row="{gid}" aria-pressed="true">{short}</button>')
        tiles = []
        for g, code, key, note in teams:
            say = f"{g} as in {key}" + (f" ({note})" if note else "")
            st = None if key in SECOND else step(g)   # the path's table gives a team's first sound only
            tiles.append(
                f'<div class="tm" data-say="{html.escape(say)}">'
                f'<button type="button" class="tm-box" aria-label="{html.escape(g)}">{team_svg(g, code)}</button>'
                + (f'<span class="tm-step t-only">step {st}</span>' if st else '<span class="tm-step t-only">&nbsp;</span>')
                + f'<button type="button" class="tm-dot" aria-label="Key word for {html.escape(g)}" aria-pressed="false"></button>'
                f'<span class="tm-key" aria-live="polite"><span class="tm-kw">{key_svg(key)}</span>'
                f'<span class="tm-as">{html.escape(g)} as in <b>{html.escape(key)}</b>{f" <small>{html.escape(note)}</small>" if note else ""}</span></span>'
                + '</div>')
        rows.append(f'<section class="tm-row" data-row="{gid}" aria-label="{html.escape(head)}"><h3>{head}</h3>'
                    f'<div class="tm-tiles">{"".join(tiles)}</div></section>')

    inner = f"""<section class="hero"><div class="wrap">
<p class="eyebrow t-only"><a href="progressions.html">Steps</a> &middot; <a href="letters.html">Letters</a> &middot; Letter teams</p>
<h1>Letter teams</h1>
<p class="lead">Two or three letters that work together. Each team is drawn in its colours, with the bond bar that joins its letters and its sound circle. Tap a circle for the key word: ow as in snow, ow as in cow.</p>
</div></section>
<section class="about teams-board" aria-labelledby="tm-h"><div class="wrap">
<h2 id="tm-h" class="t-only">The teams</h2>
<div class="lt-tools tm-tools" role="group" aria-label="Board">
  <div class="tm-chips" role="group" aria-label="Rows in the drill">{"".join(chips)}</div>
  <button type="button" class="lt-all" data-keys="show">Show the key words</button>
  <button type="button" class="lt-all" data-keys="hide">Hide them</button>
  <button type="button" class="tm-go">Drill</button>
</div>
{"".join(rows)}
<div class="tm-set t-only" role="group" aria-label="Drill settings">
  <div class="seg" role="radiogroup" aria-label="Order"><button type="button" role="radio" aria-checked="true" data-order="in">In order</button><button type="button" role="radio" aria-checked="false" data-order="mix">Shuffled</button></div>
  <div class="seg" role="radiogroup" aria-label="Mode"><button type="button" role="radio" aria-checked="true" data-mode="check">Say, then check</button><button type="button" role="radio" aria-checked="false" data-mode="fast">Fast</button></div>
  <div class="seg" role="radiogroup" aria-label="Pace"><button type="button" role="radio" aria-checked="true" data-pace="0">By tap</button><button type="button" role="radio" aria-checked="false" data-pace="3000">3 s</button><button type="button" role="radio" aria-checked="false" data-pace="2000">2 s</button><button type="button" role="radio" aria-checked="false" data-pace="1200">1.2 s</button></div>
</div>
<p class="sub t-only">The colours are the notation&rsquo;s. Red letters are vowels, and a red bar joins a vowel team. Green is for sh, ch and th, and for tch, where the t stays black. Black bars join consonant teams. An r-controlled unit keeps its vowel red and its r black under one red bar. Qu has two sounds, one circle under each letter.</p>
<p class="sub t-only">Some teams spell two sounds, and each sound gets its own tile. Ow is in <i>snow</i> and <i>cow</i>, oo in <i>moon</i> and <i>book</i>, ea in <i>eat</i> and <i>head</i>. Th is voiced in <i>this</i> (the buzzy th) and voiceless in <i>thin</i>. The step under a tile is where the path brings the team in.</p>
<p class="sub t-only">To drill: choose the rows with the buttons at the top, then Drill. Each card shows a key word, fully marked: learners say the word. In <i>Say, then check</i>, the first tap shows the team and its sound, and learners say the sound; the second tap moves on. <i>Fast</i> shows only the words, and each tap moves on. A pace of 3, 2 or 1.2 seconds runs the drill on its own; tap to pause. The count and the time show at the end. Space or the right arrow moves on, the left arrow goes back, and Escape stops.</p>
</div></section>
<div class="tm-drill" hidden role="dialog" aria-modal="true" aria-label="Drill" tabindex="-1">
  <div class="tm-dbar"><span class="tm-count" aria-live="polite"></span><span class="tm-clock"></span><button type="button" class="tm-close" aria-label="Stop the drill">&times;</button></div>
  <div class="tm-prog"><i></i></div>
  <div class="tm-card"></div>
  <div class="tm-end" hidden><p class="tm-sum"></p><button type="button" class="tm-again">Again</button> <button type="button" class="tm-done">Done</button></div>
</div>
{JS}"""
    door_page("teams", "Letter teams · Sounds and Words, Assembled",
              "The common digraphs and trigraphs, drawn in the notation's colours with their bond bars and sound circles, each with a key word, and a drill that runs them one at a time.", inner)
    return sorted({k for _, _, _, ts in GROUPS for _, _, k, _ in ts})


JS = """<script>(() => {
  const page = document.querySelector('.teams-board'); if (!page) return;
  const tiles = [...page.querySelectorAll('.tm')];
  const setKey = (t, on) => { t.classList.toggle('on', on); t.querySelector('.tm-dot').setAttribute('aria-pressed', on); };
  page.addEventListener('click', e => {
    const d = e.target.closest('.tm-dot, .tm-box'); if (d) { const t = d.closest('.tm'); setKey(t, !t.classList.contains('on')); }
    const c = e.target.closest('.tm-chip'); if (c) { const on = c.getAttribute('aria-pressed') !== 'true'; c.setAttribute('aria-pressed', on);
      page.querySelector(`.tm-row[data-row="${c.dataset.row}"]`).classList.toggle('off', !on); }
    const k = e.target.closest('[data-keys]'); if (k) tiles.forEach(t => setKey(t, k.dataset.keys === 'show'));
  });
  // the drill's settings, remembered in this browser only
  const get = (k, d) => { try { return localStorage.getItem('teams:' + k) || d; } catch (e) { return d; } };
  const put = (k, v) => { try { localStorage.setItem('teams:' + k, v); } catch (e) {} };
  const opt = { order: get('order', 'in'), mode: get('mode', 'check'), pace: get('pace', '0') };
  page.querySelectorAll('.tm-set .seg').forEach(seg => {
    const bs = [...seg.querySelectorAll('button')], key = Object.keys(bs[0].dataset)[0];
    const mark = () => bs.forEach(b => b.setAttribute('aria-checked', b.dataset[key] === opt[key])); mark();
    bs.forEach(b => b.addEventListener('click', () => { opt[key] = b.dataset[key]; put(key, opt[key]); mark(); }));
  });
  const dr = document.querySelector('.tm-drill'), card = dr.querySelector('.tm-card'), count = dr.querySelector('.tm-count'),
        clock = dr.querySelector('.tm-clock'), bar = dr.querySelector('.tm-prog i'), end = dr.querySelector('.tm-end');
  let deck = [], i = 0, shown = false, t0 = 0, tick = null, beat = null, paused = false;
  const mmss = ms => { const s = Math.round(ms / 1000); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };
  function draw() {
    const t = deck[i];
    // the word first, fully marked: say it. Then the team and its sound: say the sound (24 November 2026). The team
    // alone is ambiguous (ow in snow, ow in cow); the word settles which sound it spells.
    card.innerHTML = '<div class="tm-big">' + t.querySelector('.tm-kw').innerHTML + '</div><div class="tm-bigkey"><div class="tm-team">'
      + t.querySelector('.tm-box').innerHTML + '</div>' + t.querySelector('.tm-as').outerHTML + '</div>';
    card.classList.remove('in'); void card.offsetWidth; card.classList.add('in');
    if (shown) card.querySelector('.tm-bigkey').classList.add('on');
    count.textContent = (i + 1) + ' of ' + deck.length; bar.style.width = ((i + 1) / deck.length * 100) + '%';
  }
  function next() {
    if (!end.hidden) return;
    if (opt.mode === 'check' && !shown) { shown = true; card.querySelector('.tm-bigkey').classList.add('on'); return; }
    if (i + 1 >= deck.length) return finish();
    i++; shown = false; draw();
  }
  function back() { if (!end.hidden || i === 0) return; i--; shown = false; draw(); }
  function finish() {
    stopBeat(); clearInterval(tick); const ms = Date.now() - t0;
    end.querySelector('.tm-sum').textContent = deck.length + (deck.length === 1 ? ' team' : ' teams') + ' in ' + mmss(ms) + '.';
    card.innerHTML = ''; end.hidden = false; end.querySelector('.tm-again').focus();
  }
  const stopBeat = () => { clearInterval(beat); beat = null; };
  function startBeat() { stopBeat(); const p = +opt.pace; if (p) beat = setInterval(() => { if (!paused) next(); }, opt.mode === 'check' ? p / 2 : p); }
  function start() {
    deck = tiles.filter(t => !t.closest('.tm-row').classList.contains('off'));
    if (!deck.length) return;
    if (opt.order === 'mix') for (let k = deck.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [deck[k], deck[j]] = [deck[j], deck[k]]; }
    i = 0; shown = false; paused = false; end.hidden = true; dr.hidden = false; document.body.classList.add('tm-on');
    t0 = Date.now(); clearInterval(tick); tick = setInterval(() => { clock.textContent = mmss(Date.now() - t0); }, 250); clock.textContent = '0:00';
    draw(); startBeat(); dr.focus({ preventScroll: true });
  }
  function stop() { stopBeat(); clearInterval(tick); dr.hidden = true; document.body.classList.remove('tm-on'); page.querySelector('.tm-go').focus(); }
  page.querySelector('.tm-go').addEventListener('click', start);
  dr.querySelector('.tm-close').addEventListener('click', e => { e.stopPropagation(); stop(); });
  dr.querySelector('.tm-done').addEventListener('click', e => { e.stopPropagation(); stop(); });
  dr.querySelector('.tm-again').addEventListener('click', e => { e.stopPropagation(); start(); });
  dr.addEventListener('click', e => { if (e.target.closest('button')) return; if (beat) { paused = !paused; dr.classList.toggle('paused', paused); } else next(); });
  document.addEventListener('keydown', e => {
    if (dr.hidden) return;
    if (e.key === 'Escape') { e.preventDefault(); stop(); }
    else if ([' ', 'ArrowRight', 'Enter', 'PageDown'].includes(e.key) && !e.target.closest('button')) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'PageUp'].includes(e.key)) { e.preventDefault(); back(); }
  });
})();</script>"""
