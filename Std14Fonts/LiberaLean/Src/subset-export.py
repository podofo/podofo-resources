import sys
import os
import fontforge
import psMat

# args: glyphlist.txt input.sfd output.otf
glyphs_file = sys.argv[1]
infile  = sys.argv[2]
outfile = sys.argv[3]

# load font
font = fontforge.open(infile)

# read list of glyph names/codepoints
with open(glyphs_file, 'r') as f:
    wanted = [line.strip() for line in f if line.strip()]

font.encoding = "UnicodeFull"
# deselect all then select only wanted
font.selection.none()
for g in wanted:
    try:
        font.selection.select(("more","unicode"),g)
    except Exception as e:
        print(f"Warning: cannot select {g}: {e}")

# remove everything not selected
font.selection.invert()
font.clear()

description = next(t for t in font.sfnt_names if t[1] == 'Descriptor')[2] + "\n\nLiberation Font subset version 1.0, based on Liberation 2.1.5 with glyphs present in Liberation 1.07.5"
font.fontname = font.fontname.replace("Liberation", "LiberaLean")
font.familyname = font.familyname.replace("Liberation", "Libera Lean")
font.fullname = font.fullname.replace("Liberation", "Libera Lean")
font.copyright = font.copyright + "\nLibera Lean subset copyright (c) 2026 Francesco Pretto"
font.appendSFNTName('English (US)', 'Descriptor', description)


# generate output
font.generate(outfile, flags=('no-FFTM-table', 'omit-instructions', 'round'))
font.close()
