"""Build a sentence (13 November 2026): the builder at the top of the Sentences page.

Five slots in a row, each a marked word or two that a learner steps through, as on the word walk: an actor (I, you,
she, the dog), an operator (can, could, will, do, did), an action (go, see, play) and, if wanted, a preposition (in,
over, under; 13 November 2026) and where or what (here, there, home, the ball). Flip moves the operator in front of the actor, and the claim becomes a question: She could go. Could
she go? A second switch adds not, then squeezes it to n't, which travels with the operator when it flips: Could she not
go? Couldn't she go? The words are the high-frequency words of the Early Literacy Profile (Central Okanagan) and Dolch,
grammar words and nouns both, and each is drawn marked, in capitals where it starts the sentence.

The operator frame keeps the action bare (she could go, never she could goes), so every combination is a sentence,
though not every one is sensible: a silly sentence checks that a learner is reading, not guessing. The one agreement to
watch is do and does, and the board says so when they don't match.

Everything the builder shows is drawn at build time; the page's script only reorders it."""
import html, json

# words the site hadn't marked yet
CODES = {"mom": "c.m s.o c.m", "ball": "c.b b.a k.ll", "fish": "c.f s.i g.sh", "box": "c.b s.o c.x"}

SLOTS = [
    ("actor", "Actor", ["I", "you", "she", "he", "we", "they", "it", "the dog", "my mom", "a fish"]),
    ("operator", "Operator", ["can", "could", "will", "would", "should", "may", "might", "must", "do", "does", "did"]),
    ("action", "Action", ["go", "see", "run", "play", "jump", "help", "eat", "come", "look", "find", "get", "sit", "stop", "ride", "swim", "sing"]),
    ("prep", "Preposition", ["", "in", "on", "up", "down", "over", "under", "out", "off", "by", "with", "to", "into"]),
    ("rest", "Where or what", ["", "here", "there", "home", "it", "me", "the ball", "the box"]),
]
NT = {"can": "can’t", "could": "couldn’t", "would": "wouldn’t", "should": "shouldn’t", "will": "won’t", "do": "don’t",
      "does": "doesn’t", "did": "didn’t"}
ONE = {"she", "he", "it", "the dog", "my mom", "a fish"}      # actors that take does


def cap_code(code):
    """The code with its first letter made a capital: g.sh l.e -> g.Sh l.e."""
    toks = code.split(" ")
    for i, t in enumerate(toks):
        if "." in t:
            k, v = t.split(".", 1)
            toks[i] = f"{k}.{v[0].upper()}{v[1:]}"
            break
    return " ".join(toks)


def section(X, code_of):
    """The builder's section. code_of(word) gives a word's code."""
    words = {w for _, _, opts in SLOTS for o in opts for w in o.split()} | {"not"} | set(NT.values())
    svg = {}
    for w in sorted(words):
        c = CODES.get(w) or code_of(w)
        assert c, f"builder: no code for {w}"
        lo = X["svg_of"](w, 56, code=c, label=w)
        up = lo if w == "I" else X["svg_of"](w[0].upper() + w[1:], 56, code=cap_code(c), label=w[0].upper() + w[1:])
        svg[w] = [lo, up]
    data = {"slots": [{"key": k, "label": lab, "options": opts} for k, lab, opts in SLOTS], "nt": NT, "one": sorted(ONE)}
    start = {"actor": 2, "operator": 1, "action": 0, "prep": 0, "rest": 0}      # she could go
    tiles = "".join(f'<div class="sb-slot" data-slot="{k}" data-i="{start[k]}"><div class="sb-word" aria-live="polite"></div>'
                    f'<div class="sb-step"><button type="button" class="sb-prev" aria-label="Previous {lab.lower()}">&#8249;</button>'
                    f'<span class="sb-role">{lab}</span><button type="button" class="sb-next" aria-label="Next {lab.lower()}">&#8250;</button></div></div>'
                    for k, lab, _ in SLOTS)
    return f"""<section class="about" id="build" aria-labelledby="sb-h"><div class="wrap">
<h2 id="sb-h">Build a sentence</h2>
<p class="sub t-only">Step through the words in each slot with the arrows. Flip turns the claim into a question. The second button adds <i>not</i>, then squeezes it to <i>n&rsquo;t</i>.</p>
<div class="sb" data-flip="0" data-neg="0">
  <div class="sb-line">{tiles}<div class="sb-slot sb-neg" hidden><div class="sb-word"></div><div class="sb-step sb-spacer" aria-hidden="true"></div></div><span class="sb-end">.</span></div>
  <p class="sb-say" aria-live="polite"></p>
  <p class="sb-hint" aria-live="polite"></p>
  <div class="sb-tools">
    <button type="button" class="sb-flip">Flip</button>
    <button type="button" class="sb-not">Add <i>not</i></button>
    <button type="button" class="sb-mix">Mix it up</button>
  </div>
</div>
<div class="t-only prose sb-notes">
<p><b>What it practises.</b> The small words that carry most sentences, pronouns and operators, read with high-frequency actions and nouns in a sentence, not a list. Every word is marked, and the first word takes a capital.</p>
<p><b>A routine.</b> Build a claim and read it. Flip it and read the question. Swap one word and read again. Then ask a learner to build one that&rsquo;s true about them. Silly sentences are welcome: <i>A fish could ride.</i> They show a learner is reading, not guessing.</p>
<p><b>The grammar.</b> An actor, an operator and an action make a claim. A question in English puts the operator in front of the actor. Because the operator carries the tense and the agreement, the action stays bare: <i>she could go</i>, never <i>she could goes</i>. That is why every combination here is a sentence. A claim with no operator (<i>She goes.</i>) borrows <i>do</i> to ask: <i>Does she go?</i> The one agreement to watch is <i>do</i> and <i>does</i>: <i>does</i> goes with one actor that isn&rsquo;t <i>I</i> or <i>you</i>.</p>
<p><b>Prepositions.</b> A preposition places the action: <i>She could go in there. She could go over here.</i> Most want something after them, a place or a thing: <i>in there</i>, <i>under the box</i>. A few can stand alone after the action, where they change what it means: <i>go up</i>, <i>get out</i>, <i>sit down</i>. <i>Home</i> needs no preposition: <i>go home</i>, not <i>go to home</i>. Let learners find that one by ear.</p>
<p><b><i>Not</i> and <i>n&rsquo;t</i>.</b> <i>Not</i> stays behind the actor when the sentence flips: <i>Could she not go?</i> Squeezed to <i>n&rsquo;t</i>, it joins the operator and travels with it: <i>Couldn&rsquo;t she go?</i> <i>May</i>, <i>might</i> and <i>must</i> stop at <i>not</i> here: <i>mayn&rsquo;t</i> and <i>mightn&rsquo;t</i> are rare now. The squeeze is on <a href="contractions.html">Squeezed into oblivion</a>.</p>
</div>
</div></section>
<script>(() => {{
  const D = {json.dumps(data, ensure_ascii=False)}, SVG = {json.dumps(svg, ensure_ascii=False)};
  const box = document.querySelector('.sb'), line = box.querySelector('.sb-line'), negEl = box.querySelector('.sb-neg'), end = box.querySelector('.sb-end');
  const slots = Object.fromEntries([...box.querySelectorAll('.sb-slot[data-slot]')].map(s => [s.dataset.slot, s]));
  const opts = Object.fromEntries(D.slots.map(s => [s.key, s.options]));
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const pick = k => opts[k][+slots[k].dataset.i];
  const draw = (phrase, first) => phrase.split(' ').map((w, j) => `<span class="sb-w">${{SVG[w][first && j === 0 ? 1 : 0]}}</span>`).join('');
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  function render(animate) {{
    const before = animate && !still ? new Map([...line.children].map(e => [e, e.getBoundingClientRect()])) : null;
    const flip = box.dataset.flip === '1', neg = +box.dataset.neg, op = pick('operator');
    const canNt = op in D.nt;
    const n = neg === 2 && !canNt ? 1 : neg, opWord = n === 2 ? D.nt[op] : op;     // may, might and must keep not
    const order = flip ? ['operator', 'actor', 'action', 'prep', 'rest'] : ['actor', 'operator', 'action', 'prep', 'rest'];
    order.forEach(k => line.appendChild(slots[k]));
    // not: after the operator in a claim, after the actor in a question; n't rides on the operator
    negEl.hidden = n !== 1;
    if (n === 1) line.insertBefore(negEl, slots[flip ? 'actor' : 'operator'].nextSibling);
    negEl.querySelector('.sb-word').innerHTML = draw('not', false);
    line.appendChild(end);
    end.textContent = flip ? '?' : '.';
    order.forEach((k, j) => {{
      const w = k === 'operator' ? opWord : pick(k);
      slots[k].querySelector('.sb-word').innerHTML = w ? draw(w, j === 0) : '<span class="sb-empty">&mdash;</span>';
      slots[k].classList.toggle('blank', !w);
    }});
    const words = order.map(k => k === 'operator' ? opWord : pick(k)).filter(Boolean);
    if (n === 1) words.splice(2, 0, 'not');
    box.querySelector('.sb-say').textContent = cap(words.join(' ')) + (flip ? '?' : '.');
    const act = pick('actor'), one = D.one.includes(act);
    box.querySelector('.sb-hint').textContent =
      op === 'does' && !one ? '“Does” goes with one actor: she, he, it, the dog. Try “do”.' :
      op === 'do' && one ? '“Do” goes with I, you, we and they. Try “does”.' : '';
    box.querySelector('.sb-not').innerHTML = neg === 0 ? 'Add <i>not</i>' : neg === 1 && canNt ? 'Squeeze to <i>n&rsquo;t</i>' : 'Take out <i>not</i>';
    if (before) [...line.children].forEach(e => {{
      const a = before.get(e); if (!a || e.hidden) return;
      const b = e.getBoundingClientRect(), dx = a.left - b.left, dy = a.top - b.top;
      if (dx || dy) e.animate([{{ transform: `translate(${{dx}}px, ${{dy}}px)` }}, {{ transform: 'none' }}], {{ duration: 420, easing: 'cubic-bezier(.2,.7,.2,1)' }});
    }});
  }}
  box.addEventListener('click', e => {{
    const s = e.target.closest('.sb-slot'), prev = e.target.closest('.sb-prev'), next = e.target.closest('.sb-next');
    if (s && (prev || next)) {{ const k = s.dataset.slot, len = opts[k].length; s.dataset.i = (+s.dataset.i + (next ? 1 : len - 1)) % len; render(false); }}
    if (e.target.closest('.sb-flip')) {{ box.dataset.flip = box.dataset.flip === '1' ? '0' : '1'; render(true); }}
    if (e.target.closest('.sb-not')) {{ const n = +box.dataset.neg, canNt = pick('operator') in D.nt; box.dataset.neg = n === 0 ? 1 : n === 1 && canNt ? 2 : 0; render(true); }}
    if (e.target.closest('.sb-mix')) {{
      for (const k in slots) {{ const len = opts[k].length; slots[k].dataset.i = Math.floor(Math.random() * len); }}
      const op = pick('operator'), one = D.one.includes(pick('actor'));
      if ((op === 'does' && !one) || (op === 'do' && one)) slots.operator.dataset.i = opts.operator.indexOf(op === 'does' ? 'do' : 'does');
      render(false);
    }}
  }});
  render(false);
}})();</script>"""
