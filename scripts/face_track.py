"""Face tracking for the 4:3 rig: the camera follows the speaker's face like an operator.

    python3 face_track.py <project>                 # reads <project>/assets/aroll-cut.mp4
    python3 face_track.py <project> --follow 0.8 --sigma 0.2 --mode operator

Writes TRACK = [[t, dx, dy], ...] (world px, 10 per second) into <project>/index.html between
/*TRACK:start*/ and /*TRACK:end*/, and the full result to <project>/face-track.json.
The composition tweens the footage + matte wrappers (.trk) through these offsets and clamps every offset to
the overscan the camera has at that moment, so the frame edge never shows. Offsets are world px, so a track
made on the 720p cut carries over to the 4K final unchanged.

Needs: pip install mediapipe==0.10.14 opencv-python-headless numpy  (the user's cloud runs the same code as
hfcloud.py::track — use that on a weak machine).
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re


def track(media: pathlib.Path, fps: float = 10.0, follow: float = 1.0, sigma: float = 0.2, mode: str = "operator") -> dict:
    import cv2
    import mediapipe as mp
    import numpy as np

    cap = cv2.VideoCapture(str(media))
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    step = max(1, round(src_fps / fps))
    det = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
    ts, xs, ys = [], [], []
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if i % step == 0:
            res = det.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if res.detections:  # the biggest face is the speaker
                b = max(res.detections, key=lambda d: d.location_data.relative_bounding_box.width).location_data.relative_bounding_box
                ts.append(i / src_fps)
                xs.append(b.xmin + b.width / 2)
                ys.append(b.ymin + b.height / 2)
        i += 1
    if len(ts) < 10:
        raise SystemExit(f"face found in only {len(ts)} samples")
    t = np.array(ts)
    wx = np.array(xs) * 1920 - 240  # the 16:9 footage is a 1920x1080 layer at x = -240 in the 1440x1080 world
    wy = np.array(ys) * 1080
    grid = np.arange(0, i / src_fps, 1 / fps)
    gx, gy = np.interp(grid, t, wx), np.interp(grid, t, wy)

    def despike(v, k=5):  # running median: one bad detection can't jerk the camera
        pad = np.pad(v, k // 2, mode="edge")
        return np.array([np.median(pad[j:j + k]) for j in range(len(v))])

    def smooth(v):  # Gaussian, sigma seconds
        r = int(3 * sigma * fps)
        kx = np.arange(-r, r + 1) / fps
        ker = np.exp(-0.5 * (kx / sigma) ** 2)
        return np.convolve(np.pad(v, r, mode="edge"), ker / ker.sum(), mode="valid")

    def operator(v, hz=1.0):  # critically damped spring: trails a moving head like a camera operator
        w, dt = 2 * np.pi * hz, 1 / fps
        x, vel, out = float(v[0]), 0.0, []
        for target in v:
            vel += (w * w * (target - x) - 2 * w * vel) * dt
            x += vel * dt
            out.append(x)
        return np.array(out)

    if mode == "operator":
        gx, gy = smooth(operator(despike(gx))), smooth(operator(despike(gy)))
    else:
        gx, gy = smooth(despike(gx)), smooth(despike(gy))
    mx, my = float(np.median(gx)), float(np.median(gy))
    dx, dy = -(gx - mx) * follow, -(gy - my) * follow
    return {"fps": fps, "follow": follow, "sigma": sigma, "mode": mode, "median": [round(mx, 1), round(my, 1)],
            "found": round(len(ts) / max(1, len(grid)), 3),
            "offsets": [[round(float(a), 2), round(float(b), 1), round(float(c), 1)] for a, b, c in zip(grid, dx, dy)]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--media", default="assets/aroll-cut.mp4")
    ap.add_argument("--fps", type=float, default=10.0)
    ap.add_argument("--follow", type=float, default=1.0)
    ap.add_argument("--sigma", type=float, default=0.2)
    ap.add_argument("--mode", default="operator", choices=["operator", "smooth"])
    a = ap.parse_args()
    proj = pathlib.Path(a.project)
    res = track(proj / a.media, a.fps, a.follow, a.sigma, a.mode)
    (proj / "face-track.json").write_text(json.dumps(res))
    index = proj / "index.html"
    js = "const TRACK = " + json.dumps(res["offsets"], separators=(",", ":")) + ";"
    s, n = re.subn(r"/\*TRACK:start\*/.*?/\*TRACK:end\*/", lambda m: "/*TRACK:start*/ " + js + " /*TRACK:end*/", index.read_text(), flags=re.S)
    if n == 1:
        index.write_text(s)
    big = max(max(abs(o[1]), abs(o[2])) for o in res["offsets"])
    print(f"face found in {res['found'] * 100:.0f}% of samples · median {res['median']} · biggest pull {big:.0f}px"
          + ("" if n == 1 else " · (no TRACK markers in index.html)"))


if __name__ == "__main__":
    main()
