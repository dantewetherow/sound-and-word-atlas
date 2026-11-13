"""What's that ablaut? (13 November 2026): ablaut.html, behind Words, beside the note family in Explorations.

Ablaut is a change of the vowel inside a base to mark time: write, wrote, written. The consonants hold still and the
vowel moves. It is the oldest way English marks the past, older than -ed. The page sets the core set beside the
spelling machinery the notation already shows: the silent e's vault in write and wrote, the tt that boxes off the said e
of -en in written; then spoken, chosen and frozen, where one consonant lets the vault through to a long o, and driven,
given and risen, where the i is short with one consonant and no box (v can't double; risen just doesn't).

The box tells a reader the i of written is short; it doesn't explain why the vowel changed. Ablaut explains the vowel,
the box explains the reading. The -en takes a seam, as in been (be + en)."""
import html

CODES = {
    "wrote": "k.wr l.o c.t e>", "written": "k.wr s.i x.tt + | b.e c.n ; bv 3>2",
    "ride": "c.r l.i c.d e>", "rode": "c.r l.o c.d e>", "ridden": "c.r s.i x.dd + | b.e c.n ; bv 3>2",
    "bite": "c.b l.i c.t e>", "bit": "c.b s.i c.t", "bitten": "c.b s.i x.tt + | b.e c.n ; bv 3>2",
    "hide": "c.h l.i c.d e>", "hid": "c.h s.i c.d", "hidden": "c.h s.i x.dd + | b.e c.n ; bv 3>2",
    "rise": "c.r l.i c.s e>", "rose": "c.r l.o c.s e>", "risen": "c.r s.i c.s + | b.e c.n",
    "choose": "g.ch t.oo c.s e0", "chose": "g.ch l.o c.s e>", "chosen": "g.ch l.o | c.s + b.e c.n ; vault 3>1",
    "freeze": "c.fr t.ee c.z e0", "froze": "c.fr l.o c.z e>", "frozen": "c.fr l.o | c.z + b.e c.n ; vault 3>1",
    "drive": "c.dr l.i c.v e>", "drove": "c.dr l.o c.v e>", "driven": "c.dr s.i c.v + | b.e c.n",
    "given": "c.g s.i c.v + | b.e c.n",
    "sing": "c.s s.i k.ng", "sang": "c.s s.a k.ng", "sung": "c.s s.u k.ng", "song": "c.s s.o k.ng",
    "speak": "c.sp t.ea c.k", "spoke": "c.sp l.o c.k e>", "spoken": "c.sp l.o | c.k + b.e c.n ; vault 3>1",
    "grew": "c.gr t.ew", "grown": "c.gr t.ow + c.n", "blow": "c.bl t.ow", "blew": "c.bl t.ew", "blown": "c.bl t.ow + c.n",
    "knew": "k.kn t.ew", "known": "k.kn t.ow + c.n",
}

CORE = [("write", "<i>write</i>", "The silent e sends a vault back over the t, so the i says its name."),
        ("wrote", "<i>wrote</i>", "The vowel changes; the w, r and t hold still. The same silent e, the same vault, now to the o."),
        ("written", "<i>writ(e) + t + en</i> &rarr; <i>written</i>",
         "The e of -en is said, and on its own it would reach back and make the i long: <i>writen</i> would read &ldquo;wright-en.&rdquo; "
         "The doubled t is a block box: the vault stops there, and the i stays short.")]

SETS = [
    ("The box does it again", "Long in the first two, short behind a box in the third.",
     [[("ride", ""), ("rode", ""), ("ridden", "rid(e) + d + en")], [("bite", ""), ("bit", ""), ("bitten", "bit(e) + t + en")], [("hide", ""), ("hid", ""), ("hidden", "hid(e) + d + en")]]),
    ("Take the box away", "One consonant, nothing to stop the vault: the e of -en reaches back, and the o says its name. "
     "This is the contrast that shows the box in <i>written</i> is doing the work.",
     [[("speak", ""), ("spoke", ""), ("spoken", "spok(e) + en")], [("choose", ""), ("chose", ""), ("chosen", "chos(e) + en")],
      [("freeze", ""), ("froze", ""), ("frozen", "froz(e) + en")]]),
    ("Where the rule stops", "Short i with one consonant and no box. In <i>driven</i> and <i>given</i>, v can&rsquo;t double "
     "(step 8), so there is no box to build. In <i>risen</i>, s could double and doesn&rsquo;t. Each reads as a long i "
     "(&ldquo;dryven&rdquo;, &ldquo;ryzen&rdquo;) until a learner knows the word: the spelling shows the family, not the sound.",
     [[("drive", ""), ("drove", ""), ("driven", "driv(e) + en")], [("give", ""), ("gave", ""), ("given", "giv(e) + en")],
      [("rise", ""), ("rose", ""), ("risen", "ris(e) + en")]]),
    ("Other vowels, the same idea", "Ablaut runs through English&rsquo;s oldest verbs, each with its own pattern of vowels.",
     [[("sing", ""), ("sang", ""), ("sung", ""), ("song", "")],
      [("grow", ""), ("grew", ""), ("grown", "grow + n")], [("blow", ""), ("blew", ""), ("blown", "blow + n")], [("know", ""), ("knew", ""), ("known", "know + n")]]),
]


def write(OUT, door_page, X):
    LW = X["LW"]
    def fig(w, sub, F, cap=""):
        code = None if w in LW.W else (CODES.get(w) or X["auto_codes"][w])
        return (f'<figure class="word">{X["svg_of"](w, F, code=code, label=f"{w}, marked")}'
                f'<figcaption>{f"<span class=ws>{sub}</span>" if sub else ""}{f"<span class=t-only>{cap}</span>" if cap else ""}</figcaption></figure>')
    core = "".join(fig(w, s, 58, c) for w, s, c in CORE)
    secs = []
    for h, sub, rows in SETS:
        r = "".join(f'<div class="ab-row">{"".join(fig(w, s, 40) for w, s in row)}</div>' for row in rows)
        secs.append(f'<section class="about"><div class="wrap"><h2>{h}</h2><p class="sub t-only">{sub}</p><div class="ab-rows">{r}</div></div></section>')
    body = f"""<section class="hero"><div class="wrap">
<p class="eyebrow t-only">Explorations</p>
<h1>What&rsquo;s that ablaut?</h1>
<p class="lead">Ablaut is a change of the vowel inside a word to mark time: <i>write</i>, <i>wrote</i>, <i>written</i>. The consonants hold still and the vowel moves. It&rsquo;s the oldest way English marks the past, older than <i>-ed</i>.</p>
</div></section>
<section class="about" id="write"><div class="wrap">
<h2><i>write</i>, <i>wrote</i>, <i>written</i></h2>
<p class="sub t-only">Two things at once: the vowel changing, and the spelling around it doing its usual jobs.</p>
<div class="words fam">{core}</div>
<p class="sub t-only">Say them in a frame: <i>Today I write. Yesterday I wrote. I have written.</i></p>
</div></section>
{"".join(secs)}
<section class="about t-only"><div class="wrap prose">
<h2>Ablaut explains the vowel; the box explains the reading</h2>
<p>The doubled t didn&rsquo;t make the i of <i>written</i> short. The short vowel was there first, in the spoken word, and the spelling doubled the t to show it. So the box tells a reader how to say the word; ablaut tells why the vowel changed.</p>
<p>The <i>-en</i> takes a seam, as it does in <i>been</i> (<i>be + en</i>), <i>driven</i> and <i>awaken</i>. Some of these pairs are also on <a href="lists/apart.html#new-knew">Spelled apart</a>: <i>knew</i> and <i>new</i>, <i>blew</i> and <i>blue</i>. Every word here can be looked up in <a href="walk.html">Words</a>.</p>
{X["uc"]("the first page for the presentation &ldquo;What&rsquo;s that ablaut?&rdquo;, since 13 November 2026. Next: a spelling list on the pattern, and the animated deck once the page reads right.")}
</div></section>"""
    door_page("ablaut", "What's that ablaut? · A Legend for English Words", "write, wrote, written: the vowel changes to mark time, and the spelling around it does its usual jobs.", body)
    return sorted({w for w, *_ in CORE} | {w for _, _, rows in SETS for row in rows for w, _ in row})
