"""Legomorphic Notation for every word in the ask-and-answer lines.

Each word is written once in a short code (W below), following the marking cards
(marking_cards.json) and the rules in the manual. The code expands to the same
letters-and-marks form the marking cards use, so the result can be dropped into the
marking-system page, and it is drawn here at the Sounds to Sentences deck's scale.

THE CODE, unit by unit, left to right
    c.st    consonants, one sound each (black letters, a black circle each)
    k.kn    a consonant unit: two letters, one sound (black bond bar, one circle); also a doubled spelling that nothing
            reaches toward (k.ll in will, k.ck in pick): the box waits for an ending
    g.sh    sh, th, ch (green letters, green bond bar, one green circle)
    x.ll    a pair in a block box (black bond bar, one circle): the vowel protector, boxed only where a vowel comes after
            it in the word and the box stops that vowel's reach (filling, hopping, edge). The bar stays when the box comes:
            the bar says the two letters spell one sound, and the box says a reach is stopped. A cluster takes 'box N' on
            the same terms and no bar, since each of its letters keeps a sound of its own (dusty, wanted)
    x.sh    sh or th in a block box (cashing, gather): green letters, green bar and one green circle inside the box;
            x.tch keeps its t black, its ch green and its green bar under all three, as g.tch does in catch (catching).
            With nothing after them they stay g.sh, g.th and g.tch
    s.a     a vowel that keeps its short sound (cup)
    l.o     a vowel that says its name (bar)
    b.o     a bare vowel: it borrows another vowel's sound, or is unstressed (no cup, no bar)
    w.o     a vowel letter that spells two sounds, a consonant sound and then a vowel sound: the o of one
            (two circles under the one letter, black then red; no cup, no bar)
    t.ee    a vowel unit of two or more letters (red letters, red bond bar, one red circle)
    r.ar    an r-controlled unit (vowel red, r black, red bond bar, one red circle)
    le      the final -le unit (both letters red, red bond bar, one red circle)
    e0      a silent e in a cone of silence, with no vault
    e>      a silent e in a cone, with a vault back to the long vowel before it
    ap      the red apostrophe of a contraction, standing in for the vowel it drops, with no circle (don’t, as the
            marking card draws I’m)
    |       a syllable break (each syllable gets its own swoop)
    +       a morpheme seam
After a semicolon, by unit number (counting from 0, skipping | and +; a group such as c.nt is one unit):
    vault A>B     a vault from the sounded vowel in unit A back to the vowel in unit B. A may be a consonant unit that
                  holds a vowel letter, which sends the vault: the i of k.ti in notation, as the create family deck
                  draws creation (the t and i say sh together, and the i still makes the a long)
    bv A>B        a vault from unit A that the box at unit B stops (bv A>B-C for a box over units B to C)
    nudge A>B     a nice-nudge from the vowel in unit A to the c or g in unit B (B may be a box, as the dg of nudge)
    box A         a block box around the cluster in unit A (box A-B for units A to B)
    seam N        a morpheme seam after letter N (counting letters from 0), for a seam inside a unit: notat + ion
                  puts the seam between the t and the i of k.ti

Run:  python3 legomorphic_words.py            checks every word and prints a summary
      python3 legomorphic_words.py --cards    writes legomorphic_words_cards.json (marking-cards form)
"""
import math, json, sys, pathlib

W = {
 # ---- ELP list 1, Kindergarten
 "a": "b.a", "and": "s.a c.nd", "I": "l.I", "is": "s.i c.s", "it": "s.i c.t", "the": "g.th b.e", "to": "c.t b.o",
 "you": "c.y t.ou", "he": "c.h l.e", "she": "g.sh l.e", "was": "c.w b.a c.s", "of": "b.o c.f",
 # ---- list 2, CV
 "go": "c.g l.o", "me": "c.m l.e", "my": "c.m l.y", "we": "c.w l.e", "be": "c.b l.e", "no": "c.n l.o", "by": "c.b l.y",
 # ---- list 3
 "come": "c.c b.o c.m e0", "some": "c.s b.o c.m e0", "one": "w.o c.n e0", "put": "c.p b.u c.t", "said": "c.s t.ai c.d",
 "two": "k.tw b.o", "see": "c.s t.ee", "look": "c.l t.oo c.k", "why": "k.wh l.y", "try": "c.tr l.y",
 # ---- list 4, digraphs
 "that": "g.th s.a c.t", "this": "g.th s.i c.s", "with": "c.w s.i g.th", "then": "g.th s.e c.n", "when": "k.wh s.e c.n",
 "much": "c.m s.u g.ch", "wish": "c.w s.i g.sh", "pick": "c.p s.i k.ck", "which": "k.wh s.i g.ch",
 # ---- list 5
 "where": "k.wh r.er e0", "small": "c.sm b.a k.ll", "are": "r.ar e0", "have": "c.h s.a c.v e0", "into": "s.i c.n + | c.t b.o",
 "there": "g.th r.er e0", "they": "g.th t.ey", "want": "c.w b.a c.nt", "what": "k.wh b.a c.t", "like": "c.l l.i c.k e>",
 "little": "c.l s.i x.tt | le", "play": "c.pl t.ay",
 # ---- list 6, long vowel with silent e
 "take": "c.t l.a c.k e>", "five": "c.f l.i c.v e>", "gave": "c.g l.a c.v e>", "made": "c.m l.a c.d e>", "these": "g.th l.e c.s e>",
 "those": "g.th l.o c.s e>", "use": "l.u c.s e>", "white": "k.wh l.i c.t e>", "write": "k.wr l.i c.t e>", "here": "c.h l.e c.r e>",
 "make": "c.m l.a c.k e>", "ate": "l.a c.t e>", "came": "c.c l.a c.m e>", "ride": "c.r l.i c.d e>",
 # ---- list 7
 "who": "k.wh b.o", "again": "b.a | c.g t.ai c.n", "any": "b.a c.n | b.y", "could": "c.c t.oul c.d", "would": "c.w t.oul c.d",
 "from": "c.fr b.o c.m", "give": "c.g s.i c.v e0", "once": "w.o c.n c.c e0 ; nudge 3>2", "walk": "c.w t.al c.k", "were": "c.w r.er e0",
 "good": "c.g t.oo c.d", "her": "c.h r.er",
 # ---- list 8, r-controlled
 "over": "l.o | c.v r.er ; vault 2>0", "before": "c.b l.e + | c.f r.or e0", "first": "c.f r.ir c.st", "hurt": "c.h r.ur c.t",
 "for": "c.f r.or", "under": "s.u c.n | c.d r.er", "start": "c.st r.ar c.t",
 # ---- list 9
 "because": "c.b l.e | c.c t.au c.s e0", "been": "c.b t.ee c.n ; seam 1", "both": "c.b l.o g.th", "buy": "k.bu l.y", "old": "l.o c.ld",
 "does": "c.d b.o + e0 c.s", "goes": "c.g l.o + e0 c.s", "many": "c.m b.a c.n | b.y", "pull": "c.p b.u k.ll", "their": "g.th r.eir",
 # ---- list 10, vowel teams
 "please": "c.pl t.ea c.s e0", "each": "t.ea g.ch", "eat": "t.ea c.t", "say": "c.s t.ay", "green": "c.gr t.ee c.n", "read": "c.r t.ea c.d",
 "right": "c.r t.igh c.t", "too": "c.t t.oo", "keep": "c.k t.ee c.p", "away": "b.a | c.w t.ay", "blue": "c.bl t.ue",
 # ---- list 11, diphthongs
 "how": "c.h t.ow", "round": "c.r t.ou c.nd", "found": "c.f t.ou c.nd", "draw": "c.dr t.aw", "down": "c.d t.ow c.n", "brown": "c.br t.ow c.n",
 "new": "c.n t.ew", "now": "c.n t.ow", "our": "t.ou c.r", "out": "t.ou c.t", "saw": "c.s t.aw", "grow": "c.gr t.ow", "own": "t.ow c.n",
 "show": "g.sh t.ow", "know": "k.kn t.ow",
 # ---- list 12
 "around": "b.a | c.r t.ou c.nd", "very": "c.v s.e c.r | b.y", "wash": "c.w b.a g.sh", "work": "c.w r.or c.k", "your": "c.y r.our",
 "done": "c.d b.o c.n e0", "eight": "t.eigh c.t", "find": "c.f l.i c.nd", "kind": "c.k l.i c.nd", "laugh": "c.l t.au k.gh",
 "only": "l.o c.n | c.l b.y", "pretty": "c.pr b.e x.tt | b.y ; bv 3>2", "together": "c.t b.o | c.g s.e x.th | r.er ; bv 5>4", "warm": "c.w r.ar c.m",
 # ---- list 13, multisyllabic
 "every": "s.e c.v | r.er | b.y", "going": "c.g l.o + | s.i k.ng", "open": "l.o | c.p b.e c.n ; vault 2>0", "always": "b.a c.l | c.w t.ay c.s",
 "better": "c.b s.e x.tt | r.er ; bv 3>2", "carry": "c.c b.a x.rr | b.y ; bv 3>2", "funny": "c.f s.u x.nn + | b.y ; bv 3>2",
 "yellow": "c.y s.e x.ll | t.ow", "today": "c.t b.o | c.d t.ay", "myself": "c.m l.y + | c.s s.e c.lf", "never": "c.n s.e c.v | r.er",
 "seven": "c.s s.e c.v | b.e c.n", "other": "b.o g.th | r.er", "water": "c.w b.a c.t | r.er", "people": "c.p t.eo | c.p le",
 # ---- the operator forms that are not on the ELP lists, and not
 "am": "s.a c.m", "has": "c.h s.a c.s", "had": "c.h s.a c.d", "do": "c.d b.o", "did": "c.d s.i c.d", "can": "c.c s.a c.n",
 "will": "c.w s.i k.ll", "shall": "g.sh s.a k.ll", "should": "g.sh t.oul c.d", "may": "c.m t.ay", "might": "c.m t.igh c.t", "must": "c.m s.u c.st",
 "not": "c.n s.o c.t",
}

# Words that are marked for the key to the marks only. They are in none of the lines and none of the lists.
KEY_ONLY = {"nice": "c.n l.i c.c e> ; nudge 3>2"}
# Pieces drawn on their own with no syllable swoop, because they are a syllable in some words and not in others
# (the ed of played and wanted, the n't of can't and isn't). A tool that draws one adds it here.
NO_SWOOP = set()

def code_of(word):
    return W[word] if word in W else KEY_ONLY[word]

# Words whose marking rests on a choice the cards and the manual do not settle outright.
# word(s) -> (how it is marked here, what the choice is)
CHOICES = [
 ("I", "a long mark over I", "The manual's legend and step 1 give I the long mark. The older marking card for a and I shows no mark."),
 ("one, once", "two circles under the o, black and then red", "The o spells /w/ and then the short u sound. Rule 1 asks for a circle for each sound, so the o carries two. None of your cards shows two circles under a single letter, so this is rule 1 applied and not a mark you have drawn. With one circle the word shows two circles for three sounds."),
 ("use", "a single circle under the long u", "Long u says its name, and your 44-sounds sheet counts it as a single vowel. Said slowly it is /y/ and then /oo/, the two sounds that take a circle each in you. New has the same question if you say it nyoo."),
 ("two", "a black bond bar under tw", "The silent w is joined to t as a consonant unit, like kn and wr. It could instead join the vowel."),
 ("goes, does", "a seam after go and do, then e in a cone, then s", "The manual says do + es and go + es. The e of -es is treated as a silent e. The alternative is an oe vowel unit."),
 ("want, myself", "no box around nt or lf", "A cluster takes the box only where a vowel comes after it in the word and the box stops that vowel's reach (wanted, selfish). Nothing follows nt in want or lf in myself, so they stay plain, as and and must do."),
 ("under", "no box and no blocked vault", "The n closes the first syllable and the d opens the second, as the p and k of napkin do on your card, which has no box. If nd is boxed, a blocked vault from the e follows."),
 ("better, pretty, funny, carry", "a blocked vault from the last vowel to the box", "As in getting and happy. Little has none, following its own marking card, and yellow has none because a vowel unit does not send."),
 ("over, open", "a vault from the next vowel back to the long vowel, with no cone", "As in tiger and silent on the cards."),
 ("here", "h, long e, r, and a silent e with a vault", "It follows the ELP's own long-vowel list. The alternative is an r-controlled unit with a cone, like there and where. Your r-controlled card marks hear as h + ear with two circles, so the two spellings of that word differ by a circle here."),
 ("there, where", "an er unit, then e in a cone", "By analogy with were in the manual. The unit says the air sound, and no mark shows that."),
 ("our, your, their", "our and eir as r-controlled units of three letters", "As the cards do for air and ear."),
 ("into, myself", "a seam between the two words", "Seams are drawn for the endings -ing, -es and -y, and where two whole words join and both keep their meaning."),
 ("away, around, again, always, before, because, today, together; said", "no seam", "The first parts a-, al-, be- and to- no longer mean what the small words mean, and said changes its stem. If you want them, seams can go in after a-, al-, be- and to-. Ruled for before on 8 November 2026: be|fore takes a seam, as a compound bound by use."),
 ("into, myself", "nothing crosses the seam", "Into has two consonants before its o and no box, and myself has an e one consonant after the y and no vault. These seams join two whole words, and your ball page says that seam is a wall. The seam in funny is different: it stands before an ending, and your y-sender page has the y send across it and the nn stop it."),
 ("before, because", "a long mark over the e of be-", "Marked as be is marked on its own, as away and today keep the bare a and o of a and to. Said quickly this e is weak, so a bare e is also defensible. In because nothing sends a vault, since au is a unit. Ruled for before on 8 November 2026: be- ends an open syllable at a morpheme boundary, so its e keeps the long mark."),
 ("a, the, away, around, again, today, together, open, seven", "the unstressed vowel is bare", "A weak vowel takes no cup and no bar, as the e of chicken does on its card."),
 ("any, many, very, every, only, pretty, carry, funny", "final y is red and bare", "As in silly and pony on the cards."),
 ("buy", "the silent u is black", "It sits inside the bu unit, as your Session 1 slide draws it."),
 ("look, good, too; how, now, down, brown, grow, show, own, know; eat, read; said, again; been", "a vowel unit with a red bond bar and nothing more", "Units with two sounds are marked alike. The manual lists this as still to decide."),
 ("because, laugh, people", "au and eo as vowel units; gh as a consonant unit", "One-off spellings, marked by the general rule for units."),
 ("old, both, only, find, kind", "a long mark and no vault", "The vowel says its name before two consonants, so nothing sends a vault."),
 ("find, kind, old, round, found", "no box around nd or ld", "Nothing follows nd or ld in these words, so nothing is boxed. In finding and older a vowel does follow, but the box protects a short vowel and these have none, so the family keeps no box, as rolling does."),
 ("water", "the syllable break is wat-er", "Other, any, many, very, seven and never keep the consonant with their short first vowel, and water is treated the same way because its a says a short sound. The dictionary breaks it wa-ter."),
 ("every", "ev, er, y in three syllables", "Said carefully. In running speech the middle syllable is often dropped."),
 ("carry", "the a is bare", "Most Canadians say this a like the e of very, so it borrows, as in any and many. Said with the a of cat, it takes a cup."),
 ("was, is, has, does, goes, these, those, use, please, because, always; of", "s saying /z/ and f saying /v/ are unmarked", "The notation has no mark for a consonant letter borrowing another's sound."),
 ("funny", "a seam after the doubled n", "Fun + y is a live join, and your y-sender page puts the seam after the doubled letters. Pretty, carry and better get a box and no seam, as inherited doubles do on your medial-double page."),
 ("little, yellow, better, pretty, funny, carry", "the doubled letters stay in the first syllable", "As chick|en and ball|oon on the cards. Your medial-double page writes rab·bit, which splits the pair."),
 ("never, seven, every, very", "a short mark, with no vault and no box", "A single consonant stands before the next vowel and the first vowel is still short, as your medial-v page describes. Nothing in the marks explains it."),
 ("from", "the o is bare", "Most Canadian speakers say it with the short u sound, so it borrows. Said with a short o, it would take a cup."),
 ("any, many, pretty", "the first vowel is bare", "Each borrows another vowel's short sound: the a says short e, and the e of pretty says short i. Your y-sender page lists pretty with a short e."),
 ("walk", "al as a vowel unit", "The silent l joins the vowel, as in could. Small and always keep a sounded l, so their a is bare."),
 ("put, pull; was, want, what, wash, water, small, always; of, some, come, one, once, done, does, other; to, do, who, two, into, today, together", "the vowel is bare", "Rule 7, decided on 6 October, applied word by word. Each of these borrows another vowel's sound."),
 ("please, because, one, once, are, were, there, where, before", "a silent e in a cone, with no vault", "Rules 4 and 7 name give, have, come, some and done. Every other silent e that makes no vowel long is marked the same way."),
 ("what, when, which, why, where, white, who", "wh as a black unit with one circle", "As kn and wr are marked. Green is kept for sh, th and ch. In who the unit says /h/, and no mark shows that."),
 ("warm, work", "ar and or as r-controlled units", "After w, ar says the or sound and or says the er sound. No mark shows the change."),
]

VOWEL_KINDS = {"s", "l", "b", "w", "t", "r", "le"}
# A boxed unit that holds a green digraph: which of its letters are green. The t of tch stays black with no circle of its own,
# as the marking cards draw match, and the green bar runs under all three letters, as in catch; a boxed sh or th (cashing,
# gather) stays green all through.
GREEN_IN_BOX = {"tch": (1, 2), "sh": (0, 1), "th": (0, 1)}

def parse(word):
    """Expand a word's code into units, letters and marks (marking-cards form, plus 'cone')."""
    main, *ann = [p.strip() for p in code_of(word).split(";")]
    letters, marks, units, sylls, col, start = [], [], [], [], 0, 0
    for tok in main.split():
        if tok == "|": sylls.append((start, col - 1)); start = col; continue
        if tok == "+": marks.append({"type": "seam", "after": col - 1}); continue
        if tok == "le": kind, s = "le", "le"
        elif tok in ("e0", "e>"): kind, s = tok, "e"
        elif tok == "ap": kind, s = "ap", "’"
        else:
            kind, _, s = tok.partition(".")
            assert kind in ("c", "k", "g", "x", "s", "l", "b", "w", "t", "r") and s, (word, tok)
        cols = list(range(col, col + len(s)))
        if kind == "c":
            for ch in s: letters.append({"ch": ch, "type": "consonant"})
            for c in cols: marks.append({"type": "dot", "cols": [c], "color": "consonant"})
        elif kind == "k":
            for ch in s: letters.append({"ch": ch, "type": "consonant"})
            marks += [{"type": "blendbar", "from": cols[0], "to": cols[-1], "color": "consonant"}, {"type": "dot", "cols": cols, "color": "consonant"}]
        elif kind == "g":
            assert s in ("sh", "th", "ch", "tch"), (word, tok)
            for ch in s: letters.append({"ch": ch, "type": "consonant" if s == "tch" and ch == "t" else "team"})
            marks += [{"type": "blendbar", "from": cols[0], "to": cols[-1], "color": "team"}, {"type": "dot", "cols": cols, "color": "team"}]
        elif kind == "x":                                    # the box adds to the bar, never replaces it: a green digraph gets its bar below
            for ch in s: letters.append({"ch": ch, "type": "consonant"})
            marks.append({"type": "block", "from": cols[0], "to": cols[-1]})
            if s not in GREEN_IN_BOX: marks.append({"type": "blendbar", "from": cols[0], "to": cols[-1], "color": "consonant"})
            marks.append({"type": "dot", "cols": cols, "color": "consonant"})
        elif kind in ("s", "l", "b"):
            assert len(s) == 1 and s.lower() in "aeiouy", (word, tok)
            letters.append({"ch": s, "type": "vowel"})
            if kind == "s": marks.append({"type": "breve", "col": col})
            if kind == "l": marks.append({"type": "macron", "col": col})
            marks.append({"type": "dot", "cols": cols, "color": "vowel"})
        elif kind == "w":                                    # one letter, two sounds: a circle for each, side by side under it
            assert len(s) == 1 and s.lower() in "aeiouy", (word, tok)
            letters.append({"ch": s, "type": "vowel"})
            marks += [{"type": "dot", "cols": cols, "color": "consonant", "dx": -0.13}, {"type": "dot", "cols": cols, "color": "vowel", "dx": 0.13}]
        elif kind in ("t", "le"):
            assert len(s) >= 2, (word, tok)
            for ch in s: letters.append({"ch": ch, "type": "vowel"})
            marks += [{"type": "blendbar", "from": cols[0], "to": cols[-1], "color": "vowel"}, {"type": "dot", "cols": cols, "color": "vowel"}]
        elif kind == "r":
            assert "r" in s and len(s) >= 2, (word, tok)
            for ch in s: letters.append({"ch": ch, "type": "consonant" if ch == "r" else "vowel"})
            marks += [{"type": "blendbar", "from": cols[0], "to": cols[-1], "color": "vowel"}, {"type": "dot", "cols": cols, "color": "vowel"}]
        elif kind == "ap":                                   # red, like the vowel it stands in for; it has no sound, so no circle
            letters.append({"ch": "’", "type": "vowel"})
        elif kind == "e0":
            letters.append({"ch": "e", "type": "vowel"}); marks.append({"type": "cone", "col": col})
        elif kind == "e>":
            target = [u for u in units if u["kind"] == "l"]
            assert target, (word, "e> needs a long vowel before it")
            letters.append({"ch": "e", "type": "vowel"}); marks.append({"type": "vault", "from": target[-1]["cols"][0], "to": col})
        units.append({"kind": kind, "cols": cols, "text": s})
        col += len(s)
    sylls.append((start, col - 1))
    for a in ann:
        op, arg = a.split()
        src, _, dst = arg.partition(">")
        rng = lambda x: (units[int(x.split("-")[0])]["cols"][0], units[int(x.split("-")[-1])]["cols"][-1])
        if op == "vault":
            u = units[int(src)]
            send = u["cols"][0] if u["kind"] in VOWEL_KINDS else next(
                (c for c, ch in zip(u["cols"], u["text"]) if u["kind"] == "k" and ch.lower() in "aeiouy"), None)
            assert send is not None and units[int(dst)]["kind"] == "l", (word, a)
            marks.append({"type": "vault", "from": units[int(dst)]["cols"][0], "to": send, "cone": False})
        elif op == "bv":                                  # a vowel, or a silent e in a cone, whose vault a box stops (funny, edge)
            assert units[int(src)]["kind"] in VOWEL_KINDS | {"e0"}, (word, a)
            f, t = rng(dst); marks.append({"type": "blockedvault", "from": units[int(src)]["cols"][0], "blockFrom": f, "blockTo": t})
        elif op == "nudge":                               # to the c or g, which may sit inside a boxed unit (the dg of nudge)
            u = units[int(dst)]; cg = [c for c, ch in zip(u["cols"], u["text"]) if ch in "cg"]
            assert cg, (word, a)
            marks.append({"type": "nudge", "from": units[int(src)]["cols"][0], "to": cg[-1]})
        elif op == "box":
            f, t = rng(arg); marks.append({"type": "block", "from": f, "to": t})
        elif op == "seam":
            assert 0 <= int(arg) < col - 1, (word, a)
            marks.append({"type": "seam", "after": int(arg)})
        else: raise ValueError((word, a))
    if word not in NO_SWOOP:                              # endings that are a syllable in some words and not in others get none
        for a, b in sylls: marks.append({"type": "swoop", "from": a, "to": b})
    for u in units:                                       # a green digraph inside a block box keeps its green letters, bar and circle
        if u["kind"] == "x" and u["text"] in GREEN_IN_BOX:
            a, b = GREEN_IN_BOX[u["text"]]; c0 = u["cols"][0]
            for c in range(c0 + a, c0 + b + 1): letters[c]["type"] = "team"
            for m in marks:
                if m["type"] == "dot" and m["cols"] == u["cols"]: m["color"] = "team"
            marks.append({"type": "blendbar", "from": c0, "to": u["cols"][-1], "color": "team"})
    spelled = "".join(l["ch"] for l in letters)
    assert spelled == word, (word, spelled)
    n_sounds = sum(1 for m in marks if m["type"] == "dot")
    return {"word": word, "letters": letters, "marks": marks, "units": units, "syllables": sylls, "sounds": n_sounds}

def card_spec(word):
    p = parse(word)
    return {"letters": p["letters"], "marks": p["marks"]}

# ------------------------------------------------------------------ drawing, at the deck's scale
# Every measure is a multiple of the letter size F, taken from the word builds in Session 1
# (bond bar at +0.30 F under the baseline, circle at +0.56 F, swoop at +0.85 F, long mark at -0.91 F ...).
# The swoop came down from +0.73 F to +0.85 F on 7 November 2026, everywhere the notation is drawn, so it reads as a
# smile under the circles rather than a line hugging them; a word drawing grew from 2.36 F to 2.48 F tall to hold it.
SWOOP, HEIGHT = 0.85, 2.48
INK, RED, GREEN, BLUE, QUIET = "var(--ink)", "var(--verb)", "var(--subject)", "var(--modal)", "var(--soft)"   # the cone is drawn in the soft text grey, which shows from the back of a room
# How far each Lexend letter's ink reaches left and right of its centre, as a share of the letter size (measured from the font).
INKX = {"a": (.285, .246), "b": (.252, .279), "c": (.236, .248), "d": (.286, .261), "e": (.262, .270), "f": (.165, .194), "g": (.293, .254),
        "h": (.235, .234), "i": (.076, .080), "j": (.164, .086), "k": (.221, .279), "l": (.063, .062), "m": (.398, .399), "n": (.235, .234),
        "o": (.276, .271), "p": (.253, .278), "q": (.284, .248), "r": (.139, .205), "s": (.208, .198), "t": (.176, .183), "u": (.240, .244),
        "v": (.271, .276), "w": (.384, .381), "x": (.281, .282), "y": (.290, .288), "z": (.195, .211), "I": (.176, .167),
        "C": (.293, .317), "S": (.265, .266),             # for Christmas and Santa Claus, measured the same way in Lexend 400
        "’": (.060, .060)}
BAR = 0.33          # the bond bar sits this far under the baseline, clear of the tails of g and y
FILL = {"consonant": INK, "vowel": RED, "team": GREEN}

def slot(word):
    """Letter spacing as a share of the letter size: wider where the word has an m or a w, which are wide letters."""
    return 0.76 if any(ch in word for ch in "mw") else 0.67

def svg_word(word, F=80.0, x0=0.0, cls=True):
    """(markup, width, height) for one marked word. Layers carry classes nz1..nz9 so a strip can bring them in in order:
    1 circles, 2 circle colours, 3 swoops, 4 bond bars, 5 letters, 6 short and long marks, 7 boxes, 8 cones, vaults and nudges, 9 seams.
    With classes on, the word also carries a band (class wt) that stands in for its letters while only its sounds show."""
    p = parse(word)
    S, M, G = slot(word) * F, 0.30 * F, 0.22 * F
    B, H = 1.44 * F, HEIGHT * F
    seams = sorted(m["after"] for m in p["marks"] if m["type"] == "seam")
    n = len(p["letters"])
    room = [0.0] * n                                         # extra room after a letter
    for s in seams: room[s] += G
    for i, L in enumerate(p["letters"]):                     # an apostrophe takes half a slot, as in type, so its neighbours close in
        if L["ch"] == "’":
            if i: room[i - 1] -= 0.25 * S
            if i < n - 1: room[i] -= 0.25 * S
    box_ends = {m["to"] for m in p["marks"] if m["type"] == "block"}
    for m in p["marks"]:                                     # a cone must clear the letter before it (the m of come), and a box (the dg of nudge)
        c = m["col"] if m["type"] == "cone" else (m["to"] if m["type"] == "vault" and m.get("cone", True) else None)
        if c and (c - 1) not in seams:
            need = (INKX[p["letters"][c - 1]["ch"]][1] + 0.415 + (0.12 if (c - 1) in box_ends else 0)) * F
            if need > S: room[c - 1] += need - S
    shift = [sum(room[:i]) for i in range(n)]
    X = lambda i: x0 + M + S * (i + 0.5) + shift[i]
    mid = lambda cols: sum(X(c) for c in cols) / len(cols)
    width = 2 * M + S * n + sum(room[:n - 1])
    k = lambda n_: f' class="nz{n_}"' if cls else ""
    f = lambda v: f"{v:.1f}"
    out = []
    if cls:                                                  # a soft band where the letters will stand, for the click that shows the sounds alone
        x1 = X(0) - (INKX[p["letters"][0]["ch"]][0] + 0.05) * F
        x2 = X(n - 1) + (INKX[p["letters"][n - 1]["ch"]][1] + 0.05) * F
        out.append(f'<rect class="wt" x="{f(x1)}" y="{f(B - 0.56 * F)}" width="{f(x2 - x1)}" height="{f(0.56 * F)}" rx="{f(0.12 * F)}" fill="var(--line)"/>')
    has_top = {m["col"] for m in p["marks"] if m["type"] in ("breve", "macron")}
    dots = [{"x": mid(m["cols"]) + m.get("dx", 0) * F, "lo": min(m["cols"]), "hi": max(m["cols"]), "color": m["color"]} for m in p["marks"] if m["type"] == "dot"]
    def arrow(x, y, dx, dy, size, sw, colour, layer):
        d = math.hypot(dx, dy) or 1; dx, dy = dx / d, dy / d; th = 0.5; c, s = math.cos(th), math.sin(th)
        a = (x + size * (-dx * c + dy * s), y + size * (-dx * s - dy * c)); b = (x + size * (-dx * c - dy * s), y + size * (dx * s - dy * c))
        return f'<path{k(layer)} d="M{f(a[0])} {f(a[1])} L{f(x)} {f(y)} L{f(b[0])} {f(b[1])}" fill="none" stroke="{colour}" stroke-width="{f(sw)}" stroke-linecap="round" stroke-linejoin="round"/>'
    for m in p["marks"]:                                    # boxes and seams sit behind the letters
        if m["type"] == "block":
            x1 = X(m["from"]) - max(0.30, INKX[p["letters"][m["from"]]["ch"]][0] + 0.075) * F     # the box clears the ink of a wide letter (the k of pick)
            x2 = X(m["to"]) + max(0.30, INKX[p["letters"][m["to"]]["ch"]][1] + 0.075) * F
            out.append(f'<rect{k(7)} x="{f(x1)}" y="{f(B - 0.84 * F)}" width="{f(x2 - x1)}" height="{f(0.96 * F)}" rx="{f(0.10 * F)}" fill="none" stroke="{BLUE}" stroke-width="{f(0.036 * F)}"/>')
        if m["type"] == "seam":
            x = (X(m["after"]) + X(m["after"] + 1)) / 2
            out.append(f'<line{k(9)} x1="{f(x)}" y1="{f(B - 0.95 * F)}" x2="{f(x)}" y2="{f(B + 0.46 * F)}" stroke="{BLUE}" stroke-width="{f(0.03 * F)}" stroke-dasharray="{f(0.057 * F)} {f(0.057 * F)}"/>')
        if m["type"] in ("cone", "vault") and m.get("cone", True):
            ex = X(m["col"] if m["type"] == "cone" else m["to"])
            out.append(f'<circle{k(8)} cx="{f(ex)}" cy="{f(B - 0.26 * F)}" r="{f(0.37 * F)}" fill="none" stroke="{QUIET}" stroke-width="{f(0.038 * F)}" stroke-linecap="round" stroke-dasharray="{f(0.012 * F)} {f(0.078 * F)}"/>')
    out.append(f'<g{k(5)} font-family="Lexend, system-ui, sans-serif" font-size="{f(F)}" font-weight="400" text-anchor="middle">'
               + "".join(f'<text x="{f(X(i))}" y="{f(B)}" fill="{FILL[L["type"]]}">{L["ch"]}</text>' for i, L in enumerate(p["letters"])) + "</g>")
    for m in p["marks"]:
        t = m["type"]
        if t == "blendbar":
            out.append(f'<line{k(4)} x1="{f(X(m["from"]) - 0.257 * F)}" y1="{f(B + BAR * F)}" x2="{f(X(m["to"]) + 0.257 * F)}" y2="{f(B + BAR * F)}" stroke="{FILL[m["color"]]}" stroke-width="{f(0.05 * F)}" stroke-linecap="round"/>')
        elif t == "macron":
            x = X(m["col"]); out.append(f'<line{k(6)} x1="{f(x - 0.279 * F)}" y1="{f(B - 0.91 * F)}" x2="{f(x + 0.279 * F)}" y2="{f(B - 0.91 * F)}" stroke="{RED}" stroke-width="{f(0.05 * F)}" stroke-linecap="round"/>')
        elif t == "breve":
            x = X(m["col"]); out.append(f'<path{k(6)} d="M{f(x - 0.257 * F)} {f(B - 0.975 * F)} Q{f(x)} {f(B - 0.775 * F)} {f(x + 0.257 * F)} {f(B - 0.975 * F)}" fill="none" stroke="{RED}" stroke-width="{f(0.05 * F)}" stroke-linecap="round"/>')
        elif t == "vault":
            xs, xt = X(m["to"]), X(m["from"])               # 'to' is the sender, 'from' the vowel made long
            ys = B - 0.63 * F if m.get("cone", True) else B - (1.10 if m["to"] in has_top else 0.74) * F
            ex, ey = xt + 0.05 * F, B - 1.12 * F
            c1 = (xs - 0.04 * F, B - 1.40 * F); c2 = (xt + 0.46 * F, B - 1.40 * F)
            out.append(f'<path{k(8)} d="M{f(xs)} {f(ys)} C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(ex)} {f(ey)}" fill="none" stroke="{BLUE}" stroke-width="{f(0.043 * F)}" stroke-linecap="round"/>')
            out.append(arrow(ex, ey, ex - c2[0], ey - c2[1], 0.12 * F, 0.043 * F, BLUE, 8))
        elif t == "blockedvault":
            xv, bx = X(m["from"]), (X(m["blockFrom"]) + X(m["blockTo"])) / 2
            ys = B - (1.10 if m["from"] in has_top else 0.74) * F
            yx = B - 1.07 * F
            out.append(f'<path{k(8)} d="M{f(xv)} {f(ys)} Q{f((xv + bx) / 2 + 0.10 * F)} {f(B - 1.52 * F)} {f(bx + 0.07 * F)} {f(yx)}" fill="none" stroke="{BLUE}" stroke-width="{f(0.043 * F)}" stroke-linecap="round"/>')
            d = 0.08 * F
            out.append(f'<path{k(8)} d="M{f(bx - d)} {f(yx - d)} L{f(bx + d)} {f(yx + d)} M{f(bx + d)} {f(yx - d)} L{f(bx - d)} {f(yx + d)}" fill="none" stroke="{RED}" stroke-width="{f(0.05 * F)}" stroke-linecap="round"/>')
        elif t == "nudge":
            sx, tx = X(m["from"]), X(m["to"]); d = 1 if sx > tx else -1
            low = p["letters"][m["to"]]["ch"] in "gypqj"
            y0, yd = (B + 0.20 * F, B + 0.50 * F) if not low else (B + 0.36 * F, B + 0.46 * F)
            if any(b["type"] == "blendbar" and b["from"] <= m["to"] <= b["to"] for b in p["marks"]):
                y0, yd = B + 0.45 * F, B + 0.55 * F             # the g of a boxed dg has a bar under it: the nudge runs below the bar
            a, b = sx - d * 0.07 * F, tx + d * 0.08 * F          # from under the vowel to under the c or g, clear of a cone
            out.append(f'<path{k(8)} d="M{f(a)} {f(y0)} Q{f((a + b) / 2)} {f(yd)} {f(b)} {f(y0)}" fill="none" stroke="{BLUE}" stroke-width="{f(0.043 * F)}" stroke-linecap="round"/>')
            out.append(arrow(b, y0, b - (a + b) / 2, y0 - yd, 0.11 * F, 0.043 * F, BLUE, 8))
    for d in dots:
        out.append(f'<circle{k(1)} cx="{f(d["x"])}" cy="{f(B + 0.56 * F)}" r="{f(0.072 * F)}" fill="{INK}"/>')
        if d["color"] != "consonant":
            out.append(f'<circle{k(2)} cx="{f(d["x"])}" cy="{f(B + 0.56 * F)}" r="{f(0.072 * F)}" fill="{FILL[d["color"]]}"/>')
    for m in p["marks"]:
        if m["type"] == "swoop":
            inside = [d for d in dots if d["lo"] >= m["from"] and d["hi"] <= m["to"]]
            assert inside, (word, "a syllable with no sound")
            xl, xr = min(d["x"] for d in inside) - 0.107 * F, max(d["x"] for d in inside) + 0.107 * F
            if len(inside) == 1: xl, xr = xl - 0.10 * F, xr + 0.10 * F
            out.append(f'<path{k(3)} d="M{f(xl)} {f(B + SWOOP * F)} Q{f((xl + xr) / 2)} {f(B + (SWOOP + 0.2) * F)} {f(xr)} {f(B + SWOOP * F)}" fill="none" stroke="{BLUE}" stroke-width="{f(0.046 * F)}" stroke-linecap="round"/>')
    return "".join(out), width, H

def svg_strip(words, F=80.0, gap=None, label=None, cls=True, extra_class="", css_height=None):
    """Several marked words in one SVG, side by side."""
    gap = 0.55 * F if gap is None else gap
    x, parts = 0.0, []
    for w in words:
        g, wd, H = svg_word(w, F, x, cls)
        parts.append(f'<g data-word="{w}">{g}</g>'); x += wd + gap
    width = x - gap if words else 0
    H = HEIGHT * F
    label = label or ("Marked: " + ", ".join(words))
    style = f' style="width:{width:.0f}px;max-width:100%;height:auto"' if css_height is None else f' style="height:{css_height}px;width:auto;max-width:100%"'
    klass = ("nz " + extra_class).strip()
    return f'<svg class="{klass}" viewBox="0 0 {width:.0f} {H:.0f}" role="img" aria-label="{label}"{style}>' + "".join(parts) + "</svg>", width, H

ONE_MARK = ("circle", "swoop", "short", "long", "bond", "r", "box", "cone", "vault", "nudge", "bv", "seam", "apostrophe")

def svg_one_mark(word, mark, F=58.0, label=None, css_height=None):
    """A word with one mark drawn and nothing else, for the legend: the letters in ink and only that mark's lines. The
    r-controlled unit keeps its red vowel and its one circle, as its definition says, and the red apostrophe stays red.
    The marks are told apart by the layers svg_word draws (circles, swoops, bars, short and long marks, boxes, the cone
    layer, seams) and, inside the cone layer, by shape and place: a cone is a ring, a vault arcs above the letters, a
    nudge runs under them."""
    import re
    assert mark in ONE_MARK, mark
    g, wd, H = svg_word(word, F, 0.0, cls=True)
    B = 1.44 * F
    num = r"-?\d+(?:\.\d+)?"
    letters = re.search(r'<g class="nz5".*?</g>', g, re.S).group(0)
    if mark == "apostrophe":
        letters = re.sub(r'fill="var\(--(?:verb|subject)\)">([^<’]+)<', r'fill="var(--ink)">\1<', letters)
    elif mark != "r":
        letters = re.sub(r'fill="var\(--(?:verb|subject)\)"', 'fill="var(--ink)"', letters)
    els = [e for e in re.findall(r"<[^>]+/>", g) if 'class="wt"' not in e]
    layer = lambda e: (re.search(r'class="(nz\d)"', e) or [None, None])[1]
    ys = lambda e: [float(v) for v in re.findall(r"(?:y1|y2|cy)=\"(" + num + r")\"", e)] or \
                   [float(v) for v in re.findall(num + r"\s+(" + num + r")", (re.search(r' d="([^"]+)"', e) or [0, ""])[1])]
    above = lambda e: max(ys(e)) < B
    below = lambda e: min(ys(e)) > B
    test = {
        "circle": lambda e: layer(e) in ("nz1", "nz2"),
        "swoop": lambda e: layer(e) == "nz3",
        "short": lambda e: layer(e) == "nz6" and e.startswith("<path"),
        "long": lambda e: layer(e) == "nz6" and e.startswith("<line"),
        "bond": lambda e: layer(e) == "nz4",
        "box": lambda e: layer(e) == "nz7",
        "cone": lambda e: layer(e) == "nz8" and e.startswith("<circle"),
        "vault": lambda e: layer(e) == "nz8" and e.startswith("<path") and above(e),
        "nudge": lambda e: layer(e) == "nz8" and e.startswith("<path") and below(e),
        "bv": lambda e: layer(e) == "nz8" and e.startswith("<path") and above(e),
        "seam": lambda e: layer(e) == "nz9",
        "apostrophe": lambda e: False,
    }
    if mark == "r":                                   # the red bar, and the one circle under it
        bars = [e for e in els if layer(e) == "nz4"]
        spans = [tuple(sorted(float(v) for v in re.findall(r'x[12]="(' + num + r')"', e))) for e in bars]
        def under(e):
            cx = re.search(r'cx="(' + num + r')"', e)
            return cx and any(a - 1 <= float(cx[1]) <= b + 1 for a, b in spans)
        keep = bars + [e for e in els if layer(e) in ("nz1", "nz2") and under(e)]
    else:
        keep = [e for e in els if test[mark](e)]
    body = "".join(re.sub(r' class="nz\d"', "", e) for e in keep) + re.sub(r' class="nz5"', "", letters)
    label = label or f"{word}, with only its {mark} marks"
    style = f' style="width:{wd:.0f}px;max-width:100%;height:auto"' if css_height is None else f' style="height:{css_height}px;width:auto;max-width:100%"'
    return f'<svg class="nz one-mark" viewBox="0 0 {wd:.0f} {H:.0f}" role="img" aria-label="{label}"{style}>' + body + "</svg>"


def describe(word):
    """A plain-words account of a word's marks, for checking and for the manual."""
    p = parse(word); bits = []
    names = {"c": "", "k": "unit", "g": "green unit", "x": "boxed", "s": "short", "l": "long", "b": "bare", "w": "two sounds, two circles", "t": "vowel unit", "r": "r-unit", "le": "le unit", "e0": "cone", "e>": "cone and vault", "ap": "red apostrophe"}
    for u in p["units"]:
        bits.append(u["text"] + (f" ({names[u['kind']]})" if names[u["kind"]] else ""))
    extra = [m["type"] for m in p["marks"] if m["type"] in ("blockedvault", "nudge", "seam")] + ["vault (no cone)" for m in p["marks"] if m["type"] == "vault" and m.get("cone") is False] \
            + ["cluster box" for m in p["marks"] if m["type"] == "block" and not any(u["kind"] == "x" and u["cols"][0] == m["from"] for u in p["units"])]
    return " · ".join(bits) + ("  [" + ", ".join(extra) + "]" if extra else ""), p["sounds"], len(p["syllables"])

if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent
    for w in W: parse(w); svg_word(w)
    if "--cards" in sys.argv:
        out = [{"word": w, **card_spec(w)} for w in W]
        (here / "legomorphic_words_cards.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print("wrote legomorphic_words_cards.json:", len(out), "words")
    else:
        print(len(W), "words marked")
        for w in W:
            d, s, y = describe(w); print(f"  {w:9s} {s} sounds, {y} syll.  {d}")
