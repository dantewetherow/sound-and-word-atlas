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


def build(base, sums, label=None):
    """base: the part's key ('tect'); sums: [(word, [part, ...])], parts as the sums write them ('pro-', 'tect',
    '-ion', '-at(e)'). Returns the matrix's html, or '' if no word adds anything to the base."""
    cols, words = {}, {}
    for w, parts in sums:
        ks = [_key(p) for p in parts]
        try: i = next(n for n, k in enumerate(ks) if k.strip("-") == base)
        except StopIteration: continue
        pre, suf = ks[:i], ks[i + 1:]
        if not pre and not suf: continue
        for d, k in enumerate(reversed(pre), 1): cols.setdefault(-d, {}).setdefault(k, set()).add(w)
        for d, k in enumerate(suf, 1): cols.setdefault(d, {}).setdefault(k, set()).add(w)
        words["|".join(pre + [base] + suf)] = w
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
            f'<div class="mgrid">{pre}<div class="mcol mbase"><span>{html.escape(base)}</span></div>{suf}</div>'
            f'<p class="mpath" aria-live="polite">Tap the parts to build a path, left to right. Any box can be skipped.</p>'
            f'<div class="mlist"><span>Words in it:</span> {chips}</div>'
            f'<script type="application/json" class="mdata">{data}</script></div>')


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
