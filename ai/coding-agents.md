# Coding agents

## 1. OpenCode

## 2. Pi

> [!IMPORTANT]
> Pi and OpenCode are both AI coding agents, but they prioritize different philosophies: OpenCode is a feature-rich "batteries-included" experience (like VS Code) with built-in tools for planning and debugging. Pi is a minimal, fast, and highly customizable "harness" (like Neovim) focusing on core read/write/edit tasks, often preferred for its efficiency.

Source:

- <https://pi.dev/>
- <https://mariozechner.at/posts/2025-11-30-pi-coding-agent/>
- <https://nader.substack.com/p/how-to-build-a-custom-agent-framework>

### 2.1. Pi's design philosophy?

Pi emphasizes extensibility without dictating workflows. Features like sub-agents or plan modes can be built via extensions, skills, or packages, keeping the core lean.

- Minimal system prompt:

  You are an expert coding assistant. You help users with coding tasks by reading files, executing commands, editing code, and writing new files.

  Available tools:
  - read: Read file contents
  - bash: Execute bash commands
  - edit: Make surgical edits to files
  - write: Create or overwrite files

  Guidelines:
  - Use bash for file operations like ls, grep, find
  - Use read to examine files before editing
  - Use edit for precise changes (old text must match exactly)
  - Use write only for new files or complete rewrites
  - When summarizing your actions, output plain text directly - do NOT use cat or bash to display what you did
  - Be concise in your responses
  - Show file paths clearly when working with files

  Documentation:
  - Your own documentation (including custom model setup and theme creation) is at: /path/to/README.md
  - Read it when users ask about features, configuration, or setup, and especially if the user asks you to add a custom model or provider, or create a custom theme.

- Minimal toolset:

  read
  Read the contents of a file. Supports text files and images (jpg, png,
  gif, webp). Images are sent as attachments. For text files, defaults to
  first 2000 lines. Use offset/limit for large files.
  - path: Path to the file to read (relative or absolute)
  - offset: Line number to start reading from (1-indexed)
  - limit: Maximum number of lines to read

  write
  Write content to a file. Creates the file if it doesn't exist, overwrites
  if it does. Automatically creates parent directories.
  - path: Path to the file to write (relative or absolute)
  - content: Content to write to the file

  edit
  Edit a file by replacing exact text. The oldText must match exactly
  (including whitespace). Use this for precise, surgical edits.
  - path: Path to the file to edit (relative or absolute)
  - oldText: Exact text to find and replace (must match exactly)
  - newText: New text to replace the old text with

  bash
  Execute a bash command in the current working directory. Returns stdout
  and stderr. Optionally provide a timeout in seconds.
  - command: Bash command to execute
  - timeout: Timeout in seconds (optional, no default timeout)

- No MCP: Use CLI tools with READMEs, or build an extension for MCP support.
- No sub-agents: Spawn Pi instances with tmux, or create your own.
- No permission popups: Run in a container, or implement confirmations.
- No plan mode: Write plans to files, or build it.
- No built-in to-dos: Use a TODO.md, or create your own.
- No background bash: Use tmux for full observability and interaction.

### 2.2. The stack

    ┌─────────────────────────────────────────┐
    │  Your Application                       │
    │  (OpenClaw, a CLI tool, a Slack bot)    │
    ├────────────────────┬────────────────────┤
    │  pi-coding-agent   │  pi-tui            │
    │  Sessions, tools,  │  Terminal UI,      │
    │  extensions        │  markdown, editor  │
    ├────────────────────┴────────────────────┤
    │  pi-agent-core                          │
    │  Agent loop, tool execution, events     │
    ├─────────────────────────────────────────┤
    │  pi-ai                                  │
    │  Streaming, models, multi-provider LLM  │
    └─────────────────────────────────────────┘

Each layer adds capability. Use as much or as little as you need.

- pi-ai - Call any LLM through one interface. Anthropic, OpenAI, Google, Bedrock, Mistral, Groq, xAI, OpenRouter, Ollama, and more. Streaming, completions, tool definitions, cost tracking.
- pi-agent-core - Wraps pi-ai into an agent loop. You define tools, the agent calls the LLM, executes tools, feeds results back, and repeats until done.
- pi-coding-agent - The full agent runtime. Built-in file tools (read, write, edit, bash), JSONL session persistence, context compaction, skills, and an extension system.
- pi-tui - Terminal UI library with differential rendering. Markdown display, multi-line editor with autocomplete, loading spinners, and flicker-free screen updates.
