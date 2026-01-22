import fontforge
import sys

glyphs = set()

font = fontforge.open(sys.argv[1])
font.encoding = "UnicodeFull"
for glyph in font.glyphs("encoding"):
    if (glyph.unicode > 0):
        glyphs.add(glyph.unicode)
    if (glyph.altuni != None):
        for alt in glyph.altuni:
            if (alt[0] > 0):
                glyphs.add(alt[0])

# These may not be mapped in LiberationSans 1.7 fonts,
# but are necessary to not break some tables in 2.x versions
moreglyphs = [
    0x2080,
    0x2081,
    0x2082,
    0x2083,
    0x2084,
    0x2085,
    0x2086,
    0x2087,
    0x2088,
    0x2089,
    0x2074,
    0x2075,
    0x2076,
    0x2077,
    0x2078,
    0x2079
]

for glyph in moreglyphs:
    glyphs.add(glyph)

for glyph in sorted(glyphs):
    assert glyph < 65536, "Too large unicode code point"
    print(f"U+{glyph:04X}")

if ("Italic" in font.fontname):
    # Some glyphs, such as serbian PE and TE, don't have a
    # mapping from unicode code point and are used just in
    # substitution tables in italic fonts. We add them with
    # glyph names to not break such tables in Liberation 2.x
    # fonts
    print("S_PE")
    print("S_TE")

font.close()