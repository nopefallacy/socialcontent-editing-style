# 01 — The look

Everything here is authored in a **1440×1080 world** (4:3). One CSS scale on `#world` maps it to the output:
0.6667 → 960×720 draft, 1 → 1440×1080, 2 → 2880×2160 final. Never author in output pixels.

## Contents
1. The feel
2. Footage and grade
3. Caption type
4. Colour: deciding ink vs white, the one accent
5. Frosted glass (the essential surface)
6. UI pieces: pills, chips, toggles, cursors, photo nodes
7. Scene grounds: rack focus first
8. What never appears

---

## 1. The feel

**Fun but premium.** Fun comes from motion that *does something* and small human details (a cursor tagged
"you" or "me", a counter rolling to 30×, a waveform whose gaps snap shut, a step that says "skip it"). Premium
comes from restraint: one accent colour, one typeface family for words, translucent surfaces, smooth eases, and
the speaker never shrunk or boxed. If a detail is cute but means nothing, cut it.

## 2. Footage and grade

- Use the **whole take** the user gives you; they already cut it. Pauses are intentional.
- The 16:9 source fills the 4:3 world as a 1920×1080 layer at x = −240 (`object-fit: cover`). The camera zooms
  (≥ ~1.17× during shots) so there is always overscan for tracking and swings.
- Grade every footage layer identically (A-roll, mattes, live windows) — a cut-out graded differently reads as
  a pasted sticker. The approved grade (HyperFrames `data-color-grading`):
  `{"preset":"skin-soft","intensity":0.62,"adjust":{"exposure":0.04,"contrast":0.08,"highlights":-0.18,"shadows":0.05}}`
- HDR (HLG/PQ) take? Ask the user for their SDR export. Their verdict on a home-made tone-map: "a really bad job".

## 3. Caption type

The captions are the edit's voice. They are big, tight and stacked:

| property | value |
|---|---|
| family | Inter ExtraBold 800 (`InterK`, `assets/fonts/inter-800.woff2`) |
| tracking | −0.05em |
| line-height | 0.84 — lines overlap on purpose |
| words per line | 1–3 (a lead line can be 3–4 small words) |
| sizes (world px) | lead lines 58–66 · hero line 112–140 · the occasional single huge word 120–136 |
| stack | 2–4 lines; max 3 when a card sits under it |
| entrance | per word, on its spoken time: opacity + a soft CSS blur (≈0.07em) clearing in 0.34s, glide 0.55s expo.out (first line from the stack's side, lower lines rise from below) |
| exit | fade + small blur in 0.16s, ending before the next group's first word |

**Accent word:** one per stack, the word that carries the meaning ("perfect", "unnatural", "write it",
"problems", "30"). On the footage it is blue on a **white highlighter swipe** (`#cam .kw .mkb`) that paints in
0.5s after the word lands — the white bar makes blue readable on any sky.

**B-roll headlines** (in scenes) use the same family but put ONE emotional word in **Instrument Serif italic**
(`SerifK`) blue with a softer blue highlighter: "some of those *problems*", "it's *communication*",
"certain *sentences*". The serif is the "feeling" word; never more than one per headline.

**UI text** (inside cards): Figtree 700 (`FigK`) — pills 35px, row labels 36px, chips 31px, card headers 25px
with one serif-italic word ("my *videos*", "the *next* video", "script.txt · *this video*").
**Numbers** are odometers (`K.roller`): InterK 800, digits roll right-to-left.

## 4. Colour: ink vs white, the one accent

Decide by testing on **real frames of this take**, not by habit.

| background behind the caption | caption | accent |
|---|---|---|
| bright or mid-blue sky (most outdoor takes) | **ink #111214** + soft white halo (`text-shadow: 0 0 .14em rgba(255,255,255,.6)`) | #3170e4 on a white swipe |
| pale dusk sky | ink | #3170e4 |
| dark trees, dark shirt, indoor/night | **warm white #f6f3f2** + soft dark shadow | soft sky blue #7eb2ea with a thin bevel |
| mixed (sky above, trees below) | ink in the sky band; white only for words that land on trees (`^x` in captions.py) | — |

History: white and sky-blue vanished on a bright sky (video 2 → ink + blue); the user disliked a deep cobalt
(#1d5fd6) as "too deep" → keep the accent at #3170e4/#3a78ec; video 1 and 4 used white captions on darker
framing. Only one accent hue in the whole video. Semantic red (#ff5a5f / #e5484d) is allowed only as a small
error dot or an error outline ("sounds unnatural", "too fast", a wrong word box).

## 5. Frosted glass (the essential surface)

The user's signature surface. Two layers, like their reference of a workflow card floating over a blurred
garden (ref12 in `refs/refs.md`):

```css
.fz {            /* the rim: barely there */
  border-radius: 40px;
  background: linear-gradient(160deg, rgba(255,255,255,.30), rgba(255,255,255,.12));
  border: 1.5px solid rgba(255,255,255,.60);
  box-shadow: inset 0 1.5px 0 rgba(255,255,255,.8), 0 30px 70px rgba(20,40,80,.18);
  backdrop-filter: blur(22px) saturate(1.45);
}
.fz-in {         /* the panel: see-through, content sits here */
  inset: 14px; border-radius: 28px;
  background: linear-gradient(170deg, rgba(252,252,250,.62), rgba(246,248,250,.46));
  border: 1px solid rgba(255,255,255,.75);
}
```

Rules:
- You must be able to see the background through it. If a frame shows a flat white rectangle, it is wrong.
- `backdrop-filter` works on **screen-locked** layers (outside the camera wrapper). Keep cards there.
- Cards **grow with their content** (tween `height`) — a card never shows an empty half waiting for later steps.
- On dark footage use the dark glass variant (`.frost`: white 5–16% + `brightness(.86)` blur, light text).

## 6. UI pieces (all in `kit/`)

From the user's reference set (`refs/refs.md`). One visual grammar for the whole video:

| piece | look | states / use |
|---|---|---|
| **step pill** `fpill` | 84px tall, radius 26, status icon + Figtree 700 35px | `todo` outlined ring, faint fill · `run` white with a ticking 8-tick spinner · `ok` pale blue gradient (#f3f7ff→#cfe0fe, border #a9c3f2, text #1f4ca8) with a circle-check · `err` near-black with a red dot · `off` struck through, dimmed, slightly blurred |
| **spine** | 2.5px line rgba(30,36,46,.42) between steps | draws on as each step starts |
| **state label** `fchip` | dark #16171b pill, white Figtree 700 31px; `lite` (white) and `blue` variants; optional red dot | pinned to the exact thing by a **dashed** connector with a black end dot ("too fast", "skip it", "perfect", "don't need it") |
| **connector** `flink` | solid or dashed (7/9), rounded orthogonal corners, black dots with white rims at the ends | draws on in 0.3–0.6s |
| **toggle** `ftoggle` | 76×44 track, navy #1c3a8f when on, white knob | flips on the spoken word |
| **cursor** `fcursor` | filled arrow + a name tag in the same colour ("you", "me") | moves on power3.inOut, dips on click |
| **selection box** `fsel` | 2.5px #3170e4 border with four white square handles | snaps whole → part on expo.inOut |
| **photo node** `fface` | circle, 6px white ring, soft shadow; a real frame of the speaker (or an outlined icon) | inputs, "you", the viewer |
| **live window** `.portal` | the take itself, sharp, in a rounded rect or circle with a white ring | inside rack-focus scenes ("watch it back", "the camera") |
| **odometer** `K.roller` | digit strips | 1.0× → 1.6×, 30% → 100%, 1× → 30× |

## 7. Scene grounds: rack focus first

When a beat needs the whole frame, **don't cut away to a separate stage**. Rack focus: the camera wrapper blurs
(30px, brightness 1.05, saturate 1.15, scale 1.12) so the speaker and the sky become a soft colour field — the
exact background of the user's frosted references — and the scene's glass cards sit sharp in front. A live window
of the speaker inside the card keeps them present. This reads "native to the editing".

Fallbacks (only if the footage can't carry it, e.g. a busy indoor wall):
- **flat dark**: #0b0b0b, static film grain (~7.5%), hairline 120px grid with faint intersection dots, an inset
  hairline frame; panels #141414 with one 1px hairline; focus by dimming (others to ~0.38 opacity).
- **paper**: warm off-white with grain and a hairline frame; white cards with one hairline and a soft drop.
Never: gradients, vignettes, auras, bloom over a stage ("a little more flashy").

## 8. What never appears

Emoji, cartoons, clip-art people, sparkles/glints, neon, glow halos, bevel-and-bloom text, fisheye, screen shake,
bouncy overshoot, a different accent hue per scene, a chart standing in for a feeling, invented "fake ad" UIs
when real material exists, opaque white cards on the footage, small grey uppercase labels, text under 27px (a card's 25px header is the one exception).
