"""The gloss rules, and a check that holds the site to them (20 November 2026).

They came out of one mistake. A slide glossed *silence* as "being silent", which is what *silent* means: -ent is Latin's
present form, and describes; -ence names. Read as a noun ("being silent is hard"), the gloss was right; read the other
way ("being silent, she waited"), it was the adjective's. A learner putting the parts back together would get the word
wrong. The fix was to show the job, not define it: she is patient / she has patience.

The rules, for every meaning on the site (the parts glossary, family words, the word walk, slide tiles and glosses, and
read-from-the-end lines):

 1. Same job as the word. A noun is glossed with a noun (a plan; what you have from trying), a describing word with a
    describing phrase (able to be read; full of fear), a doing word with a doing word (to mark out; give up). The test:
    put the gloss in the word's own sentence. "We sat in silence" takes "the state of being silent", not "being silent".
 2. No bare *being* or *-ing* at the head of a noun's gloss. "Being simple" and "choosing by vote" can be read either
    way. Give the noun an article or a head noun: the quality of being simple; a choosing by vote; the bringing up.
 3. Sister endings keep different jobs, worded differently: -ent and -ant describe, -ence and -ance name; -ate makes a
    doing word, -ion names the doing; -ive describes, -ion names. A sister's gloss never borrows the other's words.
 4. Read from the end gives the word's own job. The last part decides it, so the reading starts there: *legend* is
    "something to be read", not "to be read"; *experience* is "what you have from trying things out".
 5. Where an ending's job is grammar, show it in pairs of sentences, not a definition: she is patient / she has patience.
 6. One gloss per part. A part is glossed once, in roots.PARTS (or roots.ROOT_PARTS); parts.MEANS holds only the
    parts the families don't. A part with two jobs says both, with an example of each: -ing, happening now (she is
    signing), or the doing of it (signing is fun).
 7. One meaning per word. A slide may say it more simply than the family page, but never differently: *lesson* is a
    reading on every page, never a choosing.
 8. The meaning now, the history in the note. A literal reading from the parts is welcome, marked as such ("mark out:
    a plan"), but the word's present use comes with it.

Rules 1 to 4 and 6 are checked here, where a pattern can find them; 5, 7 and 8 are for the writer and the reviewer.
The checks are deliberately narrow: they stop the build only for the shapes that went wrong before. A describing word
glossed with an -ing phrase (deductive, "reasoning from a rule to a case") reads both ways and slips past: watch for it."""
import json, re, pathlib, html as H

NOUN_ENDS = ("ence", "ance", "ency", "ancy", "ion", "ment", "ity", "ness", "ism", "ship", "hood", "dom")
ADJ_ENDS = ("ive", "ous", "ible", "able", "ful", "less")          # endings that only describe; -al, -ent, -ant, -ic, -ary also name (signal, patient, logic)
NOT_ING = {"thing", "something", "nothing", "anything", "king", "ring", "spring", "string", "wing", "evening", "morning", "meaning"}
NOUN_HEAD = re.compile(r"^(a|an|the|someone|something|what)\b")
ALLOW = {("-ing", "happening now")}                                # the -ing ending itself has the participle's job


def text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", H.unescape(s or ""))).strip()


def head(g):
    g = re.sub(r"^from the end:\s*", "", text(g).lower())
    return re.split(r"[:;,.(]", g)[0].strip()


def ing_head(h):
    w = h.split(" ")[0] if h else ""
    return w == "being" or (w.endswith("ing") and w not in NOT_ING)


def check_word(w, g, where, bad):
    lw, h = w.lower().strip(), head(g)
    if (lw, h) in ALLOW or not h: return
    if lw.endswith(NOUN_ENDS) and ing_head(h):
        bad.append(f"{where}: {w}, a noun, is glossed “{text(g)}”: give it an article or a head noun (rule 2)")
    if lw.endswith(ADJ_ENDS) and NOUN_HEAD.match(h):
        bad.append(f"{where}: {w}, a describing word, is glossed as a noun, “{text(g)}” (rule 1)")


def deck_glosses(path):
    """(word, gloss, slide) for each word and its gloss in a built deck: the word is the drawing's label or the typed word."""
    s = path.read_text(encoding="utf-8")
    for n, sl in enumerate(re.split(r'<section class="slide', s)[1:], 1):
        for cell in re.split(r'<div data-s="\d+"', sl)[1:]:
            g = re.search(r'<span class="g">(.*?)</span>', cell, re.S)
            if not g: continue
            w = re.search(r'aria-label="([^"]+)"', cell) or re.search(r'<span class="w">(.*?)</span>', cell, re.S)
            if w: yield text(w.group(1)).replace(", marked", "").replace(" ", ""), g.group(1), f"{path.name}#{n}"
        for m in re.finditer(r'<span class="pc"><b>(.*?)</b><em[^>]*>(.*?)</em>', sl, re.S):
            yield "-" + text(m.group(1)), m.group(2), f"{path.name}#{n} tile"


def run(OUT):
    import roots, parts
    bad = []
    # rule 6: one gloss per part
    for k in parts.MEANS:
        if k in roots.PARTS: bad.append(f"parts.MEANS glosses {k}, which roots.PARTS glosses too: keep one (rule 6)")
    # rule 2 for the parts themselves
    for k, v in list(roots.PARTS.items()) + list(parts.MEANS.items()):
        if head(v).split(" ")[0] == "being": bad.append(f"the part {k} is glossed “{text(v)}”: say its job (rule 2)")
    # rules 1 and 2 for words: the families (the walk shares their meanings), and the decks
    n = 0
    for R in roots.ROOTS:
        for c in R.get("clusters", []):
            for grp in c["groups"]:
                for e in grp: check_word(e[0], e[2], f"roots/{R['slug']}", bad); n += 1
        for br in R.get("branches", []):
            for e in br[2]: check_word(e[0], e[3], f"roots/{R['slug']}", bad); n += 1
    for p in sorted((OUT / "studies").glob("*.html")):
        for w, g, where in deck_glosses(p):
            if w.startswith("-"):                                    # a tile: the part's gloss on the slide, rule 2 for nouns' endings
                if w.lstrip("-").endswith(NOUN_ENDS) and head(g).split(" ")[0] == "being":
                    bad.append(f"{where}: the {w} tile reads “{text(g)}” (rule 2)")
            else: check_word(w, g, where, bad)
            n += 1
    if bad:
        raise SystemExit("gloss check failed (gloss_check.py has the rules):\n  " + "\n  ".join(bad))
    print(f"gloss check | {n} glosses, {len(roots.PARTS) + len(parts.MEANS)} parts, all within the rules")
