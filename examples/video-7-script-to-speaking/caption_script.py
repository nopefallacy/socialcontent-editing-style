"""Video 7 captions, in speaking order. Run after editing: python3 caption_script.py
Writes K.text(...) calls between /*CAPTIONS:start*/ and /*CAPTIONS:end*/ in each overlay composition.
Text sits in the sky band: x 470 (face framed right) · 970 (face framed left) · 720 centred."""

import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))  # the skill's scripts/captions.py (in the project it was tools/)
from captions import Script  # noqa: E402

sc = Script(str(HERE / "transcript-snap.json"), marker=True)
out = {}

# ---------------------------------------------------------------- ov-a (0 – 13.95)
sc.begin(0.0)
sc.group("s1", 470, 70, ["58:you have written down", "64:a", "132:*perfect", "64:script"], out=2.0)
sc.group("s1", 470, 80, ["58:to say something", "64:on your *video"], out=4.2)
sc.skip("and")
sc.group("s2", 470, 80, ["58:once you try", "112:to *record it"], out=5.58)
sc.group("s2", 470, 80, ["58:and *hear it", "64:for yourself,"], out=7.95)
sc.group("s2", 470, 80, ["58:it just feels so", "130:*unnatural."], out=9.9)
sc.group("s2", 470, 80, ["58:even though the", "112:word *choices", "58:you used are"], out=12.1)
sc.skip("perfect")  # PERFECT behind your head
sc.group("s3", 720, 40, ["58:in your *opinion."], out=13.9)
out["ov-a"] = sc.js()

# ---------------------------------------------------------------- ov-b (13.85 – 32.4)
sc.begin(13.85)
sc.group("s4", 970, 84, ["58:this is a problem", "64:I also", "124:*faced"], out=15.8)
sc.group("s4", 970, 84, ["58:when I was doing", "120:*script videos", "58:back then."], out=18.86)
sc.group("s4", 970, 84, ["58:and I also", "112:figured out", "64:how you can", "112:*navigate", "58:through it."], out=21.65)
sc.group("s5", 470, 84, ["58:so when you", "120:*script out", "58:a video,"], out=23.2)
sc.group("s5", 470, 84, ["58:rather than just", "64:doing a", "124:*voiceover", "58:on it,"], out=25.78)
sc.group("s5", 470, 84, ["58:you try to", "120:open the *camera"], out=27.0)
sc.group("s5", 470, 84, ["58:and say in front of it", "120:*naturally"], out=28.95)
sc.group("s6", 470, 84, ["58:and see for", "120:*yourself"], out=29.98)
sc.group("s6", 470, 84, ["58:what are the", "112:*problems", "58:naturally happen."], out=32.3)
out["ov-b"] = sc.js()

# sc-watch (32.3 – 38.3): its own headlines
sc.skip("Some", "of", "those", "problems", "might", "be", "you", "speak", "too", "fast,", "you", "don't", "give", "enough",
        "spaces")

# ---------------------------------------------------------------- ov-c (38.2 – 47.3)
sc.begin(38.2)
sc.group("s7", 970, 84, ["58:because the ultimate", "120:*intention", "58:of the content is"], out=42.98)
sc.group("s7", 970, 84, ["58:to make the viewer", "130:*understand"], out=45.0)
sc.group("s7", 970, 84, ["58:rather than just", "120:*telling", "58:anything."], out=46.95)
out["ov-c"] = sc.js()

# sc-comm (47.0 – 55.75): its own headlines
sc.skip("It's", "in", "communication", "and", "it's", "not", "about", "word", "communication.", "Your", "hand", "gestures,",
        "the", "silences,", "the", "expression", "you", "do", "in", "your", "face.")

# ---------------------------------------------------------------- ov-d (55.7 – 79.8)
sc.begin(55.7)
sc.group("s8", 970, 84, ["58:these all", "64:come|comes under", "128:*expression"], out=58.46)
sc.group("s8", 970, 84, ["58:and help the viewer", "120:*understand", "64:~much even more"], out=61.15)
sc.skip("so")
sc.group("s9", 470, 84, ["58:the best way", "64:to navigate it"], out=62.48)
sc.group("s9", 470, 84, ["58:just", "120:*write it", "64:down"], out=63.56)
sc.group("s9", 470, 84, ["58:try to speak in front", "64:of the camera", "130:*slowly"], out=68.2)
sc.skip("and")
sc.group("s10", 470, 84, ["58:after that", "120:*first", "64:recording"], out=70.02)
sc.group("s10", 470, 84, ["58:try to understand", "64:what are the", "120:*problems", "58:there were"], out=72.78)
sc.group("s10", 470, 84, ["58:and just try to", "130:*re-record|re+-record", "58:it"], out=74.5)
sc.skip("and")
sc.group("s11", 470, 84, ["58:once you do it", "120:10 15 20 *30", "58:times"], out=77.8)
sc.group("s11", 470, 84, ["58:it's gonna be much"], out=78.32)
sc.skip("easier")  # EASIER behind your head
sc.group("s11", 470, 84, ["58:for you"], out=79.65)
out["ov-d"] = sc.js()

# sc-anchor (79.65 – 91.0): its own headlines
sc.skip("and", "rather", "than", "remembering", "a", "whole", "segment", "of", "content", "you", "can", "just", "remember",
        "a", "certain", "sentences", "and", "just", "try", "to", "speak", "in", "front", "of", "the", "camera",
        "rather", "than", "just", "reading", "word", "by", "word")

# ---------------------------------------------------------------- ov-e (90.9 – 111.1)
sc.begin(90.9)
sc.group("s13", 470, 84, ["58:currently I don't do", "64:any", "124:*scripting"], out=93.08)
sc.group("s13", 470, 84, ["58:for the videos I make", "58:because I don't", "120:*need", "64:that anymore"], out=96.2)
sc.skip("and")
sc.group("s14", 720, 40, ["58:I'm so"], out=96.58)
sc.skip("done")  # DONE behind your head
sc.group("s14", 720, 40, ["58:with that"], out=97.75)
sc.group("s15", 970, 84, ["58:but if you need", "64:then it's gonna be", "124:*helpful"], out=99.64)
sc.group("s15", 970, 84, ["58:and I'm also gonna be", "64:talking about how you can", "64:talk in front of the camera"], out=102.4)
sc.group("s15", 970, 84, ["58:without", "64:any", "136:*script"], out=103.9)
sc.group("s16", 970, 84, ["58:but I'm not", "124:*mastered", "58:at it yet"], out=105.28)
sc.group("s16", 970, 84, ["58:I'm also trying", "64:to", "136:*learn"], out=106.48)
sc.group("s16", 970, 84, ["58:so once I see I'm", "124:*qualified", "64:enough"], out=108.6)
sc.group("s16", 970, 84, ["58:maybe I'm gonna", "120:*share it", "58:with|to you"])
sc.skip("feel", "fun.")
out["ov-e"] = sc.js()

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
