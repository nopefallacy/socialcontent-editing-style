# socialcontent editing style

A Claude Code skill: the creator's 4:3 talking-head edit, built in [HyperFrames](https://hyperframes.heygen.com).
Fun-but-premium kinetic captions beside the face, a camera that follows the speaker, hero words behind the head,
and B-roll that is **one translucent, frosted-glass interface system per video** acting out what is said.

It covers the **design** of the edit: the look, where text goes and how the eye flows, the B-roll metaphor method,
the camera and face-tracking rig, motion, sound cues and the quality gates. Cutting the take and the cloud
render/delivery pipeline are deliberately out of scope (the creator has separate context for those).

## Install

```bash
git clone https://github.com/nopefallacy/socialcontent-editing-style ~/.claude/skills/socialcontent-editing-style
```
Claude Code picks it up automatically ("edit this in my style", "4:3 edit", "B-roll ideas for this take", …).

## What's inside

| path | what |
|---|---|
| `SKILL.md` | the bar, the look in one screen, the workflow — read first |
| `references/01-the-look.md` | type, colour (ink vs white per footage), frosted glass, UI pieces, scene grounds |
| `references/02-text-layer-and-flow.md` | caption placement, sizes, timing, no ping-pong, scene headlines, hero words |
| `references/03-camera-and-face-tracking.md` | shots table, swings, punch-ins, face tracking, rack focus, live windows |
| `references/04-b-roll-metaphors.md` | the metaphor method: one throughline system, 8 questions per beat, metaphor bank, worked example, anti-patterns |
| `references/05-motion-and-sound.md` | eases and durations, state changes, SFX per event, music in brief |
| `references/06-quality-gates.md` | what to check before a draft goes out |
| `references/07-feedback-log.md` | the creator's own feedback, oldest first — the why behind every rule |
| `references/refs/refs.md` | written descriptions of the creator's 18 reference screenshots and what each is good for |
| `kit/README.md` | API of the HFKit builders (captions, odometers, frosted cards, steps, labels, connectors, cursors, toggles…) |
| `template/` | a ready project: `index.html` with the whole kit and camera rig, starter compositions, fonts, SFX, BRIEF and caption script templates |
| `scripts/` | `captions.py` (caption stacks from the transcript), `face_track.py` (MediaPipe face tracking → TRACK), `sheet.sh` (contact sheets) |
| `examples/video-7-script-to-speaking/` | an approved edit end to end, with frames |

## Notes

- The creator's reference screenshots are third-party work, so the images are not in this repo — only their
  written descriptions (`references/refs/refs.md`). The creator keeps the images locally; drop them into
  `references/refs/` as `ref01.png … ref18.png` and they are git-ignored.
- Fonts: Inter, Figtree, Instrument Serif (SIL Open Font License). Sound effects: Pixabay Content License (see
  `template/assets/sfx/CREDITS.md`).
