"""Turn caption stacks written as plain lines into K.text(...) calls with each word's spoken time.

    from captions import Script
    sc = Script("video-5/edit-4x3/transcript-snap.json")
    js = sc.group("s1", 470, 90, ["58:you have", "130:*something", "64:insightful or useful", "58:to say"])

Line syntax  "SIZE:word word *word"   (SIZE = px in the 1440x1080 screen at the shot's start)
  *word        accent colour (blue)          word^x       colour class x (e.g. ^x = white for trees)
  ~word        spoken but not shown (the cursor still moves past it)
  shown|said   show a different spelling than the transcript ("Hormozi|Sarmouzi")
  a+b          one shown token for several spoken words ("8,000|8+000")
Words are matched in order against the transcript; out = the next group's first word (or `out=`).
"""

from __future__ import annotations

import json
import re


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9']", "", s.lower())


class Script:
    def __init__(self, transcript: str, offset: float = 0.0, marker: bool = False):
        self.words = json.load(open(transcript))
        self.marker = marker  # accent words also get the highlighter swipe (K.text 4th flag "m")
        self.i = 0
        self.offset = offset  # subtracted from every time (composition-local seconds)
        self.groups: list[dict] = []

    def _take(self, said: str) -> float:
        want = _norm(said)
        for j in range(self.i, min(self.i + 12, len(self.words))):
            if _norm(self.words[j]["text"]) == want:
                self.i = j + 1
                return self.words[j]["start"]
        ctx = " ".join(w["text"] for w in self.words[self.i:self.i + 12])
        raise ValueError(f"'{said}' not found after word {self.i}: {ctx}")

    def begin(self, offset: float) -> None:
        """Start the next overlay composition: its times are local to `offset`; the word cursor carries on."""
        self.offset = offset
        self.groups = []

    def skip(self, *said: str) -> None:
        for s in said:
            self._take(s)

    def group(self, shot: str, x: float, y: float, lines: list[str], a: str = "tc", out: float | None = None,
              mode: str = "fade", extra: str = "") -> dict:
        built = []
        first = None
        for ln in lines:
            size, _, rest = ln.partition(":")
            words = []
            for tok in rest.split():
                hidden = tok.startswith("~")
                tok = tok.lstrip("~")
                color = None
                if tok.startswith("*"):
                    color, tok = "b", tok[1:]
                if "^" in tok:
                    tok, color = tok.split("^")
                shown, _, said = tok.partition("|")
                said = said or shown
                t = None
                for part in said.split("+"):
                    tt = self._take(part.replace("_", " "))
                    t = tt if t is None else t
                if first is None:
                    first = t
                if not hidden:
                    words.append((shown.replace("_", " "), round(t - self.offset, 2), color))
            if words:
                built.append((int(size), words))
        g = {"shot": shot, "x": x, "y": y, "a": a, "lines": built, "out": out, "mode": mode, "first": first, "extra": extra}
        if self.groups and self.groups[-1]["out"] is None:
            self.groups[-1]["out"] = round(first - 0.02, 2)
        elif self.groups and self.groups[-1]["out"] > first - 0.02:
            # an explicit out that runs into the next group would stack two captions: end it as the next one starts
            self.groups[-1]["out"] = round(first - 0.02, 2)
        self.groups.append(g)
        return g

    def js(self, fn: str = "K.text", stage: str = "S") -> str:
        out = []
        for g in self.groups:
            lines = ", ".join(
                "{ s: %d, w: [%s] }" % (s, ", ".join(
                    "[%s, %s%s]" % (json.dumps(w), _f(t), ((', "%s"' % c) + (', "m"' if self.marker and c == "b" else "")) if c else "") for w, t, c in ws))
                for s, ws in g["lines"])
            o = g["out"]
            o_js = "" if o is None else ", out: %s" % _f(o - self.offset)
            out.append('%s(tl, %s, { shot: "%s", x: %g, y: %g, a: "%s", lines: [%s]%s, outMode: "%s"%s });' % (
                fn, stage, g["shot"], g["x"], g["y"], g["a"], lines, o_js, g["mode"], g["extra"]))
        return "\n".join(out)


def _f(v: float) -> str:
    return ("%.2f" % v).rstrip("0").rstrip(".")
