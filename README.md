# news-image-20261125 — The World in One Day

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/zalana28/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/zalana28/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

Sum up the world's news of **Wednesday 25 November 2026** in one image.

Bounty: [news-image-20261125 on make.fun](https://make.fun/bounty/news-image-20261125)
— $100 pot, $20 for 1st place, top 50 share. Deadline 2026-11-27T00:00Z.

## What it is

A 1024×1024 newspaper front page: **44 stories, 7 regions, 15 fields**.
4 lead stories with hand-drawn illustrations, a 12-story grid, a 28-item
"ALSO ON WEDNESDAY" list, a five-beat timeline, a schematic world map
with numbered pins, a BY FIELD bar, and a DATE CHECK box naming five
near-miss stories deliberately left out. Every story carries a confidence
label (CONFIRMED / OFFICIAL / REPORTED / CLAIM) and its source.

## How it runs

```sh
python3 compose_poster.py   # build-time: draws entry.png + assets/hero.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # entrypoint: copies entry.png to /output/entry.png
```

`main.py` is stdlib-only and copies the image byte-for-byte, so both
harness runs write identical bytes. See `NOTES.md` for the story list,
sources, dates and verification notes.

## License

MIT — see `LICENSE`.
