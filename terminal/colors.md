# Terminal colors

Source: <https://github.com/termstandard/colors>

There exists common confusion about terminal colors. This is what we have right now:

- Plain ASCII
- ANSI escape codes: 16 color codes with bold/italic and background
- 256 color palette: 216 colors + 16 ANSI + 24 gray (colors are 24-bit)
- 24-bit truecolor: "888" colors (aka 16 million)

The 256-color palette is configured at start and is a 666-cube of colors, each of them defined as a 24-bit (888 RGB) color.

This means that current support can only display 256 different colors in the terminal while "truecolor" means that you can display 16 million different colors at the same time.

Truecolor escape codes do not use a color palette. They just specify the color directly.

For a quick check of your terminal, run:

```bash
printf "\x1b[38;2;255;100;0mTRUECOLOR\x1b[0m\n"
```

which will print <span style="color:#ff6400">TRUECOLOR</span> in brown if it understands Xterm-style true-color escapes.
