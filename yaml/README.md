# YAML

## 1. Write multiple-line string

Source:

- <https://stackoverflow.com/questions/3790454/how-do-i-break-a-string-in-yaml-over-multiple-lines>
- <https://yaml-multiline.info/>

There are two types of formats that YAML supports for strings: _block scalar_ and _flow scalar_ formats.

### 1.1. Block scalar

A block scalar header has three parts:

- **Block Style Indicator**: The [block style](https://yaml.org/spec/1.2.2/#812-literal-style) indicates how newlines inside the block should behave. If you would like them to be kept as newlines, use the **literal** style, indicated by a pipe (`|`). If instead you want them to be replaced by spaces, use the **folded** style, indicated by a right angle bracket (`>`). (To get a newline using the folded style, leave a blank line by putting two newlines in. Lines with extra indentation are also not folded.)

- **Block Chomping Indicator**: The [chomping indicator](https://yaml.org/spec/1.2.2/#8112-block-chomping-indicator) controls what should happen with newlines at the end of the string. The default, **clip**, puts a single newline at the end of the string. To remove all newlines, strip them by putting a minus sign (`-`) after the style indicator. Both clip and strip ignore how many newlines are actually at the end of the block; to **keep** them all put a plus sign (`+`) after the style indicator.

- **Indentation Indicator**: Ordinarily, the number of spaces you're using to indent a block will be automatically guessed from its first line. You may need a [block indentation indicator](https://yaml.org/spec/1.2.2/#8111-block-indentation-indicator) if the first line of the block starts with extra spaces. In this case, simply put the number of spaces used for indentation (between 1 and 9) at the end of the header.

### 1.2. Flow scalar

- Single-quoted:

```yaml
example: 'Several lines of text,\n
··containing ''single quotes''. Escapes (like \n) don''t do anything.\n
··\n
··Newlines can be added by leaving a blank line.\n
····Leading whitespace on lines is ignored.'\n
```

- Double-quoted:

```yaml
example: "Several lines of text,\n
··containing \"double quotes\". Escapes (like \\n) work.\nIn addition,\n
··newlines can be esc\\n
··aped to prevent them from being converted to a space.\n
··\n
··Newlines can also be added by leaving a blank line.\n
····Leading whitespace on lines is ignored."\n
```

- Plain:

```yaml
example: Several lines of text,\n
··with some "quotes" of various 'types'.\n
··Escapes (like \n) don't do anything.\n
··\n
··Newlines can be added by leaving a blank line.\n
····Additional leading whitespace is ignored.\n
```
