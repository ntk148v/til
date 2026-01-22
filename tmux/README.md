# Tmux - Terminal multiplexer

## 1. What is tmux?

Within one terminal window you can open multiple windows and split-views (called "panes"). Each pane will contain its own, independently running shell instance (bash, zsh, ...). This allows you to have multiple terminal commands and applications running side by side without the need to open multiple terminal emulator windows.

On top of that tmux keeps these windows and panes in a session. You can exit a session at any point. This is called “detaching”. tmux will keep this session alive until you kill the tmux server (e.g. when you reboot)2. This is incredibly useful because at any later point in time you can pick that session up exactly from where you left it by simply “attaching” to that session.

![](https://arcolinux.com/wp-content/uploads/2020/02/tmux-installation-02.png)

## 2. Quick start

All commands in tmux are triggered by a **prefix key** (by default it is `C-b`) followed by a **command key**.

Check out [cheatsheet](https://tmuxcheatsheet.com).

```text
C-b %       Split panes
C-b <arrow> Move between panes
C-d         Close panes
C-b c       Create windows
C-b n       Switch the next window
C-b p       Switch the previous window
C-b d       Detach session
```

## 3. Customize

Tmux uses a file called `~/.tmux.conf`.

```tmux
# change the prefix from 'C-b' to 'C-a'
# (remap capslock to CTRL for easy access)
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# start with window 1 (instead of 0)
set -g base-index 1

# start with pane 1
set -g pane-base-index 1

# split panes using h and v, make sure they open in the same path
bind h split-window -h -c "#{pane_current_path}"
bind v split-window -v -c "#{pane_current_path}"

unbind '"'
unbind %

# open new windows in the current path
bind c new-window -c "#{pane_current_path}"

# reload config file
bind r source-file ~/.tmux.conf

unbind p
bind p previous-window

# shorten command delay
set -sg escape-time 1

# don't rename windows automatically
set -g allow-rename off

# mouse control (clickable windows, panes, resizable panes)
set -g mouse on

# Use Alt-arrow keys without prefix key to switch panes
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# enable vi mode keys
set-window-option -g mode-keys vi

# set default terminal mode to 256 colors
set -g default-terminal "xterm-256color"
set -ga terminal-overrides ",xterm-256color:Tc"

# allow focus events to get through to applications running in tmux
set -g focus-events on
set -sg escape-time 0
set -g status-interval 0
set -g status-position top
set -g mode-keys vi

# Design Tweaks
# -------------

# don't do anything when a 'bell' rings
set -g visual-activity off
set -g visual-bell off
set -g visual-silence off
setw -g monitor-activity off
set -g bell-action none

# clock mode
setw -g clock-mode-colour yellow

# copy mode
setw -g mode-style 'fg=black bg=red bold'

# panes
set -g pane-border-style 'fg=red'
set -g pane-active-border-style 'fg=yellow'

# statusbar
set -g status-position bottom
set -g status-justify left
set -g status-style 'fg=red'

set -g status-left ''
set -g status-left-length 10

set -g status-right-style 'fg=black bg=yellow'
set -g status-right '%Y-%m-%d %H:%M '
set -g status-right-length 50

setw -g window-status-current-style 'fg=black bg=red'
setw -g window-status-current-format ' #I #W #F '

setw -g window-status-style 'fg=red bg=black'
setw -g window-status-format ' #I #[fg=white]#W #[fg=yellow]#F '
setw -g window-status-bell-style 'fg=yellow bg=red bold'

# messages
set -g message-style 'fg=yellow bg=red bold'

# plugins
set -g @plugin 'rose-pine/tmux'
set -g @rose_pine_bar_bg_disable 'on'

set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'christoomey/vim-tmux-navigator'

run '~/.tmux/plugins/tpm/tpm'
```
