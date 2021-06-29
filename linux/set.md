# Set

Source: https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html

## 1. Intro

[set](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) command changes value of a shell option and set the positional parameters, or display the names and values of shell variables.

```bash
# syntax
set [--abefhkmnptuvxBCEHPT] [-o option-name] [argument …]
set [+abefhkmnptuvxBCEHPT] [+o option-name] [argument …]
```

## 2. List currently configured shell options

```bash
# Type 'set -o'
set -o
# return
noaliases             off
aliasfuncdef          off
allexport             off
noalwayslastprompt    off
alwaystoend           on
appendcreate          off
noappendhistory       off
autocd                on
autocontinue          off
noautolist            off
noautomenu            off
autonamedirs          off
noautoparamkeys       off
noautoparamslash      off
autopushd             on
noautoremoveslash     off
autoresume            off
nobadpattern          off
nobanghist            off
nobareglobqual        off
bashautolist          off
bashrematch           off
nobeep                off
nobgnice              off
braceccl              off
bsdecho               off
nocaseglob            off
nocasematch           off
cbases                off
cdablevars            off
cdsilent              off
chasedots             off
chaselinks            off
nocheckjobs           off
nocheckrunningjobs    off
noclobber             off
combiningchars        off
completealiases       off
completeinword        on
continueonerror       off
correct               off
correctall            off
cprecedences          off
cshjunkiehistory      off
cshjunkieloops        off
cshjunkiequotes       off
cshnullcmd            off
cshnullglob           off
nodebugbeforecmd      off
dvorak                off
emacs                 off
noequals              off
errexit               off
errreturn             off
noevallineno          off
noexec                off
extendedglob          off
extendedhistory       on
noflowcontrol         on
forcefloat            off
nofunctionargzero     off
noglob                off
noglobalexport        off
noglobalrcs           off
globassign            off
globcomplete          off
globdots              off
globstarshort         off
globsubst             off
nohashcmds            off
nohashdirs            off
hashexecutablesonly   off
nohashlistall         off
histallowclobber      off
nohistbeep            off
histexpiredupsfirst   on
histfcntllock         off
histfindnodups        off
histignorealldups     off
histignoredups        on
histignorespace       on
histlexwords          off
histnofunctions       off
histnostore           off
histreduceblanks      off
nohistsavebycopy      off
histsavenodups        off
histsubstpattern      off
histverify            on
nohup                 off
ignorebraces          off
ignoreclosebraces     off
ignoreeof             off
incappendhistory      off
incappendhistorytime  off
interactive           on
interactivecomments   on
ksharrays             off
kshautoload           off
kshglob               off
kshoptionprint        off
kshtypeset            off
kshzerosubscript      off
nolistambiguous       off
nolistbeep            off
listpacked            off
listrowsfirst         off
nolisttypes           off
localloops            off
localoptions          off
localpatterns         off
localtraps            off
login                 off
longlistjobs          on
magicequalsubst       off
mailwarning           off
markdirs              off
menucomplete          off
monitor               on
nomultibyte           off
nomultifuncdef        off
nomultios             off
nonomatch             off
nonotify              off
nullglob              off
numericglobsort       off
octalzeroes           off
overstrike            off
pathdirs              off
pathscript            off
pipefail              off
posixaliases          off
posixargzero          off
posixbuiltins         off
posixcd               off
posixidentifiers      off
posixjobs             off
posixstrings          off
posixtraps            off
printeightbit         off
printexitvalue        off
privileged            off
promptbang            off
nopromptcr            off
nopromptpercent       off
nopromptsp            off
promptsubst           on
pushdignoredups       on
pushdminus            on
pushdsilent           off
pushdtohome           off
rcexpandparam         off
rcquotes              off
norcs                 off
recexact              off
rematchpcre           off
restricted            off
rmstarsilent          off
rmstarwait            off
sharehistory          on
shfileexpansion       off
shglob                off
shinstdin             on
shnullcmd             off
shoptionletters       off
noshortloops          off
shwordsplit           off
singlecommand         off
singlelinezle         off
sourcetrace           off
sunkeyboardhack       off
transientrprompt      off
trapsasync            off
typesetsilent         off
nounset               off
verbose               off
vi                    off
warncreateglobal      off
warnnestedvar         off
xtrace                off
zle                   on
```

## 3. Enable an option

```bash
# set -o option-name
# set -option-abbrev
# For example
#!/bin/bash

set -o verbose
# Echoes all commands before executing.
set -v
# Exact same effect as above.
```

## 4. Disable an option

```bash
# set +o option-name
# set +option-abbrev
# Example
#!/bin/bash

set -o verbose
# Command echoing on.
command
...
command

set +o verbose
# Command echoing off.
command
# Not echoed.


set -v
# Command echoing on.
command
...
command

set +v
# Command echoing off.
command

exit 0
```

## 5. Print a trace of simple commands (print each command to stdout before executing it)

```bash
#!/bin/bash
# set -x
# set -o xtrace
set -x
echo "You will see this line"
```

## 6. Prevent overwriting of files by redirection

```bash
#!/bin/bash
# set -o noclobber
# set -C
set -C
echo "$$" > "/tmp/test"
echo "$$$" > "/tmp/test"
```

## 7. Do not resolve symbolic links when performing commands

```bash
# if /usr/sys is a symbolic link to /usr/local/sys
cd /usr/sys; echo $PWD
# /usr/sys
cd ..; pwd
# /usr
set -P
cd /usr/sys; echo $PWD
# /usr/local/sys
cd ..; pwd
# /usr/local
```

## 8. Abort script at first error, when a command exits with non-zero status

```bash
#!/bin/bash
# set -e
# set -o errexit
set -e
cd /non/exist/directory
echo "This line won't be printed"

set +e
cd /non/exist/directory
echo "This line will be printed anyway"
```
