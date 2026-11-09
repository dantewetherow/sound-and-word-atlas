"""Marking codes for the Dolch sight words that had none, written for the Dolch word cards on 6 November 2026.

Same code as legomorphic_words.py (see its docstring). The other 177 of Dolch's 220 words already have codes in the
deck tools, legomorphic_words.py or site_codes.py, and those are used as they stand. Each line here follows a word
that is already marked: the analog is named in the comment. CALLS lists the places where these codes rest on a
choice. They are in the manual's Marking calls tab under "From the Dolch cards" (added 6 November 2026) for a
ruling; once ruled, change the codes here to match and rebuild the cards."""

DOLCH_CODES = {
    # pre-primer: short vowels closed by one consonant (as it, not), and a final cluster with nothing after it (as must)
    "big": "c.b s.i c.g", "jump": "c.j s.u c.mp", "red": "c.r s.e c.d", "run": "c.r s.u c.n",
    # primer: ck as pick has it, our-as-or as your has it, oo as moon
    "black": "c.bl s.a k.ck", "but": "c.b s.u c.t", "four": "c.f r.our", "ran": "c.r s.a c.n",
    "soon": "c.s t.oo c.n", "yes": "c.y s.e c.s",
    # first grade: after splits as under does; fly as try; live is the verb, which is where Dolch lists it
    "after": "s.a c.f | c.t r.er", "ask": "s.a c.sk", "fly": "c.fl l.y", "just": "c.j s.u c.st", "let": "c.l s.e c.t",
    "live": "c.l s.i c.v e0", "stop": "c.st s.o c.p", "thank": "g.th s.a c.nk", "think": "g.th s.i c.nk",
    # second grade: ff and ll as will has its ll; ng as going; upon as away; don’t with the red apostrophe of the I’m card
    "best": "c.b s.e c.st", "don’t": "c.d l.o c.n ap c.t", "fast": "c.f s.a c.st", "its": "s.i c.t + c.s",
    "off": "s.o k.ff", "sing": "c.s s.i k.ng", "sit": "c.s s.i c.t", "sleep": "c.sl t.ee c.p", "tell": "c.t s.e k.ll",
    "upon": "b.u | c.p s.o c.n",
    # third grade: the bases the word sum cards already mark (clean, cut, full, hold, hot, light, long) kept as they are there
    "about": "b.a | c.b t.ou c.t", "bring": "c.br s.i k.ng", "clean": "c.cl t.ea c.n", "cut": "c.c s.u c.t",
    "drink": "c.dr s.i c.nk", "fall": "c.f b.a k.ll", "far": "c.f r.ar", "full": "c.f b.u k.ll", "hold": "c.h l.o c.ld",
    "hot": "c.h s.o c.t", "light": "c.l t.igh c.t", "long": "c.l s.o k.ng", "six": "c.s s.i c.x", "ten": "c.t s.e c.n",
}

# Choices these codes make that the manual and the cards do not settle outright.
CALLS = [
    ("don’t", "a long mark over the o, the red apostrophe, and no seam",
     "The apostrophe follows the I’m marking card, which says it does the same job in don’t: it stands in for the dropped "
     "o of not. The o spells its name before nt, as in old and both, so it takes a long mark and no vault."),
    ("six", "one circle under the x",
     "The x spells two sounds, k and then s. Rule 1 would give it two circles, as the o of one has two. No card shows an x yet."),
    ("thank, think, drink", "n and k as two consonants, with no mark for the ng sound of the n",
     "As s spelling z is unmarked. In sing, bring and long the ng spells one sound and keeps its unit, as in going."),
    ("its", "a seam before the s", "Its is it + s, as gets is get + s. Without the seam, ts is a final cluster."),
    ("upon", "no seam, and the first vowel bare",
     "As away and today are marked on the K–2 cards, since up- no longer means up. The word sum cards would put a seam after up."),
]
