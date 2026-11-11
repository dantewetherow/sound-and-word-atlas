"""Families in the Parts layer: roots/<slug>.html. The first, the root *leg-, made on 8 November 2026; the second, the
base hap, on 9 November 2026; the third, the root *deuk- (duce, duct), on 10 November 2026, with a lesson on stress.

*leg- follows Etymonline's entry for the root, which draws on Calvert Watkins, and the Indo-European Lexicon of the
Linguistics Research Center at the University of Texas at Austin, which follows Pokorny; every word in the family is
in one or the other's list, or is a plain derivative of one that is (collection, of collect). The site plan has the
roots follow Watkins's American Heritage Dictionary of Indo-European Roots (3rd ed., 2011), which these pages haven't
yet been checked against.

Since 9 November 2026 the *leg- page is clustered by spelling. It opens with the four roads the root took into English
(ROADS), then a cluster for each spelling (leg, lect, lig, legis, lege and league, the three worn down in French, log,
logue, lex, lego). Each word is a word sum in the site's convention (a letter in brackets drops at the seam): prefixes
end in a hyphen, suffixes start with one, the root's spelling stands bare, and any other bare part is another root
(lat, bio). Every part is a button: the page's script (CX_JS) opens the part's meaning (PARTS, or ROOT_PARTS for the
root's spellings) under the word, with the other words in the family that carry it. Without script every cluster
shows, one after another, and the glossary of parts below them gives the meanings.

Hap is a base rather than a Proto-Indo-European root: a word English took from Old Norse, which is no longer said on
its own (it is bound now, as fun is not). Its page groups the family by what follows hap, since that decides whether
the p doubles, and shows the letter pairs its seams split (mishap, haphazard). Its words are drawn with the codes in
site_codes.py; happy's seam was ruled on 9 November 2026, and the rest follow the analogs named there.

Each word in a family gets an id (doors.word_id), and write() returns (word, link, label) for the search."""
import html, json, re
from urllib.parse import quote
import doors

def etym(word, slug):
    """Where a family word's own history is: its Etymonline entry (by search, so the link holds), or for the notation's
    own name, its entry in Definitions."""
    return "../definitions.html#def-legomorphic" if word == "legomorphic" else f"https://www.etymonline.com/search?q={quote(word)}"


# ------------------------------------------------------------------ *leg-
# The roads in: (from, its meaning, [(cluster key, the spellings it gave)])
ROADS = [
    ("Latin <i>legere</i>", "to gather, to choose, to read", [("leg", "leg"), ("lect", "lect"), ("lig", "lig"), ("french", "les, lite"), ("lego", "lego")]),
    ("Latin <i>l&emacr;g&amacr;re</i>", "to send with a charge", [("leg", "leg"), ("lege", "lege, league")]),
    ("Latin <i>l&emacr;x</i>, <i>l&emacr;gis</i>", "law; its link to the root is uncertain", [("leg", "leg"), ("legis", "legis"), ("lege", "lege"), ("french", "loy")]),
    ("Greek <i>legein</i>, <i>logos</i>, <i>lexis</i>", "to say, to gather; a word", [("log", "log"), ("logue", "logue"), ("lex", "lex"), ("lect", "lect"), ("lego", "lego")]),
]

# The clusters, one for each spelling. A word is (word, parts or None, meaning), or with a fourth item, the letters to
# set in bold when it has no parts to show.
CLUSTERS = [
    {"key": "leg", "label": "leg", "spells": ["leg"], "head": "gather, read; send; law",
     "road": "Latin <i>legere</i>, to gather, to choose, to read, at the start of a word; <i>l&emacr;g&amacr;re</i>, to send "
             "with a charge; and <i>l&emacr;x</i>, <i>l&emacr;gis</i>, law",
     "note": "<i>Elegant</i> kept the e that <i>eligible</i> turned to i.",
     "groups": [
         [("legend", ["leg", "-end"], "a story to be read"), ("legendary", ["leg", "-end", "-ary"], "told of in legends")],
         [("legible", ["leg", "-ible"], "clear enough to read"), ("illegible", ["il-", "leg", "-ible"], "too unclear to read")],
         [("legion", ["leg", "-ion"], "a body of soldiers, chosen and gathered")],
         [("elegant", ["e-", "leg", "-ant"], "chosen with care, graceful")],
         [("legume", ["leg", "-ume"], "a bean or a pea: what is picked")],
         [("delegate", ["de-", "leg", "-ate"], "send someone to act for you"),
          ("delegation", ["de-", "leg", "-at(e)", "-ion"], "a group sent to act for others"),
          ("relegate", ["re-", "leg", "-ate"], "send away, move down"),
          ("legacy", ["leg", "-acy"], "what is handed down")],
         [("legal", ["leg", "-al"], "to do with the law"), ("illegal", ["il-", "leg", "-al"], "against the law"),
          ("legitimate", None, "allowed by law", "leg")],
     ]},
    {"key": "lect", "label": "lect", "spells": ["lect"], "head": "gathered, chosen, read",
     "road": "Latin <i>lectus</i>, the past form of <i>legere</i>; and Greek <i>-lektos</i> in <i>dialect</i> and <i>eclectic</i>",
     "note": "<i>-ion</i>, <i>-ive</i> and <i>-or</i> join Latin&rsquo;s past form: <i>collection</i>, <i>selective</i>, <i>elector</i>.",
     "groups": [
         [("collect", ["col-", "lect"], "gather together"), ("collection", ["col-", "lect", "-ion"], "things gathered together"),
          ("collective", ["col-", "lect", "-ive"], "shared by a group"), ("collector", ["col-", "lect", "-or"], "someone who collects"),
          ("recollect", ["re-", "col-", "lect"], "gather up again: remember")],
         [("select", ["se-", "lect"], "pick out"), ("selection", ["se-", "lect", "-ion"], "what is picked out"),
          ("selective", ["se-", "lect", "-ive"], "careful about what to pick")],
         [("elect", ["e-", "lect"], "choose"), ("election", ["e-", "lect", "-ion"], "choosing by vote"),
          ("elector", ["e-", "lect", "-or"], "someone who votes")],
         [("neglect", ["neg-", "lect"], "leave untended"), ("neglectful", ["neg-", "lect", "-ful"], "given to neglect")],
         [("intellect", ["intel-", "lect"], "the power to understand")],
         [("lecture", ["lect", "-ure"], "a reading, a talk"), ("lecturer", ["lect", "-ur(e)", "-er"], "someone who gives lectures")],
         [("dialect", ["dia-", "lect"], "a way of speaking, through Greek"), ("eclectic", ["ec-", "lect", "-ic"], "picked from many places, through Greek")],
     ]},
    {"key": "lig", "label": "lig", "spells": ["lig"], "head": "choose, gather",
     "road": "Latin <i>-ligere</i>: after a prefix, <i>legere</i> usually became <i>-ligere</i> (<i>colligere</i>, <i>eligere</i>, "
             "<i>diligere</i>), while its past form stayed <i>-lectus</i>",
     "note": "Lig and lect take turns in the same families: <i>eligible</i> and <i>elect</i>, <i>negligent</i> and <i>neglect</i>, "
             "<i>intelligent</i> and <i>intellect</i>. Lig comes before <i>-ent</i>, <i>-ence</i> and <i>-ible</i>, from Latin&rsquo;s "
             "present form; lect comes before <i>-ion</i>, <i>-ive</i> and <i>-or</i>, from its past form.",
     "groups": [
         [("eligible", ["e-", "lig", "-ible"], "able to be chosen")],
         [("negligent", ["neg-", "lig", "-ent"], "careless, not attending"), ("negligible", ["neg-", "lig", "-ible"], "too small to matter")],
         [("intelligent", ["intel-", "lig", "-ent"], "quick to understand"), ("intelligence", ["intel-", "lig", "-ence"], "the power to understand"),
          ("intelligible", ["intel-", "lig", "-ible"], "able to be understood")],
         [("diligent", ["di-", "lig", "-ent"], "careful and hard-working"), ("diligence", ["di-", "lig", "-ence"], "careful, steady work")],
     ]},
    {"key": "legis", "label": "legis", "spells": ["legis"], "head": "of law",
     "road": "Latin <i>l&emacr;gis</i>, of law, the form <i>l&emacr;x</i> takes in <i>l&emacr;gis l&amacr;tor</i>, a proposer of law",
     "groups": [
         [("legislator", ["legis", "lat", "-or"], "someone who brings in laws"), ("legislation", ["legis", "lat", "-ion"], "laws, and the making of them"),
          ("legislature", ["legis", "lat", "-ure"], "the body that makes laws")],
     ]},
    {"key": "lege", "label": "lege, league", "spells": ["lege", "league"], "head": "chosen with; law",
     "road": "Latin <i>coll&emacr;ga</i>, one chosen along with another, from <i>l&emacr;g&amacr;re</i>; and <i>l&emacr;x</i>, law, in <i>privilege</i>",
     "groups": [
         [("college", ["col-", "lege"], "a body of people gathered together"), ("colleague", ["col-", "league"], "someone chosen to work alongside you")],
         [("privilege", ["privi", "lege"], "a law for one person, a special right")],
     ]},
    {"key": "french", "label": "les, loy, lite", "spells": ["les", "loy", "lite"], "head": "worn down in French",
     "road": "Latin words that reached English through French and lost letters on the way: <i>lectio</i>, a reading, became "
             "<i>le&ccedil;on</i>; <i>l&emacr;g&amacr;lis</i>, legal, became <i>loial</i>; and <i>eligere</i>, to pick out, gave "
             "<i>eslite</i>, chosen",
     "groups": [
         [("lesson", None, "something to read or learn", "les")],
         [("loyal", ["loy", "-al"], "faithful"), ("loyalty", ["loy", "-al", "-ty"], "being faithful"), ("disloyal", ["dis-", "loy", "-al"], "not faithful")],
         [("elite", None, "the chosen few", "lite")],
     ]},
    {"key": "log", "label": "log", "spells": ["log"], "head": "word, reason, account",
     "road": "Greek <i>logos</i>, a word, an account, reason, from <i>legein</i>, to say, to gather",
     "note": "The y of these words is Greek <i>-ia</i>, not the y of <a href=\"hap.html\"><i>happy</i></a>.",
     "groups": [
         [("logic", ["log", "-ic"], "reasoning that holds together"), ("logical", ["log", "-ic", "-al"], "following reason"),
          ("illogical", ["il-", "log", "-ic", "-al"], "not following reason")],
         [("analogy", ["ana-", "log", "-y"], "a likeness that explains"), ("apology", ["apo-", "log", "-y"], "words said in defence, or to say sorry"),
          ("apologize", ["apo-", "log", "-ize"], "say sorry")],
         [("anthology", ["antho", "log", "-y"], "a collection of writing: a gathering of flowers")],
         [("biology", ["bio", "log", "-y"], "the study of life"), ("geology", ["geo", "log", "-y"], "the study of the earth"),
          ("ecology", ["eco", "log", "-y"], "the study of living things and their homes"),
          ("psychology", ["psycho", "log", "-y"], "the study of the mind"),
          ("technology", ["techno", "log", "-y"], "the study and use of tools and skills")],
     ]},
    {"key": "logue", "label": "logue", "spells": ["logue"], "head": "word, talk",
     "road": "Greek <i>logos</i>, through Latin and French; Canadian and British spelling keep the -ue",
     "groups": [
         [("dialogue", ["dia-", "logue"], "talk between people"), ("monologue", ["mono-", "logue"], "talk by one person"),
          ("prologue", ["pro-", "logue"], "words before the story"), ("epilogue", ["epi-", "logue"], "words after the story"),
          ("catalogue", ["cata-", "logue"], "a list of things"), ("analogue", ["ana-", "logue"], "something that is like another")],
     ]},
    {"key": "lex", "label": "lex", "spells": ["lex"], "head": "word, speech",
     "road": "Greek <i>lexis</i>, a word, speech, from <i>legein</i>",
     "groups": [
         [("lexicon", ["lex", "-ic", "-on"], "the words of a language"), ("lexical", ["lex", "-ic", "-al"], "to do with words"),
          ("dyslexia", ["dys-", "lex", "-ia"], "a lasting difficulty with reading and spelling words")],
     ]},
    {"key": "lego", "label": "lego", "spells": ["leg"], "head": "I gather",
     "road": "Greek <i>l&eacute;g&omacr;</i> and Latin <i>leg&omacr;</i>, the verb itself, which both languages inherited from "
             "the root: in Greek, I gather, I count, I say; in Latin, I gather, I choose, I read",
     "note": "The <i>&omacr;</i> is the ending for I in both languages, so <i>lego</i> is leg + o, gather + I, as Latin "
             "<i>veto</i> is I forbid and <i>credo</i> I believe.",
     "groups": [
         [("legomorphic", ["leg", "-o", "morph", "-ic"], "this notation&rsquo;s name: <i>leg&omacr;</i>, I gather, in Greek "
           "and Latin alike, and <i>morph</i>, form")],
         [("prolegomenon", ["pro-", "leg", "-omenon"], "what is said beforehand: a formal introduction to a study. Greek "
           "<i>prolegein</i>, to say before; more than one are <i>prolegomena</i>. <a href=\"#w-prologue\"><i>Prologue</i></a> "
           "is its plainer twin: pro + logue")],
     ]},
]

# What each part means. The root's own spellings take ROOT_PARTS.
PARTS = {
    # before the root
    "col-": "with, together: Latin <i>com-</i>, written <i>col-</i> before l",
    "se-": "apart, aside",
    "e-": "out: Latin <i>ex-</i>, written <i>e-</i> before l, d and some other consonants",
    "neg-": "not: Latin <i>neg-</i>, <i>nec</i>",
    "intel-": "between: Latin <i>inter-</i>, written <i>intel-</i> before l",
    "di-": "apart: Latin <i>dis-</i>, written <i>di-</i> before l",
    "re-": "again, back",
    "de-": "down, away",
    "il-": "not: Latin <i>in-</i>, written <i>il-</i> before l",
    "dis-": "not, the opposite of",
    "dia-": "through, across, between (Greek)",
    "ec-": "out (Greek <i>ek</i>)",
    "ana-": "up, back, according to (Greek)",
    "apo-": "away, off (Greek)",
    "cata-": "down, completely (Greek)",
    "pro-": "before, forward, forth: Greek and Latin <i>pro</i>",
    "epi-": "upon, after (Greek)",
    "mono-": "one, alone (Greek)",
    "dys-": "bad, hard (Greek)",
    # after the root
    "-ion": "the act or result of",
    "-ive": "tending to, doing",
    "-or": "one who, the thing that",
    "-er": "one who, or the thing that",
    "-ful": "full of, given to",
    "-ure": "the act or result of",
    "-ic": "having to do with",
    "-al": "having to do with",
    "-ent": "being, doing: from Latin&rsquo;s present form of the verb",
    "-ence": "the state of being",
    "-ible": "able to be",
    "-end": "to be: Latin <i>legendus</i>, to be read",
    "-ary": "having to do with",
    "-ant": "being, doing: from Latin&rsquo;s present form, as <i>-ent</i>",
    "-ume": "a Latin noun ending (<i>leg&umacr;men</i>): a thing",
    "-ate": "a Latin past form: sent, made",
    "-acy": "a state, an office",
    "-ty": "the state of being",
    "-y": "the Greek ending <i>-ia</i>: a study, an art, a quality; not the y of <i>happy</i>",
    "-ize": "make, do",
    "-ia": "a condition (Greek)",
    "-omenon": "a Greek ending: a thing being done. A <i>phenomenon</i> is a thing appearing; a <i>prolegomenon</i>, a thing being said first",
    "-on": "a Greek ending: <i>lexikon</i>, a word book",
    "-o": "I: the ending of the verb&rsquo;s I form in Greek and Latin alike (<i>l&eacute;g&omacr;</i>, <i>leg&omacr;</i>), as in Latin <i>veto</i>, I forbid",
    # other roots
    "lat": "carried: Latin <i>l&amacr;tus</i>, another root. A <i>l&emacr;gis l&amacr;tor</i> carried a law forward",
    "antho": "flower (Greek <i>anthos</i>)",
    "bio": "life (Greek <i>bios</i>)",
    "geo": "earth (Greek <i>g&emacr;</i>)",
    "eco": "house, home (Greek <i>oikos</i>)",
    "psycho": "mind, breath (Greek <i>psykh&emacr;</i>)",
    "techno": "art, skill, craft (Greek <i>tekhn&emacr;</i>)",
    "privi": "one person, one&rsquo;s own (Latin <i>pr&imacr;vus</i>)",
    "morph": "form (Greek <i>morph&emacr;</i>)",
}
ROOT_PARTS = {
    "leg": "gather, read; send; or law: Latin <i>legere</i>, <i>l&emacr;g&amacr;re</i> or <i>l&emacr;x</i>; in "
           "<i>legomorphic</i>, Greek and Latin <i>leg&omacr;</i>, I gather",
    "lect": "gathered, chosen, read: Latin <i>lectus</i>, the past form of <i>legere</i>",
    "lig": "choose, gather: Latin <i>-ligere</i>, <i>legere</i> after a prefix",
    "legis": "of law: Latin <i>l&emacr;gis</i>",
    "lege": "chosen with (<i>college</i>), or law (<i>privilege</i>)",
    "league": "chosen with: Latin <i>coll&emacr;ga</i>",
    "loy": "law: Latin <i>l&emacr;g&amacr;lis</i>, legal, worn down in French",
    "log": "word, reason, account: Greek <i>logos</i>",
    "logue": "word, talk: Greek <i>logos</i>",
    "lex": "word, speech: Greek <i>lexis</i>",
}

LEG = {
    "slug": "leg", "root": "*leg-", "gloss": "to gather, to collect", "kind": "a root family",
    "h1_s": "*leg- means &lsquo;gather&rsquo;",
    "lead": "To gather, to collect. Speakers of Greek and Latin carried this Proto-Indo-European root into words about "
            "words: gathering words is choosing them, reading them and saying them. English borrowed the family back again "
            "and again, and the notation&rsquo;s own name is one of them.",
    "drawn": ("legomorphic", "legomorphic, marked: leg + o + morph + ic"),
    "sources": [("Etymonline, *leg-", "https://www.etymonline.com/word/%2Aleg-"),
                ("Indo-European Lexicon, leg̑- (Linguistics Research Center, University of Texas at Austin), with Latin&rsquo;s "
                 "prefixed forms of <i>legere</i>", "https://lrc.la.utexas.edu/lex/master/1131"),
                ("Etymonline, <i>eligible</i>: Latin <i>eligere</i>, <i>ex</i> + <i>legere</i>", "https://www.etymonline.com/word/eligible"),
                ("Etymonline, <i>intelligible</i>: Latin <i>intellegere</i>, <i>inter</i> + <i>legere</i>", "https://www.etymonline.com/word/intelligible"),
                ("Etymonline, <i>elegant</i>: a form of <i>eligere</i>&rsquo;s present participle", "https://www.etymonline.com/word/elegant"),
                ("Wiktionary, Proto-Indo-European *leǵ-", "https://en.wiktionary.org/wiki/Reconstruction:Proto-Indo-European/le%C7%B5-"),
                ("Wiktionary, Ancient Greek <i>λέγω</i>: gather, choose, count, say; its I form", "https://en.wiktionary.org/wiki/%CE%BB%CE%AD%CE%B3%CF%89"),
                ("Wiktionary, Latin <i>leg&omacr;</i>: choose, gather, read; its I form", "https://en.wiktionary.org/wiki/lego#Latin"),
                ("Etymonline, <i>veto</i>: Latin, I forbid", "https://www.etymonline.com/word/veto")],
    "roads": ROADS, "clusters": CLUSTERS, "parts": PARTS, "root_parts": ROOT_PARTS,
    "students": ["collect", "select", "elect", "lesson", "legend", "logic", "dialogue"],
    "s_lead": "These words come from one old word that meant <i>gather</i>.",
    "uc": "the family follows Etymonline, which draws on Calvert Watkins, and the Indo-European Lexicon, which follows "
          "Pokorny. Wiktionary marks the link from <i>l&emacr;x</i>, law, as uncertain. Next: check the family against "
          "Watkins&rsquo;s entry, and draw each word in the notation once its marking is ruled.",
    "label": "Root family: *leg-",
    "desc": "The root *leg-, to gather, to collect, and its family of English words, spelling by spelling, with what each part means.",
}


# ------------------------------------------------------------------ hap
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
                 "https://books.openbookpublishers.com/10.11647/obp.0053/ch4.xhtml"),
                ("Alice Turk, &ldquo;Articulatory Phonetic Clues to Syllable Affiliation&rdquo; (Cambridge University Press, 1994), "
                 "on Daniel Kahn&rsquo;s and Elisabeth Selkirk&rsquo;s accounts of where such a consonant belongs",
                 "https://www.cambridge.org/core/books/phonological-structure-and-phonetic-form/articulatory-phonetic-clues-to-syllable-affiliation-gestural-characteristics-of-bilabial-stops/55D545433F8A1184F9992C1E25902D68"),
                ("<i>Essentials of Linguistics</i>, &ldquo;Aspirated Stops in English&rdquo;: the puff after a p that starts a stressed syllable",
                 "https://open.maricopa.edu/essentialsoflinguistics/chapter/3-5-aspirated-stops-in-english/"),
                ("Sonia Ben Hedia, <i>Gemination and Degemination in English Affixation</i> (Language Science Press, 2019)",
                 "https://langsci-press.org/catalog/book/221")],
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
    # (id, heading, its paragraphs, words drawn under it as (word, caption))
    "extra": [
        ("pairs", "Letter pairs the seam splits",
         ["Read these without the seam and they go wrong. In <i>mishap</i> the s and the h meet across the seam, so they "
          "don&rsquo;t spell <i>sh</i>: mis + hap, not mish + ap. In <i>haphazard</i> the p and the h meet the same way, so "
          "they don&rsquo;t spell the sound of <i>ph</i> in <a href=\"../steps/32.html\"><i>phone</i></a>: hap + hazard. "
          "<i>Shepherd</i> (sheep + herd) and <i>uphill</i> work like this too."],
         [("mishap", "s + h, not sh"), ("haphazard", "p + h, not ph")]),
        ("meant", "What happy meant",
         ["<i>Happy</i> is hap + y: having hap. Its first meaning, in the late 1300s, was lucky, favoured by fortune, and the "
          "sense of glad came in the same century. <i>Lucky</i>, luck + y, is built the same way, and means now what "
          "<i>happy</i> meant then. The y is the ending of <i>sunny</i> and <i>funny</i>: having, or full of, what the base "
          "names. Read without hap, <i>happy</i> means being in a happy state, which goes in a circle. With hap, it means "
          "having luck."], []),
        ("double", "Does the double p show the seam?",
         ["Not on its own. A double keeps a short vowel short whether or not there&rsquo;s a join: <i>rabbit</i> and "
          "<a href=\"leg.html#w-lesson\"><i>lesson</i></a> double with nothing to join. Carney counts <i>happy</i> among the "
          "ordinary doubles, with <i>hobby</i>, <i>silly</i> and <i>merry</i>, and says the hidden boundary in <i>chubby</i> "
          "and <i>shabby</i> needn&rsquo;t be known to explain theirs. What shows the seam is the family: the same hap, with "
          "the same meaning, in <i>hapless</i> and <i>mishap</i>, where nothing doubles. <i>Fun</i> is "
          "<a href=\"../definitions.html#def-free\">free</a>, a word on its own, so the seam in <i>funny</i> is easy to see; "
          "<i>hap</i> is <a href=\"../definitions.html#def-bound\">bound</a> now, so the family does the showing.",
          "Nor does the double p spell two sounds. Carney lists pp among the spellings of the single sound /p/ (p. 16). The "
          "lips close once, at the end of <i>ha</i>, and open once, into the y, and the break between the syllables falls "
          "inside that one sound, so it seems to belong to both. Daniel Kahn called such a consonant <i>ambisyllabic</i>; "
          "Elisabeth Selkirk put it in the first syllable, as the swoops here do. The puff of breath in <i>pen</i> isn&rsquo;t "
          "a second p: English adds it where a p starts a stressed syllable, so <i>appear</i> has it and <i>happy</i> "
          "doesn&rsquo;t. Two p sounds meet only where two parts each bring one, as in <i>top pick</i>, and the lips stay "
          "shut longer; joins inside words, such as <i>unnamed</i>, work the same way."], []),
    ],
    "students": ["happy", "happen", "mishap", "perhaps"],
    "s_lead": "These words come from <b>hap</b>. It is an old word for luck.",
    "uc": "the family follows Etymonline and the Indo-European Lexicon, which cites Watkins. Next: check it against "
          "Watkins&rsquo;s entry for <i>*kob-</i>, as for <i>*leg-</i>.",
    "label": "Base family: hap",
    "desc": "The base hap, chance or luck, and its family: happy, happen, mishap and haphazard, and why happy has two p's and mishap one.",
}
ROOTS = [LEG, HAP]


# ------------------------------------------------------------------ *deuk-
# Made 10 November 2026. The word list follows the Indo-European Lexicon's entry (Pokorny's deuk-, to pull, to tow),
# fetched that day; Etymonline's *deuk- entry (to lead) couldn't be reopened then and is next to check. The family
# carries two lessons: duce and duct take turns, as lig and lect do; and stress tells the verb from the noun
# (proDUCE, PROduce), which the marks show only through the weak vowel, since the notation has no stress mark.
DEUK_ROADS = [
    ("Latin <i>d&umacr;cere</i>", "to lead, to draw along", [("duce", "duce"), ("duct", "duct")]),
    ("Latin <i>&emacr;duc&amacr;re</i>", "to bring up, to rear: a verb beside <i>&emacr;d&umacr;cere</i>, to lead out", [("duc", "duc")]),
    ("Latin <i>dux</i>, <i>ducis</i>, and French", "a leader; and Latin words worn down in French", [("french", "duke, duch, duit, due")]),
    ("Old English <i>togian</i>, <i>t&emacr;on</i>", "to pull, to draw", [("germanic", "tow, tug, tie, team")]),
]
DEUK_CLUSTERS = [
    {"key": "duce", "label": "duce", "spells": ["duce"], "head": "lead",
     "road": "Latin <i>d&umacr;cere</i>, to lead, in its present form, after a prefix that says which way",
     "note": "The final e does two jobs at once: it sends the vault that makes the u long (<a href=\"../steps/09.html\">step 9</a>) and it "
             "nudges the c soft (<a href=\"../steps/10.html\">step 10</a>). Before a vowel suffix the e drops and the suffix&rsquo;s vowel "
             "takes over both jobs: <i>producer</i>, <i>reducible</i>, <i>conducive</i>.",
     "groups": [
         [("produce", ["pro-", "duce"], "lead forth: make, bring out; as a noun, what is grown"),
          ("producer", ["pro-", "duc(e)", "-er"], "one who makes or brings out", "duc"),
          ("reproduce", ["re-", "pro-", "duce"], "make again; make a copy")],
         [("reduce", ["re-", "duce"], "lead back: bring down, make smaller"),
          ("reducible", ["re-", "duc(e)", "-ible"], "able to be made smaller", "duc")],
         [("introduce", ["intro-", "duce"], "lead inside: bring in, make known")],
         [("induce", ["in-", "duce"], "lead into: bring about, persuade"), ("deduce", ["de-", "duce"], "lead down from: work out by reasoning"),
          ("educe", ["e-", "duce"], "lead out: draw out"), ("adduce", ["ad-", "duce"], "lead toward: bring forward as proof"),
          ("seduce", ["se-", "duce"], "lead aside, lead astray")],
         [("conduce", ["con-", "duce"], "lead together: help to bring about"),
          ("conducive", ["con-", "duc(e)", "-ive"], "helping to bring about", "duc")],
         [("traduce", ["tra-", "duce"], "lead across, as a show: speak ill of"),
          ("transducer", ["trans-", "duc(e)", "-er"], "a device that carries energy across from one form to another", "duc")],
     ]},
    {"key": "duct", "label": "duct", "spells": ["duct"], "head": "led",
     "road": "Latin <i>ductus</i>, led, the past form of <i>d&umacr;cere</i>",
     "note": "Duce and duct take turns, as <a href=\"leg.html#c-lig\">lig and lect</a> do. The verb ends in duce; <i>-ion</i>, <i>-ive</i> and "
             "<i>-or</i> join Latin&rsquo;s past form, duct: <i>produce</i> and <i>production</i>, <i>reduce</i> and <i>reduction</i>, "
             "<i>induce</i> and <i>induction</i>. A speller who hears <i>duk-shun</i> can write duct + ion: the c is hard because a t "
             "follows it, and <i>ti</i> spells the sh.",
     "groups": [
         [("duct", ["duct"], "a pipe or channel that leads something along"), ("ductile", ["duct", "-ile"], "able to be drawn out, as wire is"),
          ("aqueduct", ["aque", "duct"], "a channel that leads water")],
         [("product", ["pro-", "duct"], "what is brought forth"), ("production", ["pro-", "duct", "-ion"], "the making of things"),
          ("productive", ["pro-", "duct", "-ive"], "making a lot"), ("productivity", ["pro-", "duct", "-iv(e)", "-ity"], "how much is made"),
          ("reproduction", ["re-", "pro-", "duct", "-ion"], "making again; a copy")],
         [("reduction", ["re-", "duct", "-ion"], "a making smaller")],
         [("introduction", ["intro-", "duct", "-ion"], "a leading in: a first meeting, an opening part")],
         [("conduct", ["con-", "duct"], "lead together: guide, lead; as a noun, how someone behaves"),
          ("conductor", ["con-", "duct", "-or"], "one who leads; a thing that carries heat or current"),
          ("conduction", ["con-", "duct", "-ion"], "the carrying of heat or current"),
          ("misconduct", ["mis-", "con-", "duct"], "bad behaviour")],
         [("induct", ["in-", "duct"], "lead in: bring into a group"), ("induction", ["in-", "duct", "-ion"], "a leading in; reasoning from cases to a rule"),
          ("inductive", ["in-", "duct", "-ive"], "reasoning from cases to a rule")],
         [("deduct", ["de-", "duct"], "lead away: take off"), ("deduction", ["de-", "duct", "-ion"], "a taking off; or what is deduced"),
          ("deductive", ["de-", "duct", "-ive"], "reasoning from a rule to a case")],
         [("abduct", ["ab-", "duct"], "lead away by force"), ("abduction", ["ab-", "duct", "-ion"], "a taking away by force")],
         [("seduction", ["se-", "duct", "-ion"], "a leading astray"), ("seductive", ["se-", "duct", "-ive"], "tempting")],
     ]},
    {"key": "duc", "label": "duc", "spells": ["duc"], "head": "bring up",
     "road": "Latin <i>&emacr;duc&amacr;re</i>, to bring up, to rear, a verb that stands beside <i>&emacr;d&umacr;cere</i>, to lead out",
     "note": "<i>Educate</i> and <i>educe</i> are near twins: e + duc + ate and e + duce. To educate was first to rear a child; the "
             "sense of leading out what is in the learner is a later reading of the word, and a fair one.",
     "groups": [
         [("educate", ["e-", "duc", "-ate"], "bring up, teach"), ("education", ["e-", "duc", "-at(e)", "-ion"], "bringing up, teaching"),
          ("educator", ["e-", "duc", "-at(e)", "-or"], "one who teaches"),
          ("educational", ["e-", "duc", "-at(e)", "-ion", "-al"], "having to do with teaching")],
     ]},
    {"key": "french", "label": "duke, duch, duit, due", "spells": ["duke", "duch", "duc", "duit", "due"], "head": "a leader; and words worn down in French",
     "road": "Latin <i>dux</i>, a leader, became French <i>duc</i>; and Latin <i>conductus</i> and <i>subd&umacr;cere</i> lost letters on "
             "their way through French",
     "groups": [
         [("duke", ["duke"], "a leader; a noble next below a prince"), ("duchess", ["duch", "-ess"], "a woman of a duke&rsquo;s rank"),
          ("duchy", None, "the land a duke rules", "duch"), ("ducal", ["duc", "-al"], "having to do with a duke")],
         [("conduit", ["con-", "duit"], "a channel that leads water or wires: <i>conduct</i>, through French")],
         [("subdue", ["sub-", "due"], "bring under control; its sense was shaped by another Latin verb, <i>subdere</i>, to put under")],
     ]},
    {"key": "germanic", "label": "tow, tug, tie, team", "spells": ["tow", "tug", "tie", "team"], "head": "pull: English&rsquo;s own words",
     "road": "Old English <i>togian</i>, to pull, and its kin, which English inherited and never borrowed. In the Germanic languages "
             "the root&rsquo;s d became t, so these words start with t where Latin&rsquo;s start with d",
     "note": "<i>Tug</i> and <i>duct</i> are cousins: one came down through Old English, the other was borrowed from Latin. The "
             "same change of d to t sets <i>two</i> beside <i>dual</i> and <i>ten</i> beside <i>decimal</i>.",
     "groups": [
         [("tow", None, "pull along behind", "tow"), ("tug", None, "pull hard", "tug")],
         [("tie", None, "a cord that draws tight; to fasten with one", "tie")],
         [("team", None, "animals pulling together in harness; now any group that works together", "team")],
     ]},
]
PARTS.update({
    "in-": "into, in: Latin <i>in</i>; not the <i>in-</i> that means not",
    "intro-": "to the inside, inward",
    "ad-": "to, toward",
    "con-": "with, together: Latin <i>com-</i>, written <i>con-</i> before d and most other consonants",
    "tra-": "across: Latin <i>trans-</i>, shortened before d",
    "trans-": "across",
    "ab-": "away, from",
    "sub-": "under",
    "mis-": "wrongly, badly",
    "-ile": "able to be",
    "-ity": "the state of being",
    "-ess": "a woman who is: an ending that came through French",
    "aque": "water: Latin <i>aqua</i>, another root",
})
ROOT_PARTS.update({
    "duce": "lead: Latin <i>d&umacr;cere</i>, in its present form",
    "duct": "led: Latin <i>ductus</i>, the past form of <i>d&umacr;cere</i>",
    "duc": "lead, bring up: Latin <i>duc-</i>, in <i>&emacr;duc&amacr;re</i>, to bring up, and <i>dux</i>, <i>ducis</i>, a leader",
    "duke": "a leader: Latin <i>dux</i>, through French <i>duc</i>",
    "duch": "a leader: French <i>duc</i>, with its c softened before the ending",
    "duit": "led: Latin <i>ductus</i>, worn down in French",
    "due": "lead: Latin <i>-d&umacr;cere</i>, worn down in French",
})
DEUK = {
    "slug": "deuk", "root": "*deuk-", "gloss": "to lead, to pull", "kind": "a root family",
    "h1_s": "*deuk- means &lsquo;lead&rsquo;",
    "lead": "To lead, to pull along. Latin made this Proto-Indo-European root into <i>d&umacr;cere</i>, to lead, and with a prefix "
            "in front it says which way: forth, back, in, out, aside, together. English borrowed the verbs with duce and their "
            "nouns with duct, and kept its own words from the same root, <i>tow</i> and <i>tug</i>. The family teaches two things: "
            "why <i>reduce</i> makes <i>reduction</i>, and how stress tells <i>proDUCE</i> from <i>PROduce</i>.",
    "drawn": ("duct", "duct, marked"),
    "sources": [("Indo-European Lexicon, deuk- (Linguistics Research Center, University of Texas at Austin), which follows Pokorny: the list this family is drawn from", "https://lrc.la.utexas.edu/lex/master/0355"),
                ("Etymonline, *deuk-", "https://www.etymonline.com/word/%2Adeuk-"),
                ("Etymonline: <i>produce</i>, verb and noun", "https://www.etymonline.com/search?q=produce"),
                ("Etymonline: <i>educate</i>, from Latin <i>educare</i>", "https://www.etymonline.com/search?q=educate"),
                ("Etymonline: <i>subdue</i>", "https://www.etymonline.com/search?q=subdue"),
                ("Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994), for the long vowel before a final e and the soft c before e: his pages are listed with steps 9 and 10", "../progressions.html")],
    "roads": DEUK_ROADS, "clusters": DEUK_CLUSTERS, "parts": PARTS, "root_parts": ROOT_PARTS,
    "extra": [
        ("stress", "Stress tells the verb from the noun",
         ["<i>Produce</i> is two words with one spelling. The verb is pro<b>DUCE</b>: farms produce food. The noun is "
          "<b>PRO</b>duce: the food itself. <i>Conduct</i> works the same way: to con<b>DUCT</b> a band, but good <b>CON</b>duct. "
          "The verb keeps the stress where Latin had it, on the root. The noun pulls it to the front.",
          "The marks show this only through the first vowel. In the verb the first syllable is said weakly, so its o stays bare. "
          "In the noun it is said in full, so the o takes a mark. The notation has no mark for stress itself yet, so the weak "
          "vowel is the only sign of it. These four markings are drafts, waiting for a ruling.",
          "The pattern runs well beyond this family: <i>record</i>, <i>permit</i>, <i>object</i>, <i>present</i>, <i>contract</i>, "
          "<i>rebel</i>. A learner who knows it can hear which word is meant, and a speller can see why two words that sound "
          "different are written alike: the spelling keeps the parts, pro + duce, and leaves the stress to the speaker."],
         [("produce", "verb: pro<b>DUCE</b>", "c.pr b.o | c.d l.u c.c e> ; nudge 5>4"),
          ("produce", "noun: <b>PRO</b>duce", "c.pr l.o | c.d l.u c.c e> ; vault 3>1 ; nudge 5>4"),
          ("conduct", "verb: con<b>DUCT</b>", "c.c b.o c.n | c.d s.u c.ct"),
          ("conduct", "noun: <b>CON</b>duct", "c.c s.o c.n | c.d s.u c.ct")]),
        ("shift", "An ending can move the stress",
         ["Some suffixes decide where the stress falls. Before <i>-ion</i> it lands on the syllable just ahead of the suffix: "
          "<b>ED</b>ucate becomes edu<b>CA</b>tion, and pro<b>DUCE</b> becomes pro<b>DUC</b>tion. <i>-ity</i> does the same: "
          "pro<b>DUC</b>tive becomes produc<b>TIV</b>ity. When the stress moves, vowels change with it: the long a of educ<b>A</b>tion "
          "is weak in <b>ED</b>ucate&rsquo;s cousin <i>educator</i>, and the spelling stays the same throughout.",
          "This is where spelling by parts earns its keep. The sounds shift from word to word, and the parts don&rsquo;t: "
          "e + duc + ate, e + duc + at(e) + ion, e + duc + at(e) + or."], []),
    ],
    "students": ["produce", "product", "reduce", "conduct", "educate", "duct", "tug"],
    "s_lead": "These words come from one old word that meant <i>lead</i> or <i>pull</i>.",
    "uc": "the word list follows the Indo-European Lexicon, which follows Pokorny. Next: check it against Etymonline&rsquo;s "
          "entry for the root and against Watkins; rule on the draft markings of <i>produce</i> and <i>conduct</i>; and decide "
          "whether the notation needs a stress mark.",
    "label": "Root family: *deuk-",
    "desc": "The root *deuk-, to lead, and its family: produce, reduce, conduct, educate, duke and tug, with why reduce makes reduction and how stress tells proDUCE from PROduce.",
}
ROOTS = [LEG, HAP, DEUK]


def bold_root(word, spelling):
    i = word.find(spelling)
    return html.escape(word) if i < 0 else html.escape(word[:i]) + "<b>" + html.escape(spelling) + "</b>" + html.escape(word[i + len(spelling):])


# ------------------------------------------------------------------ the clusters
def part_key(p): return p.replace("(", "").replace(")", "")          # -ur(e) is the suffix -ure, its e dropped
def part_kind(p, spells):
    if p.endswith("-"): return "pre"
    if p.startswith("-"): return "suf"
    return "root" if p in spells or part_key(p) in spells or part_key(p) + "e" in spells else "base"


def cluster_words(R):
    """Every (cluster, word, parts, meaning, the spelling to bold) on the page, in order."""
    out = []
    for c in R["clusters"]:
        for group in c["groups"]:
            for item in group:
                w, parts, mean = item[:3]
                bold = item[3] if len(item) > 3 else next(p for p in parts if p in c["spells"])
                out.append((c, w, parts, mean, bold))
    return out


def clusters_html(R):
    """The roads in, the drill-down by spelling, and the glossary of parts, with the data the script reads."""
    words = cluster_words(R)
    carriers = {}                                                      # part -> the words that carry it
    for c, w, parts, mean, bold in words:
        for p in parts or []:
            carriers.setdefault(part_key(p), [])
            if w not in carriers[part_key(p)]: carriers[part_key(p)].append(w)
    meaning = lambda k: R["parts"].get(k) or R["root_parts"].get(k)
    missing = [k for k in carriers if not meaning(k)]
    assert not missing, f"parts with no meaning: {missing}"

    counts = {c["key"]: sum(len(g) for g in c["groups"]) for c in R["clusters"]}
    chip = lambda k, label: f'<a class="cchip" href="#c-{k}" data-c="{k}"><b>{label}</b></a>'
    roads = "".join(f'<tr><td>{src}</td><td>{mean}</td><td class="rchips">{"".join(chip(k, l) for k, l in spells)}</td></tr>'
                    for src, mean, spells in R["roads"])
    chips = "".join(f'<a class="cchip" href="#c-{c["key"]}" data-c="{c["key"]}" role="tab" aria-controls="c-{c["key"]}">'
                    f'<b>{c["label"]}</b><span>{counts[c["key"]]} word{"s" if counts[c["key"]] != 1 else ""}</span></a>' for c in R["clusters"])

    def wsum(c, w, parts, mean, bold):
        link = f'<a class="rw" href="{etym(w, R["slug"])}">{bold_root(w, bold)}</a>'
        if not parts:
            return (f'<div class="wsum" id="{doors.word_id(w)}"><span class="sum plainw">{link}</span>'
                    f'<span class="rm">{mean}</span></div>')
        btns = '<span class="pl"> + </span>'.join(
            f'<button type="button" class="part {part_kind(p, c["spells"])}" data-p="{html.escape(part_key(p))}">{html.escape(p.strip("-"))}</button>'
            for p in parts)
        return (f'<div class="wsum" id="{doors.word_id(w)}"><span class="sum">{btns}<span class="to"> &rarr; </span>{link}</span>'
                f'<span class="rm">{mean}</span></div>')

    panels = []
    for c in R["clusters"]:
        groups = "".join('<div class="cgroup">' + "".join(wsum(c, w, p, m, b) for c2, w, p, m, b in words
                                                          if c2 is c and w in [it[0] for it in g]) + "</div>" for g in c["groups"])
        note = f'<p class="cnote">{c["note"]}</p>' if c.get("note") else ""
        panels.append(f'<section class="cpanel" id="c-{c["key"]}" data-c="{c["key"]}" role="tabpanel" aria-labelledby="c-{c["key"]}-h">'
                      f'<h3 id="c-{c["key"]}-h"><b>{c["label"]}</b>: {c["head"]}</h3><p class="rh">{c["road"]}.</p>{note}{groups}</section>')

    def gloss(keys, title):
        rows = "".join(f'<div class="pg" id="p-{re.sub(r"[^a-z]+", "", k)}"><dt>{html.escape(k)}</dt><dd>{meaning(k)}. '
                       f'<span class="pin">In {", ".join(carriers[k])}.</span></dd></div>' for k in keys)
        return f'<div class="pgcol"><h3>{title}</h3><dl class="pgloss">{rows}</dl></div>'
    ordered = list(carriers)
    pre = [k for k in ordered if k.endswith("-")]
    suf = [k for k in ordered if k.startswith("-")]
    base = [k for k in ordered if not k.endswith("-") and not k.startswith("-") and k in R["parts"]]
    roots = [k for k in ordered if k in R["root_parts"]]

    data = {"parts": {k: {"m": meaning(k), "w": v} for k, v in carriers.items()},
            "ids": {w: doors.word_id(w) for c, w, *_ in words}}
    script_data = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""<section class="about t-only" aria-labelledby="rd-h"><div class="wrap">
<h2 id="rd-h">{doors.NUMBER[len(R["roads"])]} roads in</h2>
<p class="sub">The root reached English by {doors.NUMBER[len(R["roads"])].lower()} roads, each with its own spellings: a time-lapse, or a <a href="../definitions.html#def-diachronic">diachronic</a> view. Pick a spelling to see its words.</p>
<div class="roads-wrap"><table class="roads"><thead><tr><th>From</th><th>Meaning</th><th>Spellings in English</th></tr></thead><tbody>{roads}</tbody></table></div>
</div></section>
<section class="about t-only cx" aria-labelledby="fam-h"><div class="wrap">
<h2 id="fam-h">The family, spelling by spelling</h2>
<p class="sub">Each word is written as a <a href="../definitions.html#def-word-sum">word sum</a>: the root&rsquo;s spelling in red, the parts that join it on either side. Tap any part to see what it means and which other words carry it. Each word links to its history in Etymonline.</p>
<nav class="cchips" role="tablist" aria-label="The root&rsquo;s spellings">{chips}</nav>
<div class="cpanels">{"".join(panels)}</div>
<div class="pcard" hidden aria-live="polite"></div>
<script type="application/json" id="cx-data">{script_data}</script>
</div></section>
<section class="about t-only" aria-labelledby="pt-h"><div class="wrap">
<h2 id="pt-h">The parts, and what they mean</h2>
<p class="sub">Every part in the word sums above, with the words that carry it.</p>
<div class="pgcols">{gloss(roots, "The root&rsquo;s spellings")}{gloss(pre, "Before the root")}{gloss(suf, "After the root")}{gloss(base, "Other roots")}</div>
</div></section>
<script>{CX_JS}</script>
"""


CX_JS = """
(function () {
  var cx = document.querySelector('.cx'); if (!cx) return;
  var data = JSON.parse(document.getElementById('cx-data').textContent);
  var panels = [].slice.call(cx.querySelectorAll('.cpanel'));
  var chips = [].slice.call(document.querySelectorAll('.cchip'));
  var card = cx.querySelector('.pcard');
  document.documentElement.classList.add('cx-on');
  function open(key, setHash) {
    if (!panels.some(function (p) { return p.dataset.c === key; })) return;
    panels.forEach(function (p) { p.classList.toggle('on', p.dataset.c === key); });
    chips.forEach(function (c) {
      var on = c.dataset.c === key;
      c.classList.toggle('on', on);
      if (c.getAttribute('role') === 'tab') c.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    card.hidden = true; clearSel();
    if (setHash) history.replaceState(null, '', '#c-' + key);
  }
  function clearSel() { [].forEach.call(cx.querySelectorAll('.part.sel'), function (b) { b.classList.remove('sel'); }); }
  function show(btn) {
    var key = btn.dataset.p, info = data.parts[key]; if (!info) return;
    var row = btn.closest('.wsum');
    var others = info.w.map(function (w) {
      return '<a href="#' + data.ids[w] + '" data-w="' + w + '">' + w + '</a>';
    }).join(', ');
    card.innerHTML = '<p><b>' + key + '</b> ' + info.m + '.</p><p class="pin">In ' + others + '.</p>';
    row.parentNode.insertBefore(card, row.nextSibling);
    card.hidden = false; clearSel();
    [].forEach.call(cx.querySelectorAll('.part'), function (b) { if (b.dataset.p === key) b.classList.add('sel'); });
  }
  function goWord(id, scroll) {
    var el = document.getElementById(id); if (!el || !el.closest('.cpanel')) return false;
    open(el.closest('.cpanel').dataset.c, false);
    [].forEach.call(cx.querySelectorAll('.wsum.hit'), function (r) { r.classList.remove('hit'); });
    el.classList.add('hit');
    if (scroll) el.scrollIntoView({ block: 'center' });
    return true;
  }
  chips.forEach(function (c) {
    c.addEventListener('click', function (e) {
      e.preventDefault(); open(c.dataset.c, true);
      if (!c.closest('.cchips')) cx.scrollIntoView({ block: 'start' });
    });
  });
  cx.addEventListener('click', function (e) {
    var b = e.target.closest('.part'); if (b) { show(b); return; }
    var a = e.target.closest('.pcard a[data-w]');
    if (a) { e.preventDefault(); var id = data.ids[a.dataset.w]; history.replaceState(null, '', '#' + id); goWord(id, true); }
  });
  function fromHash(scroll) {
    var h = decodeURIComponent(location.hash.slice(1));
    if (h.indexOf('c-') === 0 && panels.some(function (p) { return p.dataset.c === h.slice(2); })) { open(h.slice(2), false); return; }
    if (h.indexOf('w-') === 0 && goWord(h, scroll)) return;
    if (!panels.some(function (p) { return p.classList.contains('on'); })) open(panels[0].dataset.c, false);
  }
  window.addEventListener('hashchange', function () { fromHash(true); });
  fromHash(true);
})();
"""


# ------------------------------------------------------------------ the pages
def write(OUT, page, header, footer, X):
    """Each family's page; returns the family's words, their links and the family's label, for the search."""
    (OUT / "roots").mkdir(exist_ok=True)
    found = []
    def drawn_row(items):
        return ('<div class="words rrow">' + "".join(
            f'<figure class="word">{X["svg_of"](it[0], 46, code=it[2] if len(it) > 2 else None, label=f"{it[0]}, marked")}<figcaption>{it[1]}</figcaption></figure>'
            for it in items) + "</div>") if items else ""
    import parts as PT
    sums = PT.collect(X)[0]
    for R in ROOTS:
        if R.get("clusters"):
            middle = clusters_html(R)
            for c, w, *_ in cluster_words(R):
                found.append((w, f"roots/{R['slug']}.html#{doors.word_id(w)}", R["label"]))
            spell_of = {w: bold for c, w, p, m, bold in cluster_words(R)}
        else:
            spell = drawn_row(R["spell_drawn"])
            cards = []
            for lang, head, words in R["branches"]:
                items = []
                for w, parts, sp, mean in words:
                    ws = PT.sum_buttons(sums[w]["parts"], root=R["root"]) if parts and w in sums else ""
                    items.append(f'<li id="{doors.word_id(w)}" data-w="{html.escape(w)}"><a class="rw" href="{etym(w, R["slug"])}">{bold_root(w, sp)}</a>'
                                 + (f'<span class="rs">{ws}</span>' if ws else "") + f'<span class="rm">{mean}</span></li>')
                    found.append((w, f"roots/{R['slug']}.html#{doors.word_id(w)}", R["label"]))
                cards.append(f'<section class="rbranch"><h3>{lang}</h3><p class="rh">{head}</p><ul>{"".join(items)}</ul></section>')
            middle = f"""<section class="about t-only" aria-labelledby="sp-h"><div class="wrap">
<h2 id="sp-h">{R["spell_h"]}</h2>
<p class="sub">{R["spell_sub"]}</p>
{spell}
</div></section>
<section class="about t-only" aria-labelledby="fam-h"><div class="wrap">
<h2 id="fam-h">The family</h2>
<p class="sub">{R["fam_sub"]}</p>
<div class="rbranches">{"".join(cards)}</div>
</div></section>
"""
            spell_of = {w: sp for _, _, words in R["branches"] for w, _, sp, _ in words}
        kids = "".join(f'<li>{bold_root(w, spell_of[w])}</li>' for w in R["students"])
        dw, dl = R["drawn"]
        drawn = X["svg_of"](dw, 58, label=dl)
        extra = "".join(f"""<section class="about t-only" aria-labelledby="{sid}-h"><div class="wrap">
<h2 id="{sid}-h">{head}</h2>
{"".join(f'<p class="sub">{t}</p>' for t in paras)}
{drawn_row(row)}
</div></section>
""" for sid, head, paras, row in R.get("extra", []))
        srcs = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in R["sources"])
        body = f"""{header(1)}
<main class="root-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only">Parts &middot; {R["kind"]}</p>
<h1><span class="t-only">{R["root"]}</span><span class="s-only">{R["h1_s"]}</span></h1>
<p class="lead t-only">{R["lead"]}</p>
<div class="door-word t-only">{drawn}</div>
</div></section>
<section class="about s-only"><div class="wrap">
<p class="s-lead">{R["s_lead"]}</p>
<ul class="rkids">{kids}</ul>
</div></section>
{middle}{extra}<section class="about t-only" aria-labelledby="src-h"><div class="wrap prose">
<h2 id="src-h">Sources</h2>
<ul>{srcs}</ul>
<p>More on these writers and studies is on the <a href="../credits.html">Credits</a> page.</p>
{X["uc"](R["uc"])}
</div></section>
</main>
{"" if R.get("clusters") else PT.pop_js("../")}
{footer(1)}"""
        (OUT / "roots" / f"{R['slug']}.html").write_text(page(f"{R['root']}: {R['gloss']} · Sound and Word Atlas", body, 1, R["desc"]), encoding="utf-8")
    return found
