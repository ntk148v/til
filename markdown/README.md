# Markdown

## 1. Citation

Markdown has no dedicated citation syntax, sadly. Your best bet is something like this:

> Quote here.
>
> -- <cite>Benjamin Franklin</cite> --

## 2. Superscript & Subscript

This is some <sup>superscript</sup> text and <sub>subscript</sub> text.

## 3. Footnotes

[Footnotes now supported in Markdown fields](https://github.blog/changelog/2021-09-30-footnotes-now-supported-in-markdown-fields/). You can add footnotes to your content by using this bracket syntax:

```markdown
Here is a simple footnote[^1].

A footnote can also have multiple lines[^2].

[^1]: My reference.
[^2]:
    To add line breaks within a footnote, prefix new lines with 2 spaces.
    This is a second line.
```

This footnote will render like this:

Here is a simple footnote[^1].

A footnote can also have multiple lines[^2].

[^1]: My reference.
[^2]:
    To add line breaks within a footnote, prefix new lines with 2 spaces.
    This is a second line.
