from fugashi import Tagger
import jaconv

def is_kana(str):
    return not (jaconv.hira2kata(str) == str and jaconv.kata2hira(str) == str)

def split(surface, hiragana):
    out_surface = []
    out_hiragana = []
    while len(surface) > 0 and len(hiragana) > 0:

        # deal with both kana
        if surface[0] == hiragana[0]:
            out_surface.append(surface[0])
            out_hiragana.append(hiragana[0])

            surface = surface[1:]
            hiragana = hiragana[1:]
            continue

        # We have a kanji at the first spot in out_surface.
        kanji_group = ""
        while len(surface) > 0 and not is_kana(surface[0]):
            kanji_group += surface[0]
            surface = surface[1:]
        # kanji_group is the whole kanji phrase  

        if len(surface) == 0:
            out_surface.append(kanji_group)
            out_hiragana.append(hiragana)
        else:
            hiragana_group = ""
            while len(hiragana) > 0 and not hiragana[0] == surface[0]:
                hiragana_group += hiragana[0]
                hiragana = hiragana[1:]

            out_surface.append(kanji_group)
            out_hiragana.append(hiragana_group)
    return out_surface, out_hiragana

print(split( "いちご狩り", "いちごががり"))
print(split( "狩い狩ちご狩り9狩", "ががいがちごががりががが"))

tagger = Tagger('-Owakati')
text = "麩菓子は、麩を主材料とした日本の菓子 9いちご狩り"

out = tagger(text)
all_surface = [x.surface for x in out]
all_kana = [jaconv.kata2hira(x.feature.kana) if x.feature.kana else None for x in out]

out = []

for (surface, hiragana) in zip(all_surface, all_kana):
    print(surface, hiragana, is_kana(surface))
    if (hiragana == "*" or hiragana == None):
        out.append(surface)
    elif (hiragana == surface):
        out.append(surface)
    elif (jaconv.hira2kata(hiragana) == surface):
        out.append(surface)
    else:
        ss, sh = split(surface, hiragana)
        for s, h in zip(ss, sh):
            if is_kana(s):
                out.append(s)
            else:
                out.append(f"<ruby>{s}<rt>{h}</rt></ruby>")

print("".join(out))