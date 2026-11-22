"""Sound and meaning (21 November 2026): lists/phonesthemes.html, on Legomorphic spelling, with the word study
studies/phonesthemes.html. A phonestheme is a sound many words with a shared meaning have in common (gl- in glow, gleam,
glitter): J. R. Firth's word (1930). It isn't a morpheme, since the rest of the word (-ow, -eam, -itter) means nothing
on its own, and it isn't a rule: every cluster has words with the same letters and none of the meaning.

Each cluster: (id, the letters, what the words lean toward, the words that fit, a second row or None, the words with the
same letters that don't fit, the note, how the dictionary count went). The count is Otis and Sagi (2008), who tested
the clusters in Hutchins's list against the whole dictionary: "held" (confirmed), "close" (fl-, just short of their
bar), "not" (sl-, failed). Words are marked by the site's rules; the new ones are in more_codes.json.

Sources: Firth, Speech (1930); John Wallis, Grammatica Linguae Anglicanae (1653), who noticed groups like these;
Bolinger, 'The sign is not arbitrary' (1949); Marchand, 'Phonetic symbolism in English word-formation' (1959);
Bergen, 'The psychological reality of phonaesthemes', Language 80 (2004): 290-311; Otis and Sagi, 'Phonaesthemes: a
corpus-based analysis', Proceedings of the Cognitive Science Society 30 (2008); Anatoly Liberman, 'Sniff, snuff, SNAFU',
OUPblog (1 May 2019); the Indo-European Lexicon (University of Texas at Austin, after Pokorny) for *ghel- and *dwo-."""
import html

CLUSTERS = [
    ("gl", "gl-", "light and seeing",
     ["glow", "gleam", "glint", "glitter", "glisten", "glimmer", "glare", "glance", "glimpse", "glass", "gloss", "glaze"],
     None, ["glove", "glue", "globe", "glum"],
     "Most of these share an old root, <i>*ghel-</i>, to shine, with <i>gold</i> and <i>yellow</i>. So gl- is partly a "
     "family that stopped looking like one, and its sound kept the meaning together. In one count of written English, about "
     "4 in 10 different gl- words, and 6 in 10 of their uses, had to do with light or seeing (Bergen 2004).", "held"),
    ("sn", "sn-", "the nose and mouth",
     ["sniff", "snout", "sneeze", "snore", "snort", "sniffle", "snuffle", "snarl", "sneer", "snicker"],
     None, ["snow", "snail", "snake", "snap"],
     "<i>Sneeze</i> was <i>fnese</i> in Old English. The fn- dropped out of use and sn- took its place, perhaps because "
     "sn- suited the nose (Liberman 2019). Bergen (2004) tested sn- with gl-.", "held"),
    ("sl", "sl-", "sliding and slipping",
     ["slide", "slip", "slick", "slither", "slope", "slush", "slime", "sled", "sleek", "slant"],
     None, ["sleep", "slim", "slam"],
     "Firth&rsquo;s own first example (1930). The dictionary count didn&rsquo;t back it up: plenty of sl- words don&rsquo;t "
     "slide. A cluster can feel strong and still be a lean, not a rule.", "not"),
    ("sw", "sw-", "swinging and sweeping",
     ["swing", "sway", "sweep", "swirl", "swoop", "swish", "swivel", "swerve"],
     None, ["sweet", "swan", "swamp"],
     "Each of these moves like a pendulum or a broom: out and back, or round.", "held"),
    ("tw", "tw-", "twisting",
     ["twist", "twirl", "twine", "twitch", "tweak", "twiddle"],
     ("The family of two", ["two", "twin", "twelve", "twenty", "twice", "between", "twig"]), [],
     "The second row is a real family: all from the old word for two (Indo-European <i>*dwo-</i>). <i>Twist</i> and "
     "<i>twine</i> are in it too, as thread of two strands, and a twig is where a branch splits in two. <i>Twirl</i>, "
     "<i>tweak</i> and <i>twitch</i> joined by sound. Same letters, two reasons.", "held"),
    ("str", "str-", "long and thin",
     ["string", "strand", "strap", "straw", "stream", "stripe", "stretch", "straight"],
     None, ["strong", "strange"],
     "Lines, bands and things pulled out long.", "held"),
    ("ash", "-ash", "a hard, fast hit",
     ["bash", "crash", "smash", "splash", "clash", "dash", "slash", "flash"],
     None, ["cash", "ash", "wash"],
     "In <i>wash</i>, the w changes the sound of the a, so it doesn&rsquo;t echo the others. A phonestheme is a sound: the "
     "same letters with a different sound carry nothing.", "held"),
    ("ump", "-ump", "a rounded lump",
     ["bump", "lump", "clump", "stump", "plump", "dump"],
     None, ["jump", "pump"],
     "A heap, the stump of a tree, a bump in the road: something round that rises.", "held"),
    ("owl", "-owl", "growls and dark looks",
     ["growl", "howl", "yowl", "scowl", "prowl", "owl"],
     None, ["bowl"],
     "<i>Bowl</i> has the letters and not the sound: its ow spells the o of <i>snow</i>. A dog&rsquo;s growl needs no "
     "translation: the sound alone carries the meaning.", "held"),
    ("fl", "fl-", "quick, light movement",
     ["flap", "flick", "flutter", "flit", "fling", "flicker", "flip", "fly"],
     None, ["flat", "flag"],
     "Just short of the bar in the dictionary count, so a weaker lean than gl- or sn-.", "close"),
]
COUNT = {"held": "held up in a count of the whole dictionary", "close": "close, in a count of the whole dictionary",
         "not": "didn&rsquo;t hold up in a count of the whole dictionary"}


def words():
    out = []
    for c in CLUSTERS:
        out += c[3] + (c[4][1] if c[4] else []) + c[5]
    return out


def write(OUT, page, header, footer, X):
    import json, gym, pathlib
    from noun_codes import NOUN_CODES
    here = pathlib.Path(__file__).resolve().parent
    pool = dict(X["auto_codes"]); pool.update(NOUN_CODES); pool.update(gym.codes())
    for fn in ("more_codes.json", "family_codes.json"): pool.update(json.loads((here / "data" / fn).read_text(encoding="utf-8")))
    LW = X["LW"]
    def code_for(w):
        if w in LW.W: return None
        assert w in pool, w
        return pool[w]
    svg = lambda w: X["svg_of"](w, 40, code=code_for(w), label=f"{w}, marked")
    fig = lambda w: f'<figure class="word">{svg(w)}</figure>'
    secs, toc = [], []
    for cid, letters, lean, fits, second, odd, note, count in CLUSTERS:
        toc.append(f'<a href="#{cid}">{letters}</a>')
        row2 = (f'<h3>{second[0]}</h3><div class="words rrow">{"".join(fig(w) for w in second[1])}</div>') if second else ""
        oddrow = (f'<h3>Same letters, not the meaning</h3><div class="words rrow ph-odd">{"".join(fig(w) for w in odd)}</div>') if odd else ""
        secs.append(f"""<section class="about ph-cluster" id="{cid}"><div class="wrap">
<h2><span class="ph-l">{letters}</span> {lean}</h2>
<div class="words rrow">{"".join(fig(w) for w in fits)}</div>
{row2}{oddrow}
<p class="sub">{note} <span class="ph-count t-only">{letters} {COUNT[count]}.</span></p>
</div></section>""")
    body = f"""{header(1)}
<main class="ph-page">
<section class="hero"><div class="wrap">
<p class="eyebrow t-only"><a href="index.html">Legomorphic spelling</a> &middot; Sound and meaning</p>
<h1>Sound and meaning: phonesthemes</h1>
<p class="lead">Some sounds lean toward a meaning. <i>Glow</i>, <i>gleam</i> and <i>glitter</i> all start with gl- and all have to do with light; <i>sniff</i>, <i>snout</i> and <i>sneeze</i> start with sn- and all have to do with the nose. A sound shared like this is a phonestheme.</p>
<p class="sub">It isn&rsquo;t a morpheme. Take gl- away and <i>-ow</i>, <i>-eam</i> and <i>-itter</i> mean nothing, so there&rsquo;s no word sum. And it isn&rsquo;t a rule: every list here ends with words that have the letters and not the meaning. The word is J. R. Firth&rsquo;s (1930), from Greek <i>ph&omacr;n&emacr;</i>, sound, and <i>aisth&emacr;ma</i>, what is felt.</p>
<p class="sub t-only">To teach: mix the words up and have learners sort them by meaning first, then look at how they start or end. Keep the odd ones in the pile; finding them is half the lesson. The <a href="../studies/phonesthemes.html">word study</a> walks a class through it.</p>
<nav class="ph-toc" aria-label="Clusters">{"".join(toc)}</nav>
</div></section>
{"".join(secs)}
<section class="about t-only"><div class="wrap prose">
<h2>Sources</h2>
<p class="sub">J. R. Firth, <i>Speech</i> (1930), who named the phonestheme; John Wallis noticed groups like these in his grammar of English (1653). Dwight Bolinger, &ldquo;The sign is not arbitrary&rdquo; (1949), and Hans Marchand, &ldquo;Phonetic symbolism in English word-formation&rdquo; (1959). Benjamin Bergen, &ldquo;The psychological reality of phonaesthemes,&rdquo; <i>Language</i> 80 (2004): 290&ndash;311: gl- and sn- words primed each other more than words that share only letters or only meaning. Katya Otis and Eyal Sagi, &ldquo;Phonaesthemes: a corpus-based analysis&rdquo; (Cognitive Science Society, 2008): which clusters hold up across the whole dictionary. Anatoly Liberman, &ldquo;Sniff, snuff, SNAFU,&rdquo; OUPblog (2019), on <i>sneeze</i>. The roots <i>*ghel-</i> and <i>*dwo-</i> are from the Indo-European Lexicon (University of Texas at Austin, after Pokorny).</p>
{X["uc"]("ten clusters, since 21 November 2026. Next: cl-, gr- and the frequentative endings -er and -le (flicker, sparkle), which are morphemes and make a good contrast.")}
</div></section>
</main>
{footer(1)}"""
    (OUT / "lists" / "phonesthemes.html").write_text(page("Sound and meaning: phonesthemes · Sounds and Words, Assembled", body, 1, DESC), encoding="utf-8")
    return sorted(set(words()))


DESC = "Phonesthemes: sounds many words with a shared meaning have in common (gl- for light, sn- for the nose), in ten spelling clusters, each with the words that don't fit."
