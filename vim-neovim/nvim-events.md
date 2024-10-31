# Nvim Events

Source: <https://gist.github.com/dtr2300/2f867c2b6c051e946ef23f92bd9d1180>

Nvim recognizes the following events. Names are case-insensitive.

<details>
<summary>BufAdd</summary>

```
Just after creating a new buffer which is
added to the buffer list, or adding a buffer
to the buffer list, a buffer in the buffer
list was renamed.
Not triggered for the initial buffers created
during startup.
Before |BufEnter|.
NOTE: Current buffer "%" may be different from
the buffer being created "<afile>".
```
</details>

<details>
<summary>BufDelete</summary>

```
Before deleting a buffer from the buffer list.
The BufUnload may be called first (if the
buffer was loaded).
Also used just before a buffer in the buffer
list is renamed.
NOTE: Current buffer "%" may be different from
the buffer being deleted "<afile>" and "<abuf>".
Do not change to another buffer.
```
</details>

<details>
<summary>BufEnter</summary>

```
After entering a buffer.  Useful for setting
options for a file type.  Also executed when
starting to edit a buffer.
After |BufAdd|.
After |BufReadPost|.
```
</details>

<details>
<summary>BufFilePost</summary>

```
After changing the name of the current buffer
with the ":file" or ":saveas" command.
```
</details>

<details>
<summary>BufFilePre</summary>

```
Before changing the name of the current buffer
with the ":file" or ":saveas" command.
```
</details>

<details>
<summary>BufHidden</summary>

```
Before a buffer becomes hidden: when there are
no longer windows that show the buffer, but
the buffer is not unloaded or deleted.

Not used for ":qa" or ":q" when exiting Vim.
NOTE: current buffer "%" may be different from
the buffer being unloaded "<afile>".
```
</details>

<details>
<summary>BufLeave</summary>

```
Before leaving to another buffer.  Also when
leaving or closing the current window and the
new current window is not for the same buffer.

Not used for ":qa" or ":q" when exiting Vim.
```
</details>

<details>
<summary>BufModifiedSet</summary>

```
After the `'modified'` value of a buffer has
been changed.
```
</details>

<details>
<summary>BufNew</summary>

```
Just after creating a new buffer.  Also used
just after a buffer has been renamed.  When
the buffer is added to the buffer list BufAdd
will be triggered too.
NOTE: Current buffer "%" may be different from
the buffer being created "<afile>".
```
</details>

<details>
<summary>BufNewFile</summary>

```
When starting to edit a file that doesn't
exist.  Can be used to read in a skeleton
file.
```
</details>

<details>
<summary>BufRead or BufReadPost</summary>

```
When starting to edit a new buffer, after
reading the file into the buffer, before
processing modelines.  See |BufWinEnter| to do
something after processing modelines.
Also triggered:
- when writing an unnamed buffer in a way that
  the buffer gets a name
- after successfully recovering a file
- for the "filetypedetect" group when
  executing ":filetype detect"
Not triggered:
- for the `:read file` command
- when the file doesn't exist
```
</details>

<details>
<summary>BufReadCmd</summary>

```
Before starting to edit a new buffer.  Should
read the file into the buffer. |Cmd-event|
```
</details>

<details>
<summary>BufReadPre</summary>

```
When starting to edit a new buffer, before
reading the file into the buffer.  Not used
if the file doesn't exist.
```
</details>

<details>
<summary>BufUnload</summary>

```
Before unloading a buffer, when the text in
the buffer is going to be freed.
After BufWritePost.
Before BufDelete.
Triggers for all loaded buffers when Vim is
going to exit.
NOTE: Current buffer "%" may be different from
the buffer being unloaded "<afile>".
Do not switch buffers or windows!
Not triggered when exiting and v:dying is 2 or
more.
```
</details>

<details>
<summary>BufWinEnter</summary>

```
After a buffer is displayed in a window.  This
may be when the buffer is loaded (after
processing modelines) or when a hidden buffer
is displayed (and is no longer hidden).

Not triggered for |:split| without arguments,
since the buffer does not change, or :split
with a file already open in a window.
Triggered for ":split" with the name of the
current buffer, since it reloads that buffer.
```
</details>

<details>
<summary>BufWinLeave</summary>

```
Before a buffer is removed from a window.
Not when it's still visible in another window.
Also triggered when exiting.
Before BufUnload, BufHidden.
NOTE: Current buffer "%" may be different from
the buffer being unloaded "<afile>".
Not triggered when exiting and v:dying is 2 or
more.
```
</details>

<details>
<summary>BufWipeout</summary>

```
Before completely deleting a buffer.  The
BufUnload and BufDelete events may be called
first (if the buffer was loaded and was in the
buffer list).  Also used just before a buffer
is renamed (also when it's not in the buffer
list).
NOTE: Current buffer "%" may be different from
the buffer being deleted "<afile>".
Do not change to another buffer.
```
</details>

<details>
<summary>BufWrite or BufWritePre</summary>

```
Before writing the whole buffer to a file.
```
</details>

<details>
<summary>BufWriteCmd</summary>

```
Before writing the whole buffer to a file.
Should do the writing of the file and reset
'modified' if successful, unless '+' is in
'cpo' and writing to another file |cpo-+|.
The buffer contents should not be changed.
When the command resets 'modified' the undo
information is adjusted to mark older undo
states as 'modified', like |:write| does.
|Cmd-event|
```
</details>

<details>
<summary>BufWritePost</summary>

```
After writing the whole buffer to a file
(should undo the commands for BufWritePre).
```
</details>

<details>
<summary>ChanInfo</summary>

```
State of channel changed, for instance the
client of a RPC channel described itself.
Sets these |v:event| keys:
    info
See |nvim_get_chan_info()| for the format of
the info Dictionary.
```
</details>

<details>
<summary>ChanOpen</summary>

```
Just after a channel was opened.
Sets these |v:event| keys:
    info
See |nvim_get_chan_info()| for the format of
the info Dictionary.
```
</details>

<details>
<summary>CmdUndefined</summary>

```
When a user command is used but it isn't
defined.  Useful for defining a command only
when it's used.  The pattern is matched
against the command name.  Both <amatch> and
<afile> expand to the command name.
NOTE: Autocompletion won't work until the
command is defined.  An alternative is to
always define the user command and have it
invoke an autoloaded function.  See |autoload|.
```
</details>

<details>
<summary>CmdlineChanged</summary>

```
After a change was made to the text inside
command line.  Be careful not to mess up the
command line, it may cause Vim to lock up.
<afile> expands to the |cmdline-char|.
```
</details>

<details>
<summary>CmdlineEnter</summary>

```
After entering the command-line (including
non-interactive use of ":" in a mapping: use
|<Cmd>| instead to avoid this).
<afile> expands to the |cmdline-char|.
Sets these |v:event| keys:
    cmdlevel
    cmdtype
```
</details>

<details>
<summary>CmdlineLeave</summary>

```
Before leaving the command-line (including
non-interactive use of ":" in a mapping: use
|<Cmd>| instead to avoid this).
<afile> expands to the |cmdline-char|.
Sets these |v:event| keys:
    abort (mutable)
    cmdlevel
    cmdtype
Note: `abort` can only be changed from false
to true: cannot execute an already aborted
cmdline by changing it to false.
```
</details>

<details>
<summary>CmdwinEnter</summary>

```
After entering the command-line window.
Useful for setting options specifically for
this special type of window.
<afile> expands to a single character,
indicating the type of command-line.
|cmdwin-char|
```
</details>

<details>
<summary>CmdwinLeave</summary>

```
Before leaving the command-line window.
Useful to clean up any global setting done
with CmdwinEnter.
<afile> expands to a single character,
indicating the type of command-line.
|cmdwin-char|
```
</details>

<details>
<summary>ColorScheme</summary>

```
After loading a color scheme. |:colorscheme|
Not triggered if the color scheme is not
found.
The pattern is matched against the
colorscheme name. <afile> can be used for the
name of the actual file where this option was
set, and <amatch> for the new colorscheme
name.
```
</details>

<details>
<summary>ColorSchemePre</summary>

```
Before loading a color scheme. |:colorscheme|
Useful to setup removing things added by a
color scheme, before another one is loaded.
```
</details>

<details>
<summary>CompleteChanged </summary>

```
CompleteChanged
After each time the Insert mode completion
menu changed.  Not fired on popup menu hide,
use |CompleteDonePre| or |CompleteDone| for
that.

Sets these |v:event| keys:
    completed_itemSee |complete-items|.
    heightnr of items visible
    widthscreen cells
    rowtop screen row
    colleftmost screen column
    sizetotal nr of items
    scrollbarTRUE if visible

Non-recursive (event cannot trigger itself).
Cannot change the text. |textlock|

The size and position of the popup are also
available by calling |pum_getpos()|.
```
</details>

<details>
<summary>CompleteDonePre</summary>

```
After Insert mode completion is done.  Either
when something was completed or abandoning
completion. |ins-completion|
|complete_info()| can be used, the info is
cleared after triggering CompleteDonePre.
The |v:completed_item| variable contains
information about the completed item.
```
</details>

<details>
<summary>CompleteDone</summary>

```
After Insert mode completion is done.  Either
when something was completed or abandoning
completion. |ins-completion|
|complete_info()| cannot be used, the info is
cleared before triggering CompleteDone.  Use
CompleteDonePre if you need it.
|v:completed_item| gives the completed item.
```
</details>

<details>
<summary>CursorHold</summary>

```
When the user doesn't press a key for the time
specified with 'updatetime'.  Not triggered
until the user has pressed a key (i.e. doesn't
fire every 'updatetime' ms if you leave Vim to
make some coffee. :)  See |CursorHold-example|
for previewing tags.
This event is only triggered in Normal mode.
It is not triggered when waiting for a command
argument to be typed, or a movement after an
operator.
While recording the CursorHold event is not
triggered. |q|

Internally the autocommand is triggered by the
<CursorHold> key. In an expression mapping
|getchar()| may see this character.

Note: Interactive commands cannot be used for
this event.  There is no hit-enter prompt,
the screen is updated directly (when needed).
Note: In the future there will probably be
another option to set the time.
Hint: to force an update of the status lines
use: >
:let &ro = &ro
```
</details>

<details>
<summary>CursorHoldI</summary>

```
Like CursorHold, but in Insert mode. Not
triggered when waiting for another key, e.g.
after CTRL-V, and not in CTRL-X mode
|insert_expand|.
```
</details>

<details>
<summary>CursorMoved</summary>

```
After the cursor was moved in Normal or Visual
mode or to another window.  Also when the text
of the cursor line has been changed, e.g. with
"x", "rx" or "p".
Not always triggered when there is typeahead,
while executing commands in a script file, or
when an operator is pending. Always triggered
when moving to another window.
For an example see |match-parens|.
Note: Cannot be skipped with |:noautocmd|.
Careful: This is triggered very often, don't
do anything that the user does not expect or
that is slow.
```
</details>

<details>
<summary>CursorMovedI</summary>

```
After the cursor was moved in Insert mode.
Not triggered when the popup menu is visible.
Otherwise the same as CursorMoved.
```
</details>

<details>
<summary>DiffUpdated</summary>

```
After diffs have been updated.  Depending on
what kind of diff is being used (internal or
external) this can be triggered on every
change or when doing |:diffupdate|.
```
</details>

<details>
<summary>DirChanged</summary>

```
After the |current-directory| was changed.
The pattern can be:
"window"  to trigger on `:lcd`
"tabpage" to trigger on `:tcd`
"global"  to trigger on `:cd`
"auto"    to trigger on 'autochdir'.
Sets these |v:event| keys:
    cwd:            current working directory
    scope:          "global", "tabpage", "window"
    changed_window: v:true if we fired the event
                    switching window (or tab)
<afile> is set to the new directory name.
Non-recursive (event cannot trigger itself).
```
</details>

<details>
<summary>DirChangedPre</summary>

```
When the |current-directory| is going to be
changed, as with |DirChanged|.
The pattern is like with |DirChanged|.
Sets these |v:event| keys:
    directory:      new working directory
    scope:          "global", "tabpage", "window"
    changed_window: v:true if we fired the event
                    switching window (or tab)
<afile> is set to the new directory name.
Non-recursive (event cannot trigger itself).
```
</details>

<details>
<summary>ExitPre</summary>

```
When using `:quit`, `:wq` in a way it makes
Vim exit, or using `:qall`, just after
|QuitPre|.  Can be used to close any
non-essential window.  Exiting may still be
cancelled if there is a modified buffer that
isn't automatically saved, use |VimLeavePre|
for really exiting.
See also |QuitPre|, |WinClosed|.
```
</details>

<details>
<summary>FileAppendCmd</summary>

```
Before appending to a file.  Should do the
appending to the file.  Use the '[ and ']
marks for the range of lines. |Cmd-event|
```
</details>

<details>
<summary>FileAppendPost</summary>

```
After appending to a file.
```
</details>

<details>
<summary>FileAppendPre</summary>

```
Before appending to a file.  Use the '[ and ']
marks for the range of lines.
```
</details>

<details>
<summary>FileChangedRO</summary>

```
Before making the first change to a read-only
file.  Can be used to checkout the file from
a source control system.  Not triggered when
the change was caused by an autocommand.
Triggered when making the first change in
a buffer or the first change after 'readonly'
was set, just before the change is applied to
the text.
WARNING: If the autocommand moves the cursor
the effect of the change is undefined.

Cannot switch buffers.  You can reload the
buffer but not edit another one.

If the number of lines changes saving for undo
may fail and the change will be aborted.
```
</details>

<details>
<summary>FileChangedShell</summary>

```
When Vim notices that the modification time of
a file has changed since editing started.
Also when the file attributes of the file
change or when the size of the file changes.
|timestamp|
Triggered for each changed file, after:
- executing a shell command
- |:checktime|
- |FocusGained|

Not used when 'autoread' is set and the buffer
was not changed.  If a FileChangedShell
autocommand exists the warning message and
prompt is not given.
|v:fcs_reason| indicates what happened. Set
|v:fcs_choice| to control what happens next.
NOTE: Current buffer "%" may be different from
the buffer that was changed "<afile>".

Cannot switch, jump to or delete buffers.
Non-recursive (event cannot trigger itself).
```
</details>

<details>
<summary>FileChangedShellPost</summary>

```
After handling a file that was changed outside
of Vim.  Can be used to update the statusline.
```
</details>

<details>
<summary>FileReadCmd</summary>

```
Before reading a file with a ":read" command.
Should do the reading of the file. |Cmd-event|
```
</details>

<details>
<summary>FileReadPost</summary>

```
After reading a file with a ":read" command.
Note that Vim sets the '[ and '] marks to the
first and last line of the read.  This can be
used to operate on the lines just read.
```
</details>

<details>
<summary>FileReadPre</summary>

```
Before reading a file with a ":read" command.
```
</details>

<details>
<summary>FileType</summary>

```
When the 'filetype' option has been set.  The
pattern is matched against the filetype.
<afile> is the name of the file where this
option was set.  <amatch> is the new value of
'filetype'.
Cannot switch windows or buffers.
See |filetypes|.
```
</details>

<details>
<summary>FileWriteCmd</summary>

```
Before writing to a file, when not writing the
whole buffer.  Should do the writing to the
file.  Should not change the buffer.  Use the
'[ and '] marks for the range of lines.
|Cmd-event|
```
</details>

<details>
<summary>FileWritePost</summary>

```
After writing to a file, when not writing the
whole buffer.
```
</details>

<details>
<summary>FileWritePre</summary>

```
Before writing to a file, when not writing the
whole buffer.  Use the '[ and '] marks for the
range of lines.
```
</details>

<details>
<summary>FilterReadPost</summary>

```
After reading a file from a filter command.
Vim checks the pattern against the name of
the current buffer as with FilterReadPre.
Not triggered when 'shelltemp' is off.
```
</details>

<details>
<summary>FilterReadPre</summary>

```
Before reading a file from a filter command.
Vim checks the pattern against the name of
the current buffer, not the name of the
temporary file that is the output of the
filter command.
Not triggered when 'shelltemp' is off.
```
</details>

<details>
<summary>FilterWritePost</summary>

```
After writing a file for a filter command or
making a diff with an external diff (see
|DiffUpdated| for internal diff).
Vim checks the pattern against the name of
the current buffer as with FilterWritePre.
Not triggered when 'shelltemp' is off.
```
</details>

<details>
<summary>FilterWritePre</summary>

```
Before writing a file for a filter command or
making a diff with an external diff.
Vim checks the pattern against the name of
the current buffer, not the name of the
temporary file that is the output of the
filter command.
Not triggered when 'shelltemp' is off.
```
</details>

<details>
<summary>FocusGained</summary>

```
Nvim got focus.
```
</details>

<details>
<summary>FocusLost</summary>

```
Nvim lost focus.  Also (potentially) when
a GUI dialog pops up.
```
</details>

<details>
<summary>FuncUndefined</summary>

```
When a user function is used but it isn't
defined.  Useful for defining a function only
when it's used.  The pattern is matched
against the function name.  Both <amatch> and
<afile> are set to the name of the function.
NOTE: When writing Vim scripts a better
alternative is to use an autoloaded function.
See |autoload-functions|.
```
</details>

<details>
<summary>UIEnter</summary>

```
After a UI connects via |nvim_ui_attach()|, or
after builtin TUI is started, after |VimEnter|.
Sets these |v:event| keys:
    chan: 0 for builtin TUI
          1 for |--embed|
          |channel-id| of the UI otherwise
```
</details>

<details>
<summary>UILeave</summary>

```
After a UI disconnects from Nvim, or after
builtin TUI is stopped, after |VimLeave|.
Sets these |v:event| keys:
    chan: 0 for builtin TUI
          1 for |--embed|
          |channel-id| of the UI otherwise
```
</details>

<details>
<summary>InsertChange</summary>

```
When typing <Insert> while in Insert or
Replace mode.  The |v:insertmode| variable
indicates the new mode.
Be careful not to move the cursor or do
anything else that the user does not expect.
```
</details>

<details>
<summary>InsertCharPre</summary>

```
When a character is typed in Insert mode,
before inserting the char.
The |v:char| variable indicates the char typed
and can be changed during the event to insert
a different character.  When |v:char| is set
to more than one character this text is
inserted literally.

Cannot change the text. |textlock|
Not triggered when 'paste' is set.
```
</details>

<details>
<summary>InsertEnter</summary>

```
Just before starting Insert mode.  Also for
Replace mode and Virtual Replace mode.  The
|v:insertmode| variable indicates the mode.
Be careful not to do anything else that the
user does not expect.
The cursor is restored afterwards.  If you do
not want that set |v:char| to a non-empty
string.
```
</details>

<details>
<summary>InsertLeavePre</summary>

```
Just before leaving Insert mode.  Also when
using CTRL-O |i_CTRL-O|.  Be careful not to
change mode or use `:normal`, it will likely
cause trouble.
```
</details>

<details>
<summary>InsertLeave</summary>

```
Just after leaving Insert mode.  Also when
using CTRL-O |i_CTRL-O|.  But not for |i_CTRL-C|.
```
</details>

<details>
<summary>MenuPopup</summary>

```
Just before showing the popup menu (under the
right mouse button).  Useful for adjusting the
menu for what is under the cursor or mouse
pointer.
The pattern is matched against one or two
characters representing the mode:
n    Normal
v    Visual
o    Operator-pending
i    Insert
c    Command line
tl   Terminal
```
</details>

<details>
<summary>ModeChanged</summary>

```
After changing the mode. The pattern is
matched against `'old_mode:new_mode'`, for
example match against `*:c` to simulate
|CmdlineEnter|.
The following values of |v:event| are set:
old_mode The mode before it changed.
new_mode The new mode as also returned
by |mode()| called with a
non-zero argument.
When ModeChanged is triggered, old_mode will
have the value of new_mode when the event was
last triggered.
This will be triggered on every minor mode
change.
Usage example to use relative line numbers
when entering visual mode: >
:au ModeChanged [vV\x16]*:* let &l:rnu = mode() =~# '^[vV\x16]'
:au ModeChanged *:[vV\x16]* let &l:rnu = mode() =~# '^[vV\x16]'
:au WinEnter,WinLeave * let &l:rnu = mode() =~# '^[vV\x16]'
```
</details>

<details>
<summary>OptionSet</summary>

```
After setting an option (except during
|startup|).  The |autocmd-pattern| is matched
against the long option name.  |<amatch>|
indicates what option has been set.

|v:option_type| indicates whether it's global
or local scoped.
|v:option_command| indicates what type of
set/let command was used (follow the tag to
see the table).
|v:option_new| indicates the newly set value.
|v:option_oldlocal| has the old local value.
|v:option_oldglobal| has the old global value.
|v:option_old| indicates the old option value.

|v:option_oldlocal| is only set when |:set|
or |:setlocal| or a |modeline| was used to set
the option. Similarly |v:option_oldglobal| is
only set when |:set| or |:setglobal| was used.

Note that when setting a |global-local| string
option with |:set|, then |v:option_old| is the
old global value. However, for all other kinds
of options (local string options, global-local
number options, ...) it is the old local
value.

OptionSet is not triggered on startup and for
the 'key' option for obvious reasons.

Usage example: Check for the existence of the
directory in the 'backupdir' and 'undodir'
options, create the directory if it doesn't
exist yet.

Note: Do not reset the same option during this
autocommand, that may break plugins. You can
always use |:noautocmd| to prevent triggering
OptionSet.

Non-recursive: |:set| in the autocommand does
not trigger OptionSet again.
```
</details>

<details>
<summary>QuickFixCmdPre</summary>

```
Before a quickfix command is run (|:make|,
|:lmake|, |:grep|, |:lgrep|, |:grepadd|,
|:lgrepadd|, |:vimgrep|, |:lvimgrep|,
|:vimgrepadd|, |:lvimgrepadd|,
|:cfile|, |:cgetfile|, |:caddfile|, |:lfile|,
|:lgetfile|, |:laddfile|, |:helpgrep|,
|:lhelpgrep|, |:cexpr|, |:cgetexpr|,
|:caddexpr|, |:cbuffer|, |:cgetbuffer|,
|:caddbuffer|).
The pattern is matched against the command
being run.  When |:grep| is used but 'grepprg'
is set to "internal" it still matches "grep".
This command cannot be used to set the
'makeprg' and 'grepprg' variables.
If this command causes an error, the quickfix
command is not executed.
```
</details>

<details>
<summary>QuickFixCmdPost</summary>

```
Like QuickFixCmdPre, but after a quickfix
command is run, before jumping to the first
location. For |:cfile| and |:lfile| commands
it is run after the error file is read and
before moving to the first error.
See |QuickFixCmdPost-example|.
```
</details>

<details>
<summary>QuitPre</summary>

```
When using `:quit`, `:wq` or `:qall`, before
deciding whether it closes the current window
or quits Vim.  For `:wq` the buffer is written
before QuitPre is triggered.  Can be used to
close any non-essential window if the current
window is the last ordinary window.
See also |ExitPre|, |WinClosed|.
```
</details>

<details>
<summary>RemoteReply</summary>

```
When a reply from a Vim that functions as
server was received server2client().  The
pattern is matched against the {serverid}.
<amatch> is equal to the {serverid} from which
the reply was sent, and <afile> is the actual
reply string.
Note that even if an autocommand is defined,
the reply should be read with remote_read()
to consume it.
```
</details>

<details>
<summary>SearchWrapped</summary>

```
After making a search with |n| or |N| if the
search wraps around the document back to
the start/finish respectively.
```
</details>

<details>
<summary>RecordingEnter</summary>

```
When a macro starts recording.
The pattern is the current file name, and
|reg_recording()| is the current register that
is used.
```
</details>

<details>
<summary>RecordingLeave</summary>

```
When a macro stops recording.
The pattern is the current file name, and
|reg_recording()| is the recorded
register.
|reg_recorded()| is only updated after this
event.
Sets these |v:event| keys:
    regcontents
    regname
```
</details>

<details>
<summary>SessionLoadPost</summary>

```
After loading the session file created using
the |:mksession| command.
```
</details>

<details>
<summary>ShellCmdPost</summary>

```
After executing a shell command with |:!cmd|,
|:make| and |:grep|.  Can be used to check for
any changed files.
For non-blocking shell commands, see
|job-control|.
```
</details>

<details>
<summary>Signal</summary>

```
After Nvim receives a signal. The pattern is
matched against the signal name. Only
"SIGUSR1" and "SIGWINCH" are supported.  Example: >
    autocmd Signal SIGUSR1 call some#func()
```
</details>

<details>
<summary>ShellFilterPost</summary>

```
After executing a shell command with
":{range}!cmd", ":w !cmd" or ":r !cmd".
Can be used to check for any changed files.
```
</details>

<details>
<summary>SourcePre</summary>

```
Before sourcing a vim/lua file. |:source|
<afile> is the name of the file being sourced.
```
</details>

<details>
<summary>SourcePost</summary>

```
After sourcing a vim/lua file. |:source|
<afile> is the name of the file being sourced.
Not triggered when sourcing was interrupted.
Also triggered after a SourceCmd autocommand
was triggered.
```
</details>

<details>
<summary>SourceCmd</summary>

```
When sourcing a vim/lua file. |:source|
<afile> is the name of the file being sourced.
The autocommand must source this file.
|Cmd-event|
```
</details>

<details>
<summary>SpellFileMissing</summary>

```
When trying to load a spell checking file and
it can't be found.  The pattern is matched
against the language.  <amatch> is the
language, 'encoding' also matters.  See
|spell-SpellFileMissing|.
```
</details>

<details>
<summary>StdinReadPost</summary>

```
During startup, after reading from stdin into
the buffer, before executing modelines. |--|
```
</details>

<details>
<summary>StdinReadPre</summary>

```
During startup, before reading from stdin into
the buffer. |--|
```
</details>

<details>
<summary>SwapExists</summary>

```
Detected an existing swap file when starting
to edit a file.  Only when it is possible to
select a way to handle the situation, when Vim
would ask the user what to do.
The |v:swapname| variable holds the name of
the swap file found, <afile> the file being
edited.  |v:swapcommand| may contain a command
to be executed in the opened file.
The commands should set the |v:swapchoice|
variable to a string with one character to
tell Vim what should be done next:
'o'    open read-only
'e'    edit the file anyway
'r'    recover
'd'    delete the swap file
'q'    quit, don't edit the file
'a'    abort, like hitting CTRL-C
When set to an empty string the user will be
asked, as if there was no SwapExists autocmd.

Cannot change to another buffer, change
the buffer name or change directory.
```
</details>

<details>
<summary>Syntax</summary>

```
When the 'syntax' option has been set.  The
pattern is matched against the syntax name.
<afile> expands to the name of the file where
this option was set. <amatch> expands to the
new value of 'syntax'.
See |:syn-on|.
```
</details>

<details>
<summary>TabEnter</summary>

```
Just after entering a tab page. |tab-page|
After WinEnter.
Before BufEnter.
```
</details>

<details>
<summary>TabLeave</summary>

```
Just before leaving a tab page. |tab-page|
After WinLeave.
```
</details>

<details>
<summary>TabNew</summary>

```
When creating a new tab page. |tab-page|
After WinEnter.
Before TabEnter.
```
</details>

<details>
<summary>TabNewEntered</summary>

```
After entering a new tab page. |tab-page|
After BufEnter.
```
</details>

<details>
<summary>TabClosed</summary>

```
After closing a tab page. <afile> expands to
the tab page number.
```
</details>

<details>
<summary>TermOpen</summary>

```
When a |terminal| job is starting.  Can be
used to configure the terminal buffer.
```
</details>

<details>
<summary>TermEnter</summary>

```
After entering |Terminal-mode|.
After TermOpen.
```
</details>

<details>
<summary>TermLeave</summary>

```
After leaving |Terminal-mode|.
After TermClose.
```
</details>

<details>
<summary>TermClose</summary>

```
When a |terminal| job ends.
Sets these |v:event| keys:
    status
```
</details>

<details>
<summary>TermResponse</summary>

```
After the response to t_RV is received from
the terminal.  The value of |v:termresponse|
can be used to do things depending on the
terminal version.  May be triggered halfway
through another event (file I/O, a shell
command, or anything else that takes time).
```
</details>

<details>
<summary>TextChanged</summary>

```
After a change was made to the text in the
current buffer in Normal mode.  That is after
|b:changedtick| has changed (also when that
happened before the TextChanged autocommand
was defined).
Not triggered when there is typeahead or when
an operator is pending.
Note: Cannot be skipped with `:noautocmd`.
Careful: This is triggered very often, don't
do anything that the user does not expect or
that is slow.
```
</details>

<details>
<summary>TextChangedI</summary>

```
After a change was made to the text in the
current buffer in Insert mode.
Not triggered when the popup menu is visible.
Otherwise the same as TextChanged.
```
</details>

<details>
<summary>TextChangedP</summary>

```
After a change was made to the text in the
current buffer in Insert mode, only when the
popup menu is visible.  Otherwise the same as
TextChanged.
```
</details>

<details>
<summary>TextChangedT</summary>

```
After a change was made to the text in the
current buffer in |Terminal-mode|.  Otherwise
the same as TextChanged.
```
</details>

<details>
<summary>TextYankPost</summary>

```
Just after a |yank| or |deleting| command, but not
if the black hole register |quote_| is used nor
for |setreg()|. Pattern must be *.
Sets these |v:event| keys:
    inclusive
    operator
    regcontents
    regname
    regtype
    visual
The `inclusive` flag combined with the |'[|
and |']| marks can be used to calculate the
precise region of the operation.

Non-recursive (event cannot trigger itself).
Cannot change the text. |textlock|
```
</details>

<details>
<summary>User</summary>

```
Not executed automatically.  Use |:doautocmd|
to trigger this, typically for "custom events"
in a plugin.  Example: >
    :autocmd User MyPlugin echom 'got MyPlugin event'
    :doautocmd User MyPlugin
```
</details>

<details>
<summary>UserGettingBored</summary>

```
When the user presses the same key 42 times.
Just kidding! :-)
```
</details>

<details>
<summary>VimEnter</summary>

```
After doing all the startup stuff, including
loading vimrc files, executing the "-c cmd"
arguments, creating all windows and loading
the buffers in them.
Just before this event is triggered the
|v:vim_did_enter| variable is set, so that you
can do: >
   if v:vim_did_enter
     call s:init()
   else
     au VimEnter * call s:init()
   endif
```
</details>

<details>
<summary>VimLeave</summary>

```
Before exiting Vim, just after writing the
.shada file.  Executed only once, like
VimLeavePre.
Use |v:dying| to detect an abnormal exit.
Use |v:exiting| to get the exit code.
Not triggered if |v:dying| is 2 or more.
```
</details>

<details>
<summary>VimLeavePre</summary>

```
Before exiting Vim, just before writing the
.shada file.  This is executed only once,
if there is a match with the name of what
happens to be the current buffer when exiting.
Mostly useful with a "*" pattern. >
   :autocmd VimLeavePre * call CleanupStuff()
Use |v:dying| to detect an abnormal exit.
Use |v:exiting| to get the exit code.
Not triggered if |v:dying| is 2 or more.
```
</details>

<details>
<summary>VimResized</summary>

```
After the Vim window was resized, thus 'lines'
and/or 'columns' changed.  Not when starting
up though.
```
</details>

<details>
<summary>VimResume</summary>

```
After Nvim resumes from |suspend| state.
```
</details>

<details>
<summary>VimSuspend</summary>

```
Before Nvim enters |suspend| state.
```
</details>

<details>
<summary>WinClosed</summary>

```
When closing a window, just before it is
removed from the window layout.  The pattern
is matched against the |window-ID|.  Both
<amatch> and <afile> are set to the |window-ID|.
After WinLeave.
Non-recursive (event cannot trigger itself).
See also |ExitPre|, |QuitPre|.
```
</details>

<details>
<summary>WinEnter</summary>

```
After entering another window.  Not done for
the first window, when Vim has just started.
Useful for setting the window height.
If the window is for another buffer, Vim
executes the BufEnter autocommands after the
WinEnter autocommands.
Note: For split and tabpage commands the
WinEnter event is triggered after the split
or tab command but before the file is loaded.
```
</details>

<details>
<summary>WinLeave</summary>

```
Before leaving a window.  If the window to be
entered next is for a different buffer, Vim
executes the BufLeave autocommands before the
WinLeave autocommands (but not for ":new").
Not used for ":qa" or ":q" when exiting Vim.
Before WinClosed.
```
</details>

<details>
<summary>WinNew</summary>

```
When a new window was created.  Not done for
the first window, when Vim has just started.
Before WinEnter.
```
</details>

<details>
<summary>WinScrolled</summary>

```
After any window in the current tab page
scrolled the text (horizontally or vertically)
or changed width or height.  See
|win-scrolled-resized|.

The pattern is matched against the |window-ID|
of the first window that scrolled or resized.
Both <amatch> and <afile> are set to the
|window-ID|.

|v:event| is set with information about size
and scroll changes. |WinScrolled-event|

Only starts triggering after startup finished
and the first screen redraw was done.
Does not trigger when defining the first
WinScrolled or WinResized event, but may
trigger when adding more.

Non-recursive: the event will not trigger
while executing commands for the WinScrolled
event.  However, if the command causes a
window to scroll or change size, then another
WinScrolled event will be triggered later.
```
</details>

<details>
<summary>WinResized</summary>

```
After a window in the current tab page changed
width or height.
See |win-scrolled-resized|.

|v:event| is set with information about size
changes. |WinResized-event|

Same behavior as |WinScrolled| for the
pattern, triggering and recursiveness.
```
</details>
