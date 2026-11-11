"""Marking codes for route words that had none in the deck tools, written for the site on 5 November 2026, for
the hap family's page (roots/hap.html), added 9 November 2026, and for step 16's new words and contrasts, added
10 November 2026.

Same code as legomorphic_words.py (see its docstring). Each line follows a word the tools already mark:
the analog is named in the comment. Words in UNMARKED are shown in plain letters until a marking is settled.
CALLS lists the places where these codes rest on a choice. They are in the manual's Marking calls tab under
"From the atlas site" (added 5 November 2026), with telephone and photograph, for a ruling; once ruled, change
the codes here to match and rebuild."""

SITE_CODES = {
    # the legend: one word with a red, a green and a black bond bar (as speak for ea, much for ch, seeing for -ing)
    "teaching": "c.t t.ea g.ch + | s.i k.ng",
    # step 2: short vowels closed by one consonant (as am, it, in)
    "at": "s.a c.t", "an": "s.a c.n", "on": "s.o c.n", "up": "s.u c.p",
    # step 3: an open word spells its name (as no, go)
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
    "sun": "c.s s.u c.n", "sunny": "c.s s.u x.nn + | b.y ; bv 3>2", "happy": "c.h s.a x.pp + | b.y ; bv 3>2",   # hap + y, as sunny
    # step 15: the e drops, its jobs move (as hoping, giving, jazy)
    "making": "c.m l.a | c.k + s.i k.ng ; vault 3>1", "having": "c.h s.a c.v + | s.i k.ng",
    "race": "c.r l.a c.c e> ; nudge 3>2", "racing": "c.r l.a | c.c + s.i k.ng ; vault 3>1 ; nudge 3>2",
    "ice": "l.i c.c e> ; nudge 2>1", "icy": "l.i | c.c + b.y ; vault 2>0 ; nudge 2>1",
    # step 16: open and closed in longer words (as over, open, pony; seven and lemon for a short first vowel)
    "silent": "c.s l.i | c.l b.e c.nt", "tiger": "c.t l.i | c.g r.er",
    "paper": "c.p l.a | c.p r.er",
    # music and basic are two parts, muse + ic and base + ic: the i took the dropped e's place, so it sends the vault (as making)
    "music": "c.m l.u | c.s + s.i c.c ; vault 3>1", "basic": "c.b l.a | c.s + s.i c.c ; vault 3>1",
    # its contrasts, 10 November 2026: robin as the role cards draw it (noun_codes.py), robot as music, river as never
    # and tiger, silly as middle and sunny without the seam
    "robin": "c.r s.o c.b | s.i c.n", "robot": "c.r l.o | c.b s.o c.t",
    "river": "c.r s.i c.v | r.er", "silly": "c.s s.i x.ll | b.y ; bv 3>2",
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
    "happily": "c.h s.a x.pp + | b.i + | c.l b.y ; bv 3>2", "happier": "c.h s.a x.pp + | b.i + | r.er ; bv 3>2",
    "tried": "c.tr l.i + e0 c.d", "carries": "c.c b.a x.rr | b.i + e0 c.s ; bv 3>2",
    # step 30: un- and re-, the seam before the root (as into; re- marked as be is)
    "undo": "s.u c.n + | c.d b.o", "untie": "s.u c.n + | c.t t.ie",
    "unhappy": "s.u c.n + | c.h s.a x.pp + | b.y ; bv 5>4", "unlock": "s.u c.n + | c.l s.o k.ck",
    "redo": "c.r l.e + | c.d b.o", "replay": "c.r l.e + | c.pl t.ay",
    "refill": "c.r l.e + | c.f s.i k.ll", "reread": "c.r l.e + | c.r t.ea c.d",
    # step 32: ph as a black bond bar (as kn); photo as pony
    "photo": "k.ph l.o | c.t l.o ; vault 3>1", "phone": "k.ph l.o c.n e>", "graph": "c.gr s.a k.ph",
    "alphabet": "s.a c.l | k.ph b.a | c.b s.e c.t",
    # the steps' contrasts, drawn on the step pages since 10 November 2026, each as the word named beside it
    "cost": "c.c s.o c.st", "mint": "c.m s.i c.nt",              # as must and went: short before two consonants
    "mind": "c.m l.i c.nd",                                       # as find and kind
    "bone": "c.b l.o c.n e>",                                     # as home
    "gone": "c.g b.o c.n e0",                                     # as done: a borrowing vowel, bare, and an e in a cone
    "due": "c.d t.ue", "dew": "c.d t.ew",                         # as blue and new
    "snow": "c.sn t.ow",                                          # as the noun cards draw it
    "knot": "k.kn s.o c.t", "wrap": "k.wr s.a c.p", "rap": "c.r s.a c.p",   # as know and write; rap as not
    # contrasts added to steps 4, 5, 9, 10 and 17 on 10 November 2026: closed words as not and bed, vaulted ones as make and page
    "sob": "c.s s.o c.b", "shed": "g.sh s.e c.d", "mad": "c.m s.a c.d", "dim": "c.d s.i c.m", "dime": "c.d l.i c.m e>",
    "cub": "c.c s.u c.b", "cube": "c.c l.u c.b e>", "cap": "c.c s.a c.p", "cape": "c.c l.a c.p e>",
    "rag": "c.r s.a c.g", "rage": "c.r l.a c.g e> ; nudge 3>2", "bubble": "c.b s.u x.bb | le",   # bubble as apple and middle
    "mode": "c.m l.o c.d e>",                                     # the *med- page's word, as home
    "same": "c.s l.a c.m e>",                                     # the *sem- page's word, as name
    "duct": "c.d s.u c.ct",                                       # the *deuk- page's word; ct as the nt of went
    # the landing page: the notation's own name, and note to notation (as making and photo; creation as the create family deck)
    "legomorphic": "c.l s.e c.g + | l.o + | c.m r.or | k.ph + s.i c.c",   # leg + o + morph + ic since 10 November 2026
    "note": "c.n l.o c.t e>",                                    # as the sentence cards mark it
    "notate": "c.n l.o | c.t + l.a c.t e> ; vault 3>1",
    "notation": "c.n l.o | c.t + l.a | g.ti b.o c.n ; vault 3>1 ; vault 4>3 ; seam 4",
    # the hap family (roots/hap.html), 9 November 2026: hap doubles its p only before a vowel
    "happen": "c.h s.a x.pp + | b.e c.n ; bv 3>2",                  # as happy, with -en as the en of seven
    "hapless": "c.h s.a c.p + | c.l b.e k.ss",                      # as hopeless, with no box: l can't reach back
    "mishap": "c.m s.i c.s + | c.h s.a c.p",                        # as unlock: s and h on either side of the seam
    "haphazard": "c.h s.a c.p + | c.h s.a c.z | r.ar c.d",          # p and h on either side of the seam; ar as in car
}

# Rulings that change a word the deck tools (legomorphic_words.py, the card decks) still mark the old way. The site
# takes these; the decks and printed cards keep their marks until they are rebuilt.
# 10 November 2026, step 16: a long first vowel in a one-part word has its long mark and no vault, since no letter
# causes it (open, even, as tiger and paper above); today and around take the seam their word sum cards give them.
SITE_RULED = {
    "open": "l.o | c.p b.e c.n", "even": "l.e | c.v b.e c.n",
    "today": "c.t b.o + | c.d t.ay", "around": "b.a + | c.r t.ou c.nd",
}

# The affixes and roots placed on the steps (the manual's "Parts on the steps", 10 November 2026), each marked as it is
# said on its own and as the step's own words are: un as up, re as he, sub as bed, mode as home, duce as nice.
PART_CODES = {
    "in-": "s.i c.n", "un-": "s.u c.n", "ad-": "s.a c.d", "ab-": "s.a c.b", "ob-": "s.o c.b", "im-": "s.i c.m", "il-": "s.i c.l",
    "en-": "s.e c.n", "ex-": "s.e c.x", "re-": "c.r l.e", "de-": "c.d l.e", "be-": "c.b l.e", "e-": "l.e",
    "sub-": "c.s s.u c.b", "dis-": "c.d s.i c.s", "mis-": "c.m s.i c.s", "con-": "c.c s.o c.n", "com-": "c.c s.o c.m",
    "hap": "c.h s.a c.p", "leg": "c.l s.e c.g", "mod": "c.m s.o c.d", "med": "c.m s.e c.d", "-th": "g.th",
    "duct": "c.d s.u c.ct", "lect": "c.l s.e c.ct", "trans-": "c.tr s.a c.ns", "-est": "s.e c.st", "-less": "c.l s.e k.ss", "-ness": "c.n s.e k.ss",
    "mode": "c.m l.o c.d e>", "note": "c.n l.o c.t e>", "-ate": "l.a c.t e>", "-ize": "l.i c.z e>",
    "duce": "c.d l.u c.c e> ; nudge 3>2", "-ance": "b.a c.n c.c e0 ; nudge 3>2", "-ence": "b.e c.n c.c e0 ; nudge 3>2",
    "-er": "r.er", "-or": "r.or", "-ar": "r.ar", "per-": "c.p r.er",
    "-s": "c.s", "-es": "e0 c.s", "-ed": "e0 c.d", "-ing": "s.i k.ng",
    "a-": "b.a", "-able": "b.a | c.b le", "-ible": "b.i | c.b le", "ple": "c.p le", "-y": "b.y", "-ly": "c.l b.y",
    "graph": "c.gr s.a k.ph", "phone": "k.ph l.o c.n e>", "morph": "c.m r.or k.ph",
    "-ive": "s.i c.v e0",                                         # as give and live (step 8)
    "-ion": "s.a c.c | g.ti b.o c.n ; seam 2",                    # drawn inside action, as notation's ti (ruled 8 November 2026)
}
# A part drawn inside a word, because its marks need a letter of the base: the word its code spells.
PART_WORD = {"-ion": "action"}

# A spelling that is two words, each with its own marking (from flsz_family.py; produce and conduct are drafts of
# 10 November 2026 for the *deuk- family: the verb's first vowel is weak, so bare, and the noun's is said in full).
VARIANTS = {
    "produce": [("c.pr b.o | c.d l.u c.c e> ; nudge 5>4", "to produce: the verb"), ("c.pr l.o | c.d l.u c.c e> ; nudge 5>4", "produce: the noun")],
    "conduct": [("c.c b.o c.n | c.d s.u c.ct", "to conduct: the verb"), ("c.c s.o c.n | c.d s.u c.ct", "conduct: the noun")],
    "live": [("c.l l.i c.v e>", "a live show"), ("c.l s.i c.v e0", "we live here")],
}

# Shown in plain letters until their marking is settled, each with why and what comes next, for the step page's
# under-construction note (build_site.py).
CONTRACTION = ("The contractions aren't drawn here yet.", "draw them with the red apostrophe, as the verb-system cards do.")
FAMILY = ("*Act*, *create* and their families are marked in the family decks, which aren't on the site yet.", "bring their marking over from those decks.")
GREEK = ("Whether a seam goes between the Greek parts of *telephone* and *photograph* is still being decided.", "decide, then draw them.")
UNMARKED = {**{w: CONTRACTION for w in ("I'm", "it's", "isn't", "don't", "can't", "won't", "we're")},
            **{w: FAMILY for w in ("act", "action", "actor", "active", "react", "create", "creation", "creator")},
            "telephone": GREEK, "photograph": GREEK}

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
    ("legomorphic", "seams after leg, after o and after morph, a short e, and a long o with no vault",
     "Seam after leg added 10 November 2026, at Dante's question. The o is the verb's ending for I, in Greek and Latin "
     "alike (leg-o, gather-I), so it is a morpheme of its own; read instead as the linking o of biology, it still sits "
     "between seams. It is long because it ends its morpheme, as in go and going, so nothing after the seam sends it a "
     "vault. The seam between o and morph joins two Greek parts, which is still open for telephone and photograph. "
     "The e is short, as in Lego, so leg closes its syllable, as lem does in lemon."),
    ("notate", "note + ate: the e drops, and the a of ate sends a vault back to the o", "As making and photo."),
    ("notation", "notate + ion: ti as a green unit across a seam, the t black and the i red, with the vault sent from the i",
     "Ruled 8 November 2026: the t and i spell sh together, so their bar and circle are green, as for sh, and the letters "
     "keep their own colours, so the i is red, and it still makes the a long. Until then ti was a black unit, as the "
     "create family deck draws creation."),
    ("happy, happier, happily, unhappy", "a seam after the doubled p: hap + y, as sun + y",
     "Ruled 9 November 2026. Hap, chance or luck, isn't said on its own now, but its family shows the join: happen, "
     "hapless, mishap, haphazard. The double p alone doesn't show a seam, since rabbit and lesson double with nothing "
     "to join. Until then happy was drawn as an inherited double with no seam, as pretty is."),
    ("happen", "happ + en: a seam after the doubled p, and the e of -en bare",
     "As happy. Etymonline gives happen as hap with the verb-forming -n; the e is said weakly, as in seven."),
    ("hapless", "hap + less: one p and no box", "A consonant follows the seam, so nothing doubles. The e of -less is bare, as in hopeless."),
    ("mishap, haphazard", "s and h, and p and h, on either side of a seam, each with its own circle",
     "The seam splits what would otherwise read as sh and ph. The ar of hazard takes the r-controlled unit of car, "
     "though it spells the er sound: a unit's second sound is marked alike, as look's oo is."),
    ("gone", "a bare o and an e in a cone, as done",
     "Gone has the short o of got for most speakers, and done has the u of up. Both are marked as borrowing vowels at step 19, "
     "since the e sends no vault. A short mark on gone's o would be the other reading."),
    ("produce, conduct (the *deuk- page), drafts", "two markings each: the verb with a bare first vowel, the noun with a marked one",
     "Stress falls on the root in the verb (proDUCE, conDUCT) and on the prefix in the noun (PROduce, CONduct). With no "
     "stress mark, the weak vowel is the only sign. Ruled 10 November 2026: the noun produce has a long mark on its o and no vault, since "
     "a vault would name a cause the letters don't supply, and capitals show stress in captions. Some speakers say a short o, "
     "which would close the syllable instead (prod·uce). The ct of duct is one "
     "consonant cluster, as the nt of went."),
    # step 16's new words and contrasts, 10 November 2026
    ("robin", "a short o closed by b, and a short i in -in, with no vault",
     "As lemon and seven, and as the role cards draw robin. The i of -in is said lightly but still has the sound of "
     "the i in sit, so it takes a short mark, as in music and doing."),
    ("tiger, paper, open, even, robot, silent", "a long mark on the first vowel and no vault",
     "Changed 10 November 2026 at Dante's direction, after the noun produce: these are one part each, and no letter makes "
     "the first vowel long, so a vault would name a cause that isn't there. Until then each had a vault from the next vowel. "
     "Over, pony and photo still have that vault and wait for the same ruling."),
    ("music, basic", "a seam before ic, and a vault from the i to the long vowel",
     "Added 10 November 2026: muse + ic and base + ic. The i took the dropped e's place and its job, as in making. Music is "
     "from Greek mousike, of the Muses; basic is base + ic (Etymonline)."),
    ("robot", "a long first o, and a second o that is short",
     "One consonant between, and the first o spells its name. The second o is short, as in hot, "
     "for most speakers; said weakly, it would be bare."),
    ("river", "a short i closed by v, with no vault, and er as the r-controlled unit",
     "As seven and never: a short first vowel takes the consonant into its syllable (riv·er), and er is marked as in tiger."),
    ("silly", "a box over ll and a blocked vault from y, with no seam",
     "As middle. Silly comes from Old English gesælig, happy or fortunate (Etymonline), not from sill + y, so its double l "
     "is inherited, as the tt of pretty is. Happy has a seam and silly doesn't, though both once meant fortunate."),
]
