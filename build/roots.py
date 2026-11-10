"""Families behind Derivations: roots/<slug>.html. The first, the root *leg-, made on 8 November 2026; the second, the
base hap, on 9 November 2026.

A family page gives the root or base and its meaning, the spellings it takes in English, and its family group by group:
each word with the family's spelling in bold, its parts where they can be shown, and a plain meaning. *leg- follows
Etymonline's entry for the root, which draws on Calvert Watkins, and the Indo-European Lexicon of the Linguistics
Research Center at the University of Texas at Austin, which follows Pokorny; the page links both. The site plan has the
roots follow Watkins's American Heritage Dictionary of Indo-European Roots (3rd ed., 2011), which these pages haven't
yet been checked against.

Hap is a base rather than a Proto-Indo-European root: a word English took from Old Norse, which is no longer said on
its own (it is bound now, as fun is not). Its page groups the family by what follows hap, since that decides whether
the p doubles, and shows the letter pairs its seams split (mishap, haphazard). Its words are drawn with the codes in
site_codes.py; happy's seam was ruled on 9 November 2026, and the rest follow the analogs named there.

Each word in a family gets an id (doors.word_id), and write() returns (word, link, label) for the search."""
import html
from urllib.parse import quote
import doors

def etym(word, slug):
    """Where a family word's own history is: its Etymonline entry (by search, so the link holds), or for the notation's
    own name, its entry in Definitions."""
    return "../definitions.html#def-legomorphic" if word == "legomorphic" else f"https://www.etymonline.com/search?q={quote(word)}"

LEG = {
    "slug": "leg", "root": "*leg-", "gloss": "to gather, to collect", "kind": "a root family",
    "h1_s": "*leg- means &lsquo;gather&rsquo;",
    "lead": "To gather, to collect. Speakers of Greek and Latin carried this Proto-Indo-European root into words about "
            "words: gathering words is choosing them, reading them and saying them. English borrowed the family back again "
            "and again, and the notation&rsquo;s own name is one of them.",
    "drawn": ("legomorphic", "legomorphic, marked: lego + morph + ic"),
    "sources": [("Etymonline, *leg-", "https://www.etymonline.com/word/%2Aleg-"),
                ("Indo-European Lexicon, leg̑- (Linguistics Research Center, University of Texas at Austin)", "https://lrc.la.utexas.edu/lex/master/1131"),
                ("Wiktionary, Proto-Indo-European *leǵ-", "https://en.wiktionary.org/wiki/Reconstruction:Proto-Indo-European/le%C7%B5-")],
    "spell_h": "One root, many spellings",
    "spell_sub": "The root reached English by many roads, so it has many spellings. The bold letters in each word are the root.",
    "spellings": [("leg", "legend"), ("lect", "collect"), ("lig", "diligent"), ("log", "logic"), ("logue", "dialogue"),
                  ("lex", "lexicon"), ("lege", "college"), ("league", "colleague"), ("les", "lesson"), ("loy", "loyal")],
    "fam_sub": "Each word with its parts, where they can be shown, and what it means. Each word links to its history in Etymonline.",
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
    "s_lead": "These words come from one old word that meant <i>gather</i>.",
    "uc": "the family follows Etymonline, which draws on Calvert Watkins, and the Indo-European Lexicon, which follows "
          "Pokorny. Wiktionary marks the link from <i>l&emacr;x</i>, law, as uncertain. Next: check the family against "
          "Watkins&rsquo;s entry, and draw each word in the notation once its marking is ruled.",
    "label": "Root family: *leg-",
    "desc": "The root *leg-, to gather, to collect, and its family of English words.",
}

HAP = {
    "slug": "hap", "root": "hap", "gloss": "chance, luck", "kind": "a base family",
    "h1_s": "hap means &lsquo;luck&rsquo;",
    "lead": "Chance, luck. English took <i>hap</i> from Old Norse <i>happ</i> around 1200. It&rsquo;s rarely said on its "
            "own now, but it lives on in <i>happy</i>, <i>happen</i> and <i>mishap</i>, and the Indo-European Lexicon "
            "traces it back to a root <i>*kob-</i>, to fit, to fare well. Its spelling shows how it joins: <b>happ</b> "
            "before a vowel, <b>hap</b> everywhere else.",
    "drawn": ("happy", "happy, marked: happ + y"),
    "sources": [("Etymonline: <i>hap</i>, <i>happy</i>, <i>happen</i>, <i>mishap</i>, <i>haphazard</i>, <i>perhaps</i> and the rest", "https://www.etymonline.com/search?q=hap"),
                ("Indo-European Lexicon, kob- (Linguistics Research Center, University of Texas at Austin)", "https://lrc.la.utexas.edu/lex/master/0991"),
                ("Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994): <i>chubby</i>, <i>shabby</i> and "
                 "<i>happy</i>, pp. 1&ndash;3, and the spellings of /p/, p. 16, in the publisher&rsquo;s preview",
                 "https://api.pageplace.de/preview/DT0400.9781134872244_A23786723/preview-9781134872244_A23786723.pdf"),
                ("Greg Brooks, <i>Dictionary of the British English Spelling System</i>, ch. 4: <i>happy</i> among the doubled p&rsquo;s",
                 "https://books.openbookpublishers.com/10.11647/obp.0053/ch4.xhtml")],
    "spell_h": "One base, two spellings",
    "spell_sub": "The p doubles only when a vowel comes next, as the n of <i>fun</i> does in <i>funny</i>, so the box can "
                 "keep the a short (<a href=\"../steps/14.html\">step 14</a>). Before a consonant nothing reaches back, and "
                 "English doesn&rsquo;t end a word in pp (<a href=\"../steps/06.html\">step 6</a>), so one p does the job.",
    "spell_drawn": [("happen", "happ + en: a vowel comes next"), ("hapless", "hap + less: a consonant comes next"),
                    ("mishap", "mis + hap: hap ends the word")],
    "fam_sub": "Each word with its parts and what it means, grouped by what comes after <i>hap</i>. Each word links to its history in Etymonline.",
    "branches": [
        ("Before a vowel", "<b>happ</b>: the p doubles and the a stays short. The n of <i>happening</i> stays single, "
                           "because <i>en</i> isn&rsquo;t stressed, as in <i>opening</i>.", [
            ("happy", ["happ", "y"], "happ", "having hap: lucky, at first, then glad"),
            ("happen", ["happ", "en"], "happ", "to come about, at first by chance"),
            ("happily", ["happ", "i", "ly"], "happ", "in a happy way"),
            ("happiness", ["happ", "i", "ness"], "happ", "being happy"),
            ("unhappy", ["un", "happ", "y"], "happ", "not happy"),
            ("happening", ["happ", "en", "ing"], "happ", "something that happens"),
        ]),
        ("Before a consonant", "<b>hap</b>: nothing reaches back to the a, so one p is enough.", [
            ("hapless", ["hap", "less"], "hap", "without luck"),
            ("haply", ["hap", "ly"], "hap", "by chance: an old word for perhaps"),
            ("haphazard", ["hap", "hazard"], "hap", "by chance, with no plan"),
        ]),
        ("At the end", "<b>hap</b>: English doesn&rsquo;t end a word in pp.", [
            ("mishap", ["mis", "hap"], "hap", "bad luck, a small accident"),
            ("perhaps", ["per", "hap", "s"], "hap", "by chances: maybe"),
            ("mayhap", ["may", "hap"], "hap", "it may happen: an old word for perhaps"),
        ]),
    ],
    # (id, heading, the text, words drawn under it as (word, caption))
    "extra": [
        ("pairs", "Letter pairs the seam splits",
         "Read these without the seam and they go wrong. In <i>mishap</i> the s and the h meet across the seam, so they "
         "don&rsquo;t spell <i>sh</i>: mis + hap, not mish + ap. In <i>haphazard</i> the p and the h meet the same way, so "
         "they don&rsquo;t spell the sound of <i>ph</i> in <a href=\"../steps/32.html\"><i>phone</i></a>: hap + hazard. "
         "<i>Shepherd</i> (sheep + herd) and <i>uphill</i> work like this too.",
         [("mishap", "s + h, not sh"), ("haphazard", "p + h, not ph")]),
        ("meant", "What happy meant",
         "<i>Happy</i> is hap + y: having hap. Its first meaning, in the late 1300s, was lucky, favoured by fortune, and the "
         "sense of glad came in the same century. <i>Lucky</i>, luck + y, is built the same way, and means now what "
         "<i>happy</i> meant then. The y is the ending of <i>sunny</i> and <i>funny</i>: having, or full of, what the base "
         "names. Read without hap, <i>happy</i> means being in a happy state, which goes in a circle. With hap, it means "
         "having luck.", []),
        ("double", "Does the double p show the seam?",
         "Not on its own. A double keeps a short vowel short whether or not there&rsquo;s a join: <i>rabbit</i> and "
         "<a href=\"leg.html#w-lesson\"><i>lesson</i></a> double with nothing to join. Carney counts <i>happy</i> among the "
         "ordinary doubles, with <i>hobby</i>, <i>silly</i> and <i>merry</i>, and says the hidden boundary in <i>chubby</i> "
         "and <i>shabby</i> needn&rsquo;t be known to explain theirs. What shows the seam is the family: the same hap, with the same meaning, in <i>hapless</i> and "
         "<i>mishap</i>, where nothing doubles. <i>Fun</i> is <a href=\"../definitions.html#def-free\">free</a>, a word on "
         "its own, so the seam in <i>funny</i> is easy to see; <i>hap</i> is <a href=\"../definitions.html#def-bound\">bound</a> "
         "now, so the family does the showing.", []),
    ],
    "students": ["happy", "happen", "mishap", "perhaps"],
    "s_lead": "These words come from <b>hap</b>. It is an old word for luck.",
    "uc": "the family follows Etymonline and the Indo-European Lexicon, which cites Watkins. Next: check it against "
          "Watkins&rsquo;s entry for <i>*kob-</i>, as for <i>*leg-</i>.",
    "label": "Base family: hap",
    "desc": "The base hap, chance or luck, and its family: happy, happen, mishap and haphazard, and why happy has two p's and mishap one.",
}
ROOTS = [LEG, HAP]


def bold_root(word, spelling):
    i = word.find(spelling)
    return html.escape(word) if i < 0 else html.escape(word[:i]) + "<b>" + html.escape(spelling) + "</b>" + html.escape(word[i + len(spelling):])


def write(OUT, page, header, footer, X):
    """Each family's page; returns the family's words, their links and the family's label, for the search."""
    (OUT / "roots").mkdir(exist_ok=True)
    found = []
    def drawn_row(items):
        return ('<div class="words rrow">' + "".join(
            f'<figure class="word">{X["svg_of"](w, 46, label=f"{w}, marked")}<figcaption>{cap}</figcaption></figure>'
            for w, cap in items) + "</div>") if items else ""
    for R in ROOTS:
        if R.get("spell_drawn"):
            spell = drawn_row(R["spell_drawn"])
        else:
            spell = '<ul class="rspell">' + "".join(f'<li><b>{s}</b> <span>{bold_root(w, s)}</span></li>' for s, w in R["spellings"]) + "</ul>"
        cards = []
        for lang, head, words in R["branches"]:
            items = []
            for w, parts, sp, mean in words:
                ws = " + ".join(f"<b>{html.escape(p)}</b>" if p == sp else html.escape(p) for p in parts) if parts else ""
                items.append(f'<li id="{doors.word_id(w)}"><a class="rw" href="{etym(w, R["slug"])}">{bold_root(w, sp)}</a>'
                             + (f'<span class="rs">{ws}</span>' if ws else "") + f'<span class="rm">{mean}</span></li>')
                found.append((w, f"roots/{R['slug']}.html#{doors.word_id(w)}", R["label"]))
            cards.append(f'<section class="rbranch"><h3>{lang}</h3><p class="rh">{head}</p><ul>{"".join(items)}</ul></section>')
        kids = "".join(f'<li>{bold_root(w, next(sp for b in R["branches"] for x, _, sp, _ in b[2] if x == w))}</li>' for w in R["students"])
        dw, dl = R["drawn"]
        drawn = X["svg_of"](dw, 58, label=dl)
        extra = "".join(f"""<section class="about t-only" aria-labelledby="{sid}-h"><div class="wrap">
<h2 id="{sid}-h">{head}</h2>
<p class="sub">{text}</p>
{drawn_row(row)}
</div></section>
""" for sid, head, text, row in R.get("extra", []))
        srcs = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in R["sources"])
        body = f"""{header(1)}
<main class="root-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only">Derivations &middot; {R["kind"]}</p>
<h1><span class="t-only">{R["root"]}</span><span class="s-only">{R["h1_s"]}</span></h1>
<p class="lead t-only">{R["lead"]}</p>
<div class="door-word t-only">{drawn}</div>
</div></section>
<section class="about s-only"><div class="wrap">
<p class="s-lead">{R["s_lead"]}</p>
<ul class="rkids">{kids}</ul>
</div></section>
<section class="about t-only" aria-labelledby="sp-h"><div class="wrap">
<h2 id="sp-h">{R["spell_h"]}</h2>
<p class="sub">{R["spell_sub"]}</p>
{spell}
</div></section>
<section class="about t-only" aria-labelledby="fam-h"><div class="wrap">
<h2 id="fam-h">The family</h2>
<p class="sub">{R["fam_sub"]}</p>
<div class="rbranches">{"".join(cards)}</div>
</div></section>
{extra}<section class="about t-only" aria-labelledby="src-h"><div class="wrap prose">
<h2 id="src-h">Sources</h2>
<ul>{srcs}</ul>
{X["uc"](R["uc"])}
</div></section>
</main>
{footer(1)}"""
        (OUT / "roots" / f"{R['slug']}.html").write_text(page(f"{R['root']}: {R['gloss']} · Sound and Word Atlas", body, 1, R["desc"]), encoding="utf-8")
    return found
