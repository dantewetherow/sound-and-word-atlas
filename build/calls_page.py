"""Marking calls (calls.html), 21 November 2026: every place the marks rest on a choice, in one page, for Dante to rule on.

Three parts. A: the calls made on 21 November with the schwa and borrowed-sound marks, each drawn as the site marks it
with the other reading drawn beside it. B: the marking rules still to decide, drawn the same way. C: the older calls,
gathered from the CALLS lists in site_codes.py, dolch_codes.py, hop_hope_codes.py and word_sum_codes.py (which until now
pointed to the Marking calls tab of the manual), each with its status: open, ruled, or settled by a later ruling.

When Dante rules on one, change the code, move the call to C with its date, and rebuild."""
import html, re

# (id, title, question, [(word, code or None for the site's own, caption)], [(word, code, caption)], note)
NEW = [
    ("A1", "ee over every final y", "Keep the small ee over a y that says e's name at the end of a word?",
     [("happy", None, "the y borrows e's name"), ("city", None, "")],
     [("happy", "c.h s.a x.pp + | b.y ; bv 3>2", "the y bare, as before")],
     "It follows the rule (a vowel saying another vowel's sound shows that sound), and it is the biggest visible change: "
     "every <i>happy</i>, <i>city</i>, <i>very</i> and <i>funny</i> carries it. The other reading treats y saying ee at the "
     "end of a word as y's own sound, which most programs teach as a rule of its own."),
    ("A2", "was: ah, u, or weak and strong", "Which sound does the a of was borrow, and does was need a weak form beside it, as the, a and to have?",
     [("was", None, "ah, from the pronouncing dictionary")],
     [("was", "c.w b.a c.s ; says 1 u", "u, as in wuz"),
      ("was", "c.w b.a c.s ; schwa 1", "weak: it was raining"),
      ("was", "c.w b.a c.s ; says 1 ah", "strong: yes, it WAS")],
     "Merriam-Webster gives both full sounds. Ah pairs <i>was</i> with <i>want</i>, <i>wash</i> and <i>watch</i>, the wa "
     "pattern; u is what many Canadians say when the word is stressed. <i>What</i> is marked u already. Most of the time "
     "<i>was</i> is said weakly, with a &#601;, and takes a full vowel only when it ends a phrase or is stressed to make a "
     "point. The last two readings show it as a weak and strong pair, the way the word walk shows <i>the</i>, <i>a</i> and <i>to</i>.", ("As marked now", "Other readings")),
    ("A3", "put and do: one oo for two sounds", "Should the oo of book (put, push, full) look different from the oo of moon (do, to)?",
     [("put", None, "oo"), ("do", None, "oo, the same mark")],
     [("put", "c.p b.u c.t ; says 1 ŏŏ", "ŏŏ, the oo of book")],
     "One label is simpler to read; two tell a learner which oo to say. Spalding numbers them as different sounds."),
    ("A4", "carry: still bare", "What does the a of carry say?",
     [("carry", None, "bare, not yet decided")],
     [("carry", "c.c s.a x.rr | b.y ; bv 3>2 ; says 3 ee", "a short a, as in cat"),
      ("carry", "c.c b.a x.rr | b.y ; bv 3>2 ; says 1 e ; says 3 ee", "e, as many Canadians say it (merry, marry, Mary alike)")],
     "Before r is where Canadian speech varies most. <i>Carried</i> and <i>carries</i> follow whatever <i>carry</i> does."),
    ("A5", "gone: still bare", "Short o, or a borrowed sound?",
     [("gone", None, "bare, with the e in a cone")],
     [("gone", "c.g s.o c.n e0", "a short o, as in got")],
     "Most speakers say <i>gone</i> with the o of <i>got</i>. <i>Done</i> borrows u; <i>gone</i> may not need to borrow at all."),
    ("A6", "legible: a weak i", "Is the middle i of legible weak (ə) or a quick short i?",
     [("legible", None, "a weak i: ə")],
     [("legible", "c.l s.e c.g + | s.i | c.b le ; nudge 3>2", "a short mark, a quick i")],
     "In much Canadian speech the two have merged in unstressed syllables, so the ə doesn't take sides. A last, closed "
     "syllable keeps its short mark either way (<i>logic</i>, <i>lucid</i>)."),
    ("A7", "elite: ee over a French i", "Mark the i of elite and expertise with the sound it borrows?",
     [("elite", None, "ee over the i"), ("expertise", None, "")],
     [("elite", "b.e + | c.l b.i c.t e0 ; schwa 0", "the i bare")],
     "This answers the fifth open question from 20 November with the new mark, and waits on a yes. <i>Machine</i> and "
     "<i>police</i> would follow it."),
]
RULES = [
    ("B1", "gi said j before a vowel", "Is the gi of legion one unit, with its i sending the vault, as the ti of nation is?",
     [("legion", None, "gi one unit"), ("nation", "c.n l.a | g.ti b.o c.n ; vault 3>1 ; seam 2 ; schwa 3", "the ti it copies")],
     [("legion", "c.l l.e | c.g b.i | b.o c.n ; vault 3>1 ; nudge 3>2 ; says 3 ee ; schwa 4", "le-gi-on, the i its own vowel")],
     "Most speakers say two syllables, lee-jun; some say three. If you hear the i, it can't be inside the unit."),
    ("B2", "an e before a vowel sends a vault", "Does the e of simultaneous send the vault to the a, as an i before a vowel does?",
     [("simultaneous", None, "the e sends it"), ("experience", None, "the i that does the same")],
     [("simultaneous", "c.s l.i | c.m b.u c.l | c.t l.a | c.n l.e | t.ou c.s ; schwa 3 ; schwa 9", "long marks only")],
     "Built on one word so far. Some -eous words keep the long vowel before it (spontaneous) and some don't, so check a "
     "few more before ruling."),
    ("B3", "long u with no vault", "Where no word ending in e is in the family, does the long u take a vault?",
     [("ducal", None, "no vault"), ("lucid", None, "")],
     [("ducal", "c.d l.u | c.c + b.a c.l ; vault 3>1 ; schwa 3", "duke/+al, with a vault")],
     "Under rule 17 (structured word inquiry), <i>lunar</i> has its vault from <i>lune</i>. <i>Duke</i> is in the family "
     "of <i>ducal</i> but changes its k to c, so the base is <i>duc</i> and there's no e to replace."),
    ("B4", "a seam between Greek parts", "Do telephone and photograph take a seam between their Greek parts?",
     [("telephone", "c.t s.e c.l | b.e + | k.ph l.o c.n e> ; schwa 3", "tele + phone"),
      ("photograph", "k.ph l.o | c.t b.o + | c.gr s.a k.ph ; schwa 3", "photo + graph")],
     [("telephone", "c.t s.e c.l | b.e | k.ph l.o c.n e> ; schwa 3", ""),
      ("photograph", "k.ph l.o | c.t b.o | c.gr s.a k.ph ; schwa 3", "")],
     "Both are still shown in plain letters, so neither side is the site's marking yet. Rule 17 points to the seam: structured word inquiry writes tele + phone and "
     "photo + graph, and the family pages already seam homo + phone and techno + log.", ("With a seam", "No seam")),
]
# Calls in A and B that Dante has ruled on: (id, date, ruling). They move to "Ruled" at the foot of the page.
RULED = {
    "A2": ("21 November", "u. It reads most cleanly."),
    "A5": ("21 November", "A short o, as in got."),
    "A6": ("21 November", "A short mark, in every -ible word: legible, eligible, reducible, intelligible."),
    "A3": ("21 November", "ʊ, the International Phonetic Alphabet's letter for the vowel of book, over the u of put and the oo of book; do keeps oo."),
    "A7": ("21 November", "The final e makes the i long and sends a vault, which lands beside the ee: elite, police, expertise."),
}
# Older calls: status by the call's first field. Default "open".
STATUS = {
    "silent": ("settled", "21 November: the weak e takes ə."),
    "table, bugle, title": ("settled", "20 November: a long mark and no vault; no letter makes the vowel long."),
    "photo": ("settled", "20 November: no vault."),
    "happen": ("settled", "21 November: the e of -en takes ə."),
    "hapless": ("settled", "21 November: the e of -less takes ə."),
    "gone": ("settled", "21 November: a short o (A5)."),
    "produce, conduct (the *deuk- page), drafts": ("settled", "21 November: the verb's weak first vowel takes ə."),
    "hopeful, hopeless, hopelessness": ("settled", "21 November: the endings' weak vowels take ə."),
    "wanted, started, wishes, washes": ("settled", "21 November: the e of -ed and -es takes ə where it adds a syllable."),
    "-ful, -less, -ness, -est, -able": ("settled", "21 November: the weak vowels take ə."),
    "upon": ("open", "21 November: its first vowel takes ə. The seam after up is still open."),
    "notate": ("settled", "21 November, rule 17: note/+ate, the a taking the dropped e's place."),
    "music, basic": ("settled", "21 November, rule 17: muse/+ic and base/+ic."),
    "climb": ("settled", "20 November, rule 13: a long mark and no vault; no letter makes the i long."),
    "tiger, paper, open, even, robot, silent": ("settled", "20 November, rule 13: no letter makes these long, so no vault. Silent's e now takes ə."),
    "legomorphic": ("open", "The long o with no vault follows rule 13. The seam between the Greek parts waits on B4."),
    "robin": ("ruled", "12 November."), "river": ("ruled", "12 November."), "robot": ("ruled", "12 November."),
}


def _draw(LW, word, code, F=48):
    had, old = word in LW.W, LW.W.get(word)
    if code: LW.W[word] = code
    try:
        if word not in LW.W: return f'<span class="cw">{html.escape(word)}</span>'
        return LW.svg_strip([word], F=F, label=f"{word}, marked")[0]
    except Exception:
        return f'<span class="cw">{html.escape(word)}</span>'
    finally:
        if code:
            if had: LW.W[word] = old
            else: LW.W.pop(word, None)


def _fig(LW, word, code, cap):
    return f'<figure>{_draw(LW, word, code)}<figcaption>{cap}</figcaption></figure>'


def _call(LW, c):
    cid, title, q, now, other, note = c[:6]
    h1, h2 = c[6] if len(c) > 6 else ("As marked now", "The other reading")
    nowh = "".join(_fig(LW, w, code, cap) for w, code, cap in now)
    oth = "".join(_fig(LW, w, code, cap) for w, code, cap in other)
    left = f'<div class="cl-side"><h4>{h1}</h4><div class="cl-figs">{nowh}</div></div>'
    return f"""<article class="cl" id="{cid.lower()}"><h3><span class="cl-id">{cid}</span> {title}</h3>
<p class="cl-q">{q}</p>
<div class="cl-pair">{left}<div class="cl-side cl-other"><h4>{h2}</h4><div class="cl-figs">{oth}</div></div></div>
<p class="cl-note">{note}</p></article>"""


def older(LW):
    import site_codes, dolch_codes, hop_hope_codes, word_sum_codes
    rows = []
    for name, mod in (("site", site_codes), ("Dolch", dolch_codes), ("hop and hope", hop_hope_codes), ("word sums", word_sum_codes)):
        for key, what, why in mod.CALLS:
            st, note = STATUS.get(key, ("ruled", "") if re.search(r"\b(Ruled|Changed|ruled)\b", why) else ("open", ""))
            first = re.sub(r"[^A-Za-z’']", "", key.split(",")[0].split(" ")[0]) or key
            rows.append((st, key, what, why, note, first, name))
    order = {"open": 0, "ruled": 1, "settled": 2}
    rows.sort(key=lambda r: order[r[0]])
    out = []
    for st, key, what, why, note, first, name in rows:
        pic = _draw(LW, first, None, F=38) if first in LW.W else ""
        out.append(f"""<tr class="cl-{st}"><td class="cl-st">{st}</td><td class="cl-w">{pic}<div><b>{html.escape(key)}</b></div></td>
<td>{html.escape(what)}<div class="cl-why">{html.escape(why)}</div>{f'<div class="cl-now">{note}</div>' if note else ''}</td></tr>""")
    n = {k: sum(1 for r in rows if r[0] == k) for k in order}
    return n, "".join(out)


CSS = """<style>
.calls h2{margin-top:44px}
.cl{border:1px solid var(--line);border-radius:12px;background:var(--card);padding:18px 20px;margin:16px 0}
.cl h3{margin:0 0 4px;font-size:1.15rem}
.cl-id{display:inline-block;min-width:2.2em;font-family:var(--sans,system-ui);font-size:.85rem;color:var(--soft);font-weight:500}
.cl-q{margin:0 0 12px;font-weight:500}
.cl-pair{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.cl-side h4{margin:0 0 6px;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;color:var(--soft);font-weight:500}
.cl-other{border-left:3px dashed var(--line);padding-left:16px}
.cl-figs{display:flex;flex-wrap:wrap;gap:6px 22px;align-items:flex-end}
.cl figure{margin:0;display:grid;gap:2px}
.cl figure svg{max-width:100%;height:auto}
.cl figcaption{font-size:.85rem;color:var(--soft);max-width:22ch}
.cl-note{margin:10px 0 0;font-size:.95rem;color:var(--soft)}
.cl-table{width:100%;border-collapse:collapse;font-size:.95rem}
.cl-table td{border-top:1px solid var(--line);padding:10px 8px;vertical-align:top}
.cl-table .cl-w{width:150px}
.cl-table .cl-w svg{max-width:140px;width:auto;height:auto;max-height:64px}
.cl-st{width:70px;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:var(--soft)}
.cl-open .cl-st{color:var(--verb);font-weight:600}
.cl-why{color:var(--soft);font-size:.9rem;margin-top:3px}
.cl-now{margin-top:4px;font-size:.9rem}
@media (max-width:700px){.cl-pair{grid-template-columns:1fr}.cl-other{border-left:0;border-top:3px dashed var(--line);padding:12px 0 0}.cl-table .cl-w{width:96px}}
</style>"""


def _ruled(LW, c):
    cid, title = c[0], c[1]
    date, text = RULED[cid]
    w = (c[3] or c[4])[0][0]
    return f"""<tr class="cl-ruled"><td class="cl-st">ruled</td><td class="cl-w">{_draw(LW, w, None, F=38)}<div><b>{cid}</b></div></td>
<td>{title}<div class="cl-now">{date}: {text}</div></td></tr>"""


def write(OUT, door_page, LW):
    n, rows = older(LW)
    ruled = [c for c in NEW + RULES if c[0] in RULED]
    still = lambda L: [c for c in L if c[0] not in RULED]
    inner = f"""{CSS}<section class="hero door-hero"><div class="wrap">
<p class="eyebrow"><a href="explanations.html">Reasons and sources</a></p>
<h1>Marking calls</h1>
<p class="lead">Every place the marks rest on a choice that isn&rsquo;t settled, in one place. Each call is drawn as the site marks it now, with the other reading beside it. The rules the marks already follow are in <a href="definitions.html">Definitions</a> and on the <a href="about.html">About</a> page.</p>
</div></section>
<section class="calls"><div class="wrap">
<h2>A. Calls made with the new marks</h2>
<p>The &#601; for a weak vowel and the borrowed sound written over a vowel came in on 21 November 2026. These are the choices they made that need a yes or a change.</p>
{''.join(_call(LW, c) for c in still(NEW))}
<h2>B. Rules still to decide</h2>
{''.join(_call(LW, c) for c in still(RULES))}
<h2>C. Earlier calls</h2>
<p>Gathered from the code files, where they waited for a ruling: {n['open']} open, {n['ruled']} ruled, {n['settled']} settled by a later ruling. Each word is drawn as it is marked now.</p>
<table class="cl-table">{rows}</table>
<h2>Ruled from A and B</h2>
<p>Each is drawn as it is marked now.</p>
<table class="cl-table">{''.join(_ruled(LW, c) for c in ruled)}</table>
<p class="cl-note">The word walk&rsquo;s Try it has no &#601; or borrowed-sound tool yet, so a learner can&rsquo;t place these two marks there.</p>
</div></section>"""
    door_page("calls", "Marking calls · Sounds and Words, Assembled",
              "Every place the marks rest on a choice: each drawn as marked now, with the other reading beside it, and the rules still to decide.",
              inner)
    print(f"wrote calls.html | {len(still(NEW))} new calls, {len(still(RULES))} rules to decide, {len(ruled)} ruled, {sum(n.values())} earlier calls ({n['open']} open)")
