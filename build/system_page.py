"""How it fits together (27 November 2026): system.html, the system definitions. Dante asked for a target: phones in
the middle, then phonemes, graphemes and morphemes, and on outward, each ring opening its definition, written in terms
of the rings around it, with who named it. The welcome page links here, beside Where does the word come from?

The rings follow the familiar concentric picture of the levels of linguistic structure (one public-domain version is
on Wikimedia Commons). That picture has no graphemes; this one adds them, since the site is about spelling. The rings
are an order, not boxes inside boxes: a grapheme doesn't hold phonemes, it spells them. The page says so.

ENTRIES is the one place the definitions live: definitions.py lists the same terms in its section The system, so the
two pages can't drift apart. Each history was checked on 27 November 2026 against the sources it cites:
- phoneme: Mugdan, Historiographia Linguistica 38 (2011), for Dufriche-Desgenettes's manuscripts of 1865; the
  Baudouin de Courtenay article for the usual 1873 date and the Kazan school; Trubetzkoy's definition.
- morpheme: Historiographia Linguistica 28 (Kazan, early 1880s) and the LINGUIST List summary (Meillet's morpheme).
- grapheme: Meletis, Writing Systems Research (2019): Baudouin de Courtenay, Penttilä 1932, Whorf and Twaddell.
- morphology: wordorigins.org: Goethe's notes of 1796, Schleicher 1859.
- morphophonemics: Baudouin de Courtenay's alternations (1894), Trubetzkoy's morphonology (1929, after Trubetzkoy's
  Orphan), Bloomfield's Menomini Morphophonemics (1939).
- allophone: Whorf, about 1929. Semantics: Breal 1883; Morris 1938. Syntax: Apollonius Dyscolus.
- orthographic mapping: Ehri 2014, already on Credits."""
import html, math

W = lambda name: "https://en.wikipedia.org/wiki/" + name
EHRI = "https://doi.org/10.1080/10888438.2013.819356"
COMMONS = "https://commons.wikimedia.org/wiki/File:Major_levels_of_linguistic_structure.svg"

# id: (term, part of speech, what it is, how it fits, example (word, mark or None, caption) or None, who named it, sources)
ENTRIES = {
    "phone": ("phone", "noun",
              "A single speech sound, as it is actually said. Phones are written in square brackets: [p], [t].",
              "Phones are the centre: what the mouth makes and the ear takes in. Every ring outside is built on them. "
              "Many phones can count as one phoneme.",
              (None, None, "The p of <i>pin</i> comes with a puff of air, [p&#688;]. The p of <i>spin</i> has none, [p]. "
                           "Two phones, and an English speaker hears one sound."),
              "From Greek <i>ph&omacr;n&emacr;</i>, voice or sound, the root of <i>phonics</i>, <i>phoneme</i> and "
              "<i>telephone</i>. No one person named it. Benjamin Lee Whorf coined <i>allophone</i> around 1929 for the "
              "phones that count as one phoneme.",
              [("Phone (phonetics)", W("Phone_(phonetics)")), ("Allophone", W("Allophone"))]),
    "phonetics": ("phonetics", "noun",
                  "The study of phones: how the mouth makes them, how they travel through the air, and how the ear takes them in.",
                  None, None,
                  "From Greek <i>ph&omacr;n&emacr;tikos</i>, of speaking. The International Phonetic Alphabet, first "
                  "published in 1888, gives each phone one symbol.", []),
    "phoneme": ("phoneme", "noun",
                "A speech sound that tells words apart in one language. Change it and the word changes: <i>kit</i> and "
                "<i>kid</i>. Phonemes are written between slashes: /t/, /d/.",
                "A phoneme gathers the phones a language treats as one sound. It sits between those phones and the "
                "graphemes that spell it.",
                ("ship", "circle", "<i>ship</i> has three phonemes, so it gets three circles: /&#643;/, /&#618;/, /p/."),
                "Antoni Dufriche-Desgenettes was writing French <i>phon&egrave;me</i> for a speech sound by 1865, though "
                "it is usually dated 1873. Jan Baudouin de Courtenay and Miko&#322;aj Kruszewski, at Kazan in the 1870s "
                "and 1880s, gave it its modern sense. Nikolai Trubetzkoy defined it as the smallest unit that tells words "
                "apart (<i>Grundz&uuml;ge der Phonologie</i>, 1939).",
                [("Joachim Mugdan, &ldquo;On the origins of the term <i>phoneme</i>,&rdquo; <i>Historiographia Linguistica</i> 38 (2011)",
                  "https://www.benjamins.com/online/hl/articles/hl.38.1-2.03mug"),
                 ("Jan Baudouin de Courtenay", W("Jan_Baudouin_de_Courtenay"))]),
    "phonology": ("phonology", "noun",
                  "The study of a language&rsquo;s phonemes: which sounds it tells apart, and the orders they may come in.",
                  None, None,
                  "Trubetzkoy and the Prague linguists made phonology a field of its own in the 1920s and 1930s, building "
                  "on the Kazan school.", [("Nikolai Trubetzkoy", W("Nikolai_Trubetzkoy"))]),
    "grapheme": ("grapheme", "noun",
                 "A letter or team of letters that spells one phoneme: the <i>sh</i>, the <i>i</i> and the <i>p</i> of "
                 "<i>ship</i>. A grapheme can be one letter, two (<i>sh</i>), three (<i>igh</i>) or four (the <i>ough</i> "
                 "of <i>thorough</i>).",
                 "Graphemes are where speech meets the page. A grapheme doesn&rsquo;t hold phonemes; it spells them. "
                 "Strung together, graphemes spell morphemes.",
                 ("ship", "bond", "The bar joins <i>s</i> and <i>h</i>: two letters, one grapheme, one phoneme."),
                 "Baudouin de Courtenay is usually credited with the word, early in the twentieth century, for the "
                 "mind&rsquo;s picture of a letter. Aarni Penttil&auml; used it in 1932, and Benjamin Lee Whorf and W. "
                 "Freeman Twaddell in the 1930s. Two senses are in use. Phonics, and this site, use the first: letters "
                 "that spell a phoneme. Some writing-system research uses the smallest unit that tells written words apart.",
                 [("Dimitrios Meletis, &ldquo;The grapheme as a universal basic unit of writing,&rdquo; <i>Writing Systems Research</i> (2019)",
                   "https://www.tandfonline.com/doi/full/10.1080/17586801.2019.1697412")]),
    "orthography": ("orthography", "noun",
                    "A language&rsquo;s spelling system: its graphemes, and the patterns for which one to use where. "
                    "English orthography spells sounds, and it also keeps the parts of words looking the same.",
                    None, None,
                    "From Greek <i>orthos</i>, straight or correct, and <i>graphia</i>, writing: correct writing.",
                    [("Etymonline, <i>orthography</i>", "https://www.etymonline.com/word/orthography")]),
    "morpheme": ("morpheme", "noun",
                 "The smallest part of a word that carries meaning: a base like <i>sign</i>, a prefix like <i>re-</i>, a "
                 "suffix like <i class=\"nw\">-al</i>.",
                 "A morpheme is said in phonemes and spelled in graphemes. Morphemes join at seams to make words, and "
                 "a word&rsquo;s meaning is built from theirs.",
                 ("signal", "seam", "<i>signal</i> is <i>sign + al</i>: two morphemes, one seam."),
                 "Baudouin de Courtenay and Kruszewski worked out the idea at Kazan in the early 1880s, alongside the "
                 "phoneme. Antoine Meillet&rsquo;s French <i>morph&egrave;me</i> spread it. Leonard Bloomfield made it "
                 "the smallest unit of meaning in <i>Language</i> (1933).",
                 [("<i>Historiographia Linguistica</i> 28, on the morpheme at Kazan", "https://www.jbe-platform.com/content/journals/10.1075/hl.28.1.08com"),
                  ("LINGUIST List, the early sense of <i>morpheme</i> (2011)", "https://listserv.linguistlist.org/pipermail/linguist/2011-June/053579.html")]),
    "morphology": ("morphology", "noun",
                   "The study of morphemes: how words are built from parts, and how a family of words shares a base.",
                   None, None,
                   "Johann Wolfgang von Goethe coined <i>Morphologie</i> for the study of living forms, in notes from 1796. "
                   "August Schleicher applied it to language in 1859.",
                   [("wordorigins.org, <i>morphology</i>", "https://wordorigins.org/big-list-entries/morphology")]),
    "word": ("word", "noun",
             "A unit that can stand alone in speech and in writing. In print it sits between spaces.",
             "A word is one morpheme or several, joined. In a sentence it takes a job.",
             (None, None, "<i>sign</i>, <i>signal</i>, <i>signature</i>: one base, three words."),
             "Leonard Bloomfield called the word a minimum free form: the smallest form that can be said on its own "
             "(<i>Language</i>, 1933).", []),
    "sentence": ("sentence", "noun",
                 "Words put in order to make a claim or ask a question.",
                 "Words take jobs in a sentence: actor, operator, action, acted-on. The order carries meaning the words "
                 "alone don&rsquo;t. The jobs are on <a href=\"definitions.html#sentences\">Definitions</a>.",
                 (None, None, "<i>She could go.</i> <i>Could she go?</i> The same words; the order makes one a claim and one a question."),
                 None, []),
    "syntax": ("syntax", "noun",
               "The study of how words are put in order to make sentences.",
               None, None,
               "From Greek <i>syntaxis</i>, an arranging. Apollonius Dyscolus wrote the first Greek book on it, <i>On "
               "Syntax</i>, in the second century.",
               [("Britannica, Apollonius Dyscolus", "https://www.britannica.com/biography/Apollonius-Dyscolus")]),
    "meaning": ("meaning", "noun",
                "What a part, a word or a sentence says, and what it does when someone uses it.",
                "Meaning is the outer ring, and every ring inside serves it. Morphemes bring meaning into a word; a "
                "sentence brings it into use.",
                None, None, []),
    "semantics": ("semantics", "noun",
                  "The study of meaning. The study of meaning in use, in context, is pragmatics.",
                  None, None,
                  "Michel Br&eacute;al named it, French <i>s&eacute;mantique</i>, in 1883. Charles Morris (1938) set "
                  "semantics beside syntax and pragmatics.",
                  [("Semantics", W("Semantics"))]),
    "morphophonemics": ("morphophonemics", "noun",
                        "How a morpheme&rsquo;s sounds change when it joins other morphemes. Also called morphophonology, "
                        "or morphonology.",
                        "It is the bridge from the morpheme ring back to the phoneme ring. The morpheme stays the same "
                        "part; its phonemes shift.",
                        ("sign|signal", None, "<i>sign</i> has a long i and a silent g. In <i>signal</i> the i is short and "
                                              "the g is said. The spelling keeps the morpheme the same."),
                        "Baudouin de Courtenay studied these alternations in 1894. Nikolai Trubetzkoy proposed "
                        "morphonology as its own chapter of linguistics in 1929. Leonard Bloomfield&rsquo;s <i>Menomini "
                        "Morphophonemics</i> (1939) gave the English name. Noam Chomsky and Morris Halle (1968) argued that "
                        "English spelling is close to optimal because it keeps morphemes whole. Later studies find that "
                        "claim goes too far.",
                        [("Jan Baudouin de Courtenay", W("Jan_Baudouin_de_Courtenay")),
                         ("<i>Trubetzkoy&rsquo;s Orphan</i> (Benjamins)", "https://www.benjamins.com/catalog/cilt.144"),
                         ("University of Alberta, &ldquo;Sorry, Chomsky&rdquo; (2016)",
                          "https://www.ualberta.ca/science/news/2016/august/sorry-chomsky-english-spelling-is-hardly-close-to-optimal.html")]),
    "orthographic mapping": ("orthographic mapping", "noun",
                             "How a reader stores a word: by connecting its graphemes to its phonemes, so its spelling, "
                             "pronunciation and meaning are kept together.",
                             "It crosses the rings: phonemes, graphemes, morphemes and meaning bonded in one memory. Once "
                             "a word is mapped, it is read on sight and spelled from memory.",
                             ("note", "full", "The marks show what mapping connects: each sound to its letters, and the "
                                              "silent <i>e</i> to the long <i>o</i>."),
                             "The term and the account are Linnea Ehri&rsquo;s, from her research on how readers learn words by sight. Her 2014 paper sets them out.",
                             [("Linnea Ehri, &ldquo;Orthographic Mapping in the Acquisition of Sight Word Reading, Spelling "
                               "Memory, and Vocabulary Learning,&rdquo; <i>Scientific Studies of Reading</i> 18 (2014)", EHRI)]),
}

# The rings, centre outward: (unit, the field that studies it, system: sound, spelling or meaning)
RINGS = [("phone", "phonetics", "sound"), ("phoneme", "phonology", "sound"), ("grapheme", "orthography", "spell"),
         ("morpheme", "morphology", "mean"), ("word", None, "mean"), ("sentence", "syntax", "mean"),
         ("meaning", "semantics", "mean")]
# The bridges, drawn across the rings: (term, from ring, to ring, angle in degrees, clockwise from 3 o'clock)
BRIDGES = [("morphophonemics", 1, 3, 128), ("orthographic mapping", 1, 6, 58)]
R0, STEP_R = 74, 62          # the centre's radius, then each ring's width


def slug(t): return "sys-" + t.replace(" ", "-")


def radius(i): return R0 + STEP_R * i      # outer radius of ring i


def target():
    out = []
    for i in range(len(RINGS) - 1, -1, -1):              # largest first, so each ring's visible band is its own
        unit, field, sysm = RINGS[i]
        out.append(f'<a href="#{slug(unit)}" class="ring r-{sysm}" data-k="{unit}" aria-label="{unit}'
                   f'{", studied in " + field if field else ""}"><circle r="{radius(i)}"/></a>')
    for i, (unit, field, _) in enumerate(RINGS):
        mid = 0 if i == 0 else -(radius(i) + radius(i - 1)) / 2
        out.append(f'<text class="t-unit" y="{mid - (3 if field else -10):.0f}">{unit}</text>')
        if field: out.append(f'<text class="t-field" y="{mid + 20:.0f}">{field}</text>')
    for term, a, b, deg in BRIDGES:
        th = math.radians(deg)
        r1, r2 = radius(a - 1) + 14, radius(b) - 8
        x1, y1, x2, y2 = r1 * math.cos(th), r1 * math.sin(th), r2 * math.cos(th), r2 * math.sin(th)
        px, py = (radius(b) + 30) * math.cos(th), (radius(b) + 30) * math.sin(th)
        wpx = 11.6 * len(term) + 34
        out.append(f'<a href="#{slug(term)}" class="bridge" data-k="{term}" aria-label="{term}, a bridge across the rings">'
                   f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'
                   f'<circle class="end" cx="{x1:.1f}" cy="{y1:.1f}" r="7"/><circle class="end" cx="{x2:.1f}" cy="{y2:.1f}" r="7"/>'
                   f'<rect x="{px - wpx / 2:.1f}" y="{py - 21:.1f}" width="{wpx:.1f}" height="42" rx="21"/>'
                   f'<text x="{px:.1f}" y="{py + 7:.1f}">{term}</text></a>')
    E = radius(len(RINGS) - 1) + 60
    return (f'<svg class="sys-svg" viewBox="{-E} {-E + 48} {2 * E} {2 * E - 96}" role="group" '
            f'aria-label="The system as rings: phone at the centre, then phoneme, grapheme, morpheme, word, sentence and meaning">'
            f'{"".join(out)}</svg>')


CSS = """
.sys-grid { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 28px; align-items: start; }
@media (max-width: 860px) { .sys-grid { grid-template-columns: 1fr; } }
.sys-svg { width: 100%; height: auto; display: block; font-family: var(--body); }
.sys-svg .ring circle { stroke: var(--line); stroke-width: 1.5; cursor: pointer; transition: fill .2s; }
.sys-svg .r-sound circle { fill: color-mix(in srgb, var(--verb) 13%, var(--card)); }
.sys-svg .r-spell circle { fill: color-mix(in srgb, var(--subject) 15%, var(--card)); }
.sys-svg .r-mean circle { fill: color-mix(in srgb, var(--modal) 11%, var(--card)); }
.sys-svg .ring[data-k="word"] circle, .sys-svg .ring[data-k="meaning"] circle { fill: color-mix(in srgb, var(--modal) 5%, var(--card)); }
.sys-svg .ring:hover circle, .sys-svg .ring:focus-visible circle { fill: color-mix(in srgb, var(--modal) 24%, var(--card)); }
.sys-svg .ring.on circle { fill: color-mix(in srgb, var(--modal) 34%, var(--card)); stroke: var(--modal); stroke-width: 2.5; }
.sys-svg a:focus-visible { outline: none; }
.sys-svg text { text-anchor: middle; pointer-events: none; fill: var(--ink); }
.sys-svg .t-unit { font-size: 29px; font-weight: 600; }
.sys-svg .t-field { font-size: 20px; fill: var(--soft); font-style: italic; font-family: var(--display); }
.sys-svg .bridge { cursor: pointer; }
.sys-svg .bridge line { stroke: var(--ink); stroke-width: 7; stroke-linecap: round; opacity: .32; stroke-dasharray: 2 13; }
.sys-svg .bridge .end { fill: var(--ink); opacity: .45; }
.sys-svg .bridge rect { fill: var(--paper); stroke: var(--ink); stroke-width: 1.5; }
.sys-svg .bridge text { font-size: 21px; font-weight: 600; }
.sys-svg .bridge:hover rect, .sys-svg .bridge:focus-visible rect, .sys-svg .bridge.on rect { fill: color-mix(in srgb, var(--modal) 30%, var(--paper)); stroke: var(--modal); }
.sys-svg .bridge.on line { opacity: .7; stroke: var(--modal); }
.sys-key { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: .88rem; color: var(--soft); margin: 10px 0 0; }
.sys-key span::before { content: ""; display: inline-block; width: .9em; height: .9em; border-radius: 50%; margin-right: 6px; vertical-align: -1px; border: 1px solid var(--line); }
.sys-key .k-sound::before { background: color-mix(in srgb, var(--verb) 22%, var(--card)); }
.sys-key .k-spell::before { background: color-mix(in srgb, var(--subject) 25%, var(--card)); }
.sys-key .k-mean::before { background: color-mix(in srgb, var(--modal) 20%, var(--card)); }
.sys-chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 14px 0 14px; padding: 0; list-style: none; }
.sys-chips a { display: inline-block; padding: 4px 12px; border: 1px solid var(--line); border-radius: 999px; text-decoration: none; color: var(--ink); background: var(--card); font-size: .9rem; }
.sys-chips a.on { border-color: var(--modal); background: color-mix(in srgb, var(--modal) 18%, var(--card)); }
.sys-panel { position: sticky; top: 16px; }
.sys-entry { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 18px 22px; margin: 0 0 16px; }
.sys-entry h2 { font-size: 1.7rem; }
.sys-entry h2 .pos, .sys-entry h3 .pos { font-family: var(--body); font-size: .8rem; color: var(--soft); font-weight: 400; margin-left: 6px; }
.sys-entry h3 { font-size: 1.2rem; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--line); }
.sys-entry p { margin: .55em 0; line-height: 1.55; }
.sys-entry .lab { display: block; font-size: .74rem; letter-spacing: .08em; text-transform: uppercase; color: var(--soft); margin-bottom: 2px; }
.sys-entry .hist { font-size: .95rem; }
.sys-entry .src { font-size: .82rem; color: var(--soft); }
.sys-entry figure { margin: 10px 0; display: flex; gap: 18px; flex-wrap: wrap; align-items: end; }
.sys-entry figure svg { max-height: 110px; width: auto; max-width: 100%; }
.sys-entry figcaption { flex-basis: 100%; font-size: .93rem; color: var(--ink); }
.sys-steps { display: flex; justify-content: space-between; gap: 8px; margin-top: 12px; }
.sys-steps button { font: inherit; font-size: .9rem; padding: 6px 14px; border-radius: 999px; border: 1px solid var(--line); background: var(--paper); color: var(--ink); cursor: pointer; }
.sys-steps button[disabled] { visibility: hidden; }
html.sys-js .sys-entry { display: none; }
html.sys-js .sys-entry.on { display: block; }
"""

JS = """<script>(() => {
  const root = document.documentElement; root.classList.add('sys-js');
  const order = %s;
  const entries = [...document.querySelectorAll('.sys-entry')];
  const marks = [...document.querySelectorAll('[data-k]')];
  function show(k, push) {
    const id = 'sys-' + k.replace(/ /g, '-');
    if (!document.getElementById(id)) return;
    entries.forEach(e => e.classList.toggle('on', e.id === id));
    marks.forEach(m => m.classList.toggle('on', m.dataset.k === k));
    if (push) try { history.replaceState(null, '', '#' + id); } catch (e) {}
    if (push && matchMedia('(max-width: 860px)').matches) document.getElementById(id).scrollIntoView({behavior: 'smooth', block: 'start'});
  }
  marks.forEach(m => m.addEventListener('click', ev => { ev.preventDefault(); show(m.dataset.k, true); }));
  document.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => show(b.dataset.go, true)));
  const h = decodeURIComponent(location.hash.replace(/^#sys-/, '')).replace(/-/g, ' ');
  show(order.includes(h) || h === 'orthographic mapping' || h === 'morphophonemics' ? h : 'phone', false);
})();</script>"""


def write(door_page, X):
    import json, pathlib, re
    import gym
    from noun_codes import NOUN_CODES
    here = pathlib.Path(__file__).resolve().parent
    LW = X["LW"]
    pool = dict(X["auto_codes"]); pool.update(NOUN_CODES); pool.update(gym.codes())
    for fn in ("more_codes.json", "family_codes.json"): pool.update(json.loads((here / "data" / fn).read_text(encoding="utf-8")))
    import site_codes
    pool.update(site_codes.SITE_CODES); pool.update(site_codes.SITE_RULED)

    def draw(w, mark):
        had = w in LW.W
        if not had: LW.W[w] = pool[w]
        try:
            if mark in (None, "full"): svg = X["svg_of"](w, 56, label=f"{w}, marked")
            else: svg = LW.svg_one_mark(w, mark, F=56.0, label=f"{w}, with only its {mark}s drawn")
        finally:
            if not had: LW.W.pop(w, None)
        return re.sub(r' style="[^"]*"', "", svg, count=1)

    def block(k, head="h2"):
        term, pos, what, fits, ex, hist, srcs = ENTRIES[k]
        out = [f'<{head}>{term} <span class="pos">{pos}</span></{head}>', f'<p><span class="lab">What it is</span>{what}</p>']
        if fits: out.append(f'<p><span class="lab">How it fits</span>{fits}</p>')
        if ex:
            words, mark, cap = ex
            pics = "".join(draw(w, mark) for w in words.split("|")) if words else ""
            out.append(f'<figure>{pics}<figcaption>{cap}</figcaption></figure>')
        if hist: out.append(f'<p class="hist"><span class="lab">Who named it</span>{hist}</p>')
        if srcs: out.append('<p class="src">Sources: ' + "; ".join(f'<a href="{u}">{t}</a>' for t, u in srcs) + ".</p>")
        return "".join(out)

    order = [u for u, _, _ in RINGS]
    arts = []
    for i, (unit, field, _) in enumerate(RINGS):
        inner = order[i - 1] if i else None
        outer = order[i + 1] if i + 1 < len(order) else None
        steps = (f'<div class="sys-steps"><button type="button" data-go="{inner or ""}"{"" if inner else " disabled"}>&larr; In: {inner or ""}</button>'
                 f'<button type="button" data-go="{outer or ""}"{"" if outer else " disabled"}>Out: {outer or ""} &rarr;</button></div>')
        fld = f'<div class="fld">{block(field, "h3")}</div>' if field else ""
        ring_word = "the centre" if i == 0 else f"ring {i + 1} from the centre"
        arts.append(f'<article class="sys-entry" id="{slug(unit)}" aria-label="{unit}"><p class="eyebrow">{ring_word.capitalize()}</p>'
                    f'{block(unit)}{fld}{steps}</article>')
    for term, a, b, _ in BRIDGES:
        arts.append(f'<article class="sys-entry" id="{slug(term)}" aria-label="{term}"><p class="eyebrow">A bridge: {order[a]} to {order[b]}</p>'
                    f'{block(term)}</article>')
    chips = "".join(f'<li><a href="#{slug(u)}" data-k="{u}">{u}</a></li>' for u in order) + \
            "".join(f'<li><a href="#{slug(t)}" data-k="{t}">{t}</a></li>' for t, *_ in BRIDGES)

    body = f"""<style>{CSS}</style>
<section class="hero"><div class="wrap">
<p class="eyebrow">System definitions &middot; <a href="definitions.html#system">Definitions</a></p>
<h1>How it fits together</h1>
<p class="lead">Speech, spelling and meaning are layers of one system. Each ring here is one layer, from a single speech sound at the centre to meaning at the edge.</p>
<p class="sub">Choose a ring to read what it is, how it fits the rings beside it, and who named it. The dotted lines are bridges that cross the rings.</p>
</div></section>
<section class="about"><div class="wrap sys-grid">
<div class="sys-fig">
{target()}
<p class="sys-key"><span class="k-sound">sound</span><span class="k-spell">spelling</span><span class="k-mean">meaning</span></p>
<ul class="sys-chips" aria-label="Every term on the rings">{chips}</ul>
<p class="sub">The rings are an order, not boxes inside boxes. A grapheme doesn&rsquo;t hold phonemes; it spells them. A morpheme is said in phonemes and spelled in graphemes.</p>
</div>
<div class="sys-panel" aria-live="polite">{"".join(arts)}</div>
</div></section>
<section class="about"><div class="wrap prose">
<h2>Where the picture comes from</h2>
<p>Linguists often draw the levels of language as rings: speech sounds at the centre, meaning in context at the edge. One public-domain version is <a href="{COMMONS}">on Wikimedia Commons</a>, after a figure by the US National Visualization and Analytics Center.</p>
<p>That picture has no graphemes and no orthography. This one adds them, between the sounds and the parts that carry meaning, because spelling is where this site works. The same terms are listed on <a href="definitions.html#system">Definitions</a>.</p>
</div></section>
{JS % json.dumps(order)}"""
    door_page("system", "How it fits together · Sounds and Words, Assembled",
              "System definitions as rings: phone, phoneme, grapheme, morpheme, word, sentence and meaning, each with how it fits the others and who named it.",
              body)
