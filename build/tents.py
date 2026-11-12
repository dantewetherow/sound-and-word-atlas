"""Affix tent cards (12 November 2026): tents.html, for the families' extension work.

A tent card is a half sheet folded along its middle so it stands up. Both sides show the part, so the learners and the
teacher can read it; the teacher's side also carries what the part means and how it joins. Learners stand a prefix, a
root and a suffix in a row and read the word; then they swap the root and keep the affixes, which is the point: the
affixes are common, the roots change. Process cards stand at a seam where the join changes something: the e drops
(out with the old, in with the new), y turns to i, a consonant doubles, or a prefix changes its last letter.

Roots are the families' bases (roots.py) and eight common Latin roots that have no family page yet. Meanings are from
Etymonline. Each example word was checked as a real word built from the parts shown; most are on the families' pages."""
import html

SRC = "https://www.etymonline.com/"

# (part, meaning, how it joins, examples)
PREFIXES = [
    ("re-", "again, back", "Joins with no change: re + act, re + port.", "react, report, reject, reduce, respect"),
    ("un-", "not", "Joins with no change, so <i>un + named</i> keeps both n&rsquo;s.", "unformed, unselected, unreported"),
    ("in-", "not; or in, into", "Changes its n to match: <b>il-</b> before l (illuminate), <b>ir-</b> before r, <b>im-</b> before b, m and p (import).", "inform, inject, inspect, illustrate, import"),
    ("con-", "with, together", "Changes its n to match: <b>col-</b> before l (collect), <b>cor-</b> before r, <b>com-</b> before b, m and p (commodity).", "conduct, construct, contract, collect, commodity"),
    ("ad-", "to, toward", "Takes the first letter of the root: <b>ac-</b> (accommodate), <b>as-</b> (assemble), <b>at-</b> (attract).", "attract, assemble, accommodate, adduce"),
    ("e-, ex-", "out", "Usually <b>ex-</b> before a vowel and before c, p and t (export, extract), and <b>e-</b> before most other consonants (elect, erupt).", "export, extract, elect, erupt, educate"),
    ("pro-", "forward, for", "Joins with no change.", "produce, project, protract, prospect"),
    ("de-", "down, away", "Joins with no change.", "deduct, deport, destruct, detract"),
    ("pre-", "before", "Joins with no change.", "predict, preselect, prefix"),
    ("inter-", "between", "Joins with no change, so <i>inter + rupt</i> keeps both r&rsquo;s.", "interrupt, interject, interact"),
    ("trans-", "across", "Joins with no change.", "transport, transform, translucent"),
    ("sub-", "under", "Joins with no change before most letters.", "subtract, subject, submit"),
]
SUFFIXES = [
    ("-ion", "an act, or its result", "Starts with a vowel: a silent e drops before it (creat(e) + ion).", "action, election, projection, eruption"),
    ("-or", "one who, a thing that", "Starts with a vowel: a silent e drops before it.", "actor, conductor, projector, inspector"),
    ("-er", "one who, a thing that; more", "Starts with a vowel: a silent e drops, a short word doubles, y turns to i.", "reporter, producer, transformer"),
    ("-ive", "tending to", "Starts with a vowel: a silent e drops before it.", "active, selective, destructive, attractive"),
    ("-able", "can be", "Starts with a vowel: a silent e drops, unless it keeps c or g soft (noticeable).", "portable, reportable, predictable"),
    ("-ible", "can be", "Starts with a vowel: a silent e drops before it.", "legible, reducible, deductible"),
    ("-ate", "to make, to do", "Starts with a vowel: a silent e drops before it.", "illustrate, illuminate, dictate, educate"),
    ("-ure", "the act, the result", "Starts with a vowel: a silent e drops before it.", "structure, lecture, rupture"),
    ("-al", "of, like", "Starts with a vowel: a silent e drops before it.", "formal, modal, medical"),
    ("-ous", "full of", "Starts with a vowel: a silent e drops before it.", "luminous, commodious"),
    ("-ing", "doing", "Starts with a vowel: a silent e drops, a short word doubles. y stays (drying).", "reporting, inspecting, reducing"),
    ("-ed", "did, done", "Starts with a vowel: a silent e drops, a short word doubles, y turns to i.", "reported, projected, reduced"),
    ("-s, -es", "more than one; does", "-s joins with no change; -es after s, x, z, sh and ch.", "reports, projects, reduces"),
    ("-ly", "in that way", "Starts with a consonant: the e stays (safely). y turns to i (happily).", "actively, formally, selectively"),
    ("-ful", "full of", "Starts with a consonant: the e stays (hopeful).", "respectful, hopeful"),
]
ROOTS = [
    ("lect", "choose, gather, read", "roots/leg.html", "collect, select, elect, lecture, selective"),
    ("duce", "lead (before no ending, or -er, -ible)", "roots/deuk.html", "produce, reduce, deduce, producer, reducible"),
    ("duct", "led (before -ion, -or, -ive)", "roots/deuk.html", "product, conductor, deduction, productive"),
    ("simil", "like, the same", "roots/sem.html", "similar, assimilate, simile"),
    ("semble", "together, alike", "roots/sem.html", "assemble, resemble, ensemble"),
    ("mod", "measure, manner", "roots/med.html", "mode, modal, module, commodity, accommodate"),
    ("med", "heal, treat", "roots/med.html", "medical, medicate"),
    ("lumin", "light", "roots/leuk.html", "illuminate, luminous, illumination"),
    ("lustr", "light, bright", "roots/leuk.html", "illustrate, illustration, illustrative"),
    ("luc", "light, clear", "roots/leuk.html", "lucid, translucent, elucidate"),
    ("struct", "build", None, "construct, structure, instruct, destructive, construction"),
    ("port", "carry", None, "import, export, transport, report, portable"),
    ("spect", "look", None, "inspect, respect, prospect, spectator, inspection"),
    ("ject", "throw", None, "project, reject, inject, object, projector"),
    ("rupt", "break", None, "erupt, interrupt, disrupt, rupture, eruption"),
    ("tract", "pull, drag", None, "attract, tractor, subtract, extract, attractive"),
    ("dict", "say", None, "predict, dictate, contradict, prediction"),
    ("form", "shape", None, "inform, reform, transform, formal, formation"),
]
PROCESSES = [
    ("(e)", "Out with the old, in with the new", "Stand this over a silent e when a suffix starting with a vowel joins: the e drops and the new vowel does its job. creat(e) + ion, reduc(e) + ing.", "steps/15.html"),
    ("y &rarr; i", "y turns to i", "Stand this over a y after a consonant when a suffix joins, except -ing. happ(y&rarr;i) + ly.", "steps/29.html"),
    ("+ p, + t, + g&hellip;", "Double it", "Stand this at the seam when a short word with one short vowel and one consonant at the end meets a suffix that starts with a vowel. hop + p + ing.", "steps/14.html"),
    ("n &rarr; l, r, m", "The prefix changes", "Stand this over the last letter of in- or con- when it changes to match the root: in &rarr; il (illuminate), con &rarr; col (collect).", "roots/leg.html"),
]


def card(kind, part, mean, rule, ex, link=None):
    """One tent: the top panel upside down for when it stands, then the teacher's panel."""
    more = f'<span class="tlink"><a href="{link}">{"the family" if kind == "root" else "more"}</a></span>' if link else ""
    return (f'<div class="tent t-{kind}">'
            f'<div class="tpanel flip"><span class="tpart">{part}</span></div>'
            f'<div class="tpanel"><span class="tpart">{part}</span><span class="tmean">{mean}</span>'
            f'{f"<span class=trule>{rule}</span>" if rule else ""}<span class="tex">{ex}</span>{more}</div></div>')


def write(OUT, page, header, footer, X):
    sec = lambda h, kind, cards, sub: (f'<section class="about tset"><div class="wrap"><h2>{h}</h2><p class="sub noprint">{sub}</p>'
                                       f'<div class="tents">{"".join(cards)}</div></div></section>')
    body = f"""{header(0)}
<main class="tents-page">
<section class="hero noprint"><div class="wrap">
<p class="eyebrow t-only">For teachers &middot; Extension</p>
<h1>Affix tent cards</h1>
<p class="lead">Cards that stand up on a desk: prefixes, roots, suffixes, and cards for the joins that change something. Stand a prefix, a root and a suffix in a row and read the word. Then keep the affixes and swap the root. The affixes are few and come back again and again; the roots change.</p>
<p class="board"><a href="#" onclick="window.print(); return false;">Print the cards</a>: two to a page. Cut each page in half, fold each half along the dotted line, and stand it up. Both sides show the part; the side that faces you also says what it means and how it joins.</p>
</div></section>
{sec("Prefixes", "pre", [card("pre", p, m, r, e) for p, m, r, e in PREFIXES], "Some prefixes change their last letter to match the root they join. The card says when.")}
{sec("Roots", "root", [card("root", p, m, None, e, l) for p, m, l, e in ROOTS], "The first ten are the bases of the word families, extension work for intermediate and middle school. The last eight are common Latin roots with no family page yet.")}
{sec("Suffixes", "suf", [card("suf", p, m, r, e) for p, m, r, e in SUFFIXES], "A suffix that starts with a vowel changes the join; one that starts with a consonant doesn&rsquo;t.")}
{sec("Joins that change something", "proc", [card("proc", p, m, r, "", l) for p, m, r, l in PROCESSES], "Stand one of these at the seam where the join changes a letter. Out with the old, in with the new is the first.")}
<section class="about noprint"><div class="wrap prose">
<h2>Using them</h2>
<p>Start with one root and three or four affixes, and let learners find the real words. Then keep the affixes and swap the root: <i>con + struct + ion</i>, <i>con + duct + ion</i>, <i>con + tract + ion</i>, <i>con + ject + ion</i>? Not every row makes a word, and that last one doesn&rsquo;t. Asking which ones do, and checking a dictionary, is the inquiry.</p>
<p>When a join changes a letter, a process card goes at the seam. <i>Produce + er</i> needs the (e) card: <i>produc(e) + er</i>. <i>In + lumin + ate</i> needs the prefix card: <i>il + lumin + ate</i>.</p>
<p>The word families are where these come from: <a href="roots/leg.html">*leg-</a>, <a href="roots/deuk.html">*deuk-</a>, <a href="roots/sem.html">*sem-</a>, <a href="roots/med.html">*med-</a> and <a href="roots/leuk.html">*leuk-</a>, each with its own <a href="lists/index.html#families">spelling list</a>.</p>
<p class="sub">Meanings: <a href="{SRC}">Etymonline</a>. Word sums and matrices come from Melvyn Ramsden&rsquo;s Real Spelling, brought into classrooms by Peter Bowers as structured word inquiry.</p>
{X["uc"]("the first set, since 12 November 2026. Not every affix joins every root; a swap grid showing which rows make words is next.")}
</div></section>
</main>
{footer(0)}"""
    (OUT / "tents.html").write_text(page("Affix tent cards · A Legend for English Words", body, 0,
                                         "Printable tent cards for word building: prefixes, roots, suffixes and the joins that change a letter."), encoding="utf-8")
    return len(PREFIXES) + len(ROOTS) + len(SUFFIXES) + len(PROCESSES)
