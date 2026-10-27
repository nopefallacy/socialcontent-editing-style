"""Video 7 score (Key of C): a perfect script that still sounds wrong (minor, unsure) → the turn to the camera and
"make the viewer understand" (minor, steady) → the multitrack opens up (major, warm) → practice, re-record, anchors
(major, light) → "I'm so done with that" and what comes next (major, open).
Run: python3 score_script.py, then modal run tools/hfmusic.py::score --project video-7/edit-4x3"""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "tools"))
from score_tools import build, write  # noqa: E402

spec = build(
    [
        (0.0, 21.2, "Imagine If", -26.5, {}),  # a perfect script · it sounds unnatural · I faced this too
        (21.2, 47.3, "Stay The Course", -26, {}),  # open the camera · too fast, no spaces · make them understand
        (47.3, 61.2, "Something Beautiful", -25.5, {}),  # communication: hands, silences, face
        (61.2, 91.0, "Clearing", -25.5, {}),  # write it, speak it slowly, re-record, anchor sentences
        (91.0, 111.1, "What If", -25.5, {"out": 2.2}),  # I don't script anymore · next: no script · still learning
    ],
    hits=[
        (12.2, "Sonar", -26, 3.5),  # perfect
        (78.34, "Warm Signal", -27, 4.0),  # easier
        (96.6, "Neon Bell", -28, 4.0),  # done
    ],
    risers=[(47.35, "Breathe", -29), (79.65, "First Contact", -29)],
    total=111.1,
)
write(str(HERE), spec)
