"""The Parts layer (parts.html), made 10 November 2026: every analysed word, gathered by the parts it is built from.

A dictionary files words by their first letter, which scatters a part across the alphabet: the -ion words are under
a, c, d, n and every other letter. Here a part gathers its words, wherever it sits in them, each shown as a word sum,
so a teacher can pull up every word with -ion, or with re-, and see what stacks with what.

The word sums come from four places, in this order (a word keeps the first sum it gets):
- the root families (roots.py): *leg- and hap, with the meanings of their parts;
- the note family on the Words layer (landing.MORPH);
- the grade 3 word sum cards (word_sum_codes.py), as the manual's Word analysis tab writes them;
- every other marked word with a seam in its code: its parts are read off the seams, and the base is put back where
  the join changed it (mak + ing is make with its e dropped, gett + ing is get with its t doubled, carri + es is carry
  with its y turned to i). SUMS overrides a sum the seams can't give.

A word is in one of two states for now: marked (it has a code, so the Words layer can walk it) or sum only (its parts
and their meanings, with no marks yet). The joins (a doubled consonant, a dropped e, y turned to i, a prefix that
changes to match) are parts of a kind too: each lists the words it shapes.

Meanings are in our own words. Each part links to Etymonline's search for it, never to copied text."""
import html, json, re
from urllib.parse import quote
import doors

VOWELS = set("aeiouy")

# English affixes the families' glossary (roots.PARTS) doesn't have, in our own words.
MEANS = {
    "un-": "not, or the reverse of an action", "mis-": "wrongly, badly", "be-": "by, about, around: Old English <i>be-</i>",
    "a-": "on, in: Old English <i>an</i>, on", "out-": "out, beyond", "per-": "through, by: Latin <i>per</i>",
    "-s": "more than one; what he, she or it does; or belonging to, in <i>its</i>", "-es": "<i>-s</i> after a hissing sound, or after <i>o</i> and <i>y</i> turned to <i>i</i>",
    "-ed": "already happened", "-ing": "happening now; or the doing of it", "-y": "having, full of: Old English <i>-ig</i>",
    "-ly": "in that way; like", "-er": "more; or one who does it", "-est": "most", "-en": "make or become; or a past form",
    "-less": "without", "-ness": "the state of being", "-ate": "make, do; or a Latin past form", "-ion": "the act or result of",
    "-ic": "having to do with", "-ful": "full of, given to", "-th": "the number in order; or a state",
    "-able": "able to be", "ob-": "against, toward", "im-": "not, or into: Latin <i>in-</i>, written <i>im-</i> before m, b and p",
    "ex-": "out", "hap": "chance, luck", "note": "a mark", "ad-": "to, toward", "ab-": "away, from", "-ize": "make, do",
    "-ence": "the state of being", "-ance": "the act or state of", "-or": "one who, the thing that", "-ar": "like, having to do with",
    "per-": "through", "-ible": "able to be", "ple": "fold", "graph": "write", "phone": "sound, voice", "morph": "form", "-d": "<i>-ed</i> without its e, in <i>said</i>, <i>paid</i> and <i>laid</i>",
}
PREFIXES = {"un", "re", "mis", "be", "a", "out", "per", "dis", "de", "pre"}
SUFFIXES = {"s", "es", "ed", "ing", "y", "ly", "er", "est", "en", "less", "ness", "ate", "ion", "ic", "ful", "th", "al", "or", "ive", "able"}
# A prefix written another way before the root's first letter: the spelling, and the prefix it is.
ASSIM = {"ac-": "ad-", "as-": "ad-", "col-": "com-", "con-": "com-", "e-": "ex-", "intel-": "inter-", "di-": "dis-", "il-": "in-", "tra-": "trans-"}

JOINS = [
    ("double", "A consonant doubles", "The base ends in one vowel letter and one consonant, and the ending starts with a vowel. The "
     "consonant doubles so the box can keep the vowel short.", "steps/14.html", "Step 14"),
    ("e-drop", "The e drops", "The base ends in a silent <i>e</i> and the ending starts with a vowel. The <i>e</i> drops, and its "
     "jobs pass to the ending&rsquo;s vowel.", "steps/15.html", "Step 15"),
    ("y-to-i", "y turns to i", "The base ends in a consonant and <i>y</i>. Before an ending the <i>y</i> is written <i>i</i>, "
     "unless the ending starts with <i>i</i>.", "steps/29.html", "Step 29"),
    ("assim", "A prefix changes to match", "A Latin prefix takes the first letter of the root, or loses its own last letter, so "
     "the two are easier to say together. The doubled letter near the front of a word often marks this join.", None, None),
    ("f-to-v", "f turns to v", "A few words that end in <i>f</i> or <i>fe</i> write <i>v</i> before <i>-es</i>, as they are said.", None, None),
]

# A lesson that rides on a part: (heading, paragraphs). It opens the part's card, and Parts lists it under Lessons.
LESSONS = {
    "-ion": ("It&rsquo;s -ion, not -tion", [
        "The t in <i>action</i> belongs to <i>act</i>. The suffix is <b>-ion</b>: act + ion, collect + ion, product + ion. "
        "Taught as <i>-tion</i>, the base loses its last letter and its family goes out of sight: <i>ac</i> isn&rsquo;t the base, "
        "and <i>act</i> is: it is in <i>actor</i>, <i>active</i> and <i>react</i>.",
        "This is also why the letter before it varies. It is the base&rsquo;s own letter: t in act + ion, s in discuss + ion and "
        "tens(e) + ion. A speller who finds the base knows which letter to write, and one who memorizes <i>-tion</i> and "
        "<i>-sion</i> as endings has to guess.",
        "What the i does is join the letter before it. T and i together spell the sh sound, so the notation gives them one "
        "green bond bar across the seam, the t still black and the i still red. In <i>opinion</i> and <i>union</i> the i "
        "spells the y sound instead, and nothing before it changes.",
        "Where a verb ends in <i>-ate</i>, the longer ending is two parts with the e dropped: educat(e) + ion, "
        "notat(e) + ion. Where there is no such verb, as in inform + ation, English uses <i>-ation</i> whole.",
        "And <i>-ion</i> moves the stress to the syllable just before it: <b>ED</b>ucate, edu<b>CA</b>tion. More on that is "
        "with <a href=\"roots/deuk.html#shift-h\">produce and production</a>."]),
}
# The lessons the families carry, for the Parts page's list: (title, link, where).
FAMILY_LESSONS = [
    ("Stress tells the verb from the noun", "roots/deuk.html#stress-h", "*deuk-: produce, conduct"),
    ("An ending can move the stress", "roots/deuk.html#shift-h", "*deuk-: educate, education"),
    ("Duce or duct?", "roots/deuk.html#c-duct", "*deuk-: reduce, reduction"),
    ("A double at the front of a word", "roots/sem.html#front-h", "*sem-: assimilate, collect"),
    ("Accommodate: two doubles, two joins", "roots/med.html#accommodate-h", "*med-"),
    ("Does the double p show the seam?", "roots/hap.html#double-h", "hap: happy"),
    ("Letter pairs the seam splits", "roots/hap.html#pairs-h", "hap: mishap, haphazard"),
    ("Lig or lect?", "roots/leg.html#c-lig", "*leg-: eligible, elect"),
]

# Sums the seams can't give, or give wrongly: word -> parts as the sum writes them ("(e)" a dropped letter).
SUMS = {
    "being": ["be", "-ing"], "into": ["in", "to"], "today": ["to", "day"], "myself": ["my", "self"],
    "notate": ["not(e)", "-ate"], "notation": ["not(e)", "-at(e)", "-ion"], "legomorphic": ["leg", "-o", "morph", "-ic"],
    "action": ["act", "-ion"], "actor": ["act", "-or"], "active": ["act", "-ive"], "react": ["re-", "act"],
    "creation": ["creat(e)", "-ion"], "creator": ["creat(e)", "-or"],
    "teaching": ["teach", "-ing"], "hoping": ["hop(e)", "-ing"], "diving": ["div(e)", "-ing"],
    "flossing": ["floss", "-ing"], "sniffing": ["sniff", "-ing"], "jazzy": ["jazz", "-y"], "said": ["say>i", "-d"],
    "knives": ["knife>ve", "-s"], "wives": ["wife>ve", "-s"], "wolves": ["wolf>v", "-es"], "leaves": ["leaf>v", "-es"],
}
# Misspellings the decks draw on purpose, to show what a rule prevents: not words.
NOT_WORDS = {"flosing", "kising", "snifing", "jazy"}


def reconcile(word, parts):
    """Where a sum's parts don't add up to the word as they stand, write the join in: mak(e) + ing, cut+t + ing,
    carry>i + ed, and -y>i for a y written i inside the word."""
    if any(c in p for p in parts for c in "(+>"): return parts
    bs = [p.strip("-") for p in parts]
    if "".join(bs) == word: return parts
    out, pos = [], 0
    for i, (p, b) in enumerate(zip(parts, bs)):
        nxt = bs[i + 1] if i + 1 < len(bs) else None
        rest = word[pos:]
        cands = [(b, p)]
        if nxt is not None:
            if b[-1] not in VOWELS: cands.append((b + b[-1], p + "+" + b[-1]))
            if b.endswith("e") and len(b) > 1: cands.append((b[:-1], p[:len(p) - 1 - p.endswith("-")] + "(e)"))
            if b.endswith("y") and len(b) > 1: cands.append((b[:-1] + "i", p + ">i"))
        if b == "y" and nxt is not None: cands.insert(0, ("i", p + ">i")) if rest.startswith("i") else None
        ok = lambda after: nxt is None or after[:1] == nxt[:1] or (nxt[:1] == "y" and after[:1] == "i")
        hit = next(((s, w) for s, w in cands if rest.startswith(s) and ok(rest[len(s):]) and (nxt is not None or s == rest)), None)
        if not hit: return parts
        out.append(hit[1]); pos += len(hit[0])
    return out


def key_of(p): return p.replace("(", "").replace(")", "")
def kind_of(p): return "pre" if p.endswith("-") else "suf" if p.startswith("-") else "base"
def pid(key):
    k = key.strip("-")
    return "p-" + ("pre-" if key.endswith("-") else "suf-" if key.startswith("-") else "") + re.sub(r"[^a-z0-9]+", "-", k.lower()).strip("-")
def bare(p): return p.strip("-")
def shown(p): return html.escape(bare(p))


def from_seams(word, pieces, known):
    """Parts read off a code's seams, with the base put back where the join changed it. Returns (parts, joins)."""
    parts, joins = [], set()
    for i, p in enumerate(pieces):
        nxt = pieces[i + 1] if i + 1 < len(pieces) else ""
        last = i == len(pieces) - 1
        if i == 0 and len(pieces) > 1 and p in PREFIXES and nxt not in SUFFIXES: parts.append(p + "-"); continue
        if i > 0 and p in SUFFIXES: parts.append("-" + p); continue
        if i > 0 and p == "i" and not last: parts.append("-y>i"); joins.add("y-to-i"); continue      # happ + i + ly
        if not last and nxt[:1] in VOWELS:
            if len(p) > 2 and p[-1] == p[-2] and p[-1] not in VOWELS and (p[:-1] in known or p not in known):
                parts.append(p[:-1] + f"+{p[-1]}"); joins.add("double"); continue
            if p + "e" in known and p not in known: parts.append(p + "(e)"); joins.add("e-drop"); continue
        if not last and p.endswith("i") and p[:-1] + "y" in known:
            parts.append(p[:-1] + "y>i"); joins.add("y-to-i"); continue
        parts.append(p)
    return parts, joins


def collect(X):
    """Every analysed word: {word: {"parts": [...], "joins": set, "home": (url, label) or None, "mean": str}}."""
    import roots, word_sum_codes as WSC, walk
    LW = X["LW"]
    words, means = {}, dict(MEANS)
    for k, v in roots.PARTS.items(): means.setdefault(k, v)
    root_means = dict(roots.ROOT_PARTS)
    known = {w.lower() for w in LW.W} | {w.lower() for w in X["list_words"]}

    def add(word, parts, joins=(), home=None, mean=""):
        if word in words or word in NOT_WORDS: return
        parts = reconcile(word, parts)
        js = set(joins)
        for p in parts:
            if "(" in p: js.add("e-drop")
            if "+" in p: js.add("double")
            if p.endswith(">i"): js.add("y-to-i")
            if p.endswith((">ve", ">v")): js.add("f-to-v")
            if p in ASSIM: js.add("assim")
        words[word] = {"parts": parts, "joins": js, "home": home, "mean": mean}

    for R in roots.ROOTS:
        home = lambda w, R=R: (f"roots/{R['slug']}.html#{doors.word_id(w)}", R["label"])
        if R.get("clusters"):
            for c, w, parts, mean, bold in roots.cluster_words(R):
                if parts: add(w, list(parts), home=home(w), mean=mean)
        else:
            for _, _, ws in R["branches"]:
                for w, parts, sp, mean in ws:
                    if not parts: continue
                    out, js = [], set()
                    for i, p in enumerate(parts):
                        if p == "happ": out.append("hap+p"); js.add("double")
                        elif p == "i": out.append("-y>i"); js.add("y-to-i")
                        elif i == 0 and p in PREFIXES and len(parts) > 1: out.append(p + "-")
                        elif i > 0 and p in SUFFIXES: out.append("-" + p)
                        else: out.append(p)
                    add(w, out, js, home(w), mean)
    for w, parts in SUMS.items():
        add(w, parts)
    for _, _, items in WSC.SECTIONS:
        for item in items:
            s, w = item[0], item[1]
            pieces = [x.strip() for x in s.split("→")[0].split("+")]
            out, js = [], set()
            for i, p in enumerate(pieces):
                if i > 0 and len(p) == 1 and p not in VOWELS and out and bare(key_of(out[-1])).endswith(p) and i < len(pieces) - 1:
                    out[-1] = out[-1] + "+" + p; js.add("double")
                elif i > 0 and key_of(p) in SUFFIXES: out.append("-" + p)
                elif i == 0 and p in PREFIXES and len(pieces) > 1 and key_of(pieces[1]) not in SUFFIXES: out.append(p + "-")
                else: out.append(p)
            add(w, out, js)
    for w in sorted(LW.W):
        if w in words or w in X["SC"].UNMARKED or " " in w or "-" in w or "'" in w: continue
        try: pieces = walk.facts(LW, w)["parts"]
        except Exception: continue
        if len(pieces) < 2: continue
        parts, js = from_seams(w, pieces, known)
        add(w, parts, js)
    return words, means, root_means


def split_part(p):
    """A sum's part as (key, what the sum shows): hap+p is the base hap, shown hap + p; mak(e) is make; carry>i is carry."""
    if "+" in p: b, d = p.split("+"); return b, f"{html.escape(b)} + {html.escape(d)}"
    if ">" in p:
        b, d = p.split(">"); k = b.strip("-")
        if d == "ve": return b, f"{html.escape(k[:-2])}(f&rarr;v)e"
        if d == "v": return b, f"{html.escape(k[:-1])}(f&rarr;v)"
        return b, f"{html.escape(k[:-1])}(y&rarr;i)" if len(k) > 1 else "y&rarr;i"
    return key_of(p), shown(p)


def sum_buttons(parts, cur=None, root=None):
    """A sum's parts as buttons the page's script (pop_js) opens: the part's meaning and the other words that have it."""
    out = []
    for p in parts:
        k, s = split_part(p)
        cls = "part" + (" cur" if cur is not None and k == cur else "") + (" root" if root is not None and k == root else "")
        out.append(f'<button type="button" class="{cls}" data-p="{html.escape(k)}">{s}</button>')
    return '<span class="pl"> + </span>'.join(out)


def pop_js(up=""):
    """Tap a part anywhere outside a family's own explorer and the walk: a card under the word, from parts.json."""
    return """<script>(() => {
  const UP = '%s'; let data = null, card = null;
  document.addEventListener('click', async e => {
    const a = e.target.closest('.gpop a[data-close]'); if (a) { e.preventDefault(); close(); return; }
    const b = e.target.closest('.part[data-p]'); if (!b || b.closest('.cx, .walk')) return;
    e.preventDefault();
    if (b.classList.contains('sel')) { close(); return; }
    if (!data) { try { data = await (await fetch(UP + 'parts.json')).json(); } catch (err) { data = {}; } }
    const k = b.dataset.p, d = data[k]; close(); if (!d) return;
    const host = b.closest('li, .wsum, p, div'), own = host.dataset.w || '';
    const others = d.w.filter(w => w !== own), few = others.slice(0, 14), esc = s => s.replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
    card = document.createElement('div'); card.className = 'pcard gpop';
    card.innerHTML = '<p><b>' + esc(k) + '</b>' + (d.m ? ' ' + d.m + '.' : '') + '</p>'
      + (others.length ? '<p class="pin">' + (own ? 'Also in ' : 'In ') + few.map(w => '<a href="' + UP + 'walk.html?w=' + encodeURIComponent(w) + '">' + esc(w) + '</a>').join(', ')
        + (others.length > few.length ? ', and ' + (others.length - few.length) + ' more' : '') + '.</p>' : '')
      + '<p class="pin"><a href="' + UP + esc(d.u) + '">See it in Parts</a></p>';
    host.appendChild(card); b.classList.add('sel');
  });
  function close() { if (card) card.remove(); card = null; document.querySelectorAll('.part.sel').forEach(x => { if (!x.closest('.cx, .walk')) x.classList.remove('sel'); }); }
})();</script>""" % up


def sum_html(word, parts, bold=None):
    bits = []
    for p in parts:
        k, s = split_part(p)
        bits.append(f"<b>{s}</b>" if bold is not None and k == bold else s)
    return " + ".join(bits) + f" &rarr; <i>{html.escape(word)}</i>"


def write(OUT, door_page, X):
    import roots
    LW = X["LW"]
    words, means, root_means = collect(X)
    root_spells = {s for R in roots.ROOTS for c in R.get("clusters", []) for s in c["spells"]} | {"hap"}
    index, joined = {}, {j[0]: [] for j in JOINS}
    for w, d in words.items():
        for pos, p in enumerate(d["parts"]):
            k, _ = split_part(p)
            e = index.setdefault(k, {"kind": "root" if k in root_spells else kind_of(k), "words": []})
            if w not in [x[0] for x in e["words"]]:
                e["words"].append((w, "start" if pos == 0 else "end" if pos == len(d["parts"]) - 1 else "middle"))
        for j in d["joins"]: joined[j].append(w)

    on_steps = X.get("step_parts", {})                    # parts the manual places on the route: each gets a card
    for k in on_steps:
        index.setdefault(k, {"kind": "root" if k in root_spells else kind_of(k), "words": []})
    marked = lambda w: (w in LW.W or w in X["SC"].VARIANTS) and w not in X["SC"].UNMARKED
    def word_link(w):
        d = words[w]
        if marked(w): return f'walk.html?w={quote(w)}'
        return d["home"][0] if d["home"] else None
    def word_li(w, bold=None):
        d, u = words[w], word_link(w)
        wd = f'<i>{html.escape(w)}</i>'
        s = sum_buttons(d["parts"], bold) + ' <span class="to">&rarr;</span> ' + (f'<a href="{u}">{wd}</a>' if u else wd)
        state = "" if marked(w) else ' <span class="pstate">sum only</span>'
        mean = f' <span class="pmean t-only">{d["mean"]}</span>' if d["mean"] else ""
        return f'<li data-w="{html.escape(w)}">' + s + state + mean + "</li>"

    def with_it(k):
        """The other affixes this part is found beside, most often first."""
        c = {}
        for w, _ in index[k]["words"]:
            for p in words[w]["parts"]:
                k2, _ = split_part(p)
                if k2 != k and kind_of(k2) != "base": c[k2] = c.get(k2, 0) + 1
        return sorted(c, key=lambda x: (-c[x], x))[:6]

    def card(k):
        e = index[k]
        ws = sorted(e["words"], key=lambda x: (len(words[x[0]]["parts"]), x[0]))
        mean = root_means.get(k) or means.get(k, "")
        if k in ASSIM: mean = mean or f"Latin <i>{ASSIM[k]}</i>, written another way"
        if not mean and e["kind"] == "base" and len(ws) == 1 and ws[0][0] == k: mean = ""
        n = len(ws)
        stack = with_it(k) if e["kind"] in ("pre", "suf") else []
        stacks = (f'<p class="pwith t-only">Found beside: ' + ", ".join(f'<a href="#{pid(x)}">{html.escape(x)}</a>' for x in stack) + ".</p>") if stack else ""
        if k in on_steps:
            stacks += '<p class="pwith">On the route: ' + ", ".join(f'<a href="steps/{n:02d}.html#parts">Step {n}</a>' for n in on_steps[k]) + ".</p>"
        src = f'<p class="psrc t-only"><a href="https://www.etymonline.com/search?q={quote(k)}">Its history in Etymonline</a></p>'
        lesson = ""
        if k in LESSONS:
            lh, lp = LESSONS[k]
            lesson = f'<div class="plesson" id="lesson-{pid(k)[2:]}"><h3>{lh}</h3>{"".join(f"<p>{x}</p>" for x in lp)}</div>'
        return (f'<details class="ppart" id="{pid(k)}" data-k="{html.escape(bare(k))}" data-words="{html.escape(" ".join(w for w, _ in ws))}">'
                f'<summary><b>{html.escape(k)}</b>{f"<span class=pm>{mean}</span>" if mean else ""}<span class="pcnt">{n} {"word" if n == 1 else "words"}</span></summary>{lesson}'
                f'<ul class="pwords">{"".join(word_li(w, k) for w, _ in ws)}</ul>{stacks}{src}</details>')

    groups = [("pre", "Prefixes", "Before the base."), ("suf", "Suffixes", "After the base. One word can stack several."),
              ("root", "Roots", "A root can have several spellings. Its family page gathers them."),
              ("base", "Bases", "A word, or a part that carries the main meaning, that other parts join.")]
    secs = []
    for kind, head, sub in groups:
        ks = sorted((k for k, e in index.items() if e["kind"] == kind and not (kind == "base" and len(e["words"]) < 2 and k not in on_steps)),
                    key=lambda k: (-len(index[k]["words"]), bare(k)))
        if not ks: continue
        secs.append(f'<section class="about pgroup" id="g-{kind}" aria-labelledby="g-{kind}-h"><div class="wrap">'
                    f'<h2 id="g-{kind}-h">{head}</h2><p class="sub t-only">{sub}</p><div class="plist">{"".join(card(k) for k in ks)}</div></div></section>')
    jcards = []
    for jid, head, what, u, ulabel in JOINS:
        ws = sorted(joined[jid])
        if not ws: continue
        step = f' <a href="{u}">{ulabel}</a> teaches it, with Carney&rsquo;s pages.' if u else ""
        jcards.append(f'<details class="ppart" id="j-{jid}" data-k="{html.escape(head.lower())}" data-words="{html.escape(" ".join(ws))}">'
                      f'<summary><b>{head}</b><span class="pcnt">{len(ws)} {"word" if len(ws) == 1 else "words"}</span></summary>'
                      f'<p class="pwhat t-only">{what}{step}</p><ul class="pwords">{"".join(word_li(w) for w in ws)}</ul></details>')
    secs.append(f'<section class="about pgroup" id="g-join" aria-labelledby="g-join-h"><div class="wrap"><h2 id="g-join-h">Joins</h2>'
                f'<p class="sub t-only">What happens to the spelling where two parts meet.</p><div class="plist">{"".join(jcards)}</div></div></section>')

    X["part_sums"] = {w: d["parts"] for w, d in words.items()}
    fams = "".join(f'<a class="dtile" href="roots/{R["slug"]}.html"><b>{R["root"]}</b><span>{R["gloss"]}</span></a>' for R in roots.ROOTS)
    fams += '<a class="dtile" href="explorations.html#note-family"><b>note</b><span>note, notate, notation</span></a>'
    n_sum = sum(1 for w in words if not marked(w))
    body = f"""<section class="hero door-hero"><div class="wrap">
<h1>Parts</h1>
<p class="lead t-only">A dictionary files words by their first letter, which scatters a part across the alphabet. Here each part gathers its words, wherever it sits in them, so the meaning they share shows.</p>
<form class="pfilter" role="search" autocomplete="off" hidden><label class="sr" for="pf">Find a part or a word</label>
<input id="pf" type="search" placeholder="Find a part or a word: ion, re, happy" spellcheck="false" autocapitalize="off"><span class="pcount" aria-live="polite"></span></form>
<p class="sub t-only">{len(words)} words are taken apart so far, {n_sum} of them as a word sum only, with no marks yet. A word that&rsquo;s marked opens in <a href="walk.html">Words</a>.</p>
</div></section>
<section class="about" id="families" aria-labelledby="fam-h"><div class="wrap">
<h2 id="fam-h">Families</h2>
<p class="sub t-only">A root or base with all its words gathered, however each is spelled.</p>
<div class="door-tiles">{fams}</div>
<p class="t-only"><a href="derivations.html">Where the roots come from, and the sources they cite</a>.</p>
</div></section>
<section class="about" id="lessons" aria-labelledby="les-h"><div class="wrap">
<h2 id="les-h">Lessons</h2>
<p class="sub t-only">What a part or a family teaches about spelling, each with its words.</p>
<ul class="plessons">{"".join(f'<li><a href="#{pid(k)}">{LESSONS[k][0]}</a> <span>{html.escape(k)}</span></li>' for k in LESSONS)}{"".join(f'<li><a href="{u}">{t}</a> <span>{html.escape(w)}</span></li>' for t, u, w in FAMILY_LESSONS)}</ul>
</div></section>
{"".join(secs)}
<section class="about t-only"><div class="wrap">
{X["uc"]("the parts come from the words analysed so far: the route, the grade 3 word sums and the first families. Next: more families, starting with <i>accommodate</i> and the prefix <i>com-</i>, and a search by where a part sits in the word.")}
</div></section>
{PARTS_JS}{pop_js()}"""
    door_page("parts", "Parts · Sound and Word Atlas", "Every analysed word, gathered by the parts it is built from.", body)

    # for the Words layer: each word's sum, part by part, and for the search: every part
    sums = {}
    for w, d in words.items():
        row = []
        for p in d["parts"]:
            k, s = split_part(p)
            row.append({"s": s, "k": k, "r": int(index[k]["kind"] == "root"), "u": f"parts.html#{pid(k)}", "m": re.sub(r"<[^>]+>", "", html.unescape(root_means.get(k) or means.get(k, "")))})
        sums[w] = {"parts": row, "mean": re.sub(r"<[^>]+>", "", html.unescape(d["mean"])), "home": d["home"]}
    # for the popup on a word's sum (Words): each part's meaning and the words that share it
    pop = {k: {"m": root_means.get(k) or means.get(k, "") or (f"Latin <i>{ASSIM[k]}</i>, written another way" if k in ASSIM else ""),
               "u": f"parts.html#{pid(k)}", "w": sorted(w for w, _ in e["words"])} for k, e in index.items()}
    (OUT / "parts.json").write_text(json.dumps(pop, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    recs = [(k, f"parts.html#{pid(k)}", {"pre": "Prefix", "suf": "Suffix", "root": "Root", "base": "Base"}[e["kind"]] + f", {len(e['words'])} words")
            for k, e in index.items() if not (e["kind"] == "base" and len(e["words"]) < 2 and k not in on_steps)]
    print(f"wrote parts.html | {len(words)} words, {n_sum} sum only, {len(index)} parts")
    return {"sums": sums, "search": recs, "marked": marked}


PARTS_JS = """<script>(() => {
  const f = document.querySelector('.pfilter'); if (!f) return;
  const q = f.querySelector('input'), count = f.querySelector('.pcount'), parts = [...document.querySelectorAll('details.ppart')];
  f.hidden = false; f.addEventListener('submit', e => e.preventDefault());
  const norm = s => s.toLowerCase().replace(/[^a-z]/g, '');
  function run() {
    const t = norm(q.value); let n = 0;
    parts.forEach(d => {
      const k = norm(d.dataset.k), ws = d.dataset.words.split(' ');
      const hit = !t || k === t || k.startsWith(t) || ws.includes(t);
      d.hidden = !hit; if (t) d.open = hit && (k === t || ws.includes(t)); if (hit) n++;
      d.querySelectorAll('li').forEach(li => li.classList.toggle('hit', !!t && li.dataset.w === t));
    });
    document.querySelectorAll('.pgroup').forEach(s => { s.hidden = !s.querySelector('details.ppart:not([hidden])'); });
    count.textContent = t ? n + (n === 1 ? ' part' : ' parts') : '';
  }
  q.addEventListener('input', run);
  // a link to a part opens it
  const open = () => { const d = location.hash && document.getElementById(location.hash.slice(1)); if (d && d.tagName === 'DETAILS') { d.open = true; d.scrollIntoView({block: 'start'}); } };
  addEventListener('hashchange', open); open();
})();</script>"""
