"""Marking codes for route words that had none in the deck tools, written for the site on 5 November 2026.

Same code as legomorphic_words.py (see its docstring). Each line follows a word the tools already mark:
the analog is named in the comment. Words in UNMARKED are shown in plain letters until a marking is decided.
CALLS lists the places where these codes rest on a choice. They are in the manual's Marking calls tab under
"From the atlas site" (added 5 November 2026), with telephone and photograph, for a ruling; once ruled, change
the codes here to match and rebuild."""

SITE_CODES = {
    # step 2: short vowels closed by one consonant (as am, it, in)
    "at": "s.a c.t", "an": "s.a c.n", "on": "s.o c.n", "up": "s.u c.p",
    # step 3: an open word says its name (as no, go)
    "so": "c.s l.o",
    # step 4: one consonant closes it (as not, bed)
    "met": "c.m s.e c.t", "wet": "c.w s.e c.t", "got": "c.g s.o c.t",
    "hi": "c.h l.i", "him": "c.h s.i c.m", "hit": "c.h s.i c.t",
    # step 6 (as bed, and must for the nt cluster with nothing after it)
    "get": "c.g s.e c.t", "went": "c.w s.e c.nt",
    # step 9: the vault (as make, like)
    "time": "c.t l.i c.m e>", "home": "c.h l.o c.m e>", "name": "c.n l.a c.m e>",
    # step 10: the nice-nudge (as nice, page)
    "face": "c.f l.a c.c e> ; nudge 3>2", "place": "c.pl l.a c.c e> ; nudge 3>2",
    "age": "l.a c.g e> ; nudge 2>1", "huge": "c.h l.u c.g e> ; nudge 3>2",
    # step 11: vowel teams (as may, right)
    "day": "c.d t.ay", "night": "c.n t.igh c.t",
    # step 12: the r-controlled unit (as for, her, first, hurt)
    "or": "r.or", "car": "c.c r.ar", "bird": "c.b r.ir c.d", "turn": "c.t r.ur c.n",
    # step 13: a suffix at the seam (as dogs, going, goes)
    "gets": "c.g s.e c.t + c.s", "sees": "c.s t.ee + c.s",
    "doing": "c.d b.o + | s.i k.ng", "being": "c.b l.e + | s.i k.ng", "played": "c.pl t.ay + e0 c.d",
    # step 14: the box (as funny, pretty; a cluster box as the manual's helped)
    "help": "c.h s.e c.lp", "helped": "c.h s.e c.lp + e0 c.d ; box 2 ; bv 3>2",
    "sun": "c.s s.u c.n", "sunny": "c.s s.u x.nn + | b.y ; bv 3>2", "happy": "c.h s.a x.pp | b.y ; bv 3>2",
    # step 15: the e drops, its jobs move (as hoping, giving, jazy)
    "making": "c.m l.a | c.k + s.i k.ng ; vault 3>1", "having": "c.h s.a c.v + | s.i k.ng",
    "race": "c.r l.a c.c e> ; nudge 3>2", "racing": "c.r l.a | c.c + s.i k.ng ; vault 3>1 ; nudge 3>2",
    "ice": "l.i c.c e> ; nudge 2>1", "icy": "l.i | c.c + b.y ; vault 2>0 ; nudge 2>1",
    # step 16: open and closed in longer words (as over, open, pony)
    "silent": "c.s l.i | c.l b.e c.nt ; vault 3>1", "tiger": "c.t l.i | c.g r.er ; vault 3>1",
    "paper": "c.p l.a | c.p r.er ; vault 3>1", "music": "c.m l.u | c.s s.i c.c ; vault 3>1",
    # step 17: consonant + le (as the table and bugle card, and little)
    "table": "c.t l.a | c.b le ; vault 3>1", "bugle": "c.b l.u | c.g le ; vault 3>1",
    "title": "c.t l.i | c.t le ; vault 3>1", "apple": "s.a x.pp | le", "middle": "c.m s.i x.dd | le",
    # step 18: long before two consonants (as old, find)
    "cold": "c.c l.o c.ld", "most": "c.m l.o c.st", "child": "g.ch l.i c.ld", "wild": "c.w l.i c.ld",
    # step 20: teams for the long vowels (as eat, say)
    "rain": "c.r t.ai c.n", "paid": "c.p t.ai c.d", "boat": "c.b t.oa c.t", "pie": "c.p t.ie",
    # step 21: the long u sound (as too, new, blue)
    "moon": "c.m t.oo c.n", "food": "c.f t.oo c.d", "grew": "c.gr t.ew", "true": "c.tr t.ue", "soup": "c.s t.ou c.p",
    # step 22: a team's second sound, marked alike (as look, head)
    "book": "c.b t.oo c.k", "bread": "c.br t.ea c.d",
    # step 23 (as saw)
    "law": "c.l t.aw",
    # step 24 (as the coin card)
    "coin": "c.c t.oi c.n", "point": "c.p t.oi c.nt", "boy": "c.b t.oy", "toy": "c.t t.oy",
    # step 25: silent letters join their unit (as know, write, and going's ng)
    "knee": "k.kn t.ee", "wrong": "k.wr s.o k.ng", "lamb": "c.l s.a k.mb", "climb": "c.cl l.i k.mb",
    # step 26: more r-controlled units (as the hair and hear card, before, are)
    "hair": "c.h r.air", "hear": "c.h r.ear", "more": "c.m r.or e0", "care": "c.c r.ar e0",
    # step 29: -y, -ly and y turns to i (as going's seam, funny, goes)
    "sadly": "c.s s.a c.d + | c.l b.y", "slowly": "c.sl t.ow + | c.l b.y",
    "happily": "c.h s.a x.pp | b.i + | c.l b.y ; bv 3>2", "happier": "c.h s.a x.pp | b.i + | r.er ; bv 3>2",
    "tried": "c.tr l.i + e0 c.d", "carries": "c.c b.a x.rr | b.i + e0 c.s ; bv 3>2",
    # step 30: un- and re-, the seam before the root (as into; re- marked as be is)
    "undo": "s.u c.n + | c.d b.o", "untie": "s.u c.n + | c.t t.ie",
    "unhappy": "s.u c.n + | c.h s.a x.pp | b.y ; bv 5>4", "unlock": "s.u c.n + | c.l s.o k.ck",
    "redo": "c.r l.e + | c.d b.o", "replay": "c.r l.e + | c.pl t.ay",
    "refill": "c.r l.e + | c.f s.i k.ll", "reread": "c.r l.e + | c.r t.ea c.d",
    # step 32: ph as a black bond bar (as kn); photo as pony
    "photo": "k.ph l.o | c.t l.o ; vault 3>1", "phone": "k.ph l.o c.n e>", "graph": "c.gr s.a k.ph",
    "alphabet": "s.a c.l | k.ph b.a | c.b s.e c.t",
}

# A spelling that is two words, each with its own marking (from flsz_family.py).
VARIANTS = {
    "live": [("c.l l.i c.v e>", "a live show"), ("c.l s.i c.v e0", "we live here")],
}

# Shown in plain letters until their marking is decided.
UNMARKED = {
    "I'm": "the red apostrophe is not drawn on the site yet",
    "it's": "the red apostrophe is not drawn on the site yet",
    "isn't": "the red apostrophe is not drawn on the site yet",
    "don't": "the red apostrophe is not drawn on the site yet",
    "can't": "the red apostrophe is not drawn on the site yet",
    "won't": "the red apostrophe is not drawn on the site yet",
    "we're": "the red apostrophe is not drawn on the site yet",
    "act": "marked in the act family deck", "action": "marked in the act family deck",
    "actor": "marked in the act family deck", "active": "marked in the act family deck",
    "react": "marked in the act family deck", "create": "marked in the create family deck",
    "creation": "marked in the create family deck", "creator": "marked in the create family deck",
    "telephone": "whether a seam goes between the Greek roots is open",
    "photograph": "whether a seam goes between the Greek roots is open",
}

# Choices these codes make that the manual and the cards do not settle outright.
CALLS = [
    ("silent", "the weak e of -lent is bare", "The silent card puts a short mark on it; the later rule leaves a weak vowel bare."),
    ("helped", "a box over lp and a blocked vault from the e of -ed", "Follows the manual's step 14, which names helped."),
    ("played, tried", "the e of -ed in a cone after the seam", "As goes and does treat the e of -es."),
    ("table, bugle, title", "a vault from le back to the long vowel", "As the final stable syllable card draws table and bugle."),
    ("redo, replay, refill, reread", "a long mark over the e of re-", "As be- is marked in before and because."),
    ("wrong", "a short mark over o, and ng as a black unit", "As going's ng."),
    ("climb", "a long mark and no vault before mb", "As find and kind."),
    ("photo", "a vault from the second o to the first", "As pony."),
]
