# Vim snippets

Source:

- <https://github.com/honza/vim-snippets>
- <https://bhupesh-v.github.io/learn-how-to-use-code-snippets-vim-cowboy/>

## 1. Getting started

- [Snippet](https://en.wikipedia.org/wiki/Snippet_(programming) is a programming term for a small region of re-usable source code, machine code, or text. Ordinarily, these are formally defined operative units to incorporate into larger programming modules.

```bash
                ---------------------
                |  Snippet Provider | [vim-snippets]
                ---------------------
                          |
                          v
                --------------------
                |  Snippet Manager | [Ultisnips, snipMate]
                --------------------
                          |
                          v
                --------------------
                |  Code Completion | [YCM, deoplete, coc]
                --------------------

```

- Installation.

```vim
" Plug
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'
```

```bash
# Vim
mkdir -p ~/.vim/pack/bundle/start && cd $_
git clone https://github.com/SirVer/ultisnips.git
git clone https://github.com/honza/vim-snippets.git
```

## 2. How to use ultisnips

- Type "snippet trigger" (for example, `fun` -> Go function. Check [vim-snippet](https://github.com/honza/vim-snippets/tree/master/snippets) for the complete list) and press `<tab>` in insert mode to evaluate the snippet block.
- Use `Ctrl + j` to jump forward within the snippet.
- Use `Ctrl + k` to jump backward within the snippet.
- Use `Ctrl + <tab>` to list all the snippets available for the current file-type

```vim
   g:UltiSnipsExpandTrigger               <tab>
   g:UltiSnipsListSnippets                <c-tab>
   g:UltiSnipsJumpForwardTrigger          <c-j>
   g:UltiSnipsJumpBackwardTrigger         <c-k>
```
