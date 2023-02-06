# Fonts

- [Fonts](#fonts)
  - [1. Basics of font classification](#1-basics-of-font-classification)
  - [2. Font file types](#2-font-file-types)
    - [2.1. WOFF/WOFF2](#21-woffwoff2)
    - [2.2. SVG/SVGZ](#22-svgsvgz)
    - [2.3. EOT](#23-eot)
    - [2.4. OTF/TTF](#24-otfttf)

## 1. Basics of font classification

A quick summary of the most import classification:

- **Serif fonts** have largely utilized with print (books, newspapers,...). A [serif](https://en.wikipedia.org/wiki/Serif) is a small line attached to the end of a stroke in a letter or symbol. For fonts, the 'serf' line can be emellished in different ways to give it it's own unique look. Serif fonts are considered to more classical and elegant, and will talk to older audiences.

- **Sans serif fonts** are just that: fonts without serif lines attached. These are better suited for computer screens and smartphones. This is the reason why you'll primarily find the use of a sans serif font on most websites. Unsurprisingly, they are the dearest to the heart of the younger generations.

- **Script fonts** are modeled after 17th century handwriting styles. Like most font types, script has its own subsets, broken into formal and casual variants.

_Source_: <https://www.wix.com/blog/2018/01/how-to-choose-best-fonts-website>

## 2. Font file types

### 2.1. WOFF/WOFF2

- Web Open Font Format.
- WOFF fonts often load faster than other formats because they use a compressed version of the structure used by OpenType (OTF) and TrueType (TTF) fonts. This format can also include metadata and license info within the font file.

### 2.2. SVG/SVGZ

- Scalable Vector Graphics (Font).
- SVG is a vector re-creation of the font, which make it much lighter in file size, and also makes it ideal for mobile use.
- SVGZ is the zipped version of SVG.

### 2.3. EOT

- Embedded Open Type.
- In fact, it’s the only format that IE8 and below will recognize when using @font-face.

### 2.4. OTF/TTF

- TrueType Font (TTF):
  - A joint effort by Apple and Microsoft (late 1980s)
  - Include both the screen and the printer font data in a single file.
- OpenType Font (OTF):
  - A joint effort by Adobe and Microsoft.
  - Cross platform.
  - Include the display and printer font data in a single package
  - OTF extended TTF by offering many capabilities that the latter wasn't capable of providing. For example, OTF featured a format that allowed for the storage of up to 65,000 characters.
- For designers, both amateur and professional, the main useful difference between OTF and TTF is in the advanced typesetting features. In addition, OTF features embellishments like ligatures and alternate characters—also known as glyphs—that exist to give designers more options to work with.
- For most of us non-designers, the additional options will likely go unused.
- In other words, OTF is indeed the "better" of the two due to the additional features and options, but for the average computer user, those differences don't really matter.
