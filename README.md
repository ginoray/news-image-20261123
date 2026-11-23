# The World Today — 23 November 2026

[![Competition](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/ginoray/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/ginoray/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

An entry for the make.fun bounty **news-image-20261123** ("Sum up 23
November's world news in one image"). The program writes a single
1024x1024 PNG poster that sums up the world news of Monday
23 November 2026 in the style of a broadsheet front page.

## The seven stories on the poster

1. **Ukraine (lead)** — Russian strikes kill 11 near Kyiv; rescuers pull
   survivors from a collapsed block of flats in Dymer as the regional
   toll climbs. (Reuters, AFP)
2. **Middle East** — Tankers hit near Hormuz and Bahrain blames Iran for
   a strike on a civilian plant; Trump leans toward resuming strikes if
   there is no deal by the New Year. (AFP, CNBC)
3. **Indonesia** — 24 dead in the Banten candy factory fire; the toll is
   confirmed as rescuers search the Cikande plant ruins for about 30
   workers still missing. (Reuters, AP)
4. **United States** — Democrats win 258 House seats, the largest
   majority for either party since 1992. (AP, Reuters)
5. **Markets** — An AI sell-off routs Asian markets; Tokyo's Nikkei
   sank about 5% and the Nasdaq had its worst week since 2020.
   (Reuters, Seeking Alpha)
6. **Libya** — Ukraine sinks the Russian corvette Merkury at Benghazi
   with sea drones, Zelensky confirms. (CNN, WSJ)
7. **Sport** — Liverpool thrash ten-man Manchester United 4-0 at
   Anfield in Mauricio Pochettino's first match in charge. (Reuters,
   Sky Sports)

Every story was checked against at least two independent reports
published on 23 November 2026.

## How it works

- `build_poster.py` renders the poster with Pillow at build time and
  the PNG bytes are sealed as base64 in `poster_data.py`.
- `main.py` (Python 3, standard library only) decodes the sealed bytes
  and writes them directly to `entry.png` in the output directory:
  an explicit path argument wins, then `$MAKEFUN_OUTPUT_DIR`, then
  `/output`. Two runs produce byte-identical output.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
# or: python3 main.py out
```

## License

MIT — see `LICENSE`.
