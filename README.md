# The World in One Day — 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/donatfarm01/world-in-one-day-26-nov/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/donatfarm01/world-in-one-day-26-nov/reward.svg)](https://make.fun/bounty/news-image-20261126)

One dense newspaper front page summing up the world news of Thursday
26 November 2026: the Macy's Thanksgiving parade postponed by a
nor'easter, storms across America, a deadly tanker fire in Cairo, and
35 further stories from every region — every one dated, sourced, and
checked against the previous day.

## How it works

`main.py` (Python 3.13, standard library only) copies the front page
`entry.png` to the output directory. The page itself is drawn by
`gen_image.py`, run in-session from the day's verified news: masthead,
key-numbers strip, three big stories with a drawn illustration, a
ten-story brief grid, a numbered world map, a further-stories list,
and a date-check box listing the stale stories deliberately left out.

## Run

Set the output directory and run the program; two runs write
byte-identical PNG files of 1024 by 1024 pixels, under the 1 MiB cap.
