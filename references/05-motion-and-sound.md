# 05 — Motion and sound

## Contents
1. Motion principles
2. Durations and eases (the table)
3. State changes on UI pieces
4. Entrances, exits, hand-offs
5. GSAP gotchas in this rig
6. Sound effects: one sound per visible event
7. Music (brief)

---

## 1. Motion principles

- **Motion performs, it never idles.** Things move because their state changed on a word. No floating, bobbing
  or breathing loops on cards.
- **Smooth, never bouncy.** No back/elastic/bounce eases, no overshoot, no screen shake. Pops are a 1.04–1.05
  scale settling with power3.out at most.
- **Decelerate into place.** Entrances use expo.out (fast start, long settle) with a soft blur clearing.
- **Exit fast.** 0.16–0.3s fade + small blur, power1.in. Exits never overlap the next thing's entrance at the
  same spot.
- **Camera eases are sine.inOut** (swings, dolly-outs) so pan, zoom and tilt each ride their own curve.

## 2. Durations and eases

| motion | duration | ease |
|---|---|---|
| caption word: opacity + blur clear | 0.34s | power2.out |
| caption word: glide in | 0.55s | expo.out |
| highlighter swipe (scaleX) | 0.5s, +0.2s after the word | expo.out |
| caption group exit | 0.16s | power1.in |
| card entrance (opacity, y 40 → 0, scale .96 → 1, blur 14 → 0) | 0.7s | expo.out |
| card exit (opacity, blur 10) | 0.3s | power1.in |
| card grows (height) | 0.55s | expo.out |
| step appears (opacity, y 18 → 0) | 0.45s | expo.out, stagger 0.07 |
| state change: background/label colour cross-fade | 0.35s | power2.out |
| new status icon pops (scale .4 → 1) | 0.45s | expo.out |
| done/error pop (scale 1.05 → 1) | 0.55s | power3.out |
| strike-through draws | 0.42s | power3.out |
| connector draws on | 0.25–0.6s | power2.inOut |
| state label appears (scale .86 → 1, blur 6 → 0) | 0.45s | expo.out |
| odometer roll | 0.42s per column, 0.035s stagger right → left | power3.out |
| toggle | 0.42s knob, 0.3s colour | power3.inOut |
| cursor move / click dip | 0.6–0.8s / 0.1 + 0.22s | power3.inOut / power2 |
| selection box snap | 0.55–0.6s | expo.inOut |
| camera swing | 0.9–1.2s | sine.inOut (pan, zoom breath, ±2.5° tilt) |
| punch-in | 0.45s to ×1.08 | expo.out |
| rack focus in / out | 0.6s / 0.55s | power2.inOut / power2.out |
| spinner | ~1 turn per second while running | none (linear) |

## 3. State changes on UI pieces

A step's life on screen: appears **pending** with the plan → turns **running** (spinner) when the speaker starts
describing it → **done ✓** on the word that completes it (or **error ●** / **skipped (struck)**). Never jump
straight to ✓ if the speaker walks through the step — the spinner is the "now" marker.

Focus by dimming: while one thing is discussed, the others go to opacity ~0.32–0.45 and 1.5px blur; they come
back when the focus moves on.

## 4. Entrances, exits, hand-offs

- A card enters after the camera settles; it leaves before the next swing or hero word.
- When the same card returns, it fades/blurs in with the state it left in (not rebuilt step by step).
- Scene hand-offs: the on-footage card dives (scale ~1.3–1.35 toward the centre, blur 16, 0.45–0.5s power3.in)
  as the rack begins; the scene's card grows in from 0.86–0.9 scale over 0.7s.
- The last frame of the video eases to black over 0.45s after the final word.

## 5. GSAP gotchas in this rig

- Composition timelines are paused and seeked frame by frame; everything must be deterministic (no
  `Math.random`, use `K.rng(seed)`).
- `fromTo` renders its from-state at build time. For the second+ tween on an element, pass
  `immediateRender: false`, and `tl.set` initial states at 0.
- Animating `x`/`y` overwrites a CSS `transform: translate(-50%)` — centre with `xPercent/yPercent` instead.
- Absolutely positioned children of a card need explicit `left`/`top`.
- `backdrop-filter` only blurs what is behind it in the same stacking context — keep glass cards screen-locked,
  and avoid `filter` on a glass card's ancestors at rest (set `filter: "none"` after an entrance blur).
- Times inside a composition are local: `T(g) = g − hostStart`.

## 6. Sound effects: one sound per visible event

SFX are short, soft UI sounds placed on visible state changes — never decoration, never "overused".

| event | sound | volume (0–1) |
|---|---|---|
| opening whip | whoosh-short | 0.18 |
| card in / card back / swing | whoosh-short / whoosh | 0.06–0.1 |
| step done ✓ | click-soft | 0.08–0.1 |
| toggle, cursor click, play, speed change | click | 0.05–0.08 |
| state label / chip / error lands | pop | 0.05–0.07 |
| a goal / understood / badge | ping | 0.05–0.07 |
| rack focus into a scene (dive) | whoosh-cinematic (2.2s) | 0.15 |
| rack out | whoosh | 0.1 |
| per-word hops (word by word) | key-press | 0.06 |
| re-record press | key-press | 0.1 |
| progress tick to a new % | sparkle (rarely) | 0.05 |
| the closing "share it" moment | chime (2.0s) | 0.07 |

No sound on the hero words behind the head — the music hit carries those. Distribute SFX over a few audio
tracks so clips never overlap on one track; long sounds on their own track; nothing runs past the video's end.

## 7. Music (brief — the score pipeline lives in the user's other context)

A licensed film-score bed under the voice, minor while the problem builds, major from the turn; cue changes at
scene seams; 2–3 tonal hits on the hero words; the bed ≈ 19 dB under the voice (the user said "lower it down a
little" once); deliver at −14 LUFS, true peak ≤ −1 dBTP, file < 300 MB for Instagram. Check on a phone speaker.
