"""Connections, the eighth door (8 November 2026): crosswalks from the route and its words to the lists and programs schools
already use. doors.py writes the door page through write(); the pages behind it are:

- word-lists.html (word_lists.py): where the ELP words come from in Dolch's lists, the first crosswalk
- ufli.html: where each route step meets UFLI Foundations, by lesson number. UFLI's copyright statement allows original
  work made to line up with its scope and sequence, and asks for links rather than copies, so the page gives lesson numbers
  and our own descriptions, never UFLI's lesson names, and links to UFLI's own scope and sequence. The numbers and notes are
  in data/ufli_crosswalk.json.

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


def write(OUT, door_page, door_head, uc, X):
    md, groups_of = X["md"], X["groups_of"]
    D = json.loads((HERE / "data" / "ufli_crosswalk.json").read_text(encoding="utf-8"))

    # ---- the door page
    tiles = ('<div class="door-tiles">'
             '<a class="dtile" href="word-lists.html"><b>ELP and Dolch</b><span>Where the ELP high-frequency words come from in E. W. Dolch&rsquo;s 1936 lists, and what the ELP leaves out.</span></a>'
             '<a class="dtile" href="ufli.html"><b>UFLI Foundations</b><span>Where each step of the route meets UFLI&rsquo;s lessons, by lesson number, and where the two orders part.</span></a>'
             '</div>')
    F = FRY_COUNTS
    fry = f"""<section class="about" id="fry" aria-labelledby="fry-h"><div class="wrap prose">
<h2 id="fry-h">Fry&rsquo;s Instant Words</h2>
<p>Edward Fry&rsquo;s first 100 Instant Words overlap Dolch&rsquo;s heavily: {F["in_dolch"]} of them are among Dolch&rsquo;s 220 sight words, four more are Dolch nouns (<i>{"</i>, <i>".join(F["dolch_nouns"][:-1])}</i> and <i>{F["dolch_nouns"][-1]}</i>), and {F["neither"]} are on neither of his lists. Of the 100, {F["elp"]} are on the ELP lists, among them the three ELP words Dolch doesn&rsquo;t have: <i>{F["elp_only"][0]}</i>, <i>{F["elp_only"][1]}</i> and <i>{F["elp_only"][2]}</i>.</p>
<p>Fry&rsquo;s lists are still under copyright, so they aren&rsquo;t reproduced here and the site makes no Fry cards. Teacher Created Resources publishes them: <a href="{FRY_PUBLISHER}">Dr. Edward Fry</a>. The counts come from the first 100 as the <a href="{FRY_COUNTED}">Utah Education Network</a> prints them. Versions in circulation differ by a word or two, so some counts are ranges.</p>
</div></section>"""
    door_page("connections", "Connections · Sound and Word Atlas", "How the route lines up with the word lists and programs schools already use.",
              f"""{door_head("connections")}
<section class="about"><div class="wrap">
{tiles}
</div></section>
{fry}
<section class="about"><div class="wrap">
{uc("next, a crosswalk for any program a school runs alongside the route, each built the same way: step by step, by the program&rsquo;s own numbers, in our own words.")}
</div></section>""")

    # ---- the UFLI crosswalk
    rows = []
    for st in X["STEPS"]:
        n = st["n"]; m = D["map"][str(n)]
        words = [w for g in groups_of(st["words_md"]) for w in g]
        shown = ", ".join(f"<i>{html.escape(w)}</i>" for w in words[:6]) + (", &hellip;" if len(words) > 6 else "")
        lessons = f'<span class="nums">{ranges(m["lessons"])}</span>' if m["lessons"] else '<span class="nums none">none</span>'
        note = f'<p class="cw-note">{italics(m["note"])}</p>' if m.get("note") else ""
        rows.append(f'<tr><th scope="row"><a href="steps/{n:02d}.html">{n}</a></th>'
                    f'<td><p class="cw-t">{md(st["title"])}</p><p class="cw-w">{shown}</p></td>'
                    f'<td>{lessons}{note}</td></tr>')
    parts = "".join(f'<tr><th scope="row">{italics(c["what"])}</th><td>{html.escape(c["route"])}</td><td>{html.escape(c["ufli"])}</td></tr>'
                    for c in D["contrasts"])
    body = f"""<section class="hero"><div class="wrap">
<p class="eyebrow t-only">Connections</p>
<h1>The route and UFLI Foundations</h1>
<p class="lead">Where each step of the route meets UFLI Foundations, by lesson number, so a school that runs UFLI can see where a step lands in its {D["of"]} lessons, and where the two orders part.</p>
<p class="sub">{html.escape(D["made"])} UFLI asks that its materials be linked rather than copied (its <a href="{UFLI_COPYRIGHT}">copyright statement</a> says so), so its lesson names stay on its own site: its scope and sequence is in the <a href="{D["link"]}">UFLI Foundations Toolbox</a>.</p>
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
    door_page("ufli", "The route and UFLI Foundations · Sound and Word Atlas", "Where each step of the route meets UFLI Foundations, by lesson number.", body)
