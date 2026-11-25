#!/usr/bin/env python3
"""The Internet in One Word — make.fun bounty entry.

The brief: describe the whole internet in a single word. The entry is
that word and nothing else — no files, no code, no links. A judge model
compares entries two at a time, weighing, in this order:

1. Is it a single word that describes the whole internet?
2. Does it earn a laugh by itself, with no explanation needed?
3. Does it say something true about the internet as a whole, rather
   than one app, one site, or one mood?
4. Does it surprise — is it not the first obvious word anyone
   would reach for?
5. Does it land in one beat — spelled correctly, instantly readable,
   short enough to hit before the reader thinks?

The program below scores a shortlist of candidate words on those five
published criteria and writes the deterministic winner to
/output/entry.txt. Same input, same scores, same word, every run.
Only the winning word goes to stdout, because the word is the
whole entry.
"""

import os

# Candidate words, each scored 0-10 on the five published criteria:
# single — is it one word that can stand for the whole internet?
# funny  — does it land as a joke on its own?
# true   — does it say something true about the internet as a whole?
# fresh  — is it surprising, not the first obvious word?
# lands  — spelled correctly, instantly readable, short enough to hit?
CANDIDATES = [
    # word,                single, funny, true, fresh, lands
    ("pandemonium", 10, 9, 10, 9, 8),
    # The whole internet is pandemonium: a roaring crowd, everyone
    # shouting at once, a capital of demons holding a permanent
    # convention. It makes a reader laugh and then nod — that is
    # exactly the brief's "best word". It is a real, correctly
    # spelled English word, eleven letters, one beat. And it is
    # fresh: none of the 289 entries already in uses it, while the
    # obvious words below are all taken many times over.
    ("hivemind", 10, 7, 9, 8, 9),
    # True — the internet thinks as one deranged brain — and short,
    # but more of a nod than a laugh. Pandemonium is the funnier
    # picture of the same crowd.
    ("discourse", 10, 8, 9, 8, 8),
    # "The discourse" is itself an internet joke, and it is true of
    # the whole place. But it is insider slang: a comedy editor
    # laughs, a stranger shrugs. Pandemonium needs no context.
    ("oversharing", 10, 8, 9, 7, 7),
    # True — the whole internet is oversharing — and funny. But it
    # describes a habit, not the place itself, and it is eleven
    # letters of plain description where pandemonium is a scene.
    ("funhouse", 10, 8, 7, 8, 9),
    # A funhouse of distorted mirrors is a good picture, but it
    # leans on the metaphor: you have to picture the mirrors first.
    # Pandemonium is the noise itself, no metaphor required.
    ("bedlam", 10, 7, 8, 8, 9),
    # Short, chaotic, true. But "bedlam" is a quieter word — it
    # reports the chaos where pandemonium performs it.
    ("arguing", 10, 7, 9, 6, 9),
    # Very true — the internet is arguing, always — but it is one
    # activity among many, not the whole place, and it is not
    # surprising: everyone reaches for it.
    ("whatever", 10, 7, 6, 7, 10),
    # A dry shrug, funny in its own way, and it lands instantly.
    # But it says more about a mood than about the internet itself.
    ("literally", 10, 7, 6, 7, 9),
    # The internet misuses "literally" constantly, which is funny —
    # but the joke is about a word, not about the whole internet.
    ("dopamine", 10, 6, 8, 7, 8),
    # True — a dopamine machine — but clinical, not funny. It
    # explains the internet instead of describing it.
    ("content", 10, 7, 8, 7, 10),
    # Dry and funny — everything online is "content" now — but the
    # laugh is a knowing smirk, and the word is flat on its own.
    ("everyone", 10, 6, 8, 8, 10),
    # The internet is everyone, all at once, shouting. Clever and
    # surprising, but the laugh is thin: it states a fact.
    ("zoo", 10, 7, 7, 6, 10),
    # Short, funny, instantly readable. But "circus" is already an
    # entry, the animal-metaphor lane is crowded, and a zoo is a
    # place you visit — the internet is a place you live in.
    ("echochamber", 10, 5, 8, 5, 7),
    # True, but a political-science cliché by now: the opposite of
    # surprising, and eleven letters of lecture.
    ("parasocial", 10, 6, 8, 8, 7),
    # True and fresh, but insider vocabulary — it does not land in
    # one beat for a reader who never met the word.
    ("cacophony", 10, 6, 8, 8, 7),
    # A true description of the noise, and surprising — but it
    # sounds like a vocabulary test, not a joke.
    ("maincharacter", 10, 8, 7, 7, 6),
    # Funny — everyone online is the main character — but thirteen
    # letters, and it describes the users, not the internet.
    ("chronicallyonline", 10, 8, 8, 6, 5),
    # Funny and true, but seventeen letters: it does not land in
    # one beat, it arrives by paragraph.
    ("nothing", 10, 6, 6, 7, 10),
    # Philosophical and dry — the internet is everything and
    # nothing — but the laugh is a shrug, not a joke.
    ("everything", 10, 5, 7, 5, 8),
    # True in the dullest way: it says everything and therefore
    # nothing in particular.
    # The obvious words, scored honestly and rejected: each is funny
    # and true, but each is the FIRST word anyone reaches for, and
    # each is already an entry many times over — so each fails the
    # brief's surprise criterion outright.
    ("feral", 10, 8, 7, 1, 10),
    # The single most-entered word in the field. Funny, true — and
    # everybody already said it.
    ("brainrot", 10, 8, 7, 1, 9),
    # The obvious diagnosis of the internet, entered over and over.
    ("doomscrolling", 10, 7, 8, 1, 6),
    # True of a habit, not of the whole place — and the second most
    # entered word in the field.
    ("enshittification", 10, 8, 9, 2, 4),
    # The truest word on this list and the funniest diagnosis — but
    # seventeen letters, hard to land in one beat, and entered
    # repeatedly already.
    ("unhinged", 10, 8, 6, 1, 9),
    # Funny, but one mood among many, and entered many times over.
    ("slop", 10, 7, 7, 2, 10),
    # Short and punchy, but it describes the content, not the place,
    # and it is already taken.
]

# The brief lists its criteria most important first, so the weights
# follow that order: being a single word matters most, then the
# laugh, then the truth, then the surprise, then the landing.
WEIGHTS = {"single": 3.0, "funny": 2.0, "true": 2.0, "fresh": 1.5, "lands": 1.0}

# The brief's hard limit: the entry is 1 to 30 characters.
WORD_LIMIT = 30


def score(candidate):
    """Total score for one candidate: the weighted sum of its five marks."""
    _word, single, funny, true, fresh, lands = candidate
    return (
        WEIGHTS["single"] * single
        + WEIGHTS["funny"] * funny
        + WEIGHTS["true"] * true
        + WEIGHTS["fresh"] * fresh
        + WEIGHTS["lands"] * lands
    )


def pick_word():
    """Pick the single best word, deterministically.

    Highest total wins. Ties break alphabetically so the choice can
    never depend on ordering or chance.
    """
    ranked = sorted(CANDIDATES, key=lambda c: (-score(c), c[0]))
    return ranked[0][0]


def main():
    word = pick_word()
    # The entry must be exactly one word: a single alphabetic token,
    # no spaces, no punctuation, within the brief's length limit.
    assert word.isalpha(), "entry must be a single word"
    assert " " not in word and "-" not in word, "entry must be one token"
    assert 1 <= len(word) <= WORD_LIMIT, "entry must fit the 30-character limit"
    # The brief's deliverable: the program writes one text to
    # /output/entry.txt. Also print only the word, so a harness that
    # reads stdout sees exactly the entry and nothing else.
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(word)
    print(word)


if __name__ == "__main__":
    main()
