"""Connections, the eighth door (8 November 2026): crosswalks from the route and its words to the lists and programs schools
already use. doors.py writes the door page through write(); the pages behind it are:

- word-lists.html (word_lists.py): where the ELP words come from in Dolch's lists, the first crosswalk
- ufli.html: where each route step meets UFLI Foundations, by lesson number. UFLI's copyright statement allows original
  work made to line up with its scope and sequence, and asks for links rather than copies, so the page gives lesson numbers
  and our own descriptions, never UFLI's lesson names, and links to UFLI's own scope and sequence. The numbers and notes are
  in data/ufli_crosswalk.json. Since 12 November 2026 it also draws a lesson-by-step chart whose dots link to the
  spelling lists by UFLI lesson (ufli_lists.py).

Fry's Instant Words are still under copyright (Edward Fry died in 2010; Teacher Created Resources publishes them), so the
door page compares them in counts and a few words and links to the publisher, and the site makes no Fry cards. The counts
come from FRY_COUNTS below, worked out once from the first 100 as printed; two versions in circulation differ by a word or
two, which is why some counts are given as a range.
"""
import html, json, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent

FRY_PUBLISHER = "https://www.teachercreated.com/company/partnerships/dr-edward-fry.php"
FRY_COUNTED = "https://www.uen.org/earlylearning/word_lists.shtml"        # the copy the counts were made from
UFLI_COPYRIGHT = "https://ufli.education.ufl.edu/copyright/"
FRY_COUNTS = {"in_dolch": "86 or 87", "dolch_nouns": ["day", "time", "water", "way"], "neither": "about ten",
              "elp": "64 or 65", "elp_only": ["each", "other", "people"]}


def ranges(nums):
    """[24, 25, 26, 27, 30] -> '24–27, 30'"""
    nums = sorted(set(nums)); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(str(nums[i]) if j == i else (f"{nums[i]}, {nums[j]}" if j == i + 1 else f"{nums[i]}&ndash;{nums[j]}")); i = j + 1
    return ", ".join(out)


def italics(s):
    """The example words of a contrast or note in italic: would, could and should, ay, ee and igh."""
    return re.sub(r"\b(would|could|should|will|spell|my|it|I|oul|ay|ee|igh|ll|ss|ck|tch|th|wh|y)\b(?![^<]*>)", r"<i>\1</i>", html.escape(s))


def _chart(D, has_list, STEPS):
    """The visual crosswalk: UFLI lessons across, route steps down, a dot where a lesson lands on a step."""
    L0, L1, S1 = 1, D["of"], len(STEPS)
    x0, y0, W, H = 64, 26, 900, 31 * 15
    X = lambda l: x0 + (l - L0) / (L1 - L0) * W
    Y = lambda s: y0 + (s - 1) / (S1 - 1) * H
    title = {st["n"]: re.sub(r"\*([^*]+)\*", r"\1", st["title"]) for st in STEPS}
    g = [f'<line class="ch-diag" x1="{X(L0):.1f}" y1="{Y(1):.1f}" x2="{X(L1):.1f}" y2="{Y(S1):.1f}"/>']
    for l in range(10, L1 + 1, 10):
        g.append(f'<line class="ch-grid" x1="{X(l):.1f}" y1="{y0 - 6}" x2="{X(l):.1f}" y2="{y0 + H + 4}"/><text class="ch-tx" x="{X(l):.1f}" y="{y0 + H + 22}" text-anchor="middle">{l}</text>')
    for s in [1, 5, 10, 15, 20, 25, 30, S1]:
        g.append(f'<text class="ch-tx" x="{x0 - 12}" y="{Y(s) + 4:.1f}" text-anchor="end">{s}</text>')
    g.append(f'<text class="ch-ax" x="{x0 + W / 2:.0f}" y="{y0 + H + 44}" text-anchor="middle">UFLI lesson</text>')
    g.append(f'<text class="ch-ax" x="16" y="{y0 + H / 2:.0f}" text-anchor="middle" transform="rotate(-90 16 {y0 + H / 2:.0f})">Step on the route</text>')
    for s, v in sorted(D["map"].items(), key=lambda kv: int(kv[0])):
        for l in v["lessons"]:
            tip = f"Lesson {l} · step {s}: {title[int(s)]}"
            if l in has_list:
                g.append(f'<a href="lists/{has_list[l]}.html"><circle class="ch-dot on" cx="{X(l):.1f}" cy="{Y(int(s)):.1f}" r="5"><title>{html.escape(tip)}. Open its spelling list.</title></circle></a>')
            else:
                g.append(f'<circle class="ch-dot" cx="{X(l):.1f}" cy="{Y(int(s)):.1f}" r="4.5"><title>{html.escape(tip)}</title></circle>')
    return (f'<div class="tablewrap ch-wrap"><svg class="ufli-chart" viewBox="0 0 {x0 + W + 20} {y0 + H + 56}" role="img" '
            f'aria-label="UFLI lessons across, steps of the route down: each lesson as a dot at the step where it lands.">{"".join(g)}</svg></div>')


def write(OUT, door_page, door_head, uc, X):
    md, groups_of = X["md"], X["groups_of"]
    D = json.loads((HERE / "data" / "ufli_crosswalk.json").read_text(encoding="utf-8"))

    # ---- the door page
    tiles = ('<div class="door-tiles">'
             '<a class="dtile" href="word-lists.html"><b>Early Literacy Profile and Dolch</b><span>Where the Early Literacy Profile (Central Okanagan) high-frequency words come from in E. W. Dolch&rsquo;s 1936 lists, and what the ELP leaves out.</span></a>'
             '<a class="dtile" href="ufli.html"><b>UFLI Foundations</b><span>Where each step of the route meets UFLI&rsquo;s lessons, by lesson number, and where the two orders part.</span></a>'
             '</div>')
    F = FRY_COUNTS
    fry = f"""<section class="about" id="fry" aria-labelledby="fry-h"><div class="wrap prose">
<h2 id="fry-h">Fry&rsquo;s Instant Words</h2>
<p>Edward Fry&rsquo;s first 100 Instant Words overlap Dolch&rsquo;s heavily: {F["in_dolch"]} of them are among Dolch&rsquo;s 220 sight words, four more are Dolch nouns (<i>{"</i>, <i>".join(F["dolch_nouns"][:-1])}</i> and <i>{F["dolch_nouns"][-1]}</i>), and {F["neither"]} are on neither of his lists. Of the 100, {F["elp"]} are on the ELP lists, among them the three ELP words Dolch doesn&rsquo;t have: <i>{F["elp_only"][0]}</i>, <i>{F["elp_only"][1]}</i> and <i>{F["elp_only"][2]}</i>.</p>
<p>Fry&rsquo;s lists are still under copyright, so they aren&rsquo;t reproduced here and the site makes no Fry cards. Teacher Created Resources publishes them: <a href="{FRY_PUBLISHER}">Dr. Edward Fry</a>. The counts come from the first 100 as the <a href="{FRY_COUNTED}">Utah Education Network</a> prints them. Versions in circulation differ by a word or two, so some counts are ranges.</p>
</div></section>"""
    door_page("connections", "Connections · A Legend for English Words", "How the route lines up with the word lists and programs schools already use.",
              f"""{door_head("connections")}
<section class="about"><div class="wrap">
{tiles}
</div></section>
{fry}
<section class="about"><div class="wrap">
{uc("next, a crosswalk for any program a school runs alongside the route, each built the same way: step by step, by the program&rsquo;s own numbers, in our own words.")}
</div></section>""")

    # ---- the UFLI crosswalk
    import ufli_lists
    has_list = {e["n"]: e["slug"] for e in ufli_lists.entries()}
    def lesson_nums(ls):
        """The lesson numbers as ranges, with a link wherever a lesson has a spelling list."""
        txt = ranges(ls)
        return re.sub(r"\d+", lambda m: f'<a href="lists/{has_list[int(m.group())]}.html">{m.group()}</a>' if int(m.group()) in has_list else m.group(), txt)
    chart = _chart(D, has_list, X["STEPS"])
    import ufli_lessons
    inv = {}
    for s_, v in D["map"].items():
        for l in v["lessons"]: inv.setdefault(l, []).append(int(s_))
    lrows = []
    for n, v in sorted(ufli_lessons.L.items()):
        num = f'<a href="lists/{has_list[n]}.html">{n}</a>' if n in has_list else str(n)
        st = ", ".join(f'<a href="steps/{k:02d}.html">{k}</a>' for k in sorted(inv.get(n, [])))
        if v is None:
            lrows.append(f'<tr class="rev"><th scope="row">{num}</th><td colspan="2">Review: no new mark.</td><td>{st}</td></tr>')
        else:
            lrows.append(f'<tr><th scope="row">{num}</th><td>{v[0]}</td><td>{v[1]}</td><td>{st}</td></tr>')
    by_lesson = (f'<div class="tablewrap"><table class="cw-table ul-table"><thead><tr><th scope="col">Lesson</th><th scope="col">What it brings in</th>'
                 f'<th scope="col">What the notation adds</th><th scope="col">Step</th></tr></thead><tbody>{"".join(lrows)}</tbody></table></div>')
    rows = []
    for st in X["STEPS"]:
        n = st["n"]; m = D["map"][str(n)]
        words = [w for g in groups_of(st["words_md"]) for w in g]
        shown = ", ".join(f"<i>{html.escape(w)}</i>" for w in words[:6]) + (", &hellip;" if len(words) > 6 else "")
        lessons = f'<span class="nums">{lesson_nums(m["lessons"])}</span>' if m["lessons"] else '<span class="nums none">none</span>'
        note = f'<p class="cw-note">{italics(m["note"])}</p>' if m.get("note") else ""
        rows.append(f'<tr><th scope="row"><a href="steps/{n:02d}.html">{n}</a></th>'
                    f'<td><p class="cw-t">{md(st["title"])}</p><p class="cw-w">{shown}</p></td>'
                    f'<td>{lessons}{note}</td></tr>')
    parts = "".join(f'<tr><th scope="row">{italics(c["what"])}</th><td>{html.escape(c["route"])}</td><td>{html.escape(c["ufli"])}</td></tr>'
                    for c in D["contrasts"])
    body = f"""<section class="hero"><div class="wrap">
<p class="eyebrow t-only">For teachers</p>
<h1>UFLI Foundations</h1>
<p class="lead">Everything on this site for schools that run UFLI Foundations, by UFLI&rsquo;s own lesson numbers: spelling lists for each lesson, the mark to draw at each lesson, and where each of its {D["of"]} lessons meets the route.</p>
<p class="ufli-nav"><a href="#lists">Spelling lists</a> &middot; <a href="#lessons">What the notation adds</a> &middot; <a href="#chart">Lesson by step</a> &middot; <a href="#steps">Step by step</a> &middot; <a href="#part">Where the orders part</a> &middot; <a href="lists/index.html">Legomorphic spelling</a></p>
<p class="sub">{html.escape(D["made"])} UFLI asks that its materials be linked rather than copied (its <a href="{UFLI_COPYRIGHT}">copyright statement</a> says so), so its lesson names stay on its own site: its scope and sequence is in the <a href="{D["link"]}">UFLI Foundations Toolbox</a>. The spelling lists below follow the same rule: lesson numbers, our descriptions, our words.</p>
</div></section>
<section class="about" id="lists" aria-labelledby="ls-h"><div class="wrap">
<h2 id="ls-h">Spelling lists by lesson</h2>
<p class="sub">A list for each lesson that adds a new spelling. Every word uses only what UFLI has taught by that lesson, and none is taken from UFLI&rsquo;s materials. So far the kindergarten and grade 1 lessons, 4 to 110; grade 2 is next. The <a href="lists/index.html">Legomorphic spelling</a> lists follow the route instead.</p>
<div class="step-btns">{"".join(f'<a class="sbtn" href="lists/{e["slug"]}.html"><b>Lesson {e["n"]}</b><span>{re.sub(r"<[^>]+>", "", e["what"])}</span></a>' for e in ufli_lists.entries())}</div>
</div></section>
<section class="about" id="chart" aria-labelledby="ch-h"><div class="wrap">
<h2 id="ch-h">Lesson by step</h2>
<p class="sub">Each dot is a UFLI lesson (across) at the step of the route where it lands (down). Dots on the grey line come in the same order in both; above it, the route gets there sooner. A filled dot has a spelling list: tap it to open the list.</p>
{chart}
<p class="sub">Some lessons land on more than one step, so they have more than one dot. Lessons with no dot are reviews or have no step of their own.</p>
</div></section>
<section class="about" id="lessons" aria-labelledby="ul-h"><div class="wrap">
<h2 id="ul-h">Lesson by lesson: what the notation adds</h2>
<p class="sub">For a teacher in the middle of UFLI: the mark to draw on the day&rsquo;s words. Both columns are in our own words; UFLI&rsquo;s lesson titles are in its own materials. A linked lesson number opens its spelling list, and a linked step opens the step.</p>
{by_lesson}
<p class="sub">Lessons 13 to 128 were checked against the headings of UFLI&rsquo;s Roll and Read pages; lessons 1 to 12 have none, and are the ones to check.</p>
</div></section>
<section class="about" id="steps" aria-labelledby="cw-h"><div class="wrap">
<h2 id="cw-h">Step by step</h2>
<div class="tablewrap"><table class="cw-table"><thead><tr><th scope="col">Step</th><th scope="col">What the route teaches</th><th scope="col">UFLI lessons</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
</div></section>
<section class="about" id="part" aria-labelledby="pt-h"><div class="wrap">
<h2 id="pt-h">Where the two orders part</h2>
<div class="tablewrap"><table class="cw-table"><thead><tr><th scope="col">What</th><th scope="col">The route</th><th scope="col">UFLI</th></tr></thead><tbody>{parts}</tbody></table></div>
<p class="sub">{html.escape(D["source"])}</p>
</div></section>"""
    door_page("ufli", "UFLI Foundations · A Legend for English Words", "For schools that run UFLI Foundations: spelling lists by lesson, what the notation adds at each lesson, and where the lessons meet the route.", body)
