"""Codes for E. W. Dolch's 95 nouns that the notation didn't mark yet (data/dolch.json, "nouns"), each following the word
named in its comment. The actor cards (build_role_cards.py) and the Dolch noun cards (build_dolch_cards.py) both draw
from here. The calls they rest on are CALLS in build_role_cards.py, and wait in the manual's Marking calls tab under
"From the action and actor cards". Moved here from build_role_cards.py on 8 November 2026."""

NOUN_CODES = {
    "baby": "c.b l.a | c.b b.y ; vault 3>1",                 # as pony
    "ball": "c.b b.a k.ll",                                  # as call
    "bear": "c.b r.ear",                                     # as hear
    "bell": "c.b s.e k.ll",                                  # as tell
    "birthday": "c.b r.ir g.th + | c.d t.ay",                # birth + day, as into
    "box": "c.b s.o c.x",                                    # as six
    "brother": "c.br b.o g.th | r.er",                       # as other
    "cake": "c.c l.a c.k e>",                                # as make
    "chair": "g.ch r.air",                                   # as hair
    "chicken": "g.ch s.i x.ck | b.e c.n ; bv 3>2",           # as pretty and seven
    "children": "g.ch s.i c.l | c.d + c.r b.e c.n",          # child + ren, with the break before d, as making
    "Christmas": "k.Ch c.r s.i k.st + | c.m b.a c.s",        # Christ + mas; ch says k, and st says s, as in mustn't
    "coat": "c.c t.oa c.t",                                  # as boat
    "corn": "c.c r.or c.n",                                  # as for
    "cow": "c.c t.ow",                                       # as how
    "door": "c.d r.oor",                                     # as four
    "duck": "c.d s.u k.ck",                                  # as back
    "egg": "s.e k.gg",                                       # as off
    "eye": "t.eye",                                          # one vowel unit
    "farm": "c.f r.ar c.m",                                  # as warm
    "farmer": "c.f r.ar | c.m + r.er",                       # farm + er, as making
    "father": "c.f b.a g.th | r.er",                         # as water and other
    "feet": "c.f t.ee c.t",                                  # as keep
    "fire": "c.f l.i c.r e>",                                # as here
    "fish": "c.f s.i g.sh",                                  # as wish
    "floor": "c.fl r.oor",                                   # as door
    "flower": "c.fl t.ow | r.er",                            # as brown and water
    "game": "c.g l.a c.m e>",                                # as name
    "garden": "c.g r.ar | c.d b.e c.n",                      # as seven
    "girl": "c.g r.ir c.l",                                  # as bird
    "grass": "c.gr s.a k.ss",                                # as kiss
    "ground": "c.gr t.ou c.nd",                              # as round
    "hand": "c.h s.a c.nd",                                  # as and
    "hill": "c.h s.i k.ll",                                  # as fill
    "horse": "c.h r.or c.s e0",                              # as please
    "house": "c.h t.ou c.s e0",                              # as out and please
    "kitty": "c.k s.i x.tt | b.y ; bv 3>2",                  # as pretty
    "leg": "c.l s.e c.g",                                    # as big
    "letter": "c.l s.e x.tt | r.er ; bv 3>2",                # as better
    "man": "c.m s.a c.n",                                    # as ran
    "men": "c.m s.e c.n",                                    # as ten
    "milk": "c.m s.i c.lk",                                  # as help
    "money": "c.m b.o c.n | t.ey",                           # as many, with ey as in they
    "morning": "c.m r.or c.n + | s.i k.ng",                  # morn + ing, as heading
    "mother": "c.m b.o g.th | r.er",                         # as other
    "nest": "c.n s.e c.st",                                  # as best
    "party": "c.p r.ar | c.t b.y",                           # as only
    "picture": "c.p s.i c.c | c.t r.ur e0",                  # as were
    "pig": "c.p s.i c.g",                                    # as big
    "rabbit": "c.r s.a x.bb | s.i c.t ; bv 3>2",             # as better
    "ring": "c.r s.i k.ng",                                  # as sing
    "robin": "c.r s.o c.b | s.i c.n",                        # as lemon and napkin
    "Santa": "c.S s.a c.n | c.t b.a",                        # as under, with a bare final a
    "Claus": "c.Cl t.au c.s",                                # as because
    "school": "c.s k.ch t.oo c.l",                           # ch says k
    "seed": "c.s t.ee c.d",                                  # as see
    "sheep": "g.sh t.ee c.p",                                # as sleep
    "shoe": "g.sh t.oe",                                     # as blue
    "sister": "c.s s.i c.s | c.t r.er",                      # as after
    "snow": "c.sn t.ow",                                     # as grow
    "song": "c.s s.o k.ng",                                  # as long
    "squirrel": "c.s q.qu r.ir | c.r b.e c.l",              # qu on its black bar, q and u saying k and w; ir as in bird
    "stick": "c.st s.i k.ck",                                # as pick
    "street": "c.str t.ee c.t",                              # as stroll and green
    "thing": "g.th s.i k.ng",                                # as sing
    "top": "c.t s.o c.p",                                    # as hop
    "tree": "c.tr t.ee",                                     # as try and three
    "watch": "c.w b.a g.tch",                                # as wash and catch
    "way": "c.w t.ay",                                       # as day
    "wind": "c.w s.i c.nd",                                  # the noun, with a short i, unlike find
    "window": "c.w s.i c.n | c.d t.ow",                      # as yellow
    "wood": "c.w t.oo c.d",                                  # as good
}
