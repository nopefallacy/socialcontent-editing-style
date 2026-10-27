---
name: socialcontent-editing-style
description: The creator's "socialcontent" edit for 4:3 talking-head videos (Instagram feed / YouTube, 1440x1080 world → 2880x2160), built in HyperFrames — fun-but-premium kinetic captions in the sky band beside the face (ink or white Inter ExtraBold, one blue accent word on a highlighter), a camera that frames the face on the opposite side and follows it (face tracking, dolly-outs, punch-ins, smooth swings — never left-right ping-pong), hero words that rise BEHIND the head via a matte, and B-roll that is ONE translucent frosted-glass "interface" system per video (workflow steps, state labels, toggles, cursors, selection boxes, real frames of the speaker) acting out the sentence, with rack-focus scenes that keep the speaker soft behind the glass. Covers the look, text placement and visual flow, the metaphor method for B-roll, the camera/face-tracking rig, motion, sound cues and the quality gates. Use this whenever the user wants a talking-head video edited "in my style", "like video 6/7", "the socialcontent style", "4:3 edit", asks for B-roll ideas, metaphors, a beat sheet, caption layout or text placement for a talking-head take, or drops a new take into the socialcontent folder — even if they never name the style. Not for cutting the take or for the render/cloud pipeline (the user has separate context for those), and not for vertical 9:16 reels (that is origami-blue).
---

# socialcontent editing style

A 4:3 talking-head edit that feels **fun but premium**: the speaker stays the hero, big tight captions sit in
the sky beside their face, the camera breathes with them, and every B-roll is a small, translucent interface
that *acts out* what they are saying — one connected system across the whole video, never a random gadget.

Read this file first. It is the bar. The `references/` hold the depth; `kit/` and `template/` hold working
code; `examples/video-7-script-to-speaking/` is a finished, approved edit to copy the level of finish from.

## The bar (every rule here came from a real correction — see `references/07-feedback-log.md`)

1. **Translucent, always.** Every card, pill and panel that sits on the footage is frosted glass you can see the
   sky and trees through (rim ≈ white 12–30% + 22px backdrop blur; inner panel ≈ white 46–62%). Never a
   near-opaque white box. The user: *"it was translucent, and that was my essential style."*
2. **One system per video.** Pick ONE interface metaphor (a workflow, a call, an editor, a switchboard…) and let
   the whole argument play out as state changes inside it. The same card comes back in the same place, carrying
   its previous state. A new unrelated gadget per sentence reads as *"B-roll for the sake of B-roll"*.
3. **Every B-roll acts out cause → effect on a spoken word.** Something changes state exactly when the word is
   said (a step ticks ✓, a toggle flips, a label pins, a selection snaps, a counter rolls). If a box with the
   sentence in it would say the same thing, it is not a B-roll yet. Highlight the one thing being said; dim or
   blur the rest.
4. **Real over invented.** When the line refers to something real — the speaker's hands, face, pauses, their
   own script, their own take — show the real thing (frames from the take, a live window of the footage, the
   real waveform). Invented placeholder UIs read "AI-ish".
5. **The eye barely travels.** Text sits *just* left (x≈470) or *just* right (x≈970) of centre in the sky band
   above the head; the camera frames the face on the other side. Sides change only on a smooth camera swing, a
   scene, or a centred rest — a few sentences per side. Never ping-pong left-right-left.
6. **Readable on a phone** (all sizes in the 1440×1080 world): caption lead lines 58–66px and the caption's
   big line 112–140px; behind-the-head hero words 220–290px; inside cards: step pills 35px, row labels 36px,
   state labels 31px, and nothing smaller than 27px except a card's small header (25px). Small grey uppercase
   labels and thin serifs fail.
7. **Nothing covers the face.** Cards sit below the captions on the free side; hair edges are fine, eyes/nose/
   mouth never. Check the END frame of each shot too — the dolly moves things.
8. **Smooth, never bouncy.** expo.out / power3 / sine.inOut. No back/elastic/bounce eases, no screen shake, no
   fisheye, no glow, neon, gradients-for-flash, emoji, sparkles or cartoons ("childish", "flashy").
9. **The take is the user's.** They cut it themselves; pauses are intentional — never trim. Drafts at 720p;
   4K only after they approve. Never post or schedule anything without their explicit go.

## The look in one screen

| layer | spec |
|---|---|
| format | 4:3. Author everything in a **1440×1080 world**; output 960×720 (draft) or 2880×2160 (final) via one scale. |
| footage | the whole take, graded `skin-soft` 0.62 (+exposure .04, contrast .08, highlights −.18); never tone-map HDR yourself — ask for an SDR export. |
| captions | Inter ExtraBold 800 (`InterK`), tracking −0.05em, line-height 0.84 (lines overlap), 1–3 words per line. Lead lines 58–66px, the hero line 112–140px. |
| caption colour | test on real frames: bright/mid-blue sky → **ink #111214 with a soft white halo**; dark trees/shirt/indoor → **warm white #f6f3f2 with a soft dark shadow**. |
| accent | ONE blue: #3170e4 on bright skies (on a white highlighter swipe), soft sky blue #7eb2ea on dark footage. Not deep cobalt. One accent word per stack. |
| B-roll headline | the caption family + ONE emotional word in Instrument Serif italic blue (`SerifK`) with a highlighter swipe. |
| UI text | Figtree 700 (`FigK`) in pills/chips/rows; counters are odometers (InterK 800). |
| glass | `.fz` frosted rim + `.fz-in` see-through panel (kit). Dark state chips `#16171b` for labels; done-state pills a pale blue gradient. |
| scenes | **rack focus**: the footage blurs (30px) behind the glass and a live sharp window of the speaker sits inside the card. Flat dark grid or paper stages only when the footage truly can't host it — never gradients/vignettes. |
| hero words | 1 per ~30–40s: the emotional word of the beat (PERFECT, EASIER, DONE) 220–290px rising **behind the head** through a matte of the speaker. |
| sound | soft UI clicks/pops/whooshes on visible state changes; a film-score bed under the voice; deliver at −14 LUFS. |

## How to work (the order matters)

1. **Intake.** Read the transcript (word-level, edit seconds) end to end. Take snapshots of the real footage:
   where is the face (FACE), how big, what is behind (sky / trees / wall), what colour is the shirt. Read
   `references/01-the-look.md` and decide caption colour from those frames.
2. **Message + throughline.** Write the video's message in one sentence and find the *turn* (the belief it
   flips). **Listen for the image the speaker already uses** ("talk to it like a friend", "a perfect script",
   "ripples") — if they give you one, build the system from it. Then choose ONE throughline system — see
   `references/04-b-roll-metaphors.md` §2, and the reference grammar described in `references/refs/refs.md`.
   Write it at the top of `BRIEF.md`.
3. **Beat sheet** in `BRIEF.md` (table: time · line · visual · metaphor). For every sentence decide:
   captions only · a card beside the face · a rack-focus scene · a hero word behind the head. Budget for ~2 min:
   one visual beat every 8–12s, 2–3 rack scenes of 6–10s, ≥ 25% captions-only breathing room. Open on the face:
   the first caption is on screen on frame 1, the camera whips in, a punch lands on the hook's key word; the
   first card arrives only once its first step is being said.
   Run every visual beat through the 8 questions in `references/04-b-roll-metaphors.md` §3 and the litmus
   tests in §6 before writing code.
4. **Camera + text plan.** Shots table (`references/03-camera-and-face-tracking.md`): which side the face is
   on for each sentence, where the swings are, which shots are rests for hero words. Captions with
   `scripts/captions.py` (`references/02-text-layer-and-flow.md`).
5. **Build** from `template/` (it already contains the kit: captions, camera, face-tracking clamp, rack focus,
   live portals, frosted flow pieces — API in `kit/README.md`). One composition per card/scene, screen-locked
   cards outside the camera, captions inside it. Copy patterns from `examples/video-7-script-to-speaking/`.
6. **Test early.** Snapshot the first card on real frames before building the rest; fix size/translucency/
   placement once, not ten times:
   `npx hyperframes lint` (0 errors) · `npx hyperframes snapshot . -o snaps --at 1.9,7.6,22.5 --no-end`
   (look at `snaps/contact-sheet.jpg`) · `npx hyperframes preview` to scrub. On a weak machine use the user's
   cloud equivalents (`hfcloud.py::lint`, `::snapshot`).
7. **Draft at 720p**, then run the quality gates (`references/06-quality-gates.md`): frames at every shot
   change, every card state, the start and end of every scene; face, overlap, size, empty-space, contrast,
   edge checks. Fix, re-render, then send the draft (a < 30 MB phone copy if the full one is bigger).
8. **On approval:** 4K final under 300 MB at −14 LUFS (the render pipeline lives in the user's other context).

## Where to read more

| file | read it when |
|---|---|
| `references/01-the-look.md` | choosing colours, type, glass, scene grounds; per-footage decisions |
| `references/02-text-layer-and-flow.md` | placing captions and headlines, sizes, timing, the no-ping-pong rule, behind-head hero words |
| `references/03-camera-and-face-tracking.md` | shots table, swings, punch-ins, face tracking, rack focus, live windows |
| `references/04-b-roll-metaphors.md` | **always, before designing any B-roll** — the method, the metaphor bank, worked examples, anti-patterns |
| `references/05-motion-and-sound.md` | eases, durations, entrances/exits, state changes, SFX placement, music arc |
| `references/06-quality-gates.md` | before sending any draft |
| `references/07-feedback-log.md` | the user's own words — why each rule exists |
| `references/refs/refs.md` | the user's reference screenshots, described in words, with what each one is good for |
| `kit/README.md` | the HFKit API (K.text, K.roller, fcard, fpill, fchip, flink, fcursor, fsel, ftoggle, fface, rack, portal) |
| `examples/video-7-script-to-speaking/` | an approved edit end to end: BRIEF, beat table, every composition, frames |
