"""Root families, behind Derivations: roots/<slug>.html. The first, *leg-, made on 8 November 2026.

A root page gives the root and its meaning, the spellings it takes in English, and its family branch by branch: each word
with the root's spelling in bold, its parts where they can be shown, and a plain meaning. The family follows Etymonline's
entry for the root, which draws on Calvert Watkins, and the Indo-European Lexicon of the Linguistics Research Center at
the University of Texas at Austin, which follows Pokorny; the page links both. The site plan has the roots follow Watkins's
American Heritage Dictionary of Indo-European Roots (3rd ed., 2011), which this page hasn't yet been checked against.

Each word in a family gets an id (doors.word_id), and write() returns (word, link) for the search."""
import html
import doors

LEG = {
    "slug": "leg", "root": "*leg-", "gloss": "to gather, to collect",
    "sources": [("Etymonline, *leg-", "https://www.etymonline.com/word/%2Aleg-"),
                ("Indo-European Lexicon, leg̑- (Linguistics Research Center, University of Texas at Austin)", "https://lrc.la.utexas.edu/lex/master/1131"),
                ("Wiktionary, Proto-Indo-European *leǵ-", "https://en.wiktionary.org/wiki/Reconstruction:Proto-Indo-European/le%C7%B5-")],
    "spellings": [("leg", "legend"), ("lect", "collect"), ("lig", "diligent"), ("log", "logic"), ("logue", "dialogue"),
                  ("lex", "lexicon"), ("lege", "college"), ("league", "colleague"), ("les", "lesson"), ("loy", "loyal")],
    # (branch, what the root became there, [(word, parts or None, the root's spelling in it, meaning)])
    "branches": [
        ("Greek", "<i>legein</i>, to say, to count; <i>logos</i>, a word, an account", [
            ("logic", ["log", "ic"], "log", "reasoning that holds together"),
            ("dialogue", ["dia", "logue"], "logue", "talk between people"),
            ("catalogue", ["cata", "logue"], "logue", "a list of things"),
            ("prologue", ["pro", "logue"], "logue", "words before the story"),
            ("analogy", ["ana", "log", "y"], "log", "a likeness that explains"),
            ("apology", ["apo", "log", "y"], "log", "words said in defence, or to say sorry"),
            ("dialect", ["dia", "lect"], "lect", "a way of speaking"),
            ("eclectic", ["ec", "lect", "ic"], "lect", "picked from many places"),
            ("lexicon", ["lex", "ic", "on"], "lex", "the words of a language"),
            ("legomorphic", ["lego", "morph", "ic"], "lego", "this notation&rsquo;s name: <i>legō</i>, I gather, I say, and <i>morph</i>, form"),
        ]),
        ("Latin", "<i>legere</i>, to gather, to choose, to read", [
            ("collect", ["col", "lect"], "lect", "gather together"),
            ("select", ["se", "lect"], "lect", "pick out"),
            ("elect", ["e", "lect"], "lect", "choose"),
            ("neglect", ["neg", "lect"], "lect", "leave untended"),
            ("lecture", ["lect", "ure"], "lect", "a reading, a talk"),
            ("lesson", None, "les", "something to read or learn: through French, from Latin <i>lectio</i>, a reading"),
            ("legend", ["leg", "end"], "leg", "a story to be read, and the key to a map, as this atlas&rsquo;s Legend is"),
            ("legible", ["leg", "ible"], "leg", "clear enough to read"),
            ("intelligent", ["intel", "lig", "ent"], "lig", "able to choose between, to understand"),
            ("diligent", ["di", "lig", "ent"], "lig", "careful and hard-working"),
            ("elegant", ["e", "leg", "ant"], "leg", "chosen with care, graceful"),
            ("legume", ["leg", "ume"], "leg", "a bean or a pea: what is picked"),
        ]),
        ("Latin", "<i>l&emacr;g&amacr;re</i>, to send with a charge", [
            ("delegate", ["de", "leg", "ate"], "leg", "send someone to act for you"),
            ("relegate", ["re", "leg", "ate"], "leg", "send away, move down"),
            ("legacy", ["leg", "acy"], "leg", "what is handed down"),
            ("colleague", ["col", "league"], "league", "someone chosen to work alongside you"),
            ("college", ["col", "lege"], "lege", "a body of people gathered together"),
        ]),
        ("Latin", "<i>l&emacr;x</i>, <i>l&emacr;gis</i>, law, perhaps a gathering of rules: the link to <i>*leg-</i> is uncertain", [
            ("legal", ["leg", "al"], "leg", "to do with the law"),
            ("legislator", ["legis", "lat", "or"], "legis", "someone who brings in laws"),
            ("legitimate", None, "leg", "allowed by law"),
            ("loyal", ["loy", "al"], "loy", "faithful: through French, from Latin <i>l&emacr;g&amacr;lis</i>, legal"),
            ("privilege", ["privi", "lege"], "lege", "a law for one person, a special right"),
        ]),
    ],
    "students": ["collect", "select", "elect", "lesson", "legend", "logic", "dialogue"],
}
ROOTS = [LEG]


def bold_root(word, spelling):
    i = word.find(spelling)
    return html.escape(word) if i < 0 else html.escape(word[:i]) + "<b>" + html.escape(spelling) + "</b>" + html.escape(word[i + len(spelling):])


def write(OUT, page, header, footer, X):
    """Each root's page; returns the family's words and their links, for the search."""
    (OUT / "roots").mkdir(exist_ok=True)
    found = []
    for R in ROOTS:
        spell = "".join(f'<li><b>{s}</b> <span>{bold_root(w, s)}</span></li>' for s, w in R["spellings"])
        cards = []
        for lang, head, words in R["branches"]:
            items = []
            for w, parts, sp, mean in words:
                ws = " + ".join(f"<b>{html.escape(p)}</b>" if p == sp else html.escape(p) for p in parts) if parts else ""
                items.append(f'<li id="{doors.word_id(w)}"><span class="rw">{bold_root(w, sp)}</span>'
                             + (f'<span class="rs">{ws}</span>' if ws else "") + f'<span class="rm">{mean}</span></li>')
                found.append((w, f"roots/{R['slug']}.html#{doors.word_id(w)}"))
            cards.append(f'<section class="rbranch"><h3>{lang}</h3><p class="rh">{head}</p><ul>{"".join(items)}</ul></section>')
        kids = "".join(f'<li>{bold_root(w, next(sp for b in R["branches"] for x, _, sp, _ in b[2] if x == w))}</li>' for w in R["students"])
        drawn = X["svg_of"]("legomorphic", 58, label="legomorphic, marked: lego + morph + ic") if R["slug"] == "leg" else ""
        srcs = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in R["sources"])
        body = f"""{header(1)}
<main class="root-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only">Derivations &middot; a root family</p>
<h1><span class="t-only">{R["root"]}</span><span class="s-only">{R["root"]} means &lsquo;gather&rsquo;</span></h1>
<p class="lead t-only">{R["gloss"].capitalize()}. Speakers of Greek and Latin carried this Proto-Indo-European root into words about words: gathering words is choosing them, reading them and saying them. English borrowed the family back again and again, and the notation&rsquo;s own name is one of them.</p>
<div class="door-word t-only">{drawn}</div>
</div></section>
<section class="about s-only"><div class="wrap">
<p class="s-lead">These words come from one old word that meant <i>gather</i>.</p>
<ul class="rkids">{kids}</ul>
</div></section>
<section class="about t-only" aria-labelledby="sp-h"><div class="wrap">
<h2 id="sp-h">One root, many spellings</h2>
<p class="sub">The root reached English by many roads, so it has many spellings. The bold letters in each word are the root.</p>
<ul class="rspell">{spell}</ul>
</div></section>
<section class="about t-only" aria-labelledby="fam-h"><div class="wrap">
<h2 id="fam-h">The family</h2>
<p class="sub">Each word with its parts, where they can be shown, and what it means.</p>
<div class="rbranches">{"".join(cards)}</div>
</div></section>
<section class="about t-only" aria-labelledby="src-h"><div class="wrap prose">
<h2 id="src-h">Sources</h2>
<ul>{srcs}</ul>
{X["uc"]("the family follows Etymonline, which draws on Calvert Watkins, and the Indo-European Lexicon, which follows Pokorny. Wiktionary marks the link from <i>l&emacr;x</i>, law, as uncertain. Next: check the family against Watkins&rsquo;s entry, and draw each word in the notation once its marking is ruled.")}
</div></section>
</main>
{footer(1)}"""
        (OUT / "roots" / f"{R['slug']}.html").write_text(page(f"{R['root']}: {R['gloss']} · Sound and Word Atlas", body, 1,
                                                          f"The root {R['root']}, {R['gloss']}, and its family of English words."), encoding="utf-8")
    return found
