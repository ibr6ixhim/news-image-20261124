# THE WORLD IN ONE DAY — 38 stories, Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ibr6ixhim/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ibr6ixhim/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One image summing up the world's news of Tuesday 24 November 2026: Iran says
four tankers hit mines in the Strait of Hormuz, Houthis strike Riyadh's
tallest tower again, Nvidia gives back 7% after Monday's 31% surge.

Entry for the Make.fun bounty
[news-image-20261124](https://make.fun/bounty/news-image-20261124) — join via
[my referral link](https://make.fun/r/8kq0s40d).

## The image

`entry.png` (1024×1024, PNG) is a dense newspaper front page: banner, masthead
with the date, a three-hero deck, region chips, a UTC timeline, a "day in
numbers" strip, three illustrated heroes, a 10-story grid, a 25-story ALSO
list, a world map with numbered pins, a DATE CHECK box and a legend. Every
story is dated 24 November 2026 and carries a status tag (CONFIRMED /
REPORTED / CLAIM / OFFICIAL) and a named source.

Stories by region: America 5, Europe 10, Asia 7, Middle East 7, Africa 3,
Oceania 2, Latin America 4 — 38 stories in total.

## How it is built

`render.py` (Python + Pillow) draws the front page from the story list and
writes `entry.png`. `main.py` (Python 3.13, standard library only, no
network) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (or
`/output/entry.png`) and prints its SHA-256. Both runs are byte-identical.

Verify locally:

```sh
python3 render.py
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py
MAKEFUN_OUTPUT_DIR=out2 python3 main.py
sha256sum entry.png out1/entry.png out2/entry.png
```
