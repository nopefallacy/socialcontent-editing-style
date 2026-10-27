# 03 — Camera, face tracking, rack focus

The camera is what makes a static talking-head take feel edited. It is all GSAP on one wrapper — no re-cutting.

## Contents
1. The rig (layers)
2. The shot grammar: tight → one dolly-out
3. The shots table (`SHOTS`, `frame`, FR / FL / C)
4. How shots arrive: whip, cut, move, rack
5. Punch-ins
6. Face tracking
7. Rack focus into a scene
8. Live windows (portals)
9. Pitfalls

---

## 1. The rig (layers, inside `#world`, the 1440×1080 plane)

```
#world                      scale(OUTPUT/1440), perspective 2400px
 ├─ #punch                  quick +8% zooms on key words; blurred for rack focus
 │   └─ #cam                the camera: scale / x / y / rotationY per shot
 │       ├─ .trk #trk-a     follows the face (tracking offsets) → the A-roll <video>
 │       ├─ #ov-behind      hero words that sit BEHIND the speaker
 │       ├─ .trk #trk-m     follows the face → the speaker's matte clips (in front of ov-behind)
 │       └─ #ov-a… #ov-e    caption compositions (ride the camera plane)
 ├─ #fl-…, #sc-…            screen-locked cards and rack-focus scenes (do NOT move with the camera)
 ├─ .portal                 live windows of the take, positioned to match their scene's card
 └─ #endfade
```

Track indices (Studio lanes; overlapping clips go on different lanes): A-roll 0 · mattes 1 · ov-behind 2 ·
caption hosts 4 · fl-* cards 5 · sc-* scenes 6 (alternate 5/6 when hosts overlap) · live-window videos 8 ·
short SFX 10/11/13/14 · long SFX 12/15 · music 20.

Captions ride the camera (they shrink/drift with the dolly, like the inspo). Cards are screen-locked (stable, so
their glass can blur what is behind them). Tracking moves only the footage and the mattes, so the space around
the face stays constant while captions and cards stay put.

## 2. The shot grammar: tight → one dolly-out

Each sentence (shot) **arrives tight** — scale ≈ 1.26–1.32 with the face pushed to the side opposite the text —
then makes **one continuous dolly-out** across the whole sentence to ≈ 1.16–1.22 (sine.inOut). The next shot
arrives tight again. This is the inspo's grammar (`socialcontent/inspo/98ff46f6…mp4`). Don't hard-cut every
sentence ("too much cutting"): most side changes are animated swings.

## 3. The shots table

```js
const FACE = [700, 560];      // where the face sits in the raw 4:3 world — MEASURE on a snapshot of the take
function frame(s, sx, sy) {   // scale s with the face at screen (sx, sy), clamped so footage always covers
  let X = sx - 720 - (FACE[0] - 720) * s, Y = sy - 540 - (FACE[1] - 540) * s;
  const mx = Math.max(0, 960 * s - 720 - 34), my = Math.max(0, 540 * (s - 1) - 26);
  return { s, X: clamp(X, -mx, mx), Y: clamp(Y, -my, my), sx, sy };
}
const FR = (s, d = 0) => frame(s, 1030 - d, 740 - d / 2),   // face right → text at x≈470
      FL = (s, d = 0) => frame(s, 410 + d, 740 - d / 2),    // face left  → text at x≈970
      C  = (s, y = 700) => frame(s, 720, y);                // centred rest (hero words)
const SHOTS = {
  s1: { t: 0.0,  in: "whip",            a: FR(1.32), b: FR(1.22, 18) },
  s2: { t: 4.2,  in: "cut",             a: FR(1.26), b: FR(1.18, 18) },
  s3: { t: 11.0, in: "move", d: 0.9,    a: C(1.06, 720), b: C(1.1, 728) },   // PERFECT behind you
  s4: { t: 13.9, in: "move", d: 0.9,    a: FL(1.3), b: FL(1.2, 20) },
  s6: { t: 28.95, in: "cut",            a: FR(1.24), b: FR(1.16, 18), end: 32.3 },  // `end` = a scene covers after
  s7: { t: 38.3, in: "rack",            a: FL(1.28), b: FL(1.2, 18), end: 47.0 },  // first shot after a scene
};
```

**FACE** = the centre of the face (between the eyes and the nose) in the raw 4:3 world, before any zoom. From
a 16:9 still of the take (W×H px): `x = px/W·1920 − 240`, `y = py/H·1080`. Measure it on 2–3 stills and
average. **Check the clamp:** `frame()` limits the pan to |X| ≤ 960·s − 754 and |Y| ≤ 540·(s−1) − 26; when the
face sits far off-centre in the raw frame, small scales can't push it to 1030/410 and it settles short. Compute
X for each `a`/`b` (or snapshot the start and end of each shot); if it clamps, raise the scale or accept a face
nearer the centre. A centred rest needs enough scale to place the face at the requested y.

How to write it:
- One row per sentence or thought; `t` on a word boundary (or a pause), in edit seconds.
- `a` = the tight arrival, `b` = where the dolly ends (`d` pulls the face a little toward centre as it widens).
- `end` when a full scene takes over before the next shot; the camera rests under the scene. The last shot runs
  to the video's end unless it names its own `end`.
- Groups of 2–5 rows share a side; swings (`move`) between sides; centred rests for hero words.
- Caption groups name the shot they start in (`sc.group("s4", 970, 84, …)`).
- A card on one side for a long beat → keep the side through those shots (change `C` rests to FR/FL and move
  the hero word to the head instead).

## 4. How shots arrive

| in | use | motion |
|---|---|---|
| `whip` | the very first shot, energy | starts ×1.12 with 14px blur → settles in 0.75s expo.out |
| `cut` | punctuate a new thought on the same side | instant reframe with a 2-frame 4px blur smear |
| `move` | **change sides** (the default way) | 0.9–1.2s: pan with sine.inOut, a zoom "breath" (dips ~0.16 then back), plane tilts ±2.5° rotationY and returns — each on its own sine curve, no V-shaped reversals |
| `rack` | first shot after a rack-focus scene | lands in pose with 16px blur clearing in 0.45s |

## 5. Punch-ins

On the words that carry the point (≈ one per 10–15s: "perfect", "unnatural", "understand", "slowly",
"re-record"), `#punch` scales to 1.08 around the face in 0.45s expo.out and is released at the next shot
(smoothly across a swing, instantly on a cut/rack). The face stays put, so a punch never pushes it out of frame.

## 6. Face tracking (the camera follows the face)

The user found a locked camera "boring"; following the face makes it feel operated. Pipeline
(`scripts/face_track.py`, or the user's cloud `hfcloud.py::track`):

1. Run MediaPipe face detection on the **cut** A-roll at 10 fps; keep the largest face per frame; record the
   box centre in world coordinates (the 16:9 footage is 1920×1080 at x = −240 → `x*1920−240`, `y*1080`).
2. Interpolate gaps onto a regular 10 fps grid.
3. **Despike**: running median of 5 — one bad detection can't jerk the camera.
4. **Operator spring**: a critically damped spring at 1 Hz follows the target — it trails the head like a
   human operator instead of snapping.
5. **Smooth**: Gaussian, σ = 0.2s.
6. Offsets = −(position − median position) × follow (0.8–1.0). Write `TRACK = [[t, dx, dy], …]` into
   `index.html` between `/*TRACK:start*/` and `/*TRACK:end*/`.

In the composition, `.trk` wrappers (footage + mattes) are tweened through TRACK keyframes (5 per second,
linear), and **every offset is clamped** to the overscan the camera has at that moment (the tightest room in a
±0.2s window, so the clamp doesn't snap at shot changes). Result: the face stays where each shot framed it, and
the edge of the footage never shows. Tracking offsets are world px, so they carry over to 4K unchanged.

Check: the tracker should find the face in ~100% of samples; biggest pull typically < 40px.

## 7. Rack focus into a scene

```js
function rack(t0, t1) {   // the room goes soft behind the glass, the camera settles under the blur
  tl.set("#punch", { transformOrigin: "720px 540px" }, t0 - 0.01);
  tl.fromTo("#punch", { filter: "blur(0px) brightness(1) saturate(1)", scale: 1 },
                      { filter: "blur(30px) brightness(1.05) saturate(1.15)", scale: 1.12,
                        duration: 0.6, ease: "power2.inOut", immediateRender: false }, t0);
  tl.to("#cam", { scale: 1, x: 0, y: 0, rotationY: 0, rotationX: 0, duration: 0.6, ease: "power2.inOut" }, t0);
  tl.to("#punch", { filter: "blur(0px) brightness(1) saturate(1)", scale: 1, duration: 0.55, ease: "power2.out" }, t1);
  tl.set("#punch", { filter: "none" }, t1 + 0.56);
}
```

- t0 = the previous shot's `end`; t1 = the next shot's `t` (make that shot `in: "rack"`).
- The scale 1.12 pushes the blurred edges out of frame (blur pulls in black at the edges otherwise).
- The scene composition fades in its glass over 0.5–0.7s from t0 and fades out 0.3s before t1.
- Hand-offs: the on-footage card can "dive" into the scene (scale up toward the centre, blur out) as the scene's
  card grows from the same spot — the eye follows one object across the cut.

## 8. Live windows (portals)

A `<video>` of the same take (muted, same grade), inside a `.portal` div (rounded rect or circle, white ring),
declared in `index.html` after the scene hosts, as a clip covering the scene's window with
`data-media-start` = its `data-start` (so it plays in sync). Size the video so the face sits centred:
video width Wv (height Hv = Wv·9/16) → the face sits near (0.49·Wv, 0.5·Hv) in the video; set left = window
centre x − 0.49·Wv and top = window centre y − 0.5·Hv − ~40 (a little headroom). Snapshot and adjust.
Animate it in the main timeline with the same entrance as its card (`portal(id, t0, t1)`). The scene must keep
its own elements out of the portal's rectangle (the portal paints above the scene).

## 9. Pitfalls

- A card visible during a swing can end up over the face mid-move — enter cards after the swing settles.
- Check the END frame of each shot: the dolly-out changes where things are.
- Outgoing caption stacks and cards must be gone before the next group/cards arrive at a shot change.
- 3D lean (`tilt: true`) only when the camera itself leans into a side; flat otherwise.
- Keep colour-graded `<video>` layers few (the A-roll as one pre-cut file, mattes as short clips); many graded
  layers have hung cloud renders.
