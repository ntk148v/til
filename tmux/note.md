✦ tmux and neovim use opposite naming for splits.

```text
┌──────────────┬─────────────────────┬─────────────────┬───────────────┐
│ Concept      │ neovim Command      │ tmux Command    │ Result        │
├──────────────┼─────────────────────┼─────────────────┼───────────────┤
│ Side-by-Side │ :vsplit (Vertical)  │ split-window -h │ [ 1 ]         │
│ Stacked      │ :split (Horizontal) │ split-window -v │ [ 1 ] / [ 2 ] │
└──────────────┴─────────────────────┴─────────────────┴───────────────┘
```

Why the confusion?

- Neovim names the split by the resulting layout:
  - :vsplit = I want a vertical divider between panes.
- Tmux names the split by the axis being cut:
  - -h = Cut the horizontal axis (the width) into two.

Quick Reference

- Side-by-Side: v in Vim, -h in Tmux.
- Stacked: s in Vim, -v in Tmux.
