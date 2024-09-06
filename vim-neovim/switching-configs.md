# Switching configs in Neovim

## 1. Problem

Learning how to configure Neovim can be overwhelming, meanwhile there are so many nice and functional pre-built configurations ([LazyVim](https://www.lazyvim.org/), [NvChad](https://nvchad.com/), [AstroNvim](https://astronvim.com/), [LunarVim](https://www.lunarvim.org/) or [kickstart](https://github.com/nvim-lua/kickstart.nvim)). Just try them and see what fits you most.

But the problem is most installation instructions will tell you to install new configurations directly to `~/.config/nvim`, once you do, you lose the previous config. You can only have onee Neovim config installed at a time.

## 2. Solution

To be able to use more than one config:

- Install the pre-built configurations to custom `~/.config` subdirectory.

```shell
git clone https://github.com/nvim-lua/kickstart.nvim.git "${XDG_CONFIG_HOME:-$HOME/.config}"/nvim-kickstart
```

- Each time you open Neovim, specify which config you want by setting the `NVIM_APPNAME` environment variable.

```shell
NVIM_APPNAME=nvim-kickstart nvim
```

Neovim uses `NVIM_APPNAME` to determine which config directory to load. If you don’t include it (or set it to an invalid value), Neovim will use the default config in `~/.config/nvim`.

## 3. Furthermore

Typing `NVIM_APP=` everytime you use nvim is tiring. You can use `alias` or `select` to reduce tiredness.
