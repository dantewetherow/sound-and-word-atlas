"""Spelled apart (13 November 2026): lists/apart.html, on Legomorphic spelling. Words that sound the same and are
spelled differently, set side by side and marked, sorted by why the spelling keeps them apart:
  1. length marks the job: a grammar word can have one or two letters, a content word takes three or more (Carney's
     short word rule, 1994: 131-133): be and bee, in and inn;
  2. a letter kept from the family: know keeps the k that knowledge and known show; knew is the past of know;
  3. history: the two were said differently once, and the spelling kept the difference (sea and see, meat and meet).
That the third group helps a reader is a result, not a design. Each pair links from the step that can handle it.

(group, [(id, [(word, sentence)], step, why)])"""
import html

CODES = {"oar": "r.oar", "sew": "c.s t.ew", "knew": "k.kn t.ew", "blew": "c.bl t.ew", "meat": "c.m t.ea c.t",
         "meet": "c.m t.ee c.t", "knight": "k.kn t.igh c.t"}

GROUPS = [
    ("Length marks the job", "A small grammar word can have one or two letters; a word that names a thing or an action takes three or more. "
     "The length tells you the word&rsquo;s job before the sentence does (Carney 1994: 131&ndash;133).", [
        ("be-bee", [("be", "Be kind."), ("bee", "A bee buzzed by.")], 3, "<i>Bee</i> doubles its e to make three letters."),
        ("by-buy", [("by", "Sit by me."), ("buy", "We will buy bread."), ("bye", "Wave bye.")], 3, "<i>Buy</i> and <i>bye</i> both add a letter; the u of <i>buy</i> is silent with the b."),
        ("in-inn", [("in", "Come in."), ("inn", "We slept at an inn.")], 2, "<i>Inn</i> doubles its n."),
        ("I-eye", [("I", "I can see."), ("eye", "Close one eye.")], 1, "<i>I</i> is one letter, and always a capital."),
        ("or-oar", [("or", "Tea or milk?"), ("oar", "Row with an oar.")], 12, "<i>Oar</i> adds an a to the r-controlled unit."),
        ("so-sew", [("so", "I am so glad."), ("sew", "Sew on the button.")], 21, "<i>Sew</i> spells its vowel with ew, which usually says the vowel of <i>new</i>."),
        ("to-too", [("to", "Go to bed."), ("too", "Me too!")], 21, "<i>Too</i> doubles its o. For <i>two</i>, see below."),
    ]),
    ("A letter kept from the family", "The spelling keeps a letter that another form of the word, or a word in its family, says or uses.", [
        ("no-know", [("no", "No, thank you."), ("know", "I know the way.")], 25, "<i>Know</i> keeps the k it shares with <i>knowledge</i> and <i>known</i>."),
        ("new-knew", [("new", "I have new shoes."), ("knew", "She knew the answer.")], 25, "<i>Knew</i> is the past of <i>know</i>, so it keeps the k. <a href=\"../ablaut.html\">Ablaut</a>: <i>know, knew, known</i>."),
        ("blue-blew", [("blue", "The sky is blue."), ("blew", "The wind blew.")], 21, "<i>Blew</i> is the past of <i>blow</i>, as <i>grew</i> is of <i>grow</i> and <i>knew</i> of <i>know</i>."),
        ("to-two", [("to", "Go to school."), ("two", "I have two cats.")], 21, "<i>Two</i> keeps the w that <i>twin</i>, <i>twelve</i> and <i>twenty</i> say."),
        ("right-write", [("right", "Turn right."), ("write", "Write your name.")], 25, "<i>Write</i> keeps the w that <i>wrote</i> and <i>written</i> keep. It was once said."),
    ]),
    ("History keeps them apart", "These were said differently once. The sounds came together and the spellings didn&rsquo;t, so now the spelling tells a reader which word it is. That helps, but nobody planned it.", [
        ("sea-see", [("sea", "We swam in the sea."), ("see", "I see a bird.")], 20, "ea and ee once spelled two different vowels."),
        ("meat-meet", [("meat", "We ate the meat."), ("meet", "Let&rsquo;s meet at the park.")], 20, "The same two vowels."),
        ("night-knight", [("night", "Good night."), ("knight", "The knight rode a horse.")], 25, "The k of <i>knight</i> was once said."),
        ("sun-son", [("sun", "The sun is hot."), ("son", "Her son is seven.")], 19, "<i>Son</i> has the o that scribes wrote for u beside m, n and v."),
        ("our-hour", [("our", "This is our house."), ("hour", "Wait an hour.")], 25, "The h of <i>hour</i> came from Latin <i>hora</i> and was already silent in the French that brought it. It sits on the vowel&rsquo;s bar."),
    ]),
]


def by_step():
    """step number -> [(pair id, 'be / bee')], for the step pages' notes."""
    out = {}
    for _, _, pairs in GROUPS:
        for pid, ws, step, _ in pairs:
            out.setdefault(step, []).append((pid, " / ".join(w for w, _ in ws)))
    return out


def write(OUT, page, header, footer, X):
    LW = X["LW"]
    from noun_codes import NOUN_CODES
    def code_for(w):
        if w in LW.W: return None
        c = CODES.get(w) or NOUN_CODES.get(w) or X["auto_codes"].get(w)
        assert c, w
        return c
    secs = []
    for k, (h, sub, pairs) in enumerate(GROUPS, 1):
        cards = []
        for pid, ws, step, why in pairs:
            figs = "".join(f'<figure class="word">{X["svg_of"](w, 40, code=code_for(w), label=f"{w}, marked")}<figcaption>{s}</figcaption></figure>' for w, s in ws)
            cards.append(f'<div class="ap-pair" id="{pid}"><div class="words rrow">{figs}</div><p class="sub">{why} <a class="t-only" href="../steps/{step:02d}.html">Step {step}</a></p></div>')
        secs.append(f'<section class="about ap-group"><div class="wrap"><h2>{k}. {h}</h2><p class="sub">{sub}</p><div class="ap-pairs">{"".join(cards)}</div></div></section>')
    body = f"""{header(1)}
<main class="apart-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only"><a href="index.html">Legomorphic spelling</a> &middot; Spelled apart</p>
<h1>Spelled apart</h1>
<p class="lead">Words that sound the same and are spelled differently. In a sentence, the grammar tells them apart; on the page, the spelling does. Marked side by side, the difference shows: the h on the bar of <i>hour</i>, the second e of <i>bee</i>.</p>
<p class="sub t-only">Say both sentences, then write the word that fits each. Ask which group the pair is in: a short word and a long one, a letter kept from the family, or history. A spelling list of pairs tests something the other kinds don&rsquo;t: telling two spellings apart, not learning one.</p>
</div></section>
{"".join(secs)}
<section class="about t-only"><div class="wrap prose">
<p class="sub">Edward Carney, <i>A Survey of English Spelling</i> (1994): the short word rule, pp. 131&ndash;133. Every word here can be looked up in <a href="../walk.html">Words</a>.</p>
{X["uc"]("a first set of pairs, since 13 November 2026. Next: their, there and they&rsquo;re, and pairs from later steps.")}
</div></section>
</main>
{footer(1)}"""
    (OUT / "lists" / "apart.html").write_text(page("Spelled apart · A Legend for English Words", body, 1,
        "Words that sound the same and are spelled differently, marked side by side and sorted by why the spelling keeps them apart."), encoding="utf-8")
    return sorted({w for _, _, pairs in GROUPS for _, ws, _, _ in pairs for w, _ in ws})
