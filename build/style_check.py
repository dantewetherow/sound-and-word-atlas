"""Prose style check (22 November 2026), from the Prose style reference (Dante's doc, same date).

The check flags; a person decides. A flag is a question: what fact does this word stand for? Write the fact.
It reads built pages, so it sees what a reader sees: slide text (learner-facing), slide notes and page prose
(teacher-facing), and headings.

Rules
  W  flagged words: the hushed, oracular register (lean, echo, secret, whisper, story, brought to light ...) and
     wonder adjectives (beautiful, fascinating ...)
  F  closing fragments meant to sound wise ("A lean, not a rule." "No echo." "Same letters, two reasons.")
  H  headings with a flagged word, or a heading that is an instruction to listen with no content ("Listen again")
  L  length: learner slide lines over 12 words; teacher sentences over 25 words
  C  house conventions: em dashes; "says" with a letter as subject outside the explanation of the phrase; "students"

Usage: python3 build/style_check.py docs/studies/phonesthemes.html docs/lists/phonesthemes.html
       run(OUT, paths) from the build returns {path: [(rule, where, text, note)]}."""
import re, sys, pathlib
from bs4 import BeautifulSoup

WORDS = {   # pattern: what it usually stands for
    r"\blean(s|ing|ed)?\b": "a pattern with exceptions: give the count",
    r"\b(echo|echoes|rhyme|resonance)\b": "a shared sound: name it",
    r"\b(secret|hidden|hiding|buried)\b": "a fact the reader hasn't met: state it",
    r"\b(whisper\w*|quiet|quietly|gently|softly)\b": "usually nothing: cut, or name the fact",
    r"\b(magic\w*|myster\w*)\b": "a pattern we can explain: explain it",
    r"\b(story|stories|journey\w*|voyage)\b": "history or etymology: give it",
    r"\b(brought to light|unlock\w*|unveil\w*)\b": "shows, marks, explains",
    r"\breveal(s|ed|ing)?\b": "shows, marks, explains",
    r"\b(the heart of|at its core|essence)\b": "the point: state it",
    r"\bstopped looking like\b": "share a root; the spelling no longer shows it",
    r"\b(carr(y|ies)|keeps|holds) the (meaning|sound)\b": "spells, marks, comes from",
    r"\b(beautiful\w*|fascinat\w*|remarkabl\w*|elegan\w*|wonderful)\b": "show the thing; let the reader decide",
    r"\byou(&rsquo;|')ve always\b": "mind-reading: ask instead",
    r"\bdeep reason\b": "give the reason",
}
FRAGMENT = [
    (r"^(A|An|The) [\w\s-]{0,30}, not (a |an |the )?[\w-]+\.$", "an X-not-Y fragment"),
    (r"^No [\w\s]{1,15}\.$", "a 'No X.' fragment"),
    (r"^Same [\w\s]{1,20}, (two|different) [\w\s]{1,15}\.$", "a 'Same X, two Y.' fragment"),
    (r"^(And )?that changes everything\.?$", "a dramatic close"),
]
LISTEN = re.compile(r"^(listen|look)( again| closely| to the \w+)?$", re.I)
SAYS = re.compile(r"\b(?:the|its|an?)\s+(?:[a-z]{1,4}|vowel|letter|team|unit|consonant|prefix|suffix|ending|part)\s+says\b(?! (?:its name&rdquo;|its name”))", re.I)
EXPLAIN_SAYS = re.compile(r"says its name(&rdquo;|”|\")|classroom phrase", re.I)


def sentences(text):
    text = re.sub(r"\s+", " ", text).strip()
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def words(s):
    return len(re.findall(r"[A-Za-z][\w’'-]*", s))


def check_text(text, where, learner=False, out=None, wtext=None):
    """wtext: the same text with words under discussion (in italics) masked, for the word flags: a page may talk
    about the word elegant without calling anything elegant."""
    out = [] if out is None else out
    for s in sentences(wtext if wtext is not None else text):
        for pat, note in WORDS.items():
            m = re.search(pat, s, re.I)
            if m: out.append(("W", where, s, f"“{m.group(0)}”: {note}"))
    for s in sentences(text):
        for pat, note in FRAGMENT:
            if re.match(pat, s): out.append(("F", where, s, note + ": replace with a full sentence that states the result"))
        n = 0 if s.count("→") >= 3 or s.count("+") >= 4 else words(s)   # a run of word sums is a list, not a sentence
        if learner and n > 12: out.append(("L", where, s, f"{n} words on a learner line (12 or fewer)"))
        if not learner and n > 25: out.append(("L", where, s, f"{n} words (25 or fewer)"))
        if "—" in s: out.append(("C", where, s, "em dash"))
        if SAYS.search(s) and not EXPLAIN_SAYS.search(s): out.append(("C", where, s, "a letter 'says': letters spell sounds"))
        if re.search(r"\bstudents?\b", s, re.I): out.append(("C", where, s, "'students': we write 'learners'"))
    return out


def masked(el):
    """The element's text with each italic word or phrase replaced by a placeholder (a word being discussed)."""
    import copy
    c = copy.copy(el)
    for t in c.find_all(["i", "em"]): t.string = "‹w›"
    return c.get_text(" ", strip=True)


def check_page(path):
    soup = BeautifulSoup(pathlib.Path(path).read_text(encoding="utf-8"), "html.parser")
    for t in soup(["script", "style", "svg", "noscript"]): t.decompose()
    out = []
    for h in soup.find_all(["h1", "h2", "h3"]):
        t = h.get_text(" ", strip=True)
        if LISTEN.match(t): out.append(("H", "heading", t, "an instruction with no content: say what is on the page"))
        for pat, note in WORDS.items():
            if re.search(pat, t, re.I): out.append(("H", "heading", t, note))
    slides = soup.select("section.slide")
    if slides:                                   # a deck: slide text is learner-facing, notes are teacher-facing
        for i, sl in enumerate(slides, 1):
            head = sl.find(["h1", "h2"])
            learner = not (head and re.match(r"(for teachers|sources)", head.get_text(" ", strip=True), re.I))
            note = sl.select_one(".tnote")
            if note:
                check_text(note.get_text(" ", strip=True), f"slide {i} note", False, out); note.decompose()
            for el in sl.find_all(["p", "li", "figcaption"]):
                check_text(el.get_text(" ", strip=True), f"slide {i}", learner, out)
    else:
        main = soup.find("main") or soup
        for el in main.find_all(["p", "li", "td", "figcaption"]):
            if el.find(attrs={"lang": re.compile(r"^(la|grc|el)")}): continue   # a quoted line of Latin or Greek, with its translation and source
            check_text(el.get_text(" ", strip=True), "page", False, out, masked(el))
    seen, uniq = set(), []
    for r in out:
        if r not in seen: seen.add(r); uniq.append(r)
    return uniq


def run(OUT, paths=None):
    """Report only: writes docs/style-audit.json and prints the count. Pages listed in CLEAN must have no flags."""
    import json
    OUT = pathlib.Path(OUT)
    paths = paths or sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*.html") if "sessions" not in p.parts)
    res = {p: check_page(OUT / p) for p in paths}
    res = {p: v for p, v in res.items() if v}
    (OUT / "style-audit.json").write_text(json.dumps({p: [list(r) for r in v] for p, v in res.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(v) for v in res.values())
    dirty = [p for p in CLEAN if p in res]
    print(f"style check | {len(paths)} pages, {n} flags on {len(res)} pages (docs/style-audit.json) | reviewed and clean: {len(CLEAN) - len(dirty)} of {len(CLEAN)}")
    assert not dirty, f"style check: pages marked clean have flags again: {dirty}"
    return res


CLEAN = ["studies/phonesthemes.html", "lists/phonesthemes.html",   # reviewed against the reference, 22 November 2026
         "studies/per.html", "studies/education.html", "studies/leg.html", "studies/sign.html", "studies.html", "about.html",
         "roots/deuk.html", "roots/hap.html", "roots/leg.html", "roots/leuk.html", "roots/med.html", "roots/per.html",
         "roots/sem.html", "roots/sign.html", "surprising.html", "system.html", "index.html", "tools.html",
         "roots/steg.html", "studies/protect.html", "lists/family-steg.html", "teams.html",
         "roots/form.html", "studies/form.html", "lists/family-form.html", "tents/form.html"]   # form, 25 November 2026   # the protect family and study, 24 November 2026   # surprising.html: written to the reference, 23 November 2026


if __name__ == "__main__":
    for p in sys.argv[1:]:
        flags = check_page(p)
        print(f"\n== {p}: {len(flags)} flags")
        for rule, where, s, note in flags:
            print(f"  {rule} | {where} | {s[:150]}\n      -> {note}")
