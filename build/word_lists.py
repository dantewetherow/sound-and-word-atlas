"""The Word lists page: where the ELP high-frequency words come from in E. W. Dolch's sight words.

build_site.py calls write() and hands it its page, header, footer and coloured functions. The words come from
data/elp_hfw.json and data/dolch.json, and every count on the page is worked out from them, so a correction to either
list carries through. The page works without its script: the table holds every word, and the script only fills in
the panel under each chart when part of a bar is tapped."""
import html, json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
esc = html.escape

GRADES = [("K", "ELP kindergarten"), ("1", "ELP grade 1"), ("2", "ELP grade 2")]
GRADE_HEADS = {"K": "Kindergarten", "1": "Grade 1", "2": "Grade 2"}
LIST_NAMES = {"Kindergarten": "Kindergarten", "CV": "CV", "Irregular/HFW words": "Irregular/HFW", "Digraphs": "Digraphs",
              "Long Vowel Silent 'e'": "Long vowel silent e", "R-Controlled": "R-controlled", "Vowel Teams": "Vowel teams",
              "Diphthongs": "Diphthongs", "Multisyllabic": "Multisyllabic"}
# The levels as school grades, the way the University of Utah Reading Clinic sets them: the first three all in grade 1.
LEVEL_GRADE = {"pre-primer": 1, "primer": 1, "first": 1, "second": 2, "third": 3}
ELP_GRADE = {"K": 0, "1": 1, "2": 2}

SOURCES = [
    ('E. W. Dolch, &ldquo;A Basic Sight Vocabulary,&rdquo; <i>The Elementary School Journal</i> 36, no. 6 (February 1936): 456&ndash;460. '
     'His 220 words, built from three earlier lists, with the 95 nouns given separately. '
     '<a href="https://twuread5503.pbworks.com/f/a+basic+sight+vocabulary.pdf">A scan of the article</a>.'),
    ('<a href="https://readwritethink.org/sites/default/files/resources/lesson_images/lesson301/dolchwordlist.pdf">Dolch Word List</a>, '
     'ReadWriteThink (IRA/NCTE, 2004): the levels used here. It prints <i>giving</i> where Dolch&rsquo;s article has <i>going</i>.'),
    ('<a href="https://uurc.utah.edu/General/Dolch.php">Dolch Word List</a>, University of Utah Reading Clinic, which sets the '
     'first three levels as First (October), First (March) and First (End).'),
    ('<a href="https://bookroo.com/tools/fry-word-list">Fry Word List</a>, Bookroo: Fry&rsquo;s first 100 Instant Words.'),
    ('<i>Early Literacy Profile (ELP) Assessment &amp; Instructional Guide</i>, Central Okanagan Public Schools (2025), pp. 16&ndash;17. '
     'The district&rsquo;s <a href="https://assessment.sd23.bc.ca/elp">ELP page</a> is the place for the assessment itself.'),
]

SCRIPT = r"""(() => {
  const D = JSON.parse(document.getElementById('wl-data').textContent);
  const levelOf = {}, listOf = {};
  D.levels.forEach(l => l.words.forEach(w => { levelOf[w] = l; }));
  D.lists.forEach(L => L.words.forEach(w => { listOf[w] = L; }));
  const grade = {K: 'ELP kindergarten', '1': 'ELP grade 1', '2': 'ELP grade 2'};
  const ws = a => a.map(w => D.cw[w] || w).join(' ');
  const lower = s => s.charAt(0).toLowerCase() + s.slice(1);
  const count = k => k + (k === 1 ? ' word' : ' words');
  const both = a => a.length > 1 ? a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1] : a.join('');
  function byLevel(key, g) {
    const l = D.levels.find(x => x.key === key);
    const cards = `<p class="more"><a href="${D.cards[key]}" download>Print the Dolch ${lower(l.name)} cards</a> (PDF)</p>`;
    if (g === 'none') {
      const off = l.words.filter(w => !listOf[w]);
      const s = off.filter(w => D.short.includes(w)), r = off.filter(w => !D.short.includes(w));
      return `<h3>${l.name} words not on the ELP lists <span>${count(off.length)}</span></h3><dl>` +
        (s.length ? `<dt>One-syllable short-vowel words</dt><dd>${ws(s)}</dd>` : '') +
        (r.length ? `<dt>The rest</dt><dd>${ws(r)}</dd>` : '') + '</dl>' + cards;
    }
    const got = l.words.filter(w => listOf[w] && listOf[w].grade === g);
    const groups = D.lists.filter(L => L.grade === g).map(L => [L, got.filter(w => listOf[w] === L)]).filter(p => p[1].length);
    return `<h3>${l.name} &rarr; ${grade[g]} <span>${count(got.length)}</span></h3><dl>` +
      groups.map(([L, a]) => `<dt>List ${L.n} &middot; ${L.name}</dt><dd>${ws(a)}</dd>`).join('') + '</dl>' + cards;
  }
  function byList(num, key) {
    const L = D.lists.find(x => String(x.n) === num);
    if (key === 'none') {
      const a = L.words.filter(w => !levelOf[w]);
      const nouns = a.filter(w => D.nouns.includes(w)), rest = a.filter(w => !D.nouns.includes(w));
      const note = (nouns.length ? `<i>${both(nouns)}</i> ${nouns.length === 1 ? 'is' : 'are'} on Dolch&rsquo;s separate list of nouns. ` : '') +
        (rest.length ? `<i>${both(rest)}</i> ${rest.length === 1 ? 'is' : 'are'} on Fry&rsquo;s first 100 Instant Words.` : '');
      return `<h3>List ${L.n} &middot; ${L.name}: not in Dolch&rsquo;s 220 <span>${count(a.length)}</span></h3><p class="ws">${ws(a)}</p><p class="more">${note}</p>`;
    }
    const l = D.levels.find(x => x.key === key);
    const a = L.words.filter(w => levelOf[w] === l);
    return `<h3>List ${L.n} &middot; ${L.name} &larr; Dolch ${lower(l.name)} <span>${count(a.length)}</span></h3><p class="ws">${ws(a)}</p>`;
  }
  const show = b => {
    const chart = b.dataset.chart, [a, c] = b.dataset.key.split('|');
    document.querySelectorAll(`.seg[data-chart="${chart}"]`).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    document.getElementById(chart + '-detail').innerHTML = chart === 'levels' ? byLevel(a, c) : byList(a, c);
  };
  document.querySelectorAll('.seg').forEach(b => b.addEventListener('click', () => show(b)));
  [['levels', 'second|1'], ['lists', '6|second']].forEach(([c, k]) => {
    const b = document.querySelector(`.seg[data-chart="${c}"][data-key="${k}"]`); if (b) show(b);
  });
})();"""


def write(OUT, page, header, footer, coloured, LW):
    ELP = json.loads((HERE / "data" / "elp_hfw.json").read_text(encoding="utf-8"))
    DOLCH = json.loads((HERE / "data" / "dolch.json").read_text(encoding="utf-8"))
    levels = DOLCH["levels"]
    lists = [{"n": int(k), "grade": v["grade"], "name": LIST_NAMES[v["label"]], "words": v["words"]}
             for k, v in sorted(ELP["lists"].items(), key=lambda kv: int(kv[0]))]
    level_of = {w: l for l in levels for w in l["words"]}
    list_of = {w: L for L in lists for w in L["words"]}
    nouns = DOLCH["nouns"]

    def short(w):
        """One syllable, and its only vowel a short one (big, stop, thank, six): not all, cold, full or live."""
        p = LW.parse(w)
        kinds = [u["kind"] for u in p["units"] if u["kind"] in LW.VOWEL_KINDS | {"e0", "e>", "ap"}]
        return len(p["syllables"]) == 1 and kinds == ["s"]

    elp_words = [w for L in lists for w in L["words"]]
    shared = [w for w in elp_words if w in level_of]
    noun_hits = [w for w in elp_words if w not in level_of and w in nouns]
    elp_only = [w for w in elp_words if w not in level_of and w not in nouns]
    off = [w for l in levels for w in l["words"] if w not in list_of]
    off_short = [w for w in off if short(w)]
    n220 = sum(len(l["words"]) for l in levels)
    on_pattern = [w for w in shared if list_of[w]["name"] not in ("Kindergarten", "Irregular/HFW")]
    # The page says the ELP's only short-vowel words are and, is and it in kindergarten and the Digraphs list: hold it to that.
    elp_short = {w for w in elp_words if short(w)}
    digraphs = next(L for L in lists if L["name"] == "Digraphs")
    assert elp_short == {"and", "is", "it"} | set(digraphs["words"]), sorted(elp_short)
    place = [ELP_GRADE[list_of[w]["grade"]] - LEVEL_GRADE[level_of[w]["key"]] for w in shared]
    earlier, same, later = sum(d < 0 for d in place), sum(d == 0 for d in place), sum(d > 0 for d in place)
    silent_e = next(L for L in lists if L["name"] == "Long vowel silent e")
    pulled = [w for w in silent_e["words"] if level_of[w]["key"] == "second"]
    held = [w for w in shared if list_of[w]["grade"] == "2" and LEVEL_GRADE[level_of[w]["key"]] == 1]
    diph = next(L for L in lists if L["name"] == "Diphthongs")
    held_diph = [w for w in held if list_of[w] is diph]

    def i(words): return ", ".join(f"<i>{esc(w)}</i>" for w in words)
    def spell(k): return ["no", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"][k] if k < 10 else str(k)
    def and_list(words):
        return (", ".join(f"<i>{esc(w)}</i>" for w in words[:-1]) + f" and <i>{esc(words[-1])}</i>") if len(words) > 1 else i(words)

    # Chart 1: each Dolch level, split by the ELP grade whose lists take its words
    top = max(len(l["words"]) for l in levels)
    rows1 = []
    for l in levels:
        segs = []
        for g, gname in GRADES + [("none", "")]:
            k = sum(1 for w in l["words"] if (list_of[w]["grade"] == g if w in list_of else g == "none"))
            if not k: continue
            say = f'{l["name"]}: {k} words on {gname} lists' if g != "none" else f'{l["name"]}: {k} words not on the ELP lists'
            segs.append(f'<button type="button" class="seg s-{g}" style="flex-grow:{k}" data-chart="levels" data-key="{l["key"]}|{g}" '
                        f'aria-pressed="false" aria-label="{esc(say)}">{k if k >= 3 else ""}</button>')
        rows1.append(f'<div class="row"><div class="rl">{esc(l["name"])}<b>{len(l["words"])}</b></div>'
                     f'<div class="track"><div class="bar" style="width:{100 * len(l["words"]) / top:.2f}%">{"".join(segs)}</div></div></div>')
    legend1 = "".join(f'<li><span class="sw s-{g}"></span>{esc(name)}</li>' for g, name in GRADES) + '<li><span class="sw s-none"></span>Not on the ELP lists</li>'

    # Chart 2: each ELP list, split by the Dolch level its words come from
    top2 = max(len(L["words"]) for L in lists)
    rows2, seen = [], set()
    for L in lists:
        if L["grade"] not in seen:
            seen.add(L["grade"]); rows2.append(f'<p class="grade-h">{GRADE_HEADS[L["grade"]]}</p>')
        segs = []
        for key, name in [(l["key"], l["name"]) for l in levels] + [("none", "")]:
            k = sum(1 for w in L["words"] if (level_of[w]["key"] == key if w in level_of else key == "none"))
            if not k: continue
            say = (f'List {L["n"]}, {L["name"]}: {k} words from Dolch {name[0].lower() + name[1:]}' if key != "none"
                   else f'List {L["n"]}, {L["name"]}: {k} words not in Dolch\'s 220')
            segs.append(f'<button type="button" class="seg d-{key}" style="flex-grow:{k}" data-chart="lists" data-key="{L["n"]}|{key}" '
                        f'aria-pressed="false" aria-label="{esc(say)}">{k if k >= 2 else ""}</button>')
        rows2.append(f'<div class="row"><div class="rl">{L["n"]} &middot; {esc(L["name"])}<b>{len(L["words"])}</b></div>'
                     f'<div class="track"><div class="bar" style="width:{100 * len(L["words"]) / top2:.2f}%">{"".join(segs)}</div></div></div>')
    legend2 = "".join(f'<li><span class="sw d-{l["key"]}"></span>{esc(l["name"])}</li>' for l in levels) + '<li><span class="sw d-none"></span>Not in Dolch&rsquo;s 220</li>'

    # The table: every word once, each with an id so a search can land on it
    import doors
    wid = lambda w: f'<span id="{doors.word_id(w)}">{esc(w)}</span>'
    head = "".join(f'<th scope="col">{esc(l["name"])}</th>' for l in levels) + '<th scope="col">Not in Dolch&rsquo;s 220</th>'
    trs = []
    for L in lists:
        g = "K" if L["grade"] == "K" else f'Gr {L["grade"]}'
        cells = [", ".join(wid(w) for w in L["words"] if w in level_of and level_of[w] is l) for l in levels]
        cells.append(", ".join(wid(w) + (" (a Dolch noun)" if w in nouns else "") for w in L["words"] if w not in level_of))
        trs.append(f'<tr><th scope="row">{L["n"]} &middot; {esc(L["name"])} ({g})</th>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    trs.append('<tr class="off"><th scope="row">Not on the ELP lists</th>' +
               "".join(f'<td>{", ".join(wid(w) for w in l["words"] if w not in list_of)}</td>' for l in levels) + "<td></td></tr>")
    ids = re.findall(r'<span id="([^"]+)">', "".join(trs))
    assert len(ids) == len(set(ids)), "a word appears twice in the table"

    cw = {w: coloured(w) for w in sorted(set(elp_words) | set(level_of))}   # sorted, so a rebuild writes the same page
    data = {"levels": [{"key": l["key"], "name": l["name"], "words": l["words"]} for l in levels],
            "lists": lists, "cw": cw, "short": off_short, "nouns": nouns,
            "cards": {l["key"]: f'cards/dolch-word-cards-{l["key"]}.pdf' for l in levels}}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

    body = f"""{header(0)}
<main>
<section class="hero"><div class="wrap">
<p class="eyebrow">Word lists</p>
<h1>Where the ELP words come from</h1>
<p class="lead">The ELP guide names no source for its high-frequency lists, but {len(shared) + len(noun_hits)} of its {len(elp_words)} words are E. W. Dolch&rsquo;s, from the sight vocabulary he published in 1936. The other {spell(len(elp_only))} ({i(elp_only)}) are on Fry&rsquo;s first 100 Instant Words. The ELP keeps {len(shared)} of Dolch&rsquo;s {n220} words, sorts them by spelling pattern, and leaves out {len(off)}, most of them short-vowel words that phonics lessons teach.</p>
</div></section>

<section class="about wl" id="by-level" aria-labelledby="lv-h"><div class="wrap">
<h2 id="lv-h">Where Dolch&rsquo;s words went</h2>
<p class="sub">Each bar is one of Dolch&rsquo;s five levels, split by the ELP grade whose lists include its words. Tap part of a bar to see its words, sorted by ELP list.</p>
<div class="flow"><ul class="legend">{legend1}</ul><div class="rows">{"".join(rows1)}</div></div>
<div class="detail" id="levels-detail" aria-live="polite"><p class="sub">Tap part of a bar to see its words.</p></div>
</div></section>

<section class="about wl" id="by-list" aria-labelledby="li-h"><div class="wrap">
<h2 id="li-h">Where each ELP list&rsquo;s words came from</h2>
<p class="sub">Each bar is an ELP list, split by the Dolch level its words come from. Pattern lists such as Long vowel silent e draw on four of Dolch&rsquo;s five levels at once.</p>
<div class="flow"><ul class="legend">{legend2}</ul><div class="rows">{"".join(rows2)}</div></div>
<div class="detail" id="lists-detail" aria-live="polite"><p class="sub">Tap part of a bar to see its words.</p></div>
</div></section>

<section class="about" id="table" aria-labelledby="tb-h"><div class="wrap">
<h2 id="tb-h">Every word, by ELP list and Dolch level</h2>
<p class="sub">Each row is an ELP list, in the guide&rsquo;s order, and each column a Dolch level. Every ELP word and every one of Dolch&rsquo;s {n220} appears once, and the last row holds the {len(off)} the ELP lists leave out.</p>
<div class="tablewrap"><table class="wl-table"><thead><tr><th scope="col">ELP list</th>{head}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>
<p class="sub">Dolch&rsquo;s {len(nouns)} nouns are left out of the charts and the table. He kept them off his sight vocabulary, and {i(noun_hits)} is the only one on the ELP lists.</p>
</div></section>

<section class="about" aria-label="Notes"><div class="wrap"><div class="cols">
<div><h3>What the ELP leaves out</h3><p>{len(off_short)} of the {len(off)} are one-syllable short-vowel words, such as <i>big</i>, <i>can</i>, <i>run</i>, <i>stop</i>, <i>best</i> and <i>six</i>. Apart from <i>and</i>, <i>is</i> and <i>it</i> in kindergarten, the ELP&rsquo;s only short-vowel words are on its Digraphs list, so it seems to leave the rest to phonics lessons.</p></div>
<div><h3>Pattern before level</h3><p>A pattern list takes the words that share its pattern, whatever their Dolch level: {len(on_pattern)} of the {len(shared)} shared words are on one. The silent e list pulls {and_list(pulled)} into grade 1 from Dolch&rsquo;s second grade, while the diphthong list holds {len(held_diph)} early words such as {and_list(held_diph[:3])} back to grade 2.</p></div>
<div><h3>Levels aren&rsquo;t grades</h3><p>Pre-primer and primer are named for reading books, and the Utah Reading Clinic puts Dolch&rsquo;s first three levels all in grade 1. Read that way, the ELP has {earlier} of the shared words earlier than Dolch, {same} in the same grade and {later} later.</p></div>
<div><h3>The cards</h3><p>All five of Dolch&rsquo;s levels are on the <a href="cards.html#dolch">Word cards</a> page, coded on the back. Each card&rsquo;s tag names the ELP list that teaches the word, if one does.</p></div>
</div></div></section>

<section class="about" aria-labelledby="src-h"><div class="wrap">
<h2 id="src-h">Sources</h2>
<ul class="sources">{"".join(f"<li>{s}</li>" for s in SOURCES)}</ul>
<p class="sub">The lists were matched by spelling. A short-vowel word here has one syllable and one vowel letter with its short sound, so <i>all</i>, <i>cold</i>, <i>full</i> and <i>live</i> don&rsquo;t count.</p>
</div></section>
</main>
{footer(0)}
<script type="application/json" id="wl-data">{blob}</script>
<script>{SCRIPT}</script>"""
    (OUT / "word-lists.html").write_text(page("Where the ELP words come from · A Legend for English Words", body, 0,
                                              "Where the SD23 ELP high-frequency words come from in E. W. Dolch's sight words: tap a bar to see the words."),
                                         encoding="utf-8")
    print(f"wrote word-lists.html | {len(shared)} shared, {len(off)} left out ({len(off_short)} short-vowel), "
          f"earlier/same/later {earlier}/{same}/{later}, pattern lists {len(on_pattern)}")
