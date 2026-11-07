# Sound and Word Atlas

A route through English spelling for teachers: 32 steps in eight bands, with every word drawn in legomorphic notation. Each step has its own page with its words marked, the marks it brings in, its kernel words and contrasts, and the pages in Edward Carney's *A Survey of English Spelling* (Routledge, 1994) that back it.

The site is at https://dantewetherow.github.io/sound-and-word-atlas/.

## What's where

- `docs/` is the site itself. GitHub Pages publishes this folder as it is.
- `build/` has what makes it:
  - `build_site.py` writes the pages from `data/route.json`.
  - `parse_route.py` turns the manual's route section (`data/route_section.md`) into `data/route.json`.
  - `x2t.py` converts a read of the manual from the Claude Docs connector into markdown.
  - `legomorphic_words.py` draws the marked words.
  - `known_codes.py` and `deck_codes.json` hold the codes the session decks already use, and `site_codes.py` holds the codes written for route words that had none.
  - `build_elp_cards.py`, `build_dolch_cards.py` and `build_word_sum_cards.py` make the printable cards. `dolch_codes.py` holds the codes written for the 43 Dolch words that had none.
  - `word_lists.py` writes the Word lists page, which shows where the ELP words come from in Dolch's lists. Its words come from `data/elp_hfw.json` and `data/dolch.json`, and every count on it is worked out from them.
  - `sessions.py` writes the Presentations page and copies the decks in `sessions/` to the site. The decks there are the web copies: the title slide's byline is left off, and a link in the slide controls leads back to the page. Run as a script, `python3 build/sessions.py <node_modules> docs` makes each deck's offline copy (with `make_offline_deck.py`, which needs `@fontsource-variable/fraunces`, `@fontsource-variable/lexend` and `@fontsource/gentium-plus`) and its preview pictures.
  - `build_handouts.py` makes the Session 1 handouts: `python3 build/build_handouts.py <node_modules> docs/sessions/handouts <a scratch folder>`. It is the atlas tool with one change, a footer that names the session instead of the presenter.
  - `build_role_cards.py` makes the action cards (Dolch's verbs that aren't verb-system cards, on a pale red wash) and the actor cards (twelve pronouns and Dolch's 95 nouns, on a pale green wash) the same way: `python3 build/build_role_cards.py <node_modules> docs/sessions/handouts <a scratch folder>`. It holds the codes written for the nouns and the calls they rest on, which wait under "From the action and actor cards" in the Marking calls tab.
  - `build_verb_cards.py` makes the verb-system cards from `build_handouts.py`'s pieces, with the codes the notation didn't have and the calls they rest on: `python3 build/build_verb_cards.py <node_modules> docs/sessions/handouts <a scratch folder>`. The modal cards (8 October) have no builder; they are the PDFs as made, with the presenter's name taken out of the instruction sheet's footer.
  - `about_pages.py` writes the About page and the Credits page, with the copyright notice and the contact link.
  - `site.css` is the stylesheet.

`LICENSE.md` gives the terms: CC BY-NC-SA 4.0.

## The manual stays the source

The route and its notes come from the *Legomorphic notation* manual. To change what the site says, change the manual, then rebuild. Choices about how a word is marked wait for a ruling in the manual's Marking calls tab, under "From the atlas site", and `site_codes.py` changes to match once they're ruled.

## Rebuilding

1. Read the manual's route section (from "The route" to "The operator system") with the Claude Docs connector, save the result, and convert it with `build/x2t.py`. Keep the part before "## The operator system" as `build/data/route_section.md`.
2. `python3 build/parse_route.py build/data/route_section.md build/data/route.json`
3. To rebuild the word cards, run `npm install @fontsource-variable/lexend` somewhere outside the repository, then `python3 build/build_elp_cards.py <that folder>/node_modules docs/cards <a scratch folder>`. The words come from `build/data/elp_hfw.json`, taken from the SD23 ELP guide (pp. 16–17). The grade 3 word sum cards build the same way with `build/build_word_sum_cards.py`; their word sums come from the manual's Word analysis draft tab and their markings from `build/word_sum_codes.py`, whose `CALLS` wait for a ruling in the manual's Marking calls tab. The Dolch cards build the same way with `build/build_dolch_cards.py`. Their words come from `build/data/dolch.json`, which holds E. W. Dolch's 220 words (1936) at the levels ReadWriteThink prints, with his *going* where its list has *giving*, and his 95 nouns. The codes the decks don't have come from `build/dolch_codes.py`, whose `CALLS` wait under "From the Dolch cards" in the Marking calls tab.
4. `python3 build/build_site.py build/data/route.json docs --standalone`. It writes the Word cards page when the card PDFs are in `docs/cards`, and the Word lists page.
5. Commit and push. Pages republishes the site within a few minutes.

To refresh the deck codes from a copy of the atlas folder, run `python3 build/known_codes.py --refresh /path/to/atlas`.

Without `--standalone`, the home page is written with no doctype or head, which is what the claude.ai artifact version of the site needs.
