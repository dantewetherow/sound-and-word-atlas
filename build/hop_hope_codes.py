"""Draft codes for the hop and hope concept, the first to be built end to end (planned 8 November 2026).

The site doesn't use them yet. Hop, hope, hopping and hoping were already marked; these are the other nine words of
the two families, each following the word named in its comment, in the same code as legomorphic_words.py. CALLS
lists the choices they rest on, for a ruling. Once ruled, the codes move into the word file and the calls into the
manual's Marking calls tab. The plan for the concept is the "hop and hope" tab of the site plan doc."""

HOP_HOPE = {
    "hops": "c.h s.o c.p + c.s",                                   # as gets
    "hopped": "c.h s.o x.pp + e0 c.d ; bv 3>2",                    # as blocked
    "hopper": "c.h s.o x.pp + | r.er ; bv 3>2",                    # as hopping, with er as in better
    "hopes": "c.h l.o c.p e> + c.s",                               # as lives
    "hoped": "c.h l.o c.p + e> c.d",                               # as liked
    "hopeful": "c.h l.o c.p e> + | c.f b.u c.l",                   # as useful
    "hopeless": "c.h l.o c.p e> + | c.l b.e k.ss",                 # as useful, with the e of -less weak
    "hopefully": "c.h l.o c.p e> + | c.f b.u x.ll | b.y ; bv 7>6 ; seam 6",   # as fully, with the seam between the l's
    "hopelessness": "c.h l.o c.p e> + | c.l b.e k.ss + | c.n b.e k.ss",       # as hopeless, twice over
}

CALLS = [
    ("hopped", "box on pp; the e of -ed in a cone, its reach stopped by the box",
     "The -ed adds no syllable, so its e is silent, as on the verb cards."),
    ("hoped", "a seam before the e, which keeps the vault back to the o",
     "The e of -ed takes over the silent e's job, as the i does in hoping."),
    ("hopper", "box on pp; a blocked vault from er", "-er reaches back as -ing does, so the p doubles."),
    ("hopeful, hopeless, hopelessness", "the e of hope keeps its cone and its vault across the seam; the endings' vowels bare",
     "The endings' vowels are said weakly, so they take no mark."),
    ("hopefully", "box on ll, a seam between the two l's, a blocked vault from the y",
     "The two l's come from two parts but spell one sound, as the ee of been does. Or no box at all: the u of -ful is "
     "weak, so there's no short vowel to protect."),
]
