"""Letters, names and sounds (13 November 2026): letters.html, before step 1 under Steps.

The alphabet as the song sings it, in its units (ABCD, EFG, HIJK, LMNOP, QRS, TUV, WX, Y and Z), as blank tiles a
teacher taps to reveal: a letter at a time, or a unit at a time, so learners can fill in the next letter or the next unit.
Uppercase, lowercase or both. Under each tile a sound circle: tap it once for the letter's sound, and on the vowels a
second time for the long sound (the cup turns to the long mark); c and g turn soft on the second tap, y turns to a vowel.
The circles are cues for the teacher to say or sing the sounds; when recordings come, each state has its own clip name
(data-say), and a voice switch will play them.

Then two explanations: L, M, N, O, P crowded into the song's two beats against one beat each, and the vowels sung up a
scale. The teacher's notes cite what the research says about names and sounds (Piasta and Wagner 2010) and about
uppercase and lowercase (Turnbull et al. 2010), and say plainly that the LMNOP point is a teacher's observation."""

LINES = ["ABCD", "EFG", "HIJK", "LMNOP", "QRS", "TUV", "WX", "Y&Z"]
VOWELS = set("AEIOU")


def _tile(ch):
    lo = ch.lower()
    kind = "v" if ch in VOWELS else "y" if ch == "Y" else "cg" if ch in "CG" else "c"
    return (f'<div class="lt" data-k="{kind}" data-l="{lo}">'
            f'<button type="button" class="lt-box" aria-label="Letter {ch}, hidden. Tap to show." aria-pressed="false">'
            f'<span class="lt-mark" aria-hidden="true"></span>'
            f'<span class="lt-up">{ch}</span><span class="lt-lo">{lo}</span></button>'
            f'<button type="button" class="lt-dot" aria-label="Sound of {ch}" data-state="0"></button>'
            f'<span class="lt-say" aria-live="polite"></span></div>')


def write(door_page, door_head):
    rows = []
    for n, line in enumerate(LINES, 1):
        tiles = []
        for ch in line:
            tiles.append('<span class="lt-and" aria-hidden="true">and</span>' if ch == "&" else _tile(ch))
        rows.append(f'<div class="lt-row" data-row="{n}"><button type="button" class="lt-beat" aria-label="Show or hide this unit">'
                    f'<span aria-hidden="true">&#9679;</span></button>{"".join(tiles)}</div>')
    crowd = "".join(f'<span class="bt" style="--w:{w}" data-t="{t}">{c}</span>'
                    for c, w, t in [("H", 1, 0), ("I", 1, 1), ("J", 1, 2), ("K", 1, 3), ("L", .5, 4), ("M", .5, 4.5), ("N", .5, 5), ("O", .5, 5.5), ("P", 2, 6)])
    even = "".join(f'<span class="bt" style="--w:1" data-t="{t}">{c}</span>' for t, c in enumerate("HIJKLMNOP"))
    scale = "".join(f'<button type="button" class="sc" style="--s:{k}" aria-label="{c}, hidden. Tap to show."><span class="sc-m" aria-hidden="true"></span><span>{c}</span></button>'
                    for k, c in enumerate("AEIOU")) + '<button type="button" class="sc sc-y" style="--s:5" aria-label="and typically Y, hidden. Tap to show."><span class="sc-m" aria-hidden="true"></span><span><small>and typically</small> Y</span></button>'
    inner = f"""<section class="hero"><div class="wrap">
<p class="eyebrow t-only"><a href="progressions.html">Steps</a> &middot; Before step 1</p>
<h1>Letters, names and sounds</h1>
<p class="lead">The alphabet as the song sings it, one unit to a line. Tap a tile to show its letter, or the dot at the start of a line to show the whole unit. Tap the circle under a letter for its sound.</p>
</div></section>
<section class="about letters-board" aria-labelledby="ab-h"><div class="wrap">
<h2 id="ab-h" class="t-only">The alphabet</h2>
<div class="lt-tools" role="group" aria-label="Board">
  <div class="seg" role="radiogroup" aria-label="Case">
    <button type="button" role="radio" aria-checked="true" data-case="up">ABC</button>
    <button type="button" role="radio" aria-checked="false" data-case="lo">abc</button>
    <button type="button" role="radio" aria-checked="false" data-case="both">Aa</button>
  </div>
  <button type="button" class="lt-all" data-all="show">Show all</button>
  <button type="button" class="lt-all" data-all="hide">Hide all</button>
  <button type="button" class="lt-all" data-all="clear">Clear the circles</button>
</div>
<div class="lt-board case-up">{"".join(rows)}</div>
<p class="sub t-only">The circle under a consonant marks its sound. Under a vowel, the first tap gives the short sound and the cup; the second, the long sound, which is the letter&rsquo;s name, and the long mark. A third tap clears it. Under c and g, the second tap makes them soft, as an e, i or y after them does (<a href="steps/10.html">step 10</a>). Under y, the first tap is the consonant of <i>yes</i>, the second the vowel of <i>my</i> (<a href="steps/03.html">step 3</a>). Under x, two sounds: /k/ and /s/.</p>
</div></section>

<section class="about" id="lmnop" aria-labelledby="lm-h"><div class="wrap">
<h2 id="lm-h">Elemeno: L, M, N, O, P</h2>
<p class="sub">The song gives H, I, J and K a beat each, then crowds L, M, N and O into two beats and holds P. Many learners hear one long word, <i>elemeno</i>. Give each letter its own beat while they learn it, and the letters come apart.</p>
<div class="bt-rows">
  <div class="bt-row" data-row="crowd"><p class="bt-l">As it&rsquo;s sung</p><div class="bt-track">{crowd}</div></div>
  <div class="bt-row" data-row="even"><p class="bt-l">A beat each</p><div class="bt-track">{even}</div></div>
</div>
<button type="button" class="bt-play">Play both</button>
</div></section>

<section class="about" id="vowels" aria-labelledby="vw-h"><div class="wrap">
<h2 id="vw-h">A, E, I, O, U, and typically Y</h2>
<p class="sub">The vowels sung up a scale, a note each, with their names: the long sounds. Tap a step to show it. <i>Typically</i>, not <i>sometimes</i>: about four in five y&rsquo;s in running English spell a vowel (<i>my, by, very, day, they</i>), and most of the rest are <i>you</i> and <i>your</i>. The deck <a href="sessions/typically-y.html">A, E, I, O, U and typically Y</a> has the count.</p>
<div class="sc-stairs">{scale}</div>
</div></section>

<section class="about t-only" aria-labelledby="why-h"><div class="wrap prose">
<h2 id="why-h">For teachers: why names, sounds and both cases</h2>
<p><b>Names and sounds together.</b> In a study of preschoolers taught letters for several weeks, those taught the names and the sounds together learned the letters&rsquo; names better than those taught only sounds, and learned at least as many sounds. Letters whose names hold their sound (b, d, f, m) were the easiest. The study didn&rsquo;t follow the learners into reading (Piasta and Wagner 2010). The vowel names are their long sounds, so the alphabet song already gives the long vowels, and the sounds give the short ones: the first contrast on the route.</p>
<p><b>Uppercase, then lowercase.</b> Among 461 preschoolers, a child who knew a letter&rsquo;s uppercase form was more than 16 times as likely to know its lowercase form, and lowercase letters that look like their capitals (c, o, s) were known best (Turnbull et al. 2010). Learners seem to reach lowercase through uppercase. We know of no study showing that teaching lowercase first gives better or longer-lasting results. The time to spend is on the letters whose two forms look least alike: a, b, d, e, g, h, q and r.</p>
<p><b>Elemeno.</b> The crowding of L, M, N, O and P is a teacher&rsquo;s observation, not a research finding. Slowing the song costs nothing.</p>
<p class="sub">Shayne B. Piasta and Richard K. Wagner, &ldquo;Learning Letter Names and Sounds: Effects of Instruction, Letter Type, and Phonological Processing Skill,&rdquo; <i>Journal of Experimental Child Psychology</i> 105, no. 4 (2010): 324&ndash;344 (<a href="https://doi.org/10.1016/j.jecp.2009.12.008">doi</a>). Kandia Lewis Turnbull, Ryan P. Bowles, Lori E. Skibbe, Laura M. Justice and Alice K. Wiggins, &ldquo;Theoretical Explanations for Preschoolers&rsquo; Lowercase Alphabet Knowledge,&rdquo; <i>Journal of Speech, Language, and Hearing Research</i> 53, no. 6 (2010): 1757&ndash;1768 (<a href="https://doi.org/10.1044/1092-4388(2010/09-0093)">doi</a>).</p>
<p class="sub">Next on the route: <a href="steps/01.html">step 1</a>, <i>I</i> and <i>it</i>, open and closed.</p>
</div></section>
<script>(() => {{
  const board = document.querySelector('.lt-board');
  const show = (t, on) => {{ t.classList.toggle('on', on); const b = t.querySelector('.lt-box'); b.setAttribute('aria-pressed', on);
    b.setAttribute('aria-label', 'Letter ' + t.dataset.l.toUpperCase() + (on ? ', shown' : ', hidden. Tap to show.')); }};
  board.addEventListener('click', e => {{
    const box = e.target.closest('.lt-box'), dot = e.target.closest('.lt-dot'), beat = e.target.closest('.lt-beat');
    if (box) {{ const t = box.closest('.lt'); show(t, !t.classList.contains('on')); }}
    if (beat) {{ const ts = [...beat.parentNode.querySelectorAll('.lt')]; const on = !ts.every(t => t.classList.contains('on')); ts.forEach(t => show(t, on)); }}
    if (dot) {{
      const t = dot.closest('.lt'), k = t.dataset.k, l = t.dataset.l;
      const states = k === 'v' ? ['', 'short', 'long'] : k === 'cg' ? ['', 'hard', 'soft'] : k === 'y' ? ['', 'cons', 'vowel'] : ['', 'sound'];
      const s = (+dot.dataset.state + 1) % states.length; dot.dataset.state = s; t.dataset.s = states[s];
      const words = {{ short: 'short ' + l, long: 'long ' + l, hard: 'hard ' + l, soft: 'soft ' + l, cons: 'y in yes', vowel: 'y in my', sound: 'its sound' }};
      t.querySelector('.lt-say').textContent = s ? words[states[s]] : '';
      t.dataset.say = s ? states[s] + '-' + l : '';
    }}
  }});
  document.querySelectorAll('[data-case]').forEach(b => b.addEventListener('click', () => {{
    document.querySelectorAll('[data-case]').forEach(x => x.setAttribute('aria-checked', x === b));
    board.className = 'lt-board case-' + b.dataset.case; }}));
  document.querySelectorAll('[data-all]').forEach(b => b.addEventListener('click', () => {{
    const a = b.dataset.all, ts = board.querySelectorAll('.lt');
    if (a === 'clear') ts.forEach(t => {{ const d = t.querySelector('.lt-dot'); d.dataset.state = 0; t.dataset.s = ''; t.dataset.say = ''; t.querySelector('.lt-say').textContent = ''; }});
    else ts.forEach(t => show(t, a === 'show')); }}));
  document.querySelector('.sc-stairs').addEventListener('click', e => {{ const b = e.target.closest('.sc'); if (b) b.classList.toggle('on'); }});
  const play = document.querySelector('.bt-play'), beat = 520, still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  play.addEventListener('click', () => {{
    const all = [...document.querySelectorAll('.bt')]; all.forEach(x => x.classList.remove('hit'));
    if (still) {{ all.forEach(x => x.classList.add('hit')); return; }}
    play.disabled = true;
    document.querySelectorAll('.bt-row').forEach((row, k) => row.querySelectorAll('.bt').forEach(x =>
      setTimeout(() => x.classList.add('hit'), (k * 10 + +x.dataset.t) * beat)));
    setTimeout(() => {{ play.disabled = false; }}, 19 * beat);
  }});
}})();</script>"""
    door_page("letters", "Letters, names and sounds · A Legend for English Words",
              "The alphabet in the song's units, as tiles to reveal, with a sound circle under each letter; elemeno taken apart; the vowels up a scale.", inner)
