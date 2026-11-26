# Build notes — The World in One Day, 26 November 2026

## What the entry is

A single dense newspaper front page, 1024 by 1024 pixels, summing up the
world news of Thursday 26 November 2026. The lead story is the
postponement of the 100th Macy's Thanksgiving Day Parade to Saturday
because of a nor'easter, the first weather postponement in the parade's
100-year history. Around it sit 37 further stories: storms across
America, a tanker fire in Cairo, strikes and tariffs, a first astronaut,
sport and business, each one dated and carrying its source.

## How it was built

The builder first read the bounty rules and the earlier lessons learned
from five days of news-image entries, which all lost the same way: too
few stories, no source beside each story, no map, no date check, and
twice a lead story that belonged to the previous day. The build follows
the winning pattern instead: a packed broadsheet, 38 stories in total,
a strip of six key numbers, a numbered world map, and a date-check box
that names the stale stories deliberately left out.

The news was researched from wire and press reports published on
26 November 2026, and every story in the image either happened or was
first reported that day. The postponement itself was announced late on
25 November, but the parade not marching today, and the move to
Saturday, are the news of the 26th, so the lead is phrased around the
day itself. The date-check box records what was excluded: the missile
that landed in Poland on 20 November, the 2008 Mumbai attacks
themselves, and the 2025 parade.

The page is drawn programmatically from the story data, using classic
serif type on a paper background, and the entry program only copies the
finished image to the output directory, so it runs with the standard
library alone and needs no network.

## Verification

The generator was run and the image inspected at full size. Two layout
defects were found and fixed: the key-numbers labels wrapping into the
lead story, and the further-stories list overflowing past the foot of
the page. After the fixes the whole page fits inside the frame, the
date-check box and footer are visible, and every story reads cleanly.

The entry program was then run twice into fresh output directories.
Both runs wrote byte-identical files, with the same checksum as the
image in the repository. The file is 182,674 bytes, inside the one
mebibyte cap, and 1024 by 1024 pixels.
