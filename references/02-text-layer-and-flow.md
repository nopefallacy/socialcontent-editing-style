# 02 — The text layer and visual flow

Where words go, how big, when they arrive and leave, and how the viewer's eye moves through the frame.

## Contents
1. The flow principle: the centre is the focus
2. The two text positions and the face opposite
3. When to change sides
4. Sizes and line building
5. Timing: groups, entrances, exits
6. Writing captions with `scripts/captions.py`
7. Cards below captions
8. Scene headlines (rack-focus scenes)
9. Hero words behind the head
10. Common text failures

---

## 1. The flow principle: the centre is the focus

Viewers watch the middle of a 4:3 frame. Text that jumps from the far left to the far right makes their eyes
ping-pong and feels uncomfortable — the user called this out directly. So:

- Text lives **just left or just right of centre**, never in the corners.
- **The camera moves, not the text.** To bring text to the other side, the camera swings (pans/zooms) so the
  face moves across and the text appears where the eye already is.
- **Never two stacks flanking the face at once.** One caption stack on screen at a time.

## 2. The two text positions and the face opposite

Positions are in **screen px at the start of the shot** (the kit converts them into the camera plane so the
stack rides the dolly, shrinking a little as the camera pulls out — like the inspo videos).

| layout | face on screen | caption stack (top-centre anchor `tc`) | card under it |
|---|---|---|---|
| **FR** — face right | x ≈ 1030, y ≈ 740 | x ≈ 470, y ≈ 70–84 | x 36–556, top 380 |
| **FL** — face left | x ≈ 410, y ≈ 740 | x ≈ 970, y ≈ 84 | x 884–1404, top 380–404 |
| **C** — centred rest | x ≈ 720 | x ≈ 720, y ≈ 40 (short stack) | none (hero-word moments) |

The text sits in the **sky band above the trees/head** (y ≈ 40–340); the face is framed low (y ≈ 740) so the
sky is free. Measure FACE on real frames first (where the face sits in the raw 4:3 world), then the shot table
places it — see `03-camera-and-face-tracking.md`.

## 3. When to change sides

- Change sides only on (a) an animated camera swing (`move`, 0.9–1.2s, the plane tilts ~2.5° so the text
  tracks), (b) a rack-focus scene, or (c) a centred rest (C) that holds a hero word.
- Stay on a side for **a few sentences** (typically 2–5 caption groups, 8–25s). A side change is a paragraph
  break, so put it where the speaker changes thought.
- The outgoing stack slides off with the swing; the incoming stack must not start until the outgoing one is gone.
- Prefer keeping the side when a card is on screen for a long beat — the card and the captions share the free
  side (video 7 kept the fix card on the left through three shots and moved EASIER to the head instead).

## 4. Sizes and line building

Write each caption group as 1–4 short lines. One line is the hero (big, often the accent word); the others are
small lead/tail lines. Break lines at natural phrase boundaries; 1–3 words per line.

```
58: and see for            ← lead, small
120: *yourself             ← hero, accent (blue on the white swipe)
```
```
58: try to speak in front
64: of the camera
130: *slowly
```

| role | size (world px) |
|---|---|
| lead / tail lines | 58–66 |
| hero line | 112–136 |
| numbers as hero ("10 15 20 *30") | 120 |
| minimum anything on the footage | 58 for captions; 27 for UI text in cards |

Max **3 lines when a card sits under the stack** (a 5-line stack ran into the card in video 7 — split it into
two groups instead).

## 5. Timing: groups, entrances, exits

- Every word enters **on its spoken time** (word-level transcript in edit seconds).
- A group lasts until the next group's first word minus 0.02s — or an explicit `out` that ends sooner (a swing,
  a card exit). Two groups are never visible at once.
- Exit: 0.16s fade + 6px blur ("fade"), or instant ("cut") on a hard cut.
- Words that are said but not worth showing can be hidden (`~word`) — the timing cursor still passes them.
- Don't caption words the viewer will read in a B-roll headline at the same moment; the scene headline replaces
  the caption during a rack scene (its words must still be the spoken words).

## 6. Writing captions with `scripts/captions.py`

Captions are generated, not typed by hand. A `caption_script.py` in the project lists groups in speaking order:

```python
from captions import Script
sc = Script("transcript-snap.json", marker=True)      # marker=True: accent words get the highlighter
sc.begin(0.0)                                          # composition-local time base (the host's data-start)
sc.group("s1", 470, 70, ["58:you have written down", "64:a", "132:*perfect", "64:script"], out=2.0)
sc.skip("and")                                         # a spoken word with no caption
sc.group("s2", 470, 80, ["58:once you try", "112:to *record it"])
sc.skip("perfect")                                     # said while PERFECT rises behind the head
out["ov-a"] = sc.js()
```

**The transcript** `transcript-snap.json` is a JSON list of words in **edit seconds**:
`[{"text": "You", "start": 0.0, "end": 0.38}, {"text": "have", "start": 0.4, …}, …]` (the user's cut step
writes it; "snap" = word starts snapped out of measured pauses). `out=` and every time you pass to captions.py
are in these same transcript seconds; `sc.begin(hostStart)` makes the written K.text times local to the host.

Line syntax: `SIZE:words` · `*word` accent · `~word` hidden · `shown|said` (fix a mishearing:
`come|comes`, `re-record|re+-record`) · `a+b` one token for several spoken words · `word^x` colour class
(e.g. `^x` white for a word over trees). It raises an error if the words don't match the transcript in order
— that is your check that every word is accounted for (aim for N/N words consumed). Matching looks only 12 words
ahead, so `sc.skip(...)` every word of a long stretch you don't caption (a scene's words), in order. Hyphenated
words arrive split ("re", "-record"): write `re-record|re+-record`. Repeated words: the cursor takes the next
occurrence, so order matters.
A group's `out` defaults to the next group's first word — so **the last group in each caption host needs an
explicit `out=`** (before a swing, a hero word or a scene), otherwise it stays on screen until the host ends.
The script writes `K.text(...)` calls between `/*CAPTIONS:start*/` and `/*CAPTIONS:end*/` in each caption
composition. Re-run it after any shot or timing change.

## 7. Cards below captions

- A card lives on the caption's side, **below** the stack (top ≈ 380), left edge ~36 (FR) or right edge ~1404
  (FL). Width ~470–520. It may overlap the edge of the hair; never the face.
- Side labels (`fchip`) branch outward toward the face side on dashed connectors — they may sit over hair (a
  light chip on dark hair reads well) but stop before the face.
- A card enters after the camera has settled (not mid-swing) and leaves before the next swing or hero word.

## 8. Scene headlines (rack-focus scenes)

Top-left, x 100, y 64, anchor `tl`. Two lines: a 66px lead in ink and a 120–140px line with ONE serif-italic
accent word + highlighter. They swap phrase by phrase in sync with speech (fade out 0.16s, next one in):

```js
K.text(tl, W, { x: 100, y: 64, a: "tl", lines: [
  { s: 66,  w: [["some of", T(32.3)], ["those", T(32.86)]] },
  { s: 140, w: [["problems", T(33.14), "s", "m"]] } ], out: T(34.42), outMode: "fade" });
```

Keep the card area (y ≥ ~290) clear of the headline. A light white veil gradient at the top of the scene
(22% → 0 by 45% height) keeps ink readable over the blurred sky.

## 9. Hero words behind the head

The speaker's matte (`hyperframes remove-background` on a 1–1.3s clip) sits above a giant word so their head
and hair pass in front of it. Rules:

- 1 per ~30–40s, on the beat's emotional word: PERFECT (the trap), EASIER (the payoff), DONE (the close).
- 220–290px InterK, ink (or white on dark), centred on the head's x, in a shot where the head sits under it (a
  centred rest, or move the word to where the head is: x ≈ 1010 for an FR shot).
- Vertical placement: the lower ~30% of the letters must pass **behind the hair**. Find the top of the head on
  screen at that shot (snapshot), then set the word's top ≈ head top − 0.7 × size. With a 240px word and the
  head top at y ≈ 320, top ≈ 150. Check the frame: the hair must overlap the letters' bottoms.
- The word must end **before** the matte clip ends (else it pops in front). Word 0.75–0.95s; matte ≈ word ± 0.2s.
- Caption the words around it, skip the hero word itself in the captions (`sc.skip("perfect")`).
- Fit: width ≈ 0.6 × size × letters (220px "easier" ≈ 790px). Keep it ≤ ~1,000px: prefer words of ≤ 7 letters,
  or drop the size. If the word repeats in the take, use the occurrence the speaker stresses.

## 10. Common text failures (all happened once)

| failure | fix |
|---|---|
| headline didn't match the spoken words | use the actual words; rewrite the B-roll headline from the transcript |
| a 5-line stack ran into the card | split the group; max 3 lines over a card |
| two captions visible at once (explicit `out` past the next group) | captions.py clamps `out` to the next group's start |
| text tiny inside a scene (clip labels 19–26px) | pills 35px, row labels 36px, state labels 31px, nothing under 27px |
| words entering with a one-axis SVG smear → vertical stripes at 4K | soft CSS blur + glide entrance only |
| inline elements with opacity 0 still taking layout space → gaps | absolute-position or remove hidden inline tags |
| GSAP `x/y` tween wiping a CSS `translateX(-50%)` | centre with `xPercent` in GSAP or with margins, not CSS transforms |
