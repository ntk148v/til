# X Window manager

## What is X window manager?

* A window manager which run on top of the X Window System, a windowing system mainly used on Unix-like system.
* The user can choose between various 3rd-party window managers, which differ from one another in several ways, including:
  * customizability of apperance and functionality
    * textual menus used to start programs and/or change options
    * docks and other graphical ways to start programs
    * multiple desktops and virtual desktops, and pagers to switch between them

  * consumption of memory and other system resources
  * degree of integration with a desktop environment, which provides a more complete interface to the operating system, and provides a range of integrated utilites and applications

## How X window managers work

![x-window-manager](https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Schema_of_the_layers_of_the_graphical_user_interface.svg/300px-Schema_of_the_layers_of_the_graphical_user_interface.svg.png)

## Types of window managers

* **Stacking window manager**:
  * A stack window manager renders the windows one-by-one onto the screen at specific co-ordinates. if one window's area overlaps another, then the window "on top" overwrites part of the other's visible appearance. This results in the apperance familiar to many users in which windows act a little like pieces of paper on a desktop, which can be moved around and allowed to overlap.
  * Amiwm, Blackbox, Enlightenment, Fluxbox, FVWM, Openbox.

* **Tiling window manager**:
  * A window manager with an organization of the screen into mutually non-overlapping frames (hence the name tiling), as opposed to the traditional approach of coordinate-based stacking of objects (windows) that tries to emulate the desk paradigm.
  * Awesome, dwm, ion, larswm, ratpoison, stumpwm, wmii, i3, xmonad, bspwm.

* **Compositing window manager**:
  * A compositing window manager may appear to the user similar to a stacking window manager. However, the individual windows are first renders in individual buffers, and then theirs images are composited onto the screen buffer; this two-step process means that visual effects (such as shadows, translucency) can be applied.
  * Uses more resources.
  * Mutter, Xfwm, Compiz, KWin.

* **Virtual window manager**:
  * A window manager that uses virtual screens, whose resolution can be higher than the resolution of one's monitor/display adapter thus resembling a two dimensional virtual desktop with its viewport.

## Useful installtion guide

* [reddit r/unixporn](https://www.reddit.com/r/unixporn/comments/74z2z6/easily_getting_started_with_bspwm_and_polybar/)
* [bspwm for dummies](https://github.com/windelicato/dotfiles/wiki/bspwm-for-dummies)
* [bspwm archlinux](https://wiki.archlinux.org/index.php/bspwm)

## Refs

* [Wikipedia](https://en.wikipedia.org/wiki/X_window_manager)
