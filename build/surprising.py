"""Surprising connections (23 November 2026): surprising.html, under Roots and their sources. Words from one root that
no longer look related: experiment, pirate and fear; gold and yellow; two and twig; educate, tug and team; sign and seal.

Dante asked for it when pirate and fear came out of the experiment word study: they are well supported in the etymology,
and they pull the study away from parts a learner can see and build. The word studies keep to those; this page keeps the
history. Each group cites its source, checked that day: the Indo-European Lexicon (University of Texas at Austin, after
Pokorny) for every root, and Etymonline for fear, twig and tug. The two regular sound changes at the end are Grimm's law
(Jacob Grimm, Deutsche Grammatik, 2nd ed., 1822)."""

IEL = "https://lrc.la.utexas.edu/lex/master/"
GROUPS = [
    ("per", "*per-: to try, to risk", [
        ("experiment", "Latin <i>exper&imacr;r&imacr;</i>, to try out"),
        ("peril", "Latin <i>per&imacr;culum</i>, a trial, a danger"),
        ("pirate", "Greek <i>peirat&emacr;s</i>, an attacker, from <i>peira</i>, a trial, an attempt"),
        ("fear", "Old English <i>f&aelig;r</i>, a sudden danger, an attack")],
     "Three roads into English. <i>Experiment</i> and <i>peril</i> came from Latin, through French. <i>Pirate</i> came from Greek "
     "through Latin, which spelled Greek ei with an i. <i>Fear</i> never left: English has had it since Old English. Its f is the "
     "p of the root, changed in the early Germanic languages (see the end of this page).",
     [("Indo-European Lexicon, per- 2e: <i>experiment</i>, <i>peril</i>, <i>pirate</i>, <i>fear</i>", IEL + "1493"),
      ("Etymonline, <i>fear</i>: Old English <i>f&aelig;r</i>, calamity, sudden danger, from the root *per-, to try, to risk",
       "https://www.etymonline.com/word/Fear")],
     ("roots/per.html", "the *per- page", "studies/per.html", "the word study of experiment and experience")),
    ("ghel", "*ghel-: to shine", [
        ("gold", "Old English <i>gold</i>"),
        ("yellow", "Old English <i>geolu</i>"),
        ("glow", "Old English <i>glowan</i>"),
        ("glass", "Old English <i>gl&aelig;s</i>")],
     "All four are English from the start. In <i>geolu</i>, the g before e spelled the sound of y, and later spelling wrote "
     "it with a y. Many gl- words for light come from this root, which is part of why gl- and light go together.",
     [("Indo-European Lexicon, ghel- (to shine, glow; gold, yellow): <i>gold</i>, <i>yellow</i>, <i>glow</i>, <i>gleam</i>, <i>glass</i>", IEL + "0637")],
     ("lists/phonesthemes.html", "Sound and meaning: phonesthemes", None, None)),
    ("dwo", "*dwo-: two", [
        ("two", "Old English <i>tw&amacr;</i>"),
        ("twin", "two born together"),
        ("between", "be + tween: by the two"),
        ("twig", "a fork, where a branch splits in two")],
     "The w in <i>two</i> isn&rsquo;t said, and the spelling keeps it: it is the w of <i>twin</i>, <i>twice</i>, <i>twelve</i> "
     "and <i>between</i>. <i>Twig</i> is from early Germanic <i>*twigga</i>, a fork.",
     [("Indo-European Lexicon, dwo-: <i>two</i>, <i>twin</i>, <i>twelve</i>, <i>between</i>, <i>twig</i>, <i>twine</i>", IEL + "0369"),
      ("Etymonline, <i>twig</i>: Old English <i>twig</i>, from Proto-Germanic <i>*twigga</i>, a fork", "https://www.etymonline.com/word/twig")],
     ("lists/phonesthemes.html#tw", "the tw- words on Sound and meaning", None, None)),
    ("deuk", "*deuk-: to lead, to pull", [
        ("educate", "Latin <i>&emacr;duc&amacr;re</i>, to bring up"),
        ("duke", "Latin <i>dux</i>, a leader"),
        ("tug", "Old English <i>teohan</i>, to pull"),
        ("team", "Old English <i>t&emacr;am</i>, animals pulling together")],
     "Latin kept the d of the root; early Germanic, and so English, changed it to t. So <i>educate</i> and <i>duke</i> lead, and <i>tug</i>, "
     "<i>tow</i> and <i>team</i> pull.",
     [("Indo-European Lexicon, deuk- (to pull): <i>educate</i>, <i>duke</i>, <i>tug</i>, <i>tow</i>, <i>team</i>", IEL + "0355"),
      ("Etymonline, <i>tug</i>: Old English <i>teohan</i>, to pull, from the root *deuk-, to lead", "https://www.etymonline.com/word/tug")],
     ("roots/deuk.html", "the *deuk- page", "studies/education.html", "the word study From duct to education")),
    ("sign", "sign and seal", [
        ("sign", "Latin <i>signum</i>, a mark"),
        ("signal", "Latin <i>signum</i>, through French"),
        ("seal", "Latin <i>sigillum</i>, a little sign")],
     "A seal is a little sign pressed into wax. French wore <i>sigillum</i> down to <i>seel</i>, and English took it without "
     "the g. <i>Sign</i> and <i>signal</i> kept theirs.",
     [("Indo-European Lexicon, seku&#x32F;-: Latin <i>signum</i>", IEL + "1673"),
      ("Etymonline: <i>sign</i>, <i>signal</i> and <i>seal</i>", "https://www.etymonline.com/search?q=sign")],
     ("roots/sign.html", "the sign page", "studies/sign.html", "the word study The g in sign")),
]
GRIMM = [("father", "Latin <i>pater</i>: paternal"), ("foot", "Latin <i>ped</i>: pedal"),
         ("ten", "Latin <i>decem</i>: decimal"), ("tooth", "Latin <i>dent</i>: dentist")]


def write(OUT, door_page, X):
    import json, gym, pathlib
    from noun_codes import NOUN_CODES
    here = pathlib.Path(__file__).resolve().parent
    LW = X["LW"]
    pool = dict(X["auto_codes"]); pool.update(NOUN_CODES); pool.update(gym.codes())
    for fn in ("more_codes.json", "family_codes.json"): pool.update(json.loads((here / "data" / fn).read_text(encoding="utf-8")))

    def fig(w, cap):
        code = None if w in LW.W else pool[w]
        return (f'<figure class="word">{X["svg_of"](w, 44, code=code, label=f"{w}, marked")}'
                f'<figcaption><span class="sc-road">{cap}</span></figcaption></figure>')

    secs, toc = [], []
    for gid, head, words, note, srcs, (a, at, b, bt) in GROUPS:
        toc.append(f'<a href="#{gid}">{head.split(":")[0]}</a>')
        src = "; ".join(f'<a href="{u}">{t}</a>' for t, u in srcs)
        more = f'More on <a href="{a}">{at}</a>' + (f' and in <a href="{b}">{bt}</a>' if b else "") + "."
        secs.append(f"""<section class="about sc-group" id="{gid}"><div class="wrap">
<h2>{head}</h2>
<div class="words rrow">{"".join(fig(w, c) for w, c in words)}</div>
<p class="sub">{note}</p>
<p class="sub t-only sc-src">Sources: {src}. {more}</p>
</div></section>""")
    body = f"""<section class="hero"><div class="wrap">
<p class="eyebrow t-only"><a href="derivations.html">Roots and their sources</a> &middot; Surprising connections</p>
<h1>Surprising connections</h1>
<p class="lead">Each group of words here comes from one old root, but the words no longer look related. Sounds changed, and words came into English by different roads: from Latin, from Greek, or from English&rsquo;s own past.</p>
<p class="sub t-only">The word studies keep to words whose parts learners can see and build: <i>experiment</i>, <i>experimental</i>, <i>experimentation</i>. These groups are history: no word sum joins <i>experiment</i> to <i>fear</i>. They make good questions after a family is built: how could these be related?</p>
<nav class="ph-toc" aria-label="Groups">{"".join(toc)}<a href="#grimm">p and f, d and t</a></nav>
</div></section>
{"".join(secs)}
<section class="about sc-group" id="grimm"><div class="wrap">
<h2>p and f, d and t</h2>
<div class="words rrow">{"".join(fig(w, c) for w, c in GRIMM)}</div>
<p class="sub">Two changes in the early Germanic languages were regular: p became f, and d became t. Latin kept the old sounds, and English borrowed Latin words later. So English has <i>father</i> beside <i>paternal</i> and <i>tooth</i> beside <i>dentist</i>, and the same change gave <i>fear</i> its f and <i>tug</i> its t.</p>
<p class="sub t-only sc-src">Source: Grimm&rsquo;s law, set out by Jacob Grimm in the second edition of his <i>Deutsche Grammatik</i> (1822). Each pair is in the Indo-European Lexicon under its root.</p>
</div></section>"""
    door_page("surprising", "Surprising connections · Sounds and Words, Assembled",
              "Words from one root that no longer look related: experiment, pirate and fear; gold and yellow; two and twig; educate, tug and team; sign and seal.",
              body)
    return sorted({w for g in GROUPS for w, _ in g[2]} | {w for w, _ in GRIMM})
