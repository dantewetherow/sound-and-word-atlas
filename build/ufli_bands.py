"""The UFLI crosswalk in bands (13 November 2026): UFLI's 128 lessons in sixteen groups, each with the steps it meets, the
mark the notation adds, one or two marked examples, and where the two programs part. All wording ours; lesson numbers
are UFLI's. Example words are hand-marked, or marked by rule and checked by hand here (the code beside them).

(first lesson, last lesson, what UFLI teaches there, the mark, [(word, code or None)], where they part)"""

BANDS = [
    (1, 12, "The first letters, and short a, i and o",
     "A circle under each sound, the cup over a short vowel, and a swoop under the word.",
     [("I", None), ("it", None)],
     "The route opens with <i>I</i> against <i>it</i>: open and closed in the first lesson. UFLI starts a letter at a time, "
     "and open syllables wait for lesson 66."),
    (13, 19, "More letters, and short u and e",
     "The same marks: circles, cups, swoops.",
     [("bed", None), ("cup", "c.c s.u c.p")],
     "Nothing parts here. Both programs are building the closed syllable."),
    (20, 21, "The -s ending, said /s/ and /z/",
     "The seam: a dotted line before the s. One spelling, two sounds.",
     [("cats", None), ("dogs", None)],
     "UFLI is ahead here: -s comes at lesson 20, and on the route at step 13. The seam is the one mark to bring in early."),
    (22, 41, "The rest of the consonants, blends, x and qu",
     "Two circles under a blend and no bar; the bond bar ties q to u, with a circle under each.",
     [("six", "c.s s.i c.x"), ("squirrel", "c.s q.qu r.ir | c.r b.e c.l")],
     "The notation draws x with one circle (ruled 8 November 2026), where UFLI counts two sounds. Say both: one letter, two sounds."),
    (42, 44, "ff, ll, ss and zz at the end; all, oll, ull; ck",
     "A bond bar under the doubled letters. They are the doubled spellings that become a block box when an ending comes.",
     [("will", None), ("pick", None)],
     "The route ties these to the box (step 14): <i>pick</i> and <i>picking</i> are one idea. UFLI teaches them as spellings at the end."),
    (45, 53, "sh, th, ch, wh, ph, ng and nk",
     "A green bar and circle for sh, th and ch; a black bar for wh, ph and ng.",
     [("fish", None), ("thing", None)],
     "The route brings these in at step 5, well before UFLI does. One mark serves both sounds of th."),
    (54, 62, "Silent e: a_e, i_e, o_e, e_e, u_e; c and g before e; have and give",
     "The vowel vault from the e to the vowel it makes long; the nice-nudge to a soft c or g; the cone without a vault in <i>have</i>.",
     [("make", None), ("face", None), ("have", None)],
     "UFLI teaches the silent e one vowel at a time. The route teaches one vault for all of them (step 9), and <i>have</i> and <i>give</i> just before it (step 8), so the exception and the rule sit side by side."),
    (63, 65, "-es, -ed and -ing",
     "The seam before the ending; -ed is one spelling for three sounds.",
     [("played", None), ("wanted", None)],
     "UFLI adds the endings here and leaves doubling and the dropped e to lessons 107 to 109. The route brings all three together at steps 13 to 15, so <i>hoping</i> and <i>hopping</i> are learned as one system."),
    (66, 68, "Open and closed syllables, compounds",
     "The long mark on an open syllable, the cup on a closed one, a swoop for each.",
     [("robot", None), ("tiger", None)],
     "The biggest gap. UFLI reaches open syllables at lesson 66; the route starts with them. See why below."),
    (69, 76, "tch and dge; long vowels before two consonants; y as a vowel; -le",
     "tch and dge as the doubled ch and j, in a box after a short vowel; the long mark with no vault (<i>find</i>); a red circle under y; one swoop and one circle for le.",
     [("catch", None), ("table", None), ("my", None)],
     "<i>My</i> and <i>by</i> are regular on the route from step 3. In UFLI, y as a vowel waits for lesson 73, and until then they have to be learned as heart words."),
    (77, 83, "ar, or, er, ir, ur, and or after w",
     "The r-controlled unit: one red bar under the vowel and its r, one circle.",
     [("car", None), ("bird", None)],
     "The two programs agree. The unit makes visible that er, ir and ur are one sound with three spellings."),
    (84, 92, "Vowel teams: ai, ay, ee, ea, ey, oa, ow, oe, ie, igh, oo, ew, ue",
     "A red bond bar under the team: two or more letters, one vowel sound.",
     [("rain", None), ("boat", None)],
     "Close agreement. The route adds where a team sits: ai and oa inside a word, ay and ow at the end."),
    (93, 97, "au and aw; ea for short e; oi, oy, ou, ow",
     "The same red bar, for a team that says a second sound or a sound that glides.",
     [("saw", None), ("head", None), ("coin", None)],
     "Close agreement. The bar stays the same when a team says its second sound (<i>head</i>): the spelling is the unit, not the sound."),
    (98, 98, "kn, wr and mb",
     "The silent letter joins its unit under one bar. A cone only where another form of the word says the letter.",
     [("knife", None), ("sign", None)],
     "The notation splits UFLI&rsquo;s silent letters in two: empty ones bonded (<i>knife</i>), inert ones coned (<i>sign</i>, because of <i>signal</i>)."),
    (99, 118, "Prefixes and suffixes, doubling, the dropped e, y to i; more vowel spellings",
     "The seam at each join; the block box for doubling; out with the old where the e drops; y turns to i at the seam.",
     [("hopping", None), ("hoping", None), ("unhappy", None)],
     "UFLI teaches these late and one rule at a time. The route reads common prefixes early and builds the joins at steps 14, 15, 29 and 30."),
    (119, 128, "-sion, -tion, -ture, -er, -or, -ist, -ness, -ment, -able, -ible; uni-, bi-, tri-",
     "The seam before the suffix, with the base whole: <i>act + ion</i>, <i>pict + ure</i>. The green bar of <i>ti</i> runs across the seam for the sound.",
     [("action", "s.a c.c | g.ti b.o c.n ; seam 2"), ("picture", None)],
     "UFLI teaches -tion and -ture as units for the sound. Split at the meaning, the t belongs to the base, which is why it comes back in <i>act</i>, <i>actor</i> and <i>active</i>. The notation shows both at once."),
]

WHY = """<p>The route starts with open and closed syllables because the words learners need first are built on that contrast. The prepositions (<i>it, in, on, up</i>), the pronouns (<i>I, me, my, he, she, we</i>) and the pointing words (<i>this, that, these, those</i>) are the grammar of every sentence a learner says and reads. Taught together from the start, they become regular, and the first contrast learners meet is the one the spelling system is built on: <i>I</i> and <i>it</i>, <i>he</i> and <i>hen</i>, <i>no</i> and <i>not</i>.</p>
<p>UFLI comes to open syllables at lesson 66 and to y as a vowel at 73. Until then, words such as <i>he</i>, <i>me</i> and <i>my</i> have to be learned as heart words, by heart, as exceptions. Both programs teach these words early. The difference is that UFLI treats them as exceptions and the route as the rule.</p>
<p>The route also keeps a word&rsquo;s parts whole. UFLI teaches -tion and -ture as units, which works for saying them: <i>tion</i> reliably says /shun/. The cost is the base. Read as <i>ac + tion</i>, <i>action</i> hides <i>act</i>. Split at the meaning, it is <i>act + ion</i>, and the t belongs to the base, which is why it keeps turning up in <i>actor</i> and <i>active</i>. The notation shows both: the seam before <i>ion</i>, and the green bar of <i>ti</i> across it for the sound.</p>
<p>And it keeps a base&rsquo;s joins together. UFLI teaches -ing at lesson 65, doubling at 107 and the dropped e at 109. The route puts the vault, the box and the dropped e at steps 9, 14 and 15, so <i>hoping</i> and <i>hopping</i> are one system: the box blocks the vault, and the dropped e lets it through.</p>
<p>Heart words part the same way. UFLI draws a heart over the part to learn by heart. Most heart words are regular once their step comes on the route (<i>could</i>, <i>both</i>, <i>learn</i>), or have a reason a learner can use (<i>said</i> from <i>say</i>; the o of <i>son</i>, <i>month</i> and <i>love</i>); only a few are left to learn by heart. See <a href="lists/hearts.html">Words with a heart</a>.</p>
<p>Where UFLI is ahead: the -s ending comes at its lesson 20, before the route&rsquo;s step 13. The seam is the mark to bring in early.</p>"""
