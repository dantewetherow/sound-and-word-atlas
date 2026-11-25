"""Word matrices (24 November 2026): Melvyn Ramsden's word matrix (Real Spelling), as Pete Bowers brought it into
classrooms in structured word inquiry, built from the word sums the site already has.

One matrix per base spelling: tect, sign, duce and duct are each their own, because a matrix is built around one base
(a family whose base changes its spelling, like *deuk- or *leg-, shows that by having several). Its boxes hold only
parts that some word on the site carries in that place, counted outward from the base: the prefix next to the base,
the one before that; the suffix next to the base, the one after that.

A matrix offers paths that aren't words (over + de + tect). That is how Ramsden meant it: a learner builds a path and
checks it. So the builder says which paths are words in this family, and asks the learner to test the rest. It never
shows a joined spelling it hasn't been given, since the joins (e drop, y to i, doubling) are the lesson to work out.

Used on each family page (a Word sums / Matrix switch) and on the Parts page (a Matrix button on a root or base)."""
import html, json


def _key(p):
    return p.replace("(", "").replace(")", "").split(">")[0].split("+")[0]


_DICT = None
INFL = ("-s", "-es", "-ed", "-ing")


def _known(w):
    global _DICT
    if _DICT is None:
        import cmudict
        _DICT = set(cmudict.words())
    return w in _DICT


def forms(w, parts):
    """A word's inflected forms (24 November 2026): -s or -es, -ed, -ing, with the joins written into the sum: the e
    drops (pro + duc(e) + ing), y turns to i (sign + i + fy>i + es), or the last consonant doubles. Only spellings
    the CMU Pronouncing Dictionary lists are kept, so a noun gets its plural and a verb its -ed and -ing."""
    import re
    if parts[-1] in INFL or not re.fullmatch(r"[a-z]+", w): return []
    last, head, out = parts[-1], parts[:-1], []
    drop = lambda p: p[:-1] + "(e)" if p.endswith("e") else p
    cy = re.search(r"[^aeiou]y$", w)
    if re.search(r"(s|x|z|ch|sh)$", w): out.append((w + "es", parts + ["-es"]))
    elif cy: out.append((w[:-1] + "ies", head + [last + ">i", "-es"]))
    else: out.append((w + "s", parts + ["-s"]))
    if w.endswith("e"):
        out += [(w + "d", head + [drop(last), "-ed"]), (w[:-1] + "ing", head + [drop(last), "-ing"])]
    elif cy:
        out += [(w[:-1] + "ied", head + [last + ">i", "-ed"]), (w + "ing", parts + ["-ing"])]
    else:
        out += [(w + "ed", parts + ["-ed"]), (w + "ing", parts + ["-ing"])]
        if re.search(r"[^aeiou][aeiou][bdgklmnprt]$", w):
            out += [(w + w[-1] + "ed", head + [last + "+" + w[-1], "-ed"]), (w + w[-1] + "ing", head + [last + "+" + w[-1], "-ing"])]
    return [(f, ps) for f, ps in out if _known(f)]


def analyse(base, sums):
    """The matrix's boxes and its words: ({position: {part: {words}}}, {"pre|base|suf": word}). Positions count out
    from the base: -1 is the prefix next to it, 1 the suffix next to it. Each word brings its inflected forms."""
    cols, words = {}, {}
    have = {w for w, _ in sums}
    extra = [f for w, ps in sums for f in forms(w, list(ps)) if f[0] not in have]
    seen = set()
    sums = list(sums) + [f for f in extra if not (f[0] in seen or seen.add(f[0]))]
    for w, parts in sums:
        ks = [_key(p) for p in parts]
        try: i = next(n for n, k in enumerate(ks) if k.strip("-") == base)
        except StopIteration: continue
        pre, suf = ks[:i], ks[i + 1:]
        if not pre and not suf: words[base] = w; continue
        for d, k in enumerate(reversed(pre), 1): cols.setdefault(-d, {}).setdefault(k, set()).add(w)
        for d, k in enumerate(suf, 1): cols.setdefault(d, {}).setdefault(k, set()).add(w)
        words["|".join(pre + [base] + suf)] = w
    return cols, words


MIN_CARDS = 3          # a matrix with this many words or more gets its own set of morpheme cards


def card_sets():
    """Every family matrix worth a set of morpheme cards: [(base, family, family label, cluster key, sums)], one per
    base spelling, the same list the family pages and the cards page both read."""
    import roots
    out, seen = [], set()
    for R in roots.ROOTS:
        if not R.get("clusters"): continue
        words = roots.cluster_words(R)
        for c in R["clusters"]:
            for sp in c["spells"]:
                if sp in seen: continue
                # every cluster of the family that has this spelling: sign silent and sign said make one set of cards
                sums = [(w, p) for c2, w, p, m, b in words if sp in c2["spells"] and p]
                if len(analyse(sp, sums)[1]) >= MIN_CARDS:
                    seen.add(sp); out.append((sp, R["slug"], R["label"], c["key"], sums))
    return out


_SETS = None


def cards_href(base, up=""):
    global _SETS
    if _SETS is None: _SETS = {b for b, *_ in card_sets()}
    return f"{up}tents/{base}.html" if base in _SETS else None


def build(base, sums, label=None, up=""):
    """base: the part's key ('tect'); sums: [(word, [part, ...])], parts as the sums write them ('pro-', 'tect',
    '-ion', '-at(e)'). Returns the matrix's html, or '' if no word adds anything to the base. up: the path to the
    site's root, for the link to this matrix's morpheme cards."""
    cols, words = analyse(base, sums)
    if not words: return ""
    order = lambda col: sorted(col, key=lambda k: (-len(col[k]), k))
    def box(pos):
        col = cols[pos]
        ps = "".join(f'<button type="button" class="mp" data-pos="{pos}" data-p="{html.escape(k)}">{html.escape(k.strip("-"))}</button>' for k in order(col))
        return f'<div class="mcol" data-pos="{pos}">{ps}</div>'
    pre = "".join(box(p) for p in sorted(p for p in cols if p < 0))
    suf = "".join(box(p) for p in sorted(p for p in cols if p > 0))
    chips = "".join(f'<button type="button" class="mw" data-path="{html.escape(k)}">{html.escape(w)}</button>'
                    for k, w in sorted(words.items(), key=lambda kv: (kv[0].count("|"), kv[1])))
    data = json.dumps(words, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return (f'<div class="mtx" data-base="{html.escape(base)}" role="group" aria-label="{html.escape(label or base)}: the word matrix">'
            '<button type="button" class="mfull" aria-pressed="false">Full screen</button>'
            f'<div class="mgrid">{pre}<div class="mcol mbase"><span>{html.escape(base)}</span></div>{suf}</div>'
            f'<p class="mpath" aria-live="polite">Tap the parts to build a path, left to right. Any box can be skipped.</p>'
            f'<div class="mlist"><span>Words in it:</span> {chips}</div>'
            + (f'<p class="mcards"><a href="{cards_href(base, up)}">Morpheme cards for this matrix</a>, to print and stand up.</p>' if cards_href(base) else "")
            + f'<script type="application/json" class="mdata">{data}</script></div>')


CSS = """
/* word matrices (24 November 2026): Ramsden's matrix, built from the site's word sums */
.mtx { margin: 14px 0 18px; }
.mgrid { display: flex; align-items: center; flex-wrap: wrap; gap: 0; }
.mcol { display: grid; gap: 2px; padding: 8px 10px; border: 2px solid var(--ink); background: var(--card); margin-left: -2px; }
.mcol:first-child { margin-left: 0; }
.mbase { padding: 14px 20px; border-width: 3px; font-family: var(--display, serif); font-size: 1.9rem; color: var(--verb); z-index: 1; }
.mp { font: inherit; font-size: 1rem; line-height: 1.25; text-align: left; border: 0; border-radius: 6px; padding: 2px 8px; background: transparent; color: var(--ink); cursor: pointer; }
.mp:hover { background: var(--line); }
.mp.on { background: var(--ink); color: var(--paper); }
.mpath { margin: 10px 0 4px; min-height: 1.5em; color: var(--soft); }
.mpath b { color: var(--ink); font-weight: 600; }
.mpath .yes { color: var(--subject); font-weight: 600; }
.mpath .test { color: var(--verb); }
.mlist { display: flex; flex-wrap: wrap; gap: 4px 6px; align-items: baseline; font-size: 0.9rem; color: var(--soft); margin: 0; }
.mlist .mw { font: inherit; font-style: italic; border: 1px solid var(--line); border-radius: 999px; padding: 1px 10px; background: transparent; color: var(--ink); cursor: pointer; }
.mlist .mw.on { border-color: var(--ink); }
.mx-switch { display: inline-flex; gap: 2px; padding: 2px; border: 1px solid var(--line); border-radius: 999px; margin: 0 0 12px; }
.mx-switch button { font: inherit; font-size: 0.85rem; border: 0; border-radius: 999px; padding: 5px 14px; background: transparent; color: var(--soft); cursor: pointer; }
.mx-switch button[aria-checked="true"] { background: var(--ink); color: var(--paper); }
.cx.mtxview .cgroup, .cx.mtxview .pcard { display: none; }
.cx:not(.mtxview) .mtx { display: none; }
.ppart .mtx[hidden] { display: none; }
.mcards { margin: 8px 0 0; font-size: 0.9rem; }
.mfull { font: inherit; font-size: 0.85rem; border: 1px solid var(--line); border-radius: 999px; padding: 4px 12px; background: var(--card); color: var(--ink); cursor: pointer; margin: 0 0 10px; }
.mtx.mfs { position: fixed; inset: 0; z-index: 200; margin: 0; background: var(--paper); overflow: auto; padding: 3vh 4vw; display: grid; align-content: center; justify-items: center; gap: 2vh; }
.mtx.mfs .mfull { position: fixed; top: 14px; right: 16px; font-size: 1rem; padding: 8px 16px; }
.mtx.mfs .mcol { padding: 1.2vh 1.4vw; border-width: 3px; margin-left: -3px; }
.mtx.mfs .mp { font-size: clamp(1.3rem, 2.8vw, 2.8rem); padding: 0.2vh 0.8vw; }
.mtx.mfs .mbase { font-size: clamp(2.8rem, 6.5vw, 6.5rem); padding: 2vh 2.4vw; border-width: 5px; }
.mtx.mfs .mpath { font-size: clamp(1.1rem, 2.2vw, 2.1rem); text-align: center; }
.mtx.mfs .mlist { font-size: clamp(0.95rem, 1.6vw, 1.5rem); justify-content: center; max-width: 92vw; }
.mtx.mfs .mcards { display: none; }
body.mfs-on { overflow: hidden; }
.mx-open { font: inherit; font-size: 0.85rem; border: 1px solid var(--line); border-radius: 999px; padding: 4px 12px; background: var(--card); color: var(--ink); cursor: pointer; margin: 4px 0; }
"""

JS = """<script>(() => {
  const join = ps => ps.map(p => p.replace(/^-|-$/g, '')).join(' + ');
  function state(m) {
    const base = m.dataset.base, sel = [...m.querySelectorAll('.mp.on')].map(b => [+b.dataset.pos, b.dataset.p]);
    const pre = sel.filter(s => s[0] < 0).sort((a, b) => a[0] - b[0]).map(s => s[1]);
    const suf = sel.filter(s => s[0] > 0).sort((a, b) => a[0] - b[0]).map(s => s[1]);
    return pre.concat([base], suf);
  }
  function say(m) {
    const words = JSON.parse(m.querySelector('.mdata').textContent), path = state(m), out = m.querySelector('.mpath');
    m.querySelectorAll('.mw').forEach(b => b.classList.toggle('on', b.dataset.path === path.join('|')));
    if (path.length === 1) { out.textContent = 'Tap the parts to build a path, left to right. Any box can be skipped.'; return; }
    const w = words[path.join('|')];
    out.innerHTML = '<b>' + join(path) + '</b> ' + (w ? '&rarr; <span class="yes">' + w + '</span>: a word in this family.'
      : '<span class="test">is not in this family. Is it a word? Say it, use it in a sentence, check a dictionary.</span>');
  }
  document.addEventListener('click', e => {
    const p = e.target.closest('.mtx .mp'), w = e.target.closest('.mtx .mw');
    if (p) { const m = p.closest('.mtx'), on = !p.classList.contains('on');
      m.querySelectorAll(`.mp[data-pos="${p.dataset.pos}"]`).forEach(b => b.classList.remove('on')); p.classList.toggle('on', on); say(m); }
    if (w) { const m = w.closest('.mtx'), path = w.dataset.path.split('|'), base = m.dataset.base, i = path.indexOf(base);
      m.querySelectorAll('.mp').forEach(b => b.classList.remove('on'));
      path.forEach((k, n) => { if (n === i) return; const pos = n < i ? n - i : n - i;
        const b = m.querySelector(`.mp[data-pos="${pos}"][data-p="${CSS.escape(k)}"]`); if (b) b.classList.add('on'); });
      say(m); }
    const o = e.target.closest('.mx-open'); if (o) { const m = o.nextElementSibling; m.hidden = !m.hidden;
      o.textContent = m.hidden ? 'Show the matrix' : 'Hide the matrix'; }
  });
  // full screen for the board (24 November 2026): the matrix fills the window, and the browser's own full screen
  // where it allows one (an iPad does, an iPhone doesn't); Escape or the button again comes back
  const fsEl = () => document.fullscreenElement || document.webkitFullscreenElement;
  function board(m, on) {
    m.classList.toggle('mfs', on); document.body.classList.toggle('mfs-on', on);
    const b = m.querySelector('.mfull'); b.textContent = on ? 'Exit full screen' : 'Full screen'; b.setAttribute('aria-pressed', on);
    try {
      if (on && !fsEl()) (m.requestFullscreen || m.webkitRequestFullscreen || (() => {})).call(m);
      if (!on && fsEl()) (document.exitFullscreen || document.webkitExitFullscreen).call(document);
    } catch (e) {}
  }
  document.addEventListener('click', e => { const b = e.target.closest('.mtx .mfull'); if (b) { const m = b.closest('.mtx'); board(m, !m.classList.contains('mfs')); } });
  document.addEventListener('keydown', e => { const m = document.querySelector('.mtx.mfs'); if (m && e.key === 'Escape') board(m, false); });
  const left = () => { const m = document.querySelector('.mtx.mfs'); if (m && !fsEl()) board(m, false); };
  document.addEventListener('fullscreenchange', left); document.addEventListener('webkitfullscreenchange', left);
  // the family pages' switch: word sums or matrices, remembered in this browser
  document.querySelectorAll('.mx-switch').forEach(sw => {
    const cx = sw.closest('.cx'), bs = [...sw.querySelectorAll('button')];
    const set = v => { cx.classList.toggle('mtxview', v === 'matrix'); bs.forEach(b => b.setAttribute('aria-checked', b.dataset.v === v));
      try { localStorage.setItem('familyview', v); } catch (e) {} };
    bs.forEach(b => b.addEventListener('click', () => set(b.dataset.v)));
    let v = 'sums'; try { v = localStorage.getItem('familyview') || 'sums'; } catch (e) {}
    set(v);
  });
})();</script>"""
