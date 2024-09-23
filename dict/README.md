# Dictionary server protocol

Source:

- <https://shkspr.mobi/blog/2024/09/http-ftp-and-dict/>
- <https://datatracker.ietf.org/doc/html/rfc2229>

This is the first time I heard about Dictionary Server Protocol. They exist to allow you to query dictionaries over a network.

```text
For many years, the Internet community has relied on the "webster" protocol for access to natural language definitions. […] In recent years, the number of publicly available webster servers on the Internet has dramatically decreased. Fortunately, several freely-distributable dictionaries and lexicons have recently become available on the Internet. However, these freely-distributable databases are not accessible via a uniform interface, and are not accessible from a single site.
```

[The (informal) standard was published in 1997](https://datatracker.ietf.org/doc/html/rfc2229) but has kept a relatively low profile since then. You can understand why it was invented - in an age of low-size disk drives and expensive software, looking up data over a dedicated protocol seems like a nifty2 idea.

Then disk size exploded, databases became cheap, and search engines made it easy to look up words.

Run this command:

```shell
# Default database
curl dict://dict.org/d:Internet
# If you want to switch database
curl dict://dict.org/d:Internet:jargon
```

Perhaps the easiest way to explore the protocol and server is to use telnet:

```shell
telnet dict.org dict

Trying 199.48.130.6...
Connected to dict.org.
Escape character is '^]'.
220 dict.dict.org dictd 1.12.1/rf on Linux 4.19.0-10-amd64 <auth.mime> <370433951.24846.1727059196@dict.dict.org>
HELP
113 help text follows
DEFINE database word         -- look up word in database
MATCH database strategy word -- match word in database using strategy
SHOW DB                      -- list all accessible databases
SHOW DATABASES               -- list all accessible databases
SHOW STRAT                   -- list available matching strategies
SHOW STRATEGIES              -- list available matching strategies
SHOW INFO database           -- provide information about the database
SHOW SERVER                  -- provide site-specific information
OPTION MIME                  -- use MIME headers
CLIENT info                  -- identify client to server
AUTH user string             -- provide authentication information
STATUS                       -- display timing information
HELP                         -- display this help information
QUIT                         -- terminate connection

The following commands are unofficial server extensions for debugging
only.  You may find them useful if you are using telnet as a client.
If you are writing a client, you MUST NOT use these commands, since
they won't be supported on any other server!

D word                       -- DEFINE * word
D database word              -- DEFINE database word
M word                       -- MATCH * . word
M strategy word              -- MATCH * strategy word
M database strategy word     -- MATCH database strategy word
S                            -- STATUS
H                            -- HELP
Q                            -- QUIT
.
250 ok
```

Cool!
