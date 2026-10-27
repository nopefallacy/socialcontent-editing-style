"""Captions for this take, in speaking order. Run after any edit:  python3 caption_script.py
Writes K.text(...) calls between /*CAPTIONS:start*/ and /*CAPTIONS:end*/ in each caption composition.

Text sits in the sky band: x 470 when the face is framed RIGHT (FR), x 970 when it is framed LEFT (FL), x 720
for a centred rest (C). The shot named first in a group must be the shot it starts in (SHOTS in index.html).
Line syntax: "SIZE:words" · *accent · ~hidden · shown|said · a+b · word^x (white over trees).
Every spoken word must be consumed in order (the last line prints N / N)."""

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "scripts"))  # copy scripts/captions.py from the skill next to this file
from captions import Script  # noqa: E402

sc = Script(str(HERE / "transcript-snap.json"), marker=True)  # word-level transcript in EDIT seconds
out = {}

# ---------------------------------------------------------------- ov-a (0 – 20.1)
sc.begin(0.0)
sc.group("s1", 470, 70, ["58:you have written down", "64:a", "132:*perfect", "64:script"], out=2.0)
sc.group("s2", 470, 80, ["58:once you try", "112:to *record it"], out=8.9)  # the LAST group in a host needs an explicit out (before the swing / hero word), or it stays until the host ends
# sc.skip("perfect")  # a word said while its hero word rises behind the head
out["ov-a"] = sc.js()

# ---------------------------------------------------------------- sc-example (20.0 – 28.0): its own headlines
# sc.skip("see", "it", "for", "yourself", ...)

# ---------------------------------------------------------------- ov-b (27.9 – 60)
sc.begin(27.9)
# sc.group("s5", 470, 84, ["58:and see for", "120:*yourself"])
out["ov-b"] = sc.js()

for name, js in out.items():
    f = HERE / "compositions" / f"{name}.html"
    s = f.read_text()
    new, n = re.subn(r"/\*CAPTIONS:start\*/.*?/\*CAPTIONS:end\*/",
                     lambda m: "/*CAPTIONS:start*/\n" + "\n".join("          " + ln for ln in js.splitlines())
                     + "\n          /*CAPTIONS:end*/", s, flags=re.S)
    if n != 1:
        sys.exit(f"{f.name}: CAPTIONS markers not found")
    f.write_text(new)
    print(f"{name}: {js.count('K.text(')} stacks")
print(f"words consumed: {sc.i} / {len(sc.words)}")
