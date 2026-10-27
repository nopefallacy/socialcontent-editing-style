# 06 — Quality gates (before any draft goes to the user)

The user reviews drafts on a phone, pauses on frames, and calls out anything that looks like a glitch. Find it
first. Run all of this on the 720p draft before sending.

## Contents
1. Which frames to look at
2. The frame checklist
3. Automated checks
4. The B-roll self-review
5. Sending the draft

---

## 1. Which frames to look at

Extract frames from the rendered draft (or HyperFrames snapshots) and tile them into contact sheets
(`scripts/sheet.sh draft.mp4 out.jpg t1 t2 …`). Always include:
- the first and last frame of **every shot** (the dolly moves things);
- every **shot change** ±0.1s (outgoing stack vs incoming group);
- every **card state change** (a step ticking, a label pinning, a toggle flipping) — at the moment and 0.5s after;
- the start, middle and end of **every rack scene**, and 0.2s after the rack-out;
- every **hero word** at its peak;
- a sweep every 2s across the whole video for anything you didn't plan.

## 2. The frame checklist

Layout and flow
- [ ] Nothing covers the eyes, nose or mouth — in any frame of any shot (hair edges are fine).
- [ ] One caption stack on screen at a time; no stack collides with a card or a headline.
- [ ] Captions sit just left or just right of centre, in the sky band; no ping-pong between consecutive groups.
- [ ] Cards sit below the caption on the free side, never mid-swing over the face.

Readability
- [ ] Caption lines ≥ 58px (world), UI text ≥ 27–31px; read the frame at phone size (≈ 1/3 of a 1440 frame) —
  can you read every word?
- [ ] Ink on light sky, white on dark; accent words on their highlighter; no blue-on-blue.
- [ ] Headlines in scenes are the actual spoken words.

Surfaces
- [ ] Every card is translucent: the background is visibly blurred through it. No flat white boxes.
- [ ] No empty card space (cards grow with their steps); no half-empty scene.
- [ ] Icons render (a blank white circle means an icon class collision — e.g. a global `.ico` rule).
- [ ] Counters show clean glyphs (odd characters mean a roller column too narrow for a symbol — put symbols
  outside the roller).

Motion
- [ ] No two groups/cards from different beats visible at a shot change.
- [ ] Entrances have no stripes or banding at 4K (soft blur entrances only).
- [ ] Rack-outs land on the next shot (a brief soft frame is fine; a long blurry gap is not).

Edges and footage
- [ ] No exposed frame edges (black bars) anywhere — tracking and swings are clamped to the overscan.
- [ ] Hero words end before their matte clip ends; the head passes in front of them.

## 3. Automated checks

```bash
# exposed edges: any crop narrower than the frame = black showing (720p draft)
ffmpeg -i draft.mp4 -vf "fps=4,cropdetect=limit=0.06:round=2:reset=1" -f null - 2>&1 \
  | grep -o "crop=[0-9:]*" | awk -F'[=:]' '$2<956 || $3<716' | sort | uniq -c
# loudness of the delivery file (−14 LUFS integrated, true peak ≤ −1)
ffmpeg -i final.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary
```
Plus the HyperFrames lint (0 errors) and the caption script reporting every word consumed (N / N).

```bash
npx hyperframes lint                                          # 0 errors (2 known warnings are fine: file size, z-index)
npx hyperframes snapshot . -o snaps --at 1.9,7.6,22.5 --no-end  # frames + snaps/contact-sheet.jpg
npx hyperframes preview                                        # scrub in Studio
scripts/sheet.sh renders/draft.mp4 sheet.jpg 1.7 8.9 32.1      # contact sheet from a render
```
(On a weak machine the user's cloud tool runs the same: `modal run tools/hfcloud.py::lint|snapshot|render`.)

## 4. The B-roll self-review

Before sending, write one line per visual beat: *"[object] [verb] on '[word]' because [why]"*. If any line
contains "shows", "displays" or "illustrates" with no state change, or you can't say why it belongs to the
throughline, redesign that beat. Ask: would the user call any of these random, a chart for a feeling, or flashy?

## 5. Sending the draft

- Send the 720p draft; if it is over ~30 MB, also make a phone copy (H.264 ~1.65 Mb/s, AAC 128k) and send that.
- Tell the user in plain words what the B-roll does beat by beat (time · what changes · why), what you fixed
  from their last notes, and what is not done (the 4K). Don't make them repeat feedback: every note they gave
  must be visibly addressed.
- 4K only after they approve; nothing is ever posted without their explicit instruction.
