"""Families in the Parts layer: roots/<slug>.html. The first, the root *leg-, made on 8 November 2026; the second, the
base hap, on 9 November 2026; then three roots on 10 November 2026, each with a lesson attached: *deuk- (duce, duct;
stress), *sem- (simil, semble; prefixes that change to match) and *med- (mod, med; accommodate).

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
    ("Greek <i>legein</i>, <i>logos</i>, <i>lexis</i>", "to say, to gather; a word", [("log", "log"), ("logue", "logue"), ("lex", "lex"), ("lect", "lect"), ("lego", "lego")]),
]

# The clusters, one for each spelling. A word is (word, parts or None, meaning), or with a fourth item, the letters to
# set in bold when it has no parts to show.
CLUSTERS = [
    {"key": "leg", "label": "leg", "spells": ["leg"], "head": "gather, choose, read",
     "road": "Latin <i>legere</i>, to gather, to choose, to read, at the start of a word",
     "note": "<i>Elegant</i> kept the e that <i>eligible</i> turned to i.",
     "groups": [
         [("legend", ["leg", "-end"], "a story to be read"), ("legendary", ["leg", "-end", "-ary"], "told of in legends")],
         [("legible", ["leg", "-ible"], "clear enough to read"), ("illegible", ["il-", "leg", "-ible"], "too unclear to read")],
         [("legion", ["leg", "-ion"], "a body of soldiers, chosen and gathered")],
         [("elegant", ["e-", "leg", "-ant"], "chosen with care, graceful")],
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
         [("elect", ["e-", "lect"], "choose"), ("election", ["e-", "lect", "-ion"], "a choosing by vote"),
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
    {"key": "french", "label": "les, lite", "spells": ["les", "lite"], "head": "worn down in French",
     "road": "Latin words that came into English through French and lost letters on the way. <i>Lectio</i>, a reading, became <i>le&ccedil;on</i>, and <i>eligere</i>, to pick out, gave <i>eslite</i>, chosen",
     "groups": [
         [("lesson", None, "something to read or learn", "les")],
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
     "road": "Greek <i>l&eacute;g&omacr;</i> and Latin <i>leg&omacr;</i>, the verb itself, which both languages inherited from the root. In Greek, I gather, I count, I say; in Latin, I gather, I choose, I read",
     "note": "The <i>&omacr;</i> is the ending for I in both languages. So <i>lego</i> is leg + o, gather + I, as Latin <i>veto</i> is I forbid and <i>credo</i> I believe.",
     "groups": [
         [("legomorphic", ["leg", "-o", "morph", "-ic"], "this notation&rsquo;s name: <i>leg&omacr;</i>, I gather, in Greek "
           "and Latin alike, and <i>morph</i>, form")],
         [("prolegomenon", ["pro-", "leg", "-omenon"], "what is said beforehand: a formal introduction to a study. Greek "
           "<i>prolegein</i>, to say before; more than one are <i>prolegomena</i>. <i>Prologue</i> "
           "is its plainer twin: pro + logue")],
     ]},
]

# Words often listed with the root whose road back to it the sources hedge (12 November 2026). They keep their word sums,
# since the parts hold whatever the history, and stay in search and the word walk; they leave the drill-down, the roads
# and the board. Watkins (AHD, leg-) gives the law branch as "possibly", with a question mark on Latin lex as a
# "collection of rules", and a link to *legh- as possible but uncertain; Etymonline gives lex only as "perhaps";
# legare is built on lex. Latin legumen is of unknown origin (Etymonline).
DEBATED_LEAD = ("Some words are often listed with the root, but the sources call the link uncertain. They keep their word sums here, since the parts are the same whatever the history. Only the link to the root is in doubt.")
LEG_DEBATED = {"lead": DEBATED_LEAD, "clusters": [
    {"key": "law", "label": "leg, legis, loy, lege", "spells": ["leg", "legis", "loy", "lege"], "head": "law",
     "road": "Latin <i>l&emacr;x</i>, law; <i>l&emacr;gis</i>, of law, as in <i>l&emacr;gis l&amacr;tor</i>, a proposer of law",
     "why": "Watkins gives this branch as possible only, with a question mark on law as a &lsquo;collection of rules&rsquo;. "
            "He also names a possible but uncertain link to another root, <i>*legh-</i>, to lie, to lay. On that reading, law is what is laid down, the source of English <i>law</i>. Etymonline gives <i>l&emacr;x</i> only as perhaps from "
            "<i>*leg-</i>.",
     "groups": [
         [("legal", ["leg", "-al"], "to do with the law"), ("illegal", ["il-", "leg", "-al"], "against the law"),
          ("legitimate", None, "allowed by law", "leg")],
         [("legislator", ["legis", "lat", "-or"], "someone who brings in laws"), ("legislation", ["legis", "lat", "-ion"], "laws, and the making of them"),
          ("legislature", ["legis", "lat", "-ure"], "the body that makes laws")],
         [("loyal", ["loy", "-al"], "faithful: Latin <i>l&emacr;g&amacr;lis</i>, legal, worn down in French to <i>loial</i>"),
          ("loyalty", ["loy", "-al", "-ty"], "the quality of being faithful"), ("disloyal", ["dis-", "loy", "-al"], "not faithful")],
         [("privilege", ["privi", "lege"], "a law for one person, a special right")],
     ]},
    {"key": "send", "label": "leg, lege, league", "spells": ["leg", "lege", "league"], "head": "send with a charge",
     "road": "Latin <i>l&emacr;g&amacr;re</i>, to send with a charge, to appoint; <i>coll&emacr;ga</i>, one chosen along with another",
     "why": "<i>L&emacr;g&amacr;re</i> is built on <i>l&emacr;x</i>, law, so these words share its doubt.",
     "groups": [
         [("delegate", ["de-", "leg", "-ate"], "send someone to act for you"),
          ("delegation", ["de-", "leg", "-at(e)", "-ion"], "a group sent to act for others"),
          ("relegate", ["re-", "leg", "-ate"], "send away, move down"),
          ("legacy", ["leg", "-acy"], "what is handed down")],
         [("college", ["col-", "lege"], "a body of people gathered together"), ("colleague", ["col-", "league"], "someone chosen to work alongside you")],
     ]},
    {"key": "legume", "label": "leg", "spells": ["leg"], "head": "a bean or a pea",
     "road": "Latin <i>leg&umacr;men</i>, a pulse: beans, peas and lentils",
     "why": "Latin <i>leg&umacr;men</i> is of unknown origin. That it was named for being picked by hand is one suggestion, "
            "nothing firmer.",
     "groups": [[("legume", ["leg", "-ume"], "a bean or a pea")]]},
]}

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
    "il-": "not, as in <i>illegal</i>; or in, into, as in <i>illuminate</i>: two Latin prefixes spelled <i>in-</i>, both written <i>il-</i> before l",
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
    "-ive": "describes what something does or tends to do: <i>active</i>, <i>productive</i>",
    "-or": "one who, the thing that",
    "-er": "one who does it, or the thing that does (<i>designer</i>, <i>heater</i>); or more (<i>taller</i>)",
    "-ful": "full of, given to",
    "-ure": "the act or result of",
    "-ic": "having to do with",
    "-al": "having to do with",
    "-ent": "describes what something is like or does: Latin&rsquo;s present form of the verb, as in <i>silent</i>, <i>patient</i>",
    "-ence": "names it: makes a noun from a describing word in -ent, as patience from patient",
    "-ible": "able to be",
    "-end": "to be: Latin <i>legendus</i>, to be read",
    "-ary": "having to do with; or a person, thing or place for it: <i>luminary</i>, <i>library</i>",
    "-ant": "describes what something is like or does, as -ent does: <i>pleasant</i>, <i>important</i>",
    "-ume": "a Latin noun ending (<i>leg&umacr;men</i>): a thing",
    "-ate": "makes a doing word: make, do (<i>designate</i>, <i>educate</i>); or a Latin past form, in a describing word (<i>separate</i>)",
    "-acy": "a state, an office",
    "-ty": "the state of being",
    "-y": "having, full of (<i>happy</i>, <i>lucky</i>: Old English <i>-ig</i>); or, in Greek words, a study, an art, a quality (<i>biology</i>, <i>analogy</i>: Greek <i>-ia</i>)",
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

# Legō in Latin and in Greek, a usage definition (20 November 2026). The Latin senses follow the Oxford Latin Dictionary's
# legō² (1968, p. 1014), strung from the hand to the eye; the lines are the poets' own, checked against their texts, and
# the translations are ours. The Greek road follows Homer.
SECTIONS = [("Legō in Latin and in Greek", "roots/leg.html#lego-h", "Parts, *leg-",
             "lego legō legere legein λέγω lectum logos gather choose read count say usage poets Virgil Homer Ovid Oxford Latin Dictionary")]
LEGO_CSS = """<style>
.lusage{display:grid;grid-template-columns:3fr 2fr;gap:22px;margin:18px 0 6px;align-items:start}
.lusage h3{margin:0 0 4px;font-size:1.2rem}
.lusage .lform{margin:0 0 12px;color:var(--soft)}
.lusage ol{list-style:none;margin:0;padding:0 0 0 18px;border-left:3px solid var(--line);display:grid;gap:14px}
.lusage li{position:relative}
.lusage li::before{content:"";position:absolute;left:-26px;top:.45em;width:13px;height:13px;border-radius:50%;background:var(--card);border:3px solid var(--modal,#3f6488)}
.lusage li.lnow::before{background:var(--modal,#3f6488)}
.lusage b{display:block}
.lusage q{display:block;quotes:none;font-style:italic;font-family:var(--display);font-size:1.08rem;margin:4px 0 0}
.lusage .tr{display:block;margin:2px 0 0}
.lusage cite{display:block;font-style:normal;color:var(--soft);font-size:.9rem}
.lusage .lnote{color:var(--soft);font-size:.95rem;margin:4px 0 0}
@media (max-width:760px){.lusage{grid-template-columns:1fr}}
</style>"""
def _lq(lang, line, tr, cite):
    return f'<q lang="{lang}">{line}</q><span class="tr">{tr}</span><cite>{cite}</cite>'
LEGO_USE = LEGO_CSS + '<div class="lusage">' + (
    '<section><h3>Latin <i>leg&omacr;</i>: I gather, I choose, I read</h3>'
    '<p class="lform"><i>leg&omacr;, legere, l&emacr;g&imacr;, lectum</i>. The <i>lect</i> of <i>collect</i> and <i>lecture</i> is the last of these.</p><ol>'
    '<li><b>with the hand: to pick, to pluck</b>'
    + _lq("la", "legit flōrēs", "she gathers flowers", "Ovid, <i>Metamorphoses</i> 4.315") + '</li>'
    '<li><b>with the mouth</b>'
    + _lq("la", "ē foliīs nātōs, ē suāvibus herbīs / ōre legunt", "the bees gather their young from the leaves and the sweet grasses with their mouths",
          "Virgil, <i>Georgics</i> 4.200&ndash;201. Virgil had the bees wrong, but the verb is right") + '</li>'
    '<li><b>the last breath</b>'
    + _lq("la", "extrēmus sī quis super hālitus errat, / ōre legam", "if any last breath still wanders over you, I will gather it with my mouth",
          "Virgil, <i>Aeneid</i> 4.684&ndash;685: Anna to her sister Dido, dying")
    + _lq("la", "spīritus fugiēns meō legātur ōre", "let your fleeing breath be gathered by my mouth",
          "Seneca, <i>Hercules Oetaeus</i> 1342: Alcmena to her son Hercules")
    + '<p class="lnote">Commentators call it a last kindness, like closing the eyes of the dying.</p></li>'
    '<li><b>the bones, after the fire</b>'
    + _lq("la", "quae legat in maestōs ossa perusta sinūs", "a mother to gather my burnt bones into her grieving lap",
          "Tibullus 1.3.6, sick and far from home, with no mother there to do it")
    + _lq("la", "extrēmō quī legat ossa diē", "someone to gather my bones on the last day", "Propertius 2.24.50") + '</li>'
    '<li><b>in a line: sails, ropes, thread</b>'
    + _lq("la", "nauita &hellip; ūmida vēla legit", "the sailor gathers in his wet sails", "Virgil, <i>Georgics</i> 1.373")
    + _lq("la", "extrēmaque Lausō / Parcae fīla legunt", "and the Fates gather in the last threads for Lausus", "Virgil, <i>Aeneid</i> 10.814&ndash;815") + '</li>'
    '<li><b>a path: to follow tracks, to trace a shore</b>'
    + _lq("la", "vestīgia retrō / observāta legit", "he picks up his own footprints, going back the way he came", "Virgil, <i>Aeneid</i> 9.392&ndash;393: Nisus, looking for his friend")
    + _lq("la", "crebrīs legimus freta consita terrīs", "we thread the straits, sown thick with islands", "Virgil, <i>Aeneid</i> 3.127") + '</li>'
    '<li><b>with the eyes and the ears: to pick out</b>'
    + _lq("la", "unde omnīs longō ōrdine posset / adversōs legere", "from where he could pick them all out, face to face, in their long line",
          "Virgil, <i>Aeneid</i> 6.754&ndash;755: Anchises, watching the souls go by")
    + _lq("la", "unde hōrum sermōnem legam", "where I can pick up what they say", "Plautus, <i>Pseudolus</i> 414: listening in") + '</li>'
    '<li><b>to choose</b>Picked out from the rest: <i>select</i>, <i>elect</i>, soldiers enlisted, a senate chosen</li>'
    '<li class="lnow"><b>to read</b>'
    + _lq("la", "nōmen &hellip; in marmore lectum / perfūdit lacrimīs", "she drenched with her tears the name she read on the marble",
          "Ovid, <i>Metamorphoses</i> 2.338: Clymene at her son Phaethon&rsquo;s tomb")
    + _lq("la", "in tōtō plūrimus orbe legor", "all over the world, I am read more than anyone", "Ovid, <i>Tristia</i> 4.10.128, from exile") + '</li>'
    '</ol></section>'
    '<section><h3>Greek <i>leg&omacr;</i>: I gather, I count, I say</h3>'
    '<p class="lform"><i lang="grc">λέγω</i>. Its noun is <i lang="grc">λόγος</i>, <i>logos</i>: a gathering of words, an account, a reason.</p><ol>'
    '<li><b>to gather</b>'
    + _lq("grc", "ὀστέα Πατρόκλοιο Μενοιτιάδαο λέγωμεν", "let us gather the bones of Patroclus, son of Menoetius", "Homer, <i>Iliad</i> 23.239: Achilles")
    + _lq("grc", "ὀστέα λευκὰ λέγοντο", "they gathered the white bones", "Homer, <i>Iliad</i> 24.793: Hector&rsquo;s brothers and friends") + '</li>'
    '<li><b>to count: to gather one by one</b>'
    + _lq("grc", "λέκτο δ’ ἀριθμόν", "he counted their number", "Homer, <i>Odyssey</i> 4.451: Proteus, counting his seals")
    + _lq("grc", "ἐν δ’ ἡμέας πρώτους λέγε κήτεσιν", "he counted us first among the beasts", "<i>Odyssey</i> 4.452: Menelaus and his men, hidden in sealskins") + '</li>'
    '<li><b>to tell over: to lay out a story piece by piece</b>'
    + _lq("grc", "ἴσκε ψεύδεα πολλὰ λέγων ἐτύμοισιν ὁμοῖα", "he told many lies, and made them like the truth", "Homer, <i>Odyssey</i> 19.203: Odysseus, in disguise, to his wife") + '</li>'
    '<li class="lnow"><b>to say</b>In later Greek the everyday word for speaking, and the root of <i>lexicon</i>, <i>logic</i>, <i>dialogue</i> and <i>prologue</i></li>'
    '</ol>'
    '<p class="lnote">One more line in the Odyssey looks the same and isn&rsquo;t: <i lang="grc">ἔπειτα δὲ λέκτο καὶ αὐτός</i>, &ldquo;then he lay down himself&rdquo; '
    '(4.453). That <i>lekto</i> comes from another verb, to lie down, kin to <i>λέχος</i>, a bed. Two lines apart, one form counts the seals and the other goes to sleep among them.</p>'
    '</section>') + '</div>'

LEG = {
    "slug": "leg", "root": "*leg-", "gloss": "to gather, to collect", "kind": "a root family",
    "h1_s": "*leg- means &lsquo;gather&rsquo;",
    "lead": "To gather, to collect. Speakers of Greek and Latin carried this Proto-Indo-European root into words about "
            "words: gathering words is choosing them, reading them and saying them. English borrowed the family back again "
            "and again, and the notation&rsquo;s own name is one of them. <a href=\"#lego-h\">How the poets used leg&omacr;</a>, in Latin and in Greek.",
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
                ("Etymonline, <i>veto</i>: Latin, I forbid", "https://www.etymonline.com/word/veto"),
                ("Calvert Watkins, <i>The American Heritage Dictionary of Indo-European Roots</i>, leg-: the law branch given as possible (a copy of the appendix)", "https://www.proto-indo-european.ru/dic-watkins/ier-l.htm"),
                ("Etymonline, <i>legume</i>: Latin <i>leg&umacr;men</i>, of unknown origin", "https://www.etymonline.com/search?q=legume"),
                ("<i>Oxford Latin Dictionary</i>, ed. P. G. W. Glare (Clarendon Press, 1968&ndash;1982), <i>leg&omacr;</i>&sup2;, p. 1014: the nine senses and the lines for the Latin usage", "../credits.html"),
                ("Dickinson College Commentaries, Virgil&rsquo;s <i>Aeneid</i> 4.642&ndash;705, on <i>&omacr;re legam</i>: catching the last breath", "https://dcc.dickinson.edu/node/4801"),
                ("Dickinson College Commentaries, Homer&rsquo;s <i>Odyssey</i> 4.435&ndash;461: <i>lekto</i>, counted, and <i>lekto</i>, lay down", "https://dcc.dickinson.edu/node/31956"),
                ("Perseus Scaife Viewer, Homer&rsquo;s <i>Iliad</i> 24.793", "https://atlas.perseus.tufts.edu/library/passage/urn:cts:greekLit:tlg0012.tlg001.perseus-grc2:24.793/")],
    "extra": [
        ("lego", "Legō in Latin and in Greek",
         ["Latin and Greek share the form <i>leg&omacr;</i>, I gather, and each gave it a different meaning. In Latin, gathering "
          "turned to picking out, then to choosing and reading; in Greek, to counting, telling over and saying. So in "
          "<i>legomorphic</i> the Greek says &lsquo;I gather forms&rsquo;, and an English reader who knows Latin hears &lsquo;I read forms&rsquo; too.",
          "The Latin column follows the nine senses of <i>leg&omacr;</i> in the <i>Oxford Latin Dictionary</i> (1968), from the hand to the eye. Each has a line where a poet used it. The two languages meet at the funeral pyre: Achilles and "
          "Tibullus use the same verb for gathering the bones of the dead. The translations are ours.",
          "The weak point: a dictionary orders senses by meaning, not by date. Reading is already in Plautus, among the oldest Latin we have, and saying is already in Homer. So the change from gathering to reading and to saying happened before our earliest texts. The order here is a reconstruction, not something the texts let us watch happen."],
         [], LEGO_USE),
    ],
    "roads": ROADS, "clusters": CLUSTERS, "debated": LEG_DEBATED, "parts": PARTS, "root_parts": ROOT_PARTS,
    "students": ["collect", "select", "elect", "lesson", "legend", "logic", "dialogue"],
    "s_lead": "These words come from one old word that meant <i>gather</i>.",
    "uc": "the family follows Etymonline, which draws on Calvert Watkins, and the Indo-European Lexicon, which follows "
          "Pokorny. On 12 November 2026 it was checked against Watkins&rsquo;s entry, and the words he and Etymonline mark as uncertain (the law branch, and <i>legume</i>) moved to Marginal or debated. Next: draw each word in the notation once its "
          "marking is ruled.",
    "label": "Root family: *leg-",
    "desc": "The root *leg-, to gather, to collect, and its family of English words, spelling by spelling, with what each part means.",
}


# ------------------------------------------------------------------ hap
HAP = {
    "slug": "hap", "root": "hap", "gloss": "chance, luck", "kind": "a base family",
    "h1_s": "hap means &lsquo;luck&rsquo;",
    "lead": "Chance, luck. English took <i>hap</i> from Old Norse <i>happ</i> around 1200. It&rsquo;s rarely said on its own now, but it is still in <i>happy</i>, <i>happen</i> and <i>mishap</i>. The Indo-European Lexicon traces it back to a root <i>*kob-</i>, to fit, to fare well. Its spelling shows how it joins: <b>happ</b> "
            "before a vowel, <b>hap</b> everywhere else.",
    "drawn": ("happy", "happy, marked: happ + y"),
    "sources": [("Etymonline: <i>hap</i>, <i>happy</i>, <i>happen</i>, <i>mishap</i>, <i>haphazard</i>, <i>perhaps</i> and the rest", "https://www.etymonline.com/search?q=hap"),
                ("Indo-European Lexicon, kob- (Linguistics Research Center, University of Texas at Austin)", "https://lrc.la.utexas.edu/lex/master/0991"),
                ("Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994): <i>chubby</i>, <i>shabby</i> and "
                 "<i>happy</i>, pp. 1&ndash;3, and the spellings of /p/, p. 16",
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
    "spell_sub": "The p doubles only when a vowel comes next, as the n of <i>fun</i> does in <i>funny</i>. The box keeps the a short (<a href=\"../steps/14.html\">step 14</a>). Before a consonant nothing reaches back, and "
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
            ("happiness", ["happ", "i", "ness"], "happ", "the feeling of being happy"),
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
          "<a href=\"leg.html#w-lesson\"><i>lesson</i></a> double with nothing to join. Carney counts <i>happy</i> among the ordinary doubles, with <i>hobby</i>, <i>silly</i> and <i>merry</i>. He notes that <i>chubby</i> and <i>shabby</i> have a seam inside, but you needn&rsquo;t know it to explain their doubles. What shows the seam is the family: the same hap, with "
          "the same meaning, in <i>hapless</i> and <i>mishap</i>, where nothing doubles. <i>Fun</i> is "
          "<a href=\"../definitions.html#def-free\">free</a>, a word on its own, so the seam in <i>funny</i> is easy to see. <i>Hap</i> is <a href=\"../definitions.html#def-bound\">bound</a> now, so its relatives show the seam: <i>hapless</i> and <i>mishap</i>.",
          "Nor does the double p spell two sounds. Carney lists pp among the spellings of the single sound /p/ (p. 16). The lips close once, at the end of <i>ha</i>, and open once, into the y. The break between the syllables falls inside that one sound, so it seems to belong to both. Daniel Kahn called such a consonant <i>ambisyllabic</i>; "
          "Elisabeth Selkirk put it in the first syllable, as the swoops here do. The puff of breath in <i>pen</i> isn&rsquo;t a second p. English adds it where a p starts a stressed syllable, so <i>appear</i> has it and <i>happy</i> doesn&rsquo;t. Two p sounds meet only where two parts each bring one, as in <i>top pick</i>, and the lips stay shut longer. Joins inside words, such as <i>unnamed</i>, work the same way."], []),
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
          ("reproduction", ["re-", "pro-", "duct", "-ion"], "a making again; a copy")],
         [("reduction", ["re-", "duct", "-ion"], "a making smaller")],
         [("introduction", ["intro-", "duct", "-ion"], "a leading in: a first meeting, an opening part")],
         [("conduct", ["con-", "duct"], "lead together: guide, lead; as a noun, how someone behaves"),
          ("conductor", ["con-", "duct", "-or"], "one who leads; a thing that carries heat or current"),
          ("conduction", ["con-", "duct", "-ion"], "the carrying of heat or current"),
          ("misconduct", ["mis-", "con-", "duct"], "bad behaviour")],
         [("induct", ["in-", "duct"], "lead in: bring into a group"), ("induction", ["in-", "duct", "-ion"], "a leading in; reasoning from cases to a rule"),
          ("inductive", ["in-", "duct", "-ive"], "that reasons from cases to a rule")],
         [("deduct", ["de-", "duct"], "lead away: take off"), ("deduction", ["de-", "duct", "-ion"], "a taking off; or what is deduced"),
          ("deductive", ["de-", "duct", "-ive"], "that reasons from a rule to a case")],
         [("abduct", ["ab-", "duct"], "lead away by force"), ("abduction", ["ab-", "duct", "-ion"], "a taking away by force")],
         [("seduction", ["se-", "duct", "-ion"], "a leading astray"), ("seductive", ["se-", "duct", "-ive"], "tempting")],
     ]},
    {"key": "duc", "label": "duc", "spells": ["duc"], "head": "bring up",
     "road": "Latin <i>&emacr;duc&amacr;re</i>, to bring up, to rear, a verb that stands beside <i>&emacr;d&umacr;cere</i>, to lead out",
     "note": "<i>Educate</i> and <i>educe</i> are closely related: e + duc + ate and e + duce. To educate was first to rear a child. Reading it as leading out what is in the learner came later, and it fits the parts.",
     "groups": [
         [("educate", ["e-", "duc", "-ate"], "bring up, teach"), ("education", ["e-", "duc", "-at(e)", "-ion"], "the bringing up and teaching of the young"),
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
                ("Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994): the long vowel before a final e, and the soft c before e. His pages are listed with steps 9 and 10", "../progressions.html")],
    "roads": DEUK_ROADS, "clusters": DEUK_CLUSTERS, "parts": PARTS, "root_parts": ROOT_PARTS,
    "extra": [
        ("stress", "Stress tells the verb from the noun",
         ["<i>Produce</i> is two words with one spelling. The verb is pro<b>DUCE</b>: farms produce food. The noun is "
          "<b>PRO</b>duce: the food itself. <i>Conduct</i> works the same way: to con<b>DUCT</b> a band, but good <b>CON</b>duct. "
          "The verb keeps the stress where Latin had it, on the root. The noun pulls it to the front.",
          "The marks show this only through the first vowel. In the verb the first syllable is said weakly, so its o stays bare. "
          "In the noun it is said in full, so the o takes a long mark. Nothing sends that o a vault: stress makes it long, and "
          "stress isn&rsquo;t a letter. The notation has no mark for stress itself, so the captions use capitals for it. Among the marks, only the &#601; of a weak vowel shows it.",
          "The pattern runs well beyond this family: <i>record</i>, <i>permit</i>, <i>object</i>, <i>present</i>, <i>contract</i>, "
          "<i>rebel</i>. A learner who knows it can hear which word is meant. A speller can see why two words that sound different are written alike. The spelling keeps the parts, pro + duce, and leaves the stress to the speaker."],
         [("produce", "verb: pro<b>DUCE</b>", "c.pr b.o | c.d l.u c.c e> ; nudge 5>4"),
          ("produce", "noun: <b>PRO</b>duce", "c.pr l.o | c.d l.u c.c e> ; nudge 5>4"),
          ("conduct", "verb: con<b>DUCT</b>", "c.c b.o c.n | c.d s.u c.ct"),
          ("conduct", "noun: <b>CON</b>duct", "c.c s.o c.n | c.d s.u c.ct")]),
        ("shift", "An ending can move the stress",
         ["Some suffixes decide where the stress falls. Before <i>-ion</i> it lands on the syllable just ahead of the suffix: "
          "<b>ED</b>ucate becomes edu<b>CA</b>tion, and pro<b>DUCE</b> becomes pro<b>DUC</b>tion. <i>-ity</i> does the same: "
          "pro<b>DUC</b>tive becomes produc<b>TIV</b>ity. The vowels don&rsquo;t always change with it. The a is long in <b>ED</b>ucate, edu<b>CA</b>tion and <b>ED</b>ucator alike; only the beat moves. The spelling stays the same throughout.",
          "This is where spelling by parts earns its keep. The sounds shift from word to word, and the parts don&rsquo;t: "
          "e + duc + ate, e + duc + at(e) + ion, e + duc + at(e) + or."], []),
    ],
    "students": ["produce", "product", "reduce", "conduct", "educate", "duct", "tug"],
    "s_lead": "These words come from one old word that meant <i>lead</i> or <i>pull</i>.",
    "uc": "the word list follows the Indo-European Lexicon, which follows Pokorny. It was checked on 10 November 2026 against Etymonline&rsquo;s list for the root, read in a copy of that dictionary. Etymonline doesn&rsquo;t list <i>subdue</i> "
          "or <i>educe</i>; the Lexicon does. <i>Product</i>, <i>induct</i> and <i>reproduce</i> are in neither list and are here "
          "as plain kin of <i>produce</i> and <i>induction</i>. The weak vowel took its mark, &#601;, on 21 November 2026. Next: check the list against Watkins, and decide whether stress needs a mark.",
    "label": "Root family: *deuk-",
    "desc": "The root *deuk-, to lead, and its family: produce, reduce, conduct, educate, duke and tug, with why reduce makes reduction and how stress tells proDUCE from PROduce.",
}
ROOTS = [LEG, HAP, DEUK]


# ------------------------------------------------------------------ *sem-
# Made 10 November 2026, for the lesson on assimilation: assimilate is ad + simil + ate, and its own first s is the d of
# ad made like the s after it. The word list follows the Indo-European Lexicon's entry (Pokorny's sem-, one, together),
# fetched that day; simulate and simulation are plain kin of simultaneous and are in Etymonline's list as I recall it,
# which is still to be checked against the entry itself.
SEM_ROADS = [
    ("Latin <i>similis</i>", "like, of the same kind", [("simil", "simil")]),
    ("Latin <i>simul</i>", "at the same time, together", [("simul", "simul"), ("semble", "semble")]),
    ("Latin <i>simplex</i>, <i>singulus</i>", "one-fold; one at a time", [("sim", "sim, sin")]),
    ("Greek <i>homos</i>", "same", [("homo", "homo")]),
    ("Old English and Old Norse", "same, some: words English inherited", [("germanic", "same, some, seem")]),
]
SEM_CLUSTERS = [
    {"key": "simil", "label": "simil", "spells": ["simil"], "head": "like",
     "road": "Latin <i>similis</i>, like, of the same kind",
     "note": "<i>Assimilate</i> does what it says. It is ad + simil + ate, to make like, and the d of <i>ad-</i> was itself made "
             "like the s that follows: as + simil + ate. That is why it has two s&rsquo;s.",
     "groups": [
         [("similar", ["simil", "-ar"], "alike"), ("similarity", ["simil", "-ar", "-ity"], "a likeness"),
          ("dissimilar", ["dis-", "simil", "-ar"], "not alike")],
         [("simile", None, "a likeness drawn in words: as brave as a lion", "simil")],
         [("assimilate", ["as-", "simil", "-ate"], "make like; take in and make part of oneself"),
          ("assimilation", ["as-", "simil", "-at(e)", "-ion"], "a making like: in speech, one sound made like its neighbour")],
     ]},
    {"key": "simul", "label": "simul", "spells": ["simul"], "head": "together, at one time; make like",
     "road": "Latin <i>simul</i>, at the same time, and <i>simul&amacr;re</i>, to make like, to copy",
     "groups": [
         [("simulate", ["simul", "-ate"], "copy, act like"), ("simulation", ["simul", "-at(e)", "-ion"], "a copy that acts like the real thing")],
         [("simultaneous", None, "happening at one time", "simul")],
     ]},
    {"key": "semble", "label": "semble", "spells": ["semble"], "head": "together; like: worn down in French",
     "road": "Latin <i>simul</i> and <i>similis</i>, through French, where the vowels changed and a b grew between the m and the l",
     "note": "<i>Assemble</i> has the same front double as <i>assimilate</i>, for the same reason: ad + semble, written as + semble.",
     "groups": [
         [("assemble", ["as-", "semble"], "bring together"), ("assembly", None, "a gathering; a putting together", "sembl")],
         [("resemble", ["re-", "semble"], "be like"), ("resemblance", ["re-", "sembl(e)", "-ance"], "a likeness", "sembl")],
         [("ensemble", ["en-", "semble"], "all the parts together; a group that plays as one")],
     ]},
    {"key": "sim", "label": "sim, sin", "spells": ["sim", "sin"], "head": "one",
     "road": "Latin <i>simplex</i>, one-fold, and <i>singulus</i>, one at a time",
     "groups": [
         [("simple", ["sim", "ple"], "of one fold: not mixed, not hard"), ("simplicity", ["sim", "plic", "-ity"], "the quality of being simple")],
         [("single", None, "one only", "sin"), ("singular", None, "one of a kind; in grammar, naming one", "sin")],
     ]},
    {"key": "homo", "label": "homo", "spells": ["homo"], "head": "same",
     "road": "Greek <i>homos</i>, same",
     "note": "Three words a teacher of spelling uses. <i>To</i>, <i>two</i> and <i>too</i> are homophones; <i>produce</i> the verb "
             "and <i>produce</i> the noun are <a href=\"deuk.html#stress-h\">homographs</a>.",
     "groups": [
         [("homophone", ["homo", "phone"], "a word with the same sound as another"),
          ("homograph", ["homo", "graph"], "a word written the same as another"),
          ("homonym", ["homo", "nym"], "a word with the same name as another: the same sound, the same spelling, or both")],
     ]},
    {"key": "germanic", "label": "same, some, seem", "spells": ["same", "some", "seem"], "head": "English&rsquo;s inherited words",
     "road": "Old English and Old Norse words from the root, which English inherited and never borrowed",
     "groups": [
         [("same", None, "not another", "same"), ("some", None, "a certain one, a certain amount", "some")],
         [("seem", None, "appear to be: at first, to fit, to be like", "seem")],
     ]},
]
PARTS.update({
    "as-": "to, toward: Latin <i>ad-</i>, written <i>as-</i> before s",
    "en-": "in: French <i>en</i>, from Latin <i>in</i>",
    "-ar": "like, having to do with",
    "-ance": "names it: makes a noun, often from a describing word in -ant, as <i>importance</i> from <i>important</i>",
    "ple": "fold: Latin <i>-plex</i>, another root",
    "plic": "fold: Latin <i>plic&amacr;re</i>, to fold, another root",
    "phone": "sound, voice (Greek <i>ph&omacr;n&emacr;</i>)",
    "graph": "write (Greek <i>graphein</i>)",
    "nym": "name (Greek <i>onyma</i>)",
})
ROOT_PARTS.update({
    "simil": "like: Latin <i>similis</i>",
    "simul": "at one time, together; make like: Latin <i>simul</i>, <i>simul&amacr;re</i>",
    "semble": "together; like: Latin <i>simul</i> and <i>similis</i>, worn down in French",
    "sim": "one: Latin <i>sim-</i>, in <i>simplex</i>, one-fold",
    "homo": "same: Greek <i>homos</i>",
})
SEM = {
    "slug": "sem", "root": "*sem-", "gloss": "one; as one, together", "kind": "a root family",
    "h1_s": "*sem- means &lsquo;one&rsquo; or &lsquo;same&rsquo;",
    "lead": "One; as one, together. From this Proto-Indo-European root Latin made <i>similis</i>, like, and <i>simul</i>, at the "
            "same time; Greek made <i>homos</i>, same; and English kept <i>same</i> and <i>some</i>. The family shows a spelling pattern of its own. <i>Assimilate</i> means to make like, and its double s is a prefix made like its neighbour.",
    "drawn": ("same", "same, marked"),
    "sources": [("Indo-European Lexicon, sem- (Linguistics Research Center, University of Texas at Austin), which follows Pokorny: the list this family is drawn from", "https://lrc.la.utexas.edu/lex/master/1686"),
                ("Etymonline, *sem- (1)", "https://www.etymonline.com/search?q=*sem-"),
                ("Etymonline: <i>assimilate</i>, <i>assemble</i>, <i>accommodate</i>, and the prefixes <i>ad-</i>, <i>com-</i>, <i>in-</i>, <i>sub-</i>, <i>ob-</i>, <i>dis-</i> and <i>ex-</i>, each with the forms it takes", "https://www.etymonline.com/search?q=ad-"),
                ("Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994), on doubled consonants: his pages are listed with step 14", "../steps/14.html")],
    "roads": SEM_ROADS, "clusters": SEM_CLUSTERS, "parts": PARTS, "root_parts": ROOT_PARTS,
    "extra": [
        ("front", "A double at the front of a word",
         ["A double near the end of a word usually marks a suffix joining a short vowel: get + t + ing "
          "(<a href=\"../steps/14.html\">step 14</a>). A double near the front usually marks something else: a Latin prefix whose "
          "last letter changed to match the first letter of the root. Two different consonants in a row take two movements of "
          "the mouth; one held a little longer takes one. Speakers changed the prefix to match the next sound, which is easier to say, and the spelling shows the change.",
          "<b>ad-</b>, to, toward: <i>ac</i>cept, <i>af</i>fix, <i>al</i>lot, <i>ap</i>pear, <i>as</i>semble, <i>at</i>tract. "
          "<b>com-</b>, with: <i>col</i>lect, <i>cor</i>rect, <i>con</i>duct. "
          "<b>in-</b>, not, or into: <i>il</i>legal, <i>im</i>mature, <i>ir</i>regular. "
          "<b>sub-</b>, under: <i>suc</i>ceed, <i>suf</i>fix, <i>sup</i>port. "
          "<b>ob-</b>, against: <i>oc</i>cur, <i>of</i>fer, <i>op</i>pose. "
          "<b>dis-</b>, apart: <i>dif</i>fer. <b>ex-</b>, out: <i>ef</i>fect.",
          "<i>Affix</i> and <i>suffix</i> are themselves examples: ad + fix, fastened to, and sub + fix, fastened under. The "
          "words for word parts were built the way they describe."], []),
        ("accommodate", "Accommodate: two doubles, two joins",
         ["<i>Accommodate</i> is ad + com + mod + ate: to fit one thing to another. The d of <i>ad-</i> became c before the c of "
          "<i>com-</i>, which gives the two c&rsquo;s. Then <i>com-</i> met the m of <i>mod</i>, a measure, which gives the two "
          "m&rsquo;s with no change at all. A speller who knows the parts writes ac + com + mod + ate and has nothing to remember. Its family is "
          "<a href=\"med.html\">*med-</a>, to measure."], []),
        ("test", "A test for the speller",
         ["Take the front off and see what is left. <i>Collect</i> without <i>col</i> leaves <a href=\"leg.html#c-lect\">lect</a>, "
          "which turns up in <i>select</i> and <i>elect</i>: a prefix and a root, so the double belongs. <i>Assemble</i> without "
          "<i>as</i> leaves semble, as in <i>resemble</i>.",
          "Not every front double is a prefix that changed. In <i>unnatural</i>, <i>misspell</i> and <i>dissatisfied</i> nothing "
          "changed: each part brought its own letter, un + natural, mis + spell, dis + satisfied. And some doubles have no join "
          "at all: <i>rabbit</i>, <a href=\"leg.html#w-lesson\"><i>lesson</i></a>. The family is what shows a join, as it does "
          "for <a href=\"hap.html\"><i>happy</i></a>."], []),
    ],
    "students": ["same", "some", "similar", "simple", "single", "assemble", "resemble"],
    "s_lead": "These words come from one old word that meant <i>one</i> or <i>same</i>.",
    "uc": "the word list follows the Indo-European Lexicon, which follows Pokorny. It was checked on 10 November 2026 against Etymonline&rsquo;s list for the root, read in a copy of that dictionary. That list has <i>simulate</i>, <i>simulation</i>, "
          "<i>homophone</i> and <i>homonym</i>. <i>Simile</i> and <i>homograph</i> are in neither list and are here as "
          "plain kin of <i>similar</i> and <i>homophone</i>. Next: check it against Watkins, and decide whether the path needs a "
          "step for prefixes that change to match.",
    "label": "Root family: *sem-",
    "desc": "The root *sem-, one or same, and its family: similar, simple, single, assemble, resemble and same, with a lesson on assimilation: why assimilate, collect and accommodate double at the front.",
}
ROOTS = [LEG, HAP, DEUK, SEM]


# ------------------------------------------------------------------ *med-
# Made 10 November 2026, as the home of accommodate. The word list follows the Indo-European Lexicon's entry
# (Pokorny's med-, to mete, to allot; to heal, to give advice), fetched that day; accommodation is a plain derivative.
MED_ROADS = [
    ("Latin <i>modus</i>", "a measure; a limit; a manner", [("mod", "mod, mode"), ("commod", "mod, after com-"), ("french", "mould")]),
    ("Latin <i>med&emacr;r&imacr;</i>, <i>medit&amacr;r&imacr;</i>", "to heal; to think over", [("med", "med")]),
    ("Old English <i>metan</i>, <i>m&omacr;tan</i>", "to measure; to be allowed", [("germanic", "mete, must")]),
]
MED_CLUSTERS = [
    {"key": "mod", "label": "mod, mode", "spells": ["mod", "mode"], "head": "a measure, a manner",
     "road": "Latin <i>modus</i>, a measure, a limit, a way of doing something",
     "groups": [
         [("mode", ["mode"], "a way of doing something"), ("modal", ["mod(e)", "-al"], "having to do with manner; in grammar, a verb such as <i>can</i> or <i>must</i>", "mod")],
         [("model", None, "a small measure: a pattern to copy", "mod"), ("module", ["mod", "-ule"], "a small measure: a unit that fits with others"),
          ("modulate", ["mod", "-ul(e)", "-ate"], "adjust to a measure")],
         [("moderate", None, "kept within measure", "mod"), ("immoderate", None, "beyond measure", "mod")],
         [("modest", None, "keeping due measure: not boastful", "mod"), ("immodest", None, "not modest", "mod")],
         [("modern", None, "of just now: Latin <i>modo</i>, by the measure, just now", "mod"), ("modicum", None, "a small amount", "mod")],
     ]},
    {"key": "commod", "label": "mod, after com-", "spells": ["mod"], "head": "with due measure: fitting",
     "road": "Latin <i>commodus</i>, com + modus, with measure: fitting, convenient",
     "note": "Com + mod doubles the m with nothing changed: each part brings its own. Put <i>ad-</i> in front and its d turns to c "
             "before the c of com: ac + com + mod + ate.",
     "groups": [
         [("accommodate", ["ac-", "com-", "mod", "-ate"], "fit one thing to another; make room for"),
          ("accommodation", ["ac-", "com-", "mod", "-at(e)", "-ion"], "a fitting in; a place to stay")],
         [("commodity", ["com-", "mod", "-ity"], "a useful thing; a thing bought and sold"),
          ("commodious", ["com-", "mod", "-ious"], "roomy"), ("commode", ["com-", "mode"], "a fitting piece of furniture", "mod")],
     ]},
    {"key": "med", "label": "med", "spells": ["med"], "head": "heal; think over",
     "road": "Latin <i>med&emacr;r&imacr;</i>, to heal, to take the right measures for, and <i>medit&amacr;r&imacr;</i>, to think over",
     "groups": [
         [("medical", ["med", "-ic", "-al"], "having to do with healing"), ("medicate", ["med", "-ic", "-ate"], "treat with medicine"),
          ("medicine", None, "the art of healing; what heals", "med")],
         [("remedy", None, "a cure: what heals again", "med")],
         [("meditate", None, "think over", "med")],
     ]},
    {"key": "french", "label": "mould", "spells": ["mould"], "head": "a shape to measure by",
     "road": "Latin <i>modulus</i>, a small measure, worn down in French",
     "groups": [[("mould", None, "a hollow shape that gives its form to what is poured in; <i>mold</i> in American spelling", "mould")]],
    },
    {"key": "germanic", "label": "mete, must", "spells": ["mete", "must"], "head": "measure; be allowed: English&rsquo;s own words",
     "road": "Old English <i>metan</i>, to measure, and <i>m&omacr;tan</i>, to be allowed, to have room to",
     "note": "<i>Must</i> is on the path as an <a href=\"../constructions.html\">operator</a>. It began as the past form of a verb for "
             "being allowed, for having the measure of time or room to do a thing.",
     "groups": [[("mete", None, "measure out, as in <i>mete out</i>", "mete"), ("must", None, "have to: at first, was allowed to", "must")]],
    },
]
PARTS.update({
    "ac-": "to, toward: Latin <i>ad-</i>, written <i>ac-</i> before c",
    "com-": "with, together",
    "-ule": "small",
    "-ious": "full of, having",
})
ROOT_PARTS.update({
    "mod": "a measure, a manner: Latin <i>modus</i>",
    "mode": "a measure, a manner: Latin <i>modus</i>",
    "med": "heal; think over: Latin <i>med&emacr;r&imacr;</i>, <i>medit&amacr;r&imacr;</i>",
})
MED = {
    "slug": "med", "root": "*med-", "gloss": "to take the right measure", "kind": "a root family",
    "h1_s": "*med- means &lsquo;measure&rsquo;",
    "lead": "To take the right measure. Latin made this Proto-Indo-European root into <i>modus</i>, a measure or a manner. It also made verbs for healing and for thinking something over: measures of another kind. English kept <i>mete</i> and "
            "<i>must</i> from the same root. <i>Accommodate</i>, a word people find hard to spell, is in this family. Its parts explain its spelling.",
    "drawn": ("mode", "mode, marked"),
    "sources": [("Indo-European Lexicon, med- (Linguistics Research Center, University of Texas at Austin), which follows Pokorny: the list this family is drawn from", "https://lrc.la.utexas.edu/lex/master/1238"),
                ("Etymonline, *med-, read on its page for <i>modus</i>", "https://www.etymonline.com/word/modus"),
                ("Etymonline: <i>accommodate</i>, from Latin <i>ad</i> + <i>commodare</i>", "https://www.etymonline.com/search?q=accommodate"),
                ("Etymonline: <i>must</i>", "https://www.etymonline.com/search?q=must")],
    "roads": MED_ROADS, "clusters": MED_CLUSTERS, "parts": PARTS, "root_parts": ROOT_PARTS,
    "extra": [
        ("accommodate", "Accommodate: two doubles, two joins",
         ["<i>Accommodate</i> is ad + com + mod + ate: to fit one thing to the measure of another. It has two doubles, and "
          "they aren&rsquo;t the same kind.",
          "The two c&rsquo;s are a prefix that changed. The d of <i>ad-</i> became c before the c of <i>com-</i>, as it does in "
          "<i>accept</i> and <i>accuse</i>. The two m&rsquo;s are two parts meeting: <i>com-</i> ends in m and <i>mod</i> begins "
          "with one, and nothing changed. A speller who writes the parts, ac + com + mod + ate, has no letters to count.",
          "More on prefixes that change to match is with <a href=\"sem.html#front-h\"><i>assimilate</i></a>, whose own spelling "
          "shows it."], []),
    ],
    "students": ["mode", "model", "modern", "medicine", "remedy", "must", "accommodate"],
    "s_lead": "These words come from one old word that meant <i>measure</i>.",
    "uc": "the word list follows the Indo-European Lexicon, which follows Pokorny. It was checked on 10 November 2026 against Etymonline&rsquo;s list for the root, which has every word here. Next: check it against Watkins.",
    "label": "Root family: *med-",
    "desc": "The root *med-, to take the right measure, and its family: mode, model, modern, medicine, must and accommodate, with why accommodate has two c's and two m's.",
}
ROOTS = [LEG, HAP, DEUK, SEM, MED]


# ------------------------------------------------------------------ *leuk-
# Made 12 November 2026, as the home of illustrate. The word list follows the Indo-European Lexicon's entry (Pokorny's
# leuk-, to light, shine; see), fetched that day, and was checked against Etymonline's list for the root. Etymonline
# lists illustration and illumination (the verbs are their stems). Lynx, which Etymonline gives only as probable, is
# under Marginal or debated (12 November 2026). Illustrate is drawn as Dante ruled that day: il + lustr + ate, the seams
# at the joins of the parts, the syllables il | lus | trate crossing them.
LEUK_ROADS = [
    ("Latin <i>l&umacr;str&amacr;re</i>", "to make bright, to light up", [("lustr", "lustr, lustre")]),
    ("Latin <i>l&umacr;men</i>", "a light", [("lumin", "lumen, lumin")]),
    ("Latin <i>l&umacr;x</i>, <i>l&umacr;c&emacr;re</i>", "light; to shine", [("luc", "luc, lux")]),
    ("Latin <i>l&umacr;na</i>", "the moon: the bright one", [("lun", "lun")]),
    ("Greek <i>leukos</i>", "white, bright", [("greek", "leuk")]),
    ("Old English <i>l&emacr;oht</i>", "light", [("germanic", "light")]),
]
LEUK_CLUSTERS = [
    {"key": "lustr", "label": "lustr, lustre", "spells": ["lustr", "lustre"], "head": "make bright; a shine",
     "road": "Latin <i>l&umacr;str&amacr;re</i>, to make bright, to light up, joined in <i>ill&umacr;str&amacr;re</i> to <i>in-</i>, in, on",
     "note": "To illustrate is to throw light on a thing. It meant that before it meant pictures. First it meant to make bright or famous, then to make clear by examples, and only later to add pictures to a book.",
     "groups": [
         [("illustrate", ["il-", "lustr", "-ate"], "throw light on: make clear, by an example or a picture"),
          ("illustration", ["il-", "lustr", "-at(e)", "-ion"], "an example or a picture that makes something clear"),
          ("illustrative", ["il-", "lustr", "-at(e)", "-ive"], "serving to make clear")],
         [("illustrious", ["il-", "lustr", "-ious"], "shining: famous for what one has done")],
         [("lustre", None, "a soft shine; <i>luster</i> in American spelling", "lustre"),
          ("lacklustre", ["lack", "lustre"], "without shine: dull")],
     ]},
    {"key": "lumin", "label": "lumen, lumin", "spells": ["lumen", "lumin"], "head": "a light",
     "road": "Latin <i>l&umacr;men</i>, a light; <i>l&umacr;minis</i>, of a light",
     "note": "Latin wrote <i>lumen</i> on its own and <i>lumin-</i> with an ending after it, as English does: lumen, but "
             "lumin + ous.",
     "groups": [
         [("illuminate", ["il-", "lumin", "-ate"], "light up; make clear"),
          ("illumination", ["il-", "lumin", "-at(e)", "-ion"], "a lighting up")],
         [("luminous", ["lumin", "-ous"], "giving off light"), ("luminary", ["lumin", "-ary"], "a body that gives light; a person who lights the way")],
         [("lumen", ["lumen"], "a measure of light: what a bulb&rsquo;s box counts")],
     ]},
    {"key": "luc", "label": "luc, lux", "spells": ["luc", "lux"], "head": "light; shine",
     "road": "Latin <i>l&umacr;x</i>, light, <i>l&umacr;cis</i>, of light, and <i>l&umacr;c&emacr;re</i>, to shine",
     "note": "<i>Lux</i> is luc + s. The x spells the c and the s together, so the c doesn&rsquo;t show. Take the s away and the c "
             "comes back: <i>lucid</i>, <i>lucent</i>.",
     "groups": [
         [("lucid", ["luc", "-id"], "clear: easy to understand"),
          ("elucidate", ["e-", "luc", "-id", "-ate"], "make clear: bring out into the light")],
         [("lucent", ["luc", "-ent"], "shining"), ("translucent", ["trans-", "luc", "-ent"], "letting light through, but not clear like glass")],
         [("pellucid", ["pel-", "luc", "-id"], "clear right through")],
         [("lux", ["lux"], "a measure of the light falling on a surface")],
     ]},
    {"key": "lun", "label": "lun, lune", "spells": ["lun", "lune", "lun(e)"], "head": "the moon",
     "road": "Latin <i>l&umacr;na</i>, the moon, from an older <i>*leuksn&amacr;</i>: the bright one",
     "groups": [[("lune", ["lune"], "a crescent, the shape of a new moon"), ("lunar", ["lun(e)", "-ar"], "having to do with the moon")]]},
    {"key": "greek", "label": "leuk", "spells": ["leuk", "leuko"], "head": "white, bright",
     "road": "Greek <i>leukos</i>, white, bright",
     "groups": [
         [("leukemia", ["leuk", "-emia"], "a cancer of the blood, named for its white cells; <i>leukaemia</i> in British spelling"),
          ("leukocyte", ["leuko", "cyte"], "a white blood cell")],
     ]},
    {"key": "germanic", "label": "light", "spells": ["light"], "head": "light: English&rsquo;s own word",
     "road": "Old English <i>l&emacr;oht</i>, light",
     "note": "Not every <i>light</i> is this root&rsquo;s. See <a href=\"#two-h\">Two lights</a>.",
     "groups": [
         [("light", ["light"], "brightness: what lets us see"), ("lighten", ["light", "-en"], "make brighter")],
         [("lightning", None, "a flash of light in a storm: once <i>lightening</i>", "light")],
     ]},
]
PARTS.update({
    "pel-": "through: Latin <i>per-</i>, written <i>pel-</i> before l",
    "lack": "be without: an English word",
    "-ous": "full of, having",
    "-id": "having the quality of: Latin <i>-idus</i>",
    "-emia": "a condition of the blood (Greek <i>haima</i>, blood)",
    "cyte": "a cell (Greek <i>kytos</i>, a hollow)",
    "-en": "make or become (<i>lighten</i>); or a past form (<i>taken</i>)",
})
ROOT_PARTS.update({
    "lustr": "make bright: Latin <i>l&umacr;str&amacr;re</i>",
    "lustre": "a shine: Latin <i>l&umacr;str&amacr;re</i>, through French",
    "lumin": "a light: Latin <i>l&umacr;men</i>, <i>l&umacr;minis</i>",
    "lumen": "a light: Latin <i>l&umacr;men</i>",
    "luc": "light, shine: Latin <i>l&umacr;x</i>, <i>l&umacr;cis</i>, <i>l&umacr;c&emacr;re</i>",
    "lux": "light: Latin <i>l&umacr;x</i>",
    "lun": "the moon: Latin <i>l&umacr;na</i>",
    "lune": "the moon: Latin <i>l&umacr;na</i>, through French <i>lune</i>",
    "leuk": "white: Greek <i>leukos</i>",
    "leuko": "white: Greek <i>leukos</i>",
    "light": "light: Old English <i>l&emacr;oht</i>",
})
LEUK_DEBATED = {"lead": DEBATED_LEAD, "clusters": [
    {"key": "lynx", "label": "lynx", "spells": ["lynx"], "head": "a wild cat", "road": "Greek <i>lynx</i>, through Latin",
     "why": "The Indo-European Lexicon lists <i>lynx</i> with the root. Etymonline leaves it off its list for the root. Its entry for the word gives the link only as probable: the cat named for its sharp sight.",
     "groups": [[("lynx", None, "a wild cat with sharp eyes", "lynx")]]},
]}
LEUK = {
    "slug": "leuk", "root": "*leuk-", "gloss": "light, brightness", "kind": "a root family",
    "h1_s": "*leuk- means &lsquo;light&rsquo;",
    "lead": "Light, brightness: to shine. Latin made this Proto-Indo-European root into <i>l&umacr;x</i>, light, and <i>l&umacr;c&emacr;re</i>, to shine. It also made <i>l&umacr;men</i>, a light; <i>l&umacr;str&amacr;re</i>, to make bright; and <i>l&umacr;na</i>, the moon, the bright one. Greek made it <i>leukos</i>, white. English kept "
            "<i>light</i>. <i>Illustrate</i> is in this family: to throw light on a thing, by an example or a picture.",
    "drawn": ("illustrate", "illustrate, marked: il + lustr + ate"),
    "sources": [("Indo-European Lexicon, leuk- (Linguistics Research Center, University of Texas at Austin), which follows Pokorny: the list this family is drawn from", "https://lrc.la.utexas.edu/lex/master/1197"),
                ("Etymonline, *leuk-: the root&rsquo;s list, which has illustration, illumination and every word here", "https://www.etymonline.com/word/*leuk-"),
                ("Etymonline: <i>illustrate</i>, from Latin <i>ill&umacr;str&amacr;re</i>, in- + <i>l&umacr;str&amacr;re</i>", "https://www.etymonline.com/search?q=illustrate"),
                ("Etymonline: <i>illuminate</i>, from Latin in- + <i>l&umacr;men</i>", "https://www.etymonline.com/word/Illuminate"),
                ("Etymonline, *legwh-: the root of <i>light</i>, not heavy, and of <i>lung</i>", "https://www.etymonline.com/word/*legwh-")],
    "roads": LEUK_ROADS, "clusters": LEUK_CLUSTERS, "debated": LEUK_DEBATED, "parts": PARTS, "root_parts": ROOT_PARTS,
    "extra": [
        ("il", "Il-: in- before l",
         ["Why two l&rsquo;s in <i>illustrate</i>? The first belongs to the prefix. Latin <i>in-</i> became <i>il-</i> before "
          "the l of <i>lustr</i> and <i>lumin</i>, as it does before <i>legal</i>. Each part brings its own l: il + lustr + ate, "
          "il + lumin + ate.",
          "Here <i>in-</i> means in, into: to put light into a thing. In <i>illegal</i> it means not. They are two Latin "
          "prefixes spelled alike, and both are written <i>il-</i> before l. <i>Pellucid</i> does the same with "
          "<i>per-</i>, through: pel + luc + id.",
          "More on prefixes that change to match is with <a href=\"sem.html#front-h\"><i>assimilate</i></a>."], []),
        ("lux", "The c inside lux",
         ["<i>Lux</i>, light, ends in x, and x spells two sounds, /k/ and /s/. In Latin those were the c of the root and an "
          "ending s: luc + s. Wherever the s isn&rsquo;t there, the c shows again: <i>lucid</i>, <i>lucent</i>, "
          "<i>translucent</i>, <i>elucidate</i>. A speller who knows the root is <i>luc</i> knows why those words have a c "
          "and not a k or an s."], []),
        ("two", "Two lights",
         ["English has two words spelled <i>light</i>. One is this root&rsquo;s: brightness, a lamp, to light a fire. The "
          "other means not heavy, and it comes from another root, <i>*legwh-</i>, which also gave <i>lung</i>, the light "
          "organ. They met in the same spelling by chance.",
          "So <i>lighten</i> is two words as well: to make brighter, and to make less heavy. The sentence says which. The "
          "word sum is the same, light + en, because each <i>light</i> is a base in its own right."], []),
    ],
    "students": ["light", "lighten", "lunar", "lucid", "translucent", "illuminate", "illustrate", "illustration"],
    "s_lead": "These words come from one old word that meant <i>light</i>.",
    "uc": "the word list follows the Indo-European Lexicon, which follows Pokorny. It was checked on 12 November 2026 against Etymonline&rsquo;s list for the root, which has every word here or the word it&rsquo;s made from. <i>Lynx</i>, "
          "which Etymonline gives only as probable, is under Marginal or debated. Next: check it against Watkins.",
    "label": "Root family: *leuk-",
    "desc": "The root *leuk-, light, and its family: illustrate, illuminate, lucid, translucent, lunar and light, with why illustrate has two l's and lucid has a c.",
}
ROOTS = [LEG, HAP, DEUK, SEM, MED, LEUK]


# ------------------------------------------------------------------ *per-
# Made 19 November 2026, as a word study of experiment and experience. The word list follows the Indo-European Lexicon's
# entry (Pokorny's per- 2e, to dare, to risk, to try), fetched that day: fear, experience, experiment, expert, peril,
# perilous, parlous, empiric, pirate. Etymonline's own pages weren't reachable that day. The Middle English Dictionary's
# entry for experiment was. The marks (data/family_codes.json) follow very (per, closed: a short e) and here (pe, open: a
# long e with the vault), and the pair's two syllable breaks are the page's lesson.
PER_ROADS = [
    ("Latin <i>exper&imacr;r&imacr;</i>", "to try out, to put to the test", [("peri", "peri"), ("pert", "pert")]),
    ("Latin <i>per&imacr;culum</i>", "a trial; a danger", [("peril", "peril, parl")]),
    ("Greek <i>peira</i>, <i>peir&amacr;n</i>", "a trial; to try, to attack", [("pir", "pir")]),
    ("Old English <i>f&aelig;r</i>", "a danger, a sudden attack: a word English inherited", [("fear", "fear")]),
]
PER_CLUSTERS = [
    {"key": "peri", "label": "peri", "spells": ["peri"], "head": "try, test",
     "road": "Latin <i>exper&imacr;r&imacr;</i>, to try out: ex- and the verb&rsquo;s stem, <i>per&imacr;-</i>",
     "note": "The i is the stem&rsquo;s own vowel, and it stays in every word. It also decides how the e before it sounds: see "
             "<a href=\"#break-h\">Short e, long e</a>.",
     "groups": [
         [("experiment", ["ex-", "peri", "-ment"], "a test you set up, to find something out"),
          ("experimental", ["ex-", "peri", "-ment", "-al"], "done as a test; new and untried"),
          ("experimentation", ["ex-", "peri", "-ment", "-ation"], "the work of testing")],
         [("experience", ["ex-", "peri", "-ence"], "what you learn by living through things"),
          ("experienced", ["ex-", "peri", "-enc(e)", "-ed"], "having lived through it, and learned"),
          ("experiential", ["ex-", "peri", "-ent", "-ial"], "learned by doing: the c of -ence is a t again")],
     ]},
    {"key": "pert", "label": "pert", "spells": ["pert"], "head": "tried, tested",
     "road": "Latin <i>expertus</i>, tried, tested: the past form of <i>exper&imacr;r&imacr;</i>",
     "note": "An expert is someone who has been tried: the word is the Latin past form, as <i>collect</i> is from <i>lectus</i>.",
     "groups": [
         [("expert", ["ex-", "pert"], "someone tried and found skilled"), ("expertise", ["ex-", "pert", "-ise"], "the skill of an expert")],
     ]},
    {"key": "peril", "label": "peril, parl", "spells": ["peril", "parl"], "head": "a trial; a danger",
     "road": "Latin <i>per&imacr;culum</i>, a trial, a danger, worn down in French",
     "note": "<i>Parlous</i> is <i>perilous</i> worn down in speech: an old word for risky, still heard in a parlous state of affairs.",
     "groups": [
         [("peril", None, "danger", "peril"), ("perilous", ["peril", "-ous"], "full of danger"),
          ("parlous", None, "risky, dangerous: <i>perilous</i>, worn down", "parl")],
     ]},
    {"key": "pir", "label": "pir", "spells": ["pir"], "head": "a trial; to try",
     "road": "Greek <i>peira</i>, a trial, and <i>peir&amacr;n</i>, to try, to attack, through Latin, which wrote Greek&rsquo;s ei as i",
     "note": "<i>Pirate</i> and <i>empirical</i> keep the same i, and the path&rsquo;s first idea sorts its sound: <i>pi</i> is "
             "open and long, <i>pir</i> is closed and short.",
     "groups": [
         [("empirical", ["em-", "pir", "-ic", "-al"], "known by trying and looking, not from theory")],
         [("pirate", None, "one who attacks ships: in Greek, one who tries an attack", "pir")],
     ]},
    {"key": "fear", "label": "fear", "spells": ["fear"], "head": "danger, and the feeling it brings",
     "road": "Old English <i>f&aelig;r</i>, a danger, a sudden attack. English inherited it and never borrowed it",
     "groups": [
         [("fear", None, "the feeling that danger is near", "fear"), ("fearful", ["fear", "-ful"], "full of fear")],
     ]},
]
PARTS.update({
    "ex-": "out; or thoroughly: Latin <i>ex</i>",
    "-ment": "the act, the means or the result of: Latin <i>-mentum</i>",
    "-ation": "the act or process of",
    "-ial": "having to do with",
    "-ise": "the state or skill of: French <i>-ise</i>",
    "-ed": "already happened (<i>jumped</i>); or describing what was done (<i>experienced</i>)",
    "em-": "in: Greek <i>en</i>, written <i>em-</i> before p",
})
ROOT_PARTS.update({
    "peri": "try, test: Latin <i>exper&imacr;r&imacr;</i>, to try out",
    "pert": "tried, tested: Latin <i>expertus</i>",
    "peril": "a trial, a danger: Latin <i>per&imacr;culum</i>, worn down in French",
    "pir": "a trial; to try: Greek <i>peira</i>",
    "fear": "a danger; the feeling it brings: Old English <i>f&aelig;r</i>",
})
SWALK = [   # the stress walk: (word, [(syllable, 1 main stress | 2 a lighter stress | 0 weak)], what changed)
    ("experiment", [("ex", 0), ("per", 1), ("i", 0), ("ment", 0)], "the noun: <i>per</i> takes the stress, and its e is short"),
    ("experimental", [("ex", 0), ("per", 2), ("i", 0), ("men", 1), ("tal", 0)], "the stress walks to <i>men</i>, and its weak e comes back full"),
    ("experimentation", [("ex", 0), ("per", 2), ("i", 0), ("men", 0), ("ta", 1), ("tion", 0)], "on again, to <i>ta</i>: <i>men</i> goes weak, and the t spells sh before <i>-ion</i>"),
    ("experience", [("ex", 0), ("pe", 1), ("ri", 0), ("ence", 0)], "<i>pe</i> takes the stress, and its e is long"),
    ("experiential", [("ex", 0), ("pe", 2), ("ri", 0), ("en", 1), ("tial", 0)], "the stress walks to <i>en</i>, the c is a t, and the t spells sh"),
    ("expert", [("ex", 1), ("pert", 0)], "the stress sits on the prefix, and <i>per</i> is an r unit, as in <i>her</i>"),
    ("expertise", [("ex", 2), ("per", 0), ("tise", 1)], "a French ending takes the stress, and keeps its French sound"),
]
SWALK_CSS = """<style>
.swalk{display:grid;gap:10px;margin:18px 0 6px}
.swalk .pwr{display:grid;grid-template-columns:minmax(9rem,max-content) 1fr;gap:4px 18px;align-items:end;padding:10px 14px;border:1px solid var(--line);border-radius:12px;background:var(--card)}
.swalk .pws{display:flex;align-items:flex-end;gap:2px;font-family:var(--display);line-height:1}
.swalk .pws span{padding:0 1px}
.swalk .pw0{font-size:1.15rem;color:var(--soft)}
.swalk .pw2{font-size:1.55rem;color:var(--ink)}
.swalk .pw1{font-size:2.2rem;color:var(--verb,#b5402f);font-weight:600;transform:translateY(-6px)}
.swalk .pwr p{grid-column:1/-1;margin:0;color:var(--soft);font-size:.95rem}
.swalk .pwd{color:var(--line);font-size:1.1rem}
.pwkey{color:var(--soft);font-size:.92rem;margin:0}
.ptime{list-style:none;margin:16px 0 4px;padding:0 0 0 18px;border-left:3px solid var(--line);display:grid;gap:14px}
.ptime li{position:relative}
.ptime li::before{content:"";position:absolute;left:-26px;top:.45em;width:13px;height:13px;border-radius:50%;background:var(--card);border:3px solid var(--modal,#3f6488)}
.ptime b{display:block}
.ptime .now::before{background:var(--modal,#3f6488)}
@media (max-width:560px){.swalk .pwr{grid-template-columns:1fr}}
</style>"""
def _swalk():
    rows = []
    for w, sy, why in SWALK:
        parts = '<span class="pwd">&middot;</span>'.join(f'<span class="pw{k}">{s}</span>' for s, k in sy)
        aria = "-".join(s.upper() if k == 1 else s for s, k in sy)
        rows.append(f'<div class="pwr"><span class="pww"><b>{w}</b></span><span class="pws" role="img" aria-label="{aria}">{parts}</span><p>{why}</p></div>')
    return (SWALK_CSS + '<div class="swalk">' + "".join(rows) + '</div><p class="pwkey">Large and red: the main stress. '
            'Middle: a lighter stress. Small and grey: weak, where the vowel is said quickly, often as the sound in the a of <i>about</i>.</p>')
PER_TIME = ('<ol class="ptime">'
    '<li><b>Proto-Indo-European <i>*per-</i></b>to try, to risk</li>'
    '<li><b>Latin <i>exper&imacr;r&imacr;</i>, to try out</b>One verb, three words from it. <i>Exper&imacr;mentum</i>, a trial or a proof; '
    '<i>experientia</i>, a trying, and the knowing that comes of it; <i>expertus</i>, tried</li>'
    '<li><b>French, then English, in the 1300s</b><i>Experiment</i> and <i>experience</i> arrive meaning nearly the same thing: a trial, '
    'a proof, what trying shows. The Middle English Dictionary&rsquo;s <i>experiment</i> is a test, a proof, even a tried remedy for an illness</li>'
    '<li><b>English since</b>The two drift apart. An <i>experiment</i> becomes the test you set up; <i>experience</i>, what you have lived through</li>'
    '<li class="now"><b>French today</b>Still one word. <i>Exp&eacute;rience</i> means both, and a French science class does <i>une exp&eacute;rience</i></li>'
    '</ol>')
PER = {
    "slug": "per", "root": "*per-", "gloss": "to try, to risk", "kind": "a root family: a word study",
    "h1_s": "*per- means &lsquo;try&rsquo; or &lsquo;risk&rsquo;",
    "lead": "To try, to risk. From this Proto-Indo-European root Latin made <i>exper&imacr;r&imacr;</i>, to try out, with <i>expertus</i>, tried, and <i>per&imacr;culum</i>, a trial or a danger. Greek made <i>peira</i>, a trial, and English kept <i>fear</i>. "
            "At the centre of the family are two words that began as one, <i>experiment</i> and <i>experience</i>. They have the same spelling up to the i and two different sounds for the e; the history explains both.",
    "drawn": ("experience", "experience, marked: ex + peri + ence, with the vault that makes the e long"),
    "sources": [("Indo-European Lexicon, per- 2e (Linguistics Research Center, University of Texas at Austin), which follows Pokorny: the list this family is drawn from", "https://lrc.la.utexas.edu/lex/master/1493"),
                ("Middle English Dictionary, <i>experiment</i> (n.): a test, a proof, a remedy, a feat", "https://quod.lib.umich.edu/m/middle-english-dictionary/dictionary/MED14948"),
                ("Etymonline: <i>experiment</i>, <i>experience</i>, <i>expert</i>, <i>peril</i>, <i>empirical</i>, <i>pirate</i> and <i>fear</i>, each with its history", "https://www.etymonline.com/search?q=experiment"),
                ("Noam Chomsky and Morris Halle, <i>The Sound Pattern of English</i> (Harper &amp; Row, 1968). On vowels shortening three syllables from the end, and lengthening before i and a vowel", "../credits.html"),
                ("Geoffrey Chaucer, the Wife of Bath&rsquo;s Prologue, which opens on <i>experience</i> against the authority of books", "https://www.etymonline.com/search?q=experience")],
    "roads": PER_ROADS, "clusters": PER_CLUSTERS, "parts": PARTS, "root_parts": ROOT_PARTS,
    "extra": [
        ("one", "Two words that were one",
         ["Latin had one verb, <i>exper&imacr;r&imacr;</i>, to try out, and made nouns from it that English took twice. Here is the "
          "time-lapse, the <a href=\"../definitions.html#def-diachronic\">diachronic</a> view:"],
         [("experiment", "the test you set up"), ("experience", "what trying leaves you with")], PER_TIME),
        ("break", "Short e, long e: the letter after the i",
         ["Say them slowly: ex-<b>per</b>-i-ment, ex-<b>pe</b>-ri-ence. The letters match up to the i, but the e is short in one and "
          "spells its name in the other. The letter that decides it is the one after the i. In <i>experience</i> the i stands before a vowel, the e of <i>-ence</i>, and makes the e long across the r. The notation draws that vault. In "
          "<i>experiment</i> the i stands before the m of <i>-ment</i>, and nothing reaches back. Where the syllables break, "
          "ex-per-i-ment and ex-pe-ri-ence, follows from the sound, so it describes the difference rather than causing it. That is "
          "the snapshot, the synchronic view: what English does now.",
          "Underneath are two patterns that Chomsky and Halle set out in <i>The Sound Pattern of English</i>. A stressed vowel with "
          "two syllables after it tends to be short: <i>divine</i> but <i>divinity</i>, <i>serene</i> but <i>serenity</i>, "
          "<i>nation</i> but <i>national</i>. That is <i>experiment</i>. But a vowel before one consonant, then an i, then another vowel is usually long, even with two syllables after it. <i>Canada</i> but <i>Canadian</i>, <i>comedy</i> but "
          "<i>comedian</i>, <i>colony</i> but <i>colonial</i>. That is <i>experience</i>, where the i stands before the e of "
          "<i>-ence</i>.",
          "They are tendencies, not laws. <i>Obesity</i> keeps the long e of <i>obese</i>, and <i>Italian</i> has a short a where "
          "<i>Canadian</i> has a long one. Teach the i before a vowel, which the vault shows, and let the family carry the rest.",
          "Expect speech to vary here, too. Before an r is where it varies most: Merriam-Webster gives ik-SPER-i-ment, also "
          "ik-SPIR-i-ment. A learner who says the second has the same parts and the same spelling; mark what the learner says."],
         [("experiment", "the i before the m of -ment: a short e"), ("experience", "the i before a vowel makes the e long")]),
        ("i", "A note on the i, for the curious",
         ["Both words have an i after <i>per</i>, and it is the same i. It is the stem vowel of Latin&rsquo;s verb, <i>exper&imacr;r&imacr;</i>, "
          "whose stem ends in &imacr; as <i>aud&imacr;re</i>&rsquo;s does. Latin built both nouns on that stem: exper&imacr; + mentum, "
          "exper&imacr; + ent + ia. <i>Expert</i> shows the root without it. It comes from the past form <i>expertus</i>, built on "
          "exper- alone. So the root is <i>per</i>, and the i belongs to the verb&rsquo;s stem.",
          "It has no meaning of its own. It marks which class of verb Latin&rsquo;s word belonged to, as the a of <i>&emacr;duc&amacr;re</i> and the e of <i>doc&emacr;re</i> do. A linguist calls it a theme vowel. It isn&rsquo;t a connecting vowel either, like "
          "the i of <i>carnivore</i> or the o of <i>photograph</i>, which join two parts and belong to neither. In English its only "
          "job is in the sound. Before the e of <i>-ence</i> it makes the e of <i>pe</i> long; before the m of <i>-ment</i> it "
          "doesn&rsquo;t.",
          "None of this is needed to teach the family. The word sums on this page write the stem as one part, <i>peri</i>, because "
          "every word in that cluster keeps the i. A learner who knows ex + peri + ment and ex + peri + ence can read, spell and "
          "connect them. The i is a deeper point, here for anyone who wants it."], []),
        ("stress", "The stress walks, and the spelling holds",
         ["Add a suffix and the stress moves. Every vowel it leaves goes weak, and a weak vowel it lands on comes back full. The "
          "letters hold still while the sounds change, and that is why the spelling is a better guide to the family than the sound.",
          "<i>Experiential</i> has a t where <i>experience</i> has a c: <i>-ence</i> and <i>-ential</i>, as in <i>essence</i> and "
          "<i>essential</i>, <i>confidence</i> and <i>confidential</i>. Latin wrote both with a t, <i>experientia</i>. French and English wrote the noun with a c and kept the t in <i>-ential</i>. There the t spells sh before <i>-ial</i>, as it does in <i>notation</i>."],
         [], _swalk()),
        ("sounds", "One spelling, three sounds",
         ["In the Latin words the root keeps one spelling, <i>per</i>, and its e spells three sounds. <i>Per</i> is closed and "
          "short in <i>experiment</i> and <i>peril</i>, open and long in <i>experience</i>, and an r unit in <i>expert</i>, as in "
          "<i>her</i>. The Greek words do the same with their i: open and long in <i>pirate</i>, closed and short in "
          "<i>empirical</i>."],
         [("experiment", "per: short"), ("experience", "pe: long"), ("expert", "per: an r unit"), ("peril", "per: short"),
          ("pirate", "pi: long"), ("empirical", "pir: short")]),
        ("speller", "For the speller",
         ["<b>Per, not pir or pur.</b> The vowel is weak in <i>experiment</i> and hard to hear. <i>Expert</i> and <i>peril</i> say "
          "the e plainly, and they&rsquo;re the same root.",
          "<b>-iment, not -ament.</b> The i is the stem&rsquo;s own vowel, and the same i is in <i>experience</i>: "
          "ex + peri + ment, ex + peri + ence.",
          "<b>-ience, not -iance.</b> The noun comes from Latin&rsquo;s present form, <i>experient-</i>, with an e, as "
          "<i>patience</i> goes with <i>patient</i>. And where the stress lands on it, the t comes back: <i>experiential</i>."], []),
    ],
    "students": ["experiment", "experience", "expert", "peril", "pirate", "fear"],
    "s_lead": "These words come from one old word that meant <i>try</i>, or <i>take a risk</i>.",
    "s_pair": [("experiment", "You try something, to find out."), ("experience", "What you learn by living and trying.")],
    "s_paras": ["Say them slowly: ex-<b>per</b>-i-ment, ex-<b>pe</b>-ri-ence.",
                "In <b>per</b>, the r closes the syllable, so the e is short.",
                "In <b>pe</b>, the syllable is open, so the e spells its name.",
                "Both words have an <b>i</b> after per. It came with the old Latin word, and it&rsquo;s in both. You don&rsquo;t need to know why it&rsquo;s there to read them.",
                "A <b>pirate</b> was someone who tried an attack. <b>Fear</b> is what you feel when danger is near. Same old word."],
    "uc": "the word list follows the Indo-European Lexicon, which follows Pokorny, fetched on 19 November 2026. Etymonline&rsquo;s "
          "own pages weren&rsquo;t reachable that day, so its links here are searches. Next: check the family against Etymonline and Watkins. Then check the vault from the i to the e in <i>experience</i> and <i>experiential</i> against <i>here</i> and <i>serious</i>.",
    "label": "Root family: *per-",
    "desc": "A word study of experiment and experience: the root *per-, to try or risk, and its family (expert, peril, pirate, empirical, fear), with why the e is short in one and long in the other, how the stress walks, and how two words that were one came apart.",
}
ROOTS = [LEG, HAP, DEUK, SEM, MED, LEUK, PER]


# ------------------------------------------------------------------ sign
# Made 20 November 2026: the classic word of structured word inquiry, why sign keeps a g it doesn't say. A base family,
# since the root under Latin signum is debated (the Indo-European Lexicon and Watkins: *sekw-, to follow; de Vaan: *sek-,
# to cut; a 2025 study in the Journal of Latin Linguistics argues for follow). Clustered by what the g does. The marks
# follow the 12 November ruling (site_codes.py): the g in a cone where it is silent, said and closing the syllable where
# a Latin ending follows.
SIGN_ROADS = [
    ("Latin <i>signum</i>", "a mark, a token; a soldiers&rsquo; standard; a seal", [("silent", "sign")]),
    ("Latin <i>sign&amacr;re</i>, with a prefix", "to mark: <i>d&emacr;sign&amacr;re</i>, mark out; <i>assign&amacr;re</i>, mark to someone; "
     "<i>resign&amacr;re</i>, unseal", [("silent", "design, assign, resign"), ("said", "designate")]),
    ("Latin <i>sign&amacr;lis</i>, <i>sign&amacr;t&umacr;ra</i>, <i>signific&amacr;re</i>", "of a sign; a signing; to make a sign", [("said", "signal, signature, signify")]),
    ("Latin <i>sigillum</i>, through French <i>seel</i>", "a little sign: a seal", [("seal", "seal")]),
]
SIGN_CLUSTERS = [
    {"key": "silent", "label": "sign, g silent", "spells": ["sign"], "head": "the g kept but not said",
     "road": "<i>sign</i> at the end of a word, or with an English ending after it",
     "note": "The g sits in its cone: not said, but kept, because <i>signal</i> and <i>signature</i> say it. With the g silent, the i "
             "spells its name, as it does in <i>find</i> and <i>child</i>. English endings don&rsquo;t wake the g: <i>signs</i>, "
             "<i>signing</i>, <i>designer</i>, <i>assignment</i>.",
     "groups": [
         [("sign", ["sign"], "a mark that tells you something; to write your name"), ("signs", ["sign", "-s"], "more than one sign"),
          ("signing", ["sign", "-ing"], "writing your name; talking with your hands")],
         [("design", ["de-", "sign"], "mark out: a plan or a pattern, or to make one"), ("designer", ["de-", "sign", "-er"], "someone who designs")],
         [("assign", ["as-", "sign"], "mark to someone: give out a job"), ("assignment", ["as-", "sign", "-ment"], "a job given out")],
         [("resign", ["re-", "sign"], "unseal, sign back: give up a job"), ("consign", ["con-", "sign"], "seal with: hand over to be kept or sent")],
     ]},
    {"key": "said", "label": "sign, g said", "spells": ["sign"], "head": "the g said",
     "road": "<i>sign</i> with a Latin ending after it: the g closes the syllable, sig, and the i is short",
     "note": "Here the g is heard: sig-nal, sig-na-ture, sig-ni-fy. These are the words that keep the g in <i>sign</i>. Take it out of "
             "<i>sign</i> and the family no longer looks like one.",
     "groups": [
         [("signal", ["sign", "-al"], "a sign that sends a message: a light, a sound, a wave")],
         [("signature", ["sign", "-at(e)", "-ure"], "your name, written by you"), ("signatory", ["sign", "-at(e)", "-ory"], "someone who signs an agreement")],
         [("signify", ["sign", "-i", "-fy"], "make a sign: show, mean"), ("significant", ["sign", "-i", "-fic", "-ant"], "that makes a sign: full of meaning, important"),
          ("significance", ["sign", "-i", "-fic", "-ance"], "meaning, importance")],
         [("designate", ["de-", "sign", "-ate"], "mark out: name or choose for a job"), ("designation", ["de-", "sign", "-at(e)", "-ion"], "a name or a title given")],
         [("resignation", ["re-", "sign", "-at(e)", "-ion"], "a giving up of a job; a calm acceptance of what can&rsquo;t be changed")],
         [("signet", ["sign", "-et"], "a small seal, often on a ring"), ("insignia", ["in-", "sign", "-ia"], "badges and marks of rank")],
     ]},
    {"key": "seal", "label": "seal, sig", "spells": ["seal", "sig"], "head": "a little sign",
     "road": "Latin <i>sigillum</i>, a little sign, a seal",
     "note": "<i>Seal</i> lost the g in French, where <i>sigillum</i> became <i>seel</i>; English took the word "
             "without it. <i>Sigil</i> came straight from Latin and kept the g, soft before the i.",
     "groups": [
         [("seal", ["seal"], "a little sign pressed into wax; to close tight")],
         [("sigil", None, "a seal or a sign said to have power, in old books and stories", "sig")],
     ]},
]
PARTS.update({
    "-s": "more than one (<i>signs</i>); what he, she or it does (<i>she signs</i>); or belonging to, in <i>its</i>",
    "-ing": "happening now (<i>she is signing</i>); or the doing of it (<i>signing is fun</i>)",
    "-ory": "having to do with; or a person or place that does it",
    "-et": "small: a French ending",
    "-ia": "things of a kind: a Latin plural",
    "-fic": "that makes or causes: Latin <i>-ficus</i>, from <i>facere</i>, to make",
    "-fy": "make: Latin <i>-fic&amacr;re</i>, through French <i>-fier</i>",
    "-i": "a connecting vowel, joining a base to an ending that starts with a consonant",
})
ROOT_PARTS.update({
    "sign": "a mark: Latin <i>signum</i>; in verbs, <i>sign&amacr;re</i>, to mark",
    "seal": "a little sign: Latin <i>sigillum</i>, worn down in French to <i>seel</i>",
    "sig": "a little sign: Latin <i>sigillum</i>",
})
SIGN = {
    "slug": "sign", "root": "sign", "gloss": "a mark", "kind": "a base family",
    "h1_s": "sign means &lsquo;a mark&rsquo;",
    "lead": "A mark, a token. Latin <i>signum</i> was a mark, a sign, a seal, and the standard soldiers followed into battle. English borrowed it again and again. Its spelling keeps a letter that <i>sign</i> doesn&rsquo;t sound: the g, heard in <i>signal</i> and <i>signature</i>. It&rsquo;s the classic example of English spelling keeping a part the same when its sound changes.",
    "drawn": ("sign", "sign, marked: the g in its cone"),
    "sources": [("Indo-European Lexicon, seku̯- (Linguistics Research Center, University of Texas at Austin), which follows Pokorny: Latin <i>signum</i> under to follow", "https://lrc.la.utexas.edu/lex/master/1673"),
                ("Wiktionary, Proto-Italic *seknom, after Michiel de Vaan, <i>Etymological Dictionary of Latin and the other Italic Languages</i> (Brill, 2008), p. 563: from *sek-, to cut", "https://en.wiktionary.com/wiki/Reconstruction:Proto-Italic/seknom"),
                ("&ldquo;On the etymology of Latin <i>signum</i> and its Sabellic counterparts,&rdquo; <i>Journal of Latin Linguistics</i> (2025): for to follow, against to cut", "https://www.degruyterbrill.com/document/doi/10.1515/joll-2025-2004/html"),
                ("Etymonline: <i>sign</i>, <i>signal</i>, <i>signature</i>, <i>design</i>, <i>seal</i> and the rest", "https://www.etymonline.com/search?q=sign"),
                ("Edward Carney, <i>A Survey of English Spelling</i> (Routledge, 1994): the g of <i>sign</i> as an inert letter, pp. 41, 47, 247", "../credits.html"),
                ("Noam Chomsky and Morris Halle, <i>The Sound Pattern of English</i> (Harper &amp; Row, 1968), on <i>sign</i> and <i>signify</i>, <i>malign</i> and <i>malignant</i>", "../credits.html"),
                ("Melvyn Ramsden&rsquo;s Real Spelling and Pete Bowers&rsquo;s structured word inquiry, where <i>sign</i> is the classic first matrix", "../credits.html"),
                ("Ferdinand de Saussure, <i>Course in General Linguistics</i> (1916): the sign, the signifier and the signified", "../credits.html")],
    "roads": SIGN_ROADS, "clusters": SIGN_CLUSTERS, "parts": PARTS, "root_parts": ROOT_PARTS,
    "extra": [
        ("g", "Why sign keeps its g",
         ["Say <i>sign</i> and you don&rsquo;t hear a g. Say <i>signal</i> and you do. The spelling keeps the g in both, so the "
          "family looks like a family: sign, signal, signature, design, designate. Carney calls a letter like this inert: silent in "
          "one word, said in another (1994: 41). The notation draws it in a cone of silence, joined to neither the i nor the n. So it sits in the same place in every word of the family.",
          "The g also changes the i. When the g is silent, the i spells its name, as in <i>find</i> and <i>child</i>. When the g is "
          "said, it closes the syllable, sig, and the i is short. Venezky calls this kind of trade, a long vowel where a consonant is silent, a compensatory alternation.",
          "Chomsky and Halle used <i>sign</i> and <i>signify</i>, <i>malign</i> and <i>malignant</i>, and <i>paradigm</i> and <i>paradigmatic</i>. Their point: English spelling writes the part, not the sound. Melvyn Ramsden and Pete Bowers made "
          "<i>sign</i> the first word a class takes apart in structured word inquiry. This page follows that tradition."],
         [("sign", "the g in its cone, and a long i"), ("signal", "the g said: sig | nal"), ("design", "de + sign"), ("designate", "des | ig | nate: the g said")]),
        ("root", "Follow or cut?",
         ["Under Latin <i>signum</i> sits a root that scholars still argue about. Pokorny, and the Indo-European Lexicon after him, "
          "put it with <i>*sekw-</i>, to follow: a sign as the standard soldiers followed. Michiel de Vaan&rsquo;s Latin dictionary "
          "(2008) puts it with <i>*sek-</i>, to cut: a sign as a mark cut into something. A study in the <i>Journal of Latin "
          "Linguistics</i> (2025) argues for follow again, on the sounds of <i>signum</i>&rsquo;s cousins in Oscan.",
          "The family on this page doesn&rsquo;t depend on the answer: every word in it is built on <i>sign</i>, a mark. That&rsquo;s "
          "why it is a base family here and not a root family. If follow is right, <i>sign</i> is a cousin of <i>sequence</i>, "
          "<i>second</i> and <i>pursue</i>."], []),
        ("saussure", "Signifier and signified",
         ["Ferdinand de Saussure built modern linguistics on this word. A linguistic sign, he said, has two sides, joined like the two sides of a sheet of paper. One is the <i>signifier</i>, the sound pattern; the other is the <i>signified</i>, the idea. His French "
          "words were <i>signifiant</i> and <i>signifi&eacute;</i>, the present and past forms of <i>signifier</i>, to signify.",
          "The notation marks the signifier: the sounds and the letters that spell them. The parts and the seams are where the "
          "signified shows through: <i>design</i> is de + sign, to mark out, whatever the g is doing."], []),
    ],
    "students": ["sign", "signal", "signature", "design", "assign", "seal"],
    "s_lead": "These words come from <b>sign</b>. It means a mark.",
    "s_pair": [("sign", "The g is silent."), ("signal", "The g is heard.")],
    "s_paras": ["Say them: <b>sign</b>, <b>sig</b>-nal.",
                "In <b>signal</b> you hear the g. In <b>sign</b> you don&rsquo;t, but it is still there.",
                "It stays so the words look like one family: sign, signal, signature, design.",
                "When the g is silent, the i spells its name: s<b>i</b>gn, like f<b>i</b>nd.",
                "A <b>seal</b> was a little sign pressed into wax. It lost its g long ago."],
    "uc": "the family follows the Indo-European Lexicon and Etymonline&rsquo;s entries; Etymonline&rsquo;s own pages weren&rsquo;t "
          "reachable on 20 November 2026, so its link here is a search. The root is debated (see Follow or cut?). Next: check each "
          "word against Etymonline, and the marks of <i>significant</i> and <i>signatory</i>.",
    "label": "Base family: sign",
    "desc": "The base sign, a mark, and its family: why sign keeps a g that signal and signature say, with design, assign, resign, designate, signify, significant and seal.",
}
ROOTS = [LEG, HAP, DEUK, SEM, MED, LEUK, PER, SIGN]


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
    for c in R["clusters"] + R.get("debated", {}).get("clusters", []):
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

    # Marginal or debated: the same word sums, their parts as plain text (the drill-down's script works on its own panels)
    deb = R.get("debated")
    def wsum_plain(c, w, parts, mean, bold):
        link = f'<a class="rw" href="{etym(w, R["slug"])}">{bold_root(w, bold)}</a>'
        if not parts:
            return f'<div class="wsum" id="{doors.word_id(w)}"><span class="sum plainw">{link}</span><span class="rm">{mean}</span></div>'
        ps = '<span class="pl"> + </span>'.join(f'<span class="part {part_kind(p, c["spells"])}">{html.escape(p.strip("-"))}</span>' for p in parts)
        return f'<div class="wsum" id="{doors.word_id(w)}"><span class="sum">{ps}<span class="to"> &rarr; </span>{link}</span><span class="rm">{mean}</span></div>'
    debated = ""
    if deb:
        blocks = "".join(
            f'<div class="dcl" id="c-{c["key"]}"><h3><b>{c["label"]}</b>: {c["head"]}</h3><p class="rh">{c["road"]}.</p><p class="cnote">{c["why"]}</p>'
            + "".join('<div class="cgroup">' + "".join(wsum_plain(c2, w, p, m, b) for c2, w, p, m, b in words if c2 is c and w in [it[0] for it in g]) + "</div>" for g in c["groups"])
            + "</div>" for c in deb["clusters"])
        debated = f"""<section class="about t-only debated" aria-labelledby="deb-h"><div class="wrap">
<h2 id="deb-h">Marginal or debated</h2>
<p class="sub">{deb["lead"]}</p>
{blocks}
</div></section>
"""

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
<h2 id="rd-h">How the words came into English</h2>
<p class="sub">The root came into English {doors.NUMBER[len(R["roads"])].lower()} ways, each with its own spellings. This is the time-lapse, or <a href="../definitions.html#def-diachronic">diachronic</a>, view. Pick a spelling to see its words.</p>
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
{debated}<section class="about t-only" aria-labelledby="pt-h"><div class="wrap">
<h2 id="pt-h">The parts, and what they mean</h2>
<p class="sub">Every part in the word sums above, with the words that carry it.</p>
<div class="pgcols">{gloss(roots, "The root&rsquo;s spellings")}{gloss(pre, "Before the root")}{gloss(suf, "After the root")}{gloss(base, "Other roots") if base else ""}</div>
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
        dw, dl = R["drawn"][:2]
        drawn = X["svg_of"](dw, 58, label=dl)
        import landing          # *leg- has legomorphic built up a layer at a time, as the home page had until 12 November 2026
        drawn_hero = landing.lego_block(X["LW"]) if R["slug"] == "leg" else drawn
        extra = "".join(f"""<section class="about t-only" aria-labelledby="{sid}-h"><div class="wrap">
<h2 id="{sid}-h">{head}</h2>
{"".join(f'<p class="sub">{t}</p>' for t in paras)}
{drawn_row(row)}{more[0] if more else ""}
</div></section>
""" for sid, head, paras, row, *more in R.get("extra", []))      # a fifth item is an illustration: a timeline, a stress walk
        # The learner's view can carry a marked pair and a few short lines (the *per- word study, 19 November 2026).
        s_more = ""
        if R.get("s_pair"):
            pair = "".join(f'<figure class="word">{X["svg_of"](w, 72, label=f"{w}, marked")}<figcaption>{c}</figcaption></figure>' for w, c in R["s_pair"])
            s_more = f'<div class="words rrow s-pair">{pair}</div>' + "".join(f'<p class="s-line">{x}</p>' for x in R.get("s_paras", []))
        srcs = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in R["sources"])
        import studies                                    # a word study for this family links from here (20 November 2026)
        study_line = "".join(f'<p class="rstudy"><a class="btn" href="../{studies.link(s)}">Word study: {s["title"]}</a> <span class="t-only">a presentation for learners, built a piece at a time</span></p>\n'
                             for s in studies.for_page(f'roots/{R["slug"]}.html'))
        body = f"""{header(1)}
<main class="root-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only">Parts &middot; {R["kind"]}</p>
<h1><span class="t-only">{R["root"]}</span><span class="s-only">{R["h1_s"]}</span></h1>
<p class="lead t-only">{R["lead"]}</p>
{study_line}<div class="door-word t-only">{drawn_hero}</div>
</div></section>
<section class="about s-only"><div class="wrap">
<p class="s-lead">{R["s_lead"]}</p>
<ul class="rkids">{kids}</ul>
{s_more}
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
        (OUT / "roots" / f"{R['slug']}.html").write_text(page(f"{R['root']}: {R['gloss']} · Sounds and Words, Assembled", body, 1, R["desc"]), encoding="utf-8")
    return found
