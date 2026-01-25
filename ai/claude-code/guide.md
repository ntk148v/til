# Guide

Source:

- <https://x.com/affaanmustafa/article/2012378465664745795>
- <https://x.com/affaanmustafa/article/2014040193557471352>
- <https://github.com/affaan-m/everything-claude-code>

## 1. Skills and Commands

Skills operate like rules, constricted to certain scopes and workflows. They're shorthand to prompts when you need to execute a particular workflow.

Run `/refactor-clean`. Need testing? `/tdd`,`/e2e`, `/test-coverage`. Skills and commands can be chained together in a single prompt.

Commands are skills executed via slash commands. They overlap but are stored differently:

- Skills (`~/.claude/skills`) - broader workflow definitions.
- Commands (`~/.claude/commands`) - quick executable prompts.

## 2. Hooks

Hooks are trigger-based automations that fire on specific events. Unlike skills, they're constricted to tool calls and lifecycle events.

Hook Types:

- PreToolUse: Before a tool executes (validation, reminders)
- PostToolUse: After a tool finishes (formatting, feedback, loops)
- UserPromptSubmit: When you send a message.
- Stop: When Claude finishes responding.
- PreCompact: Before context compaction.
- Notification: Permission requests.

**Pro tip**: Use the `hookify` plugin to create hooks conversationally instead of writing JSON manually. Run `/hookify` and describe what you want.

## 3 Subagents

Subagents are processes your orchestrator (main Claude) can delegate tasks to with limited scopes. They can run in background or foreground, freeing up context for the main agent.

Subagents work nicely with skills - a subagent capable of executing a subset of your skills can be delegated tasks and use those skills autonomously. They can also be sandboxed with specific tool permissions.

```shell
# Example subagent structure
~/.claude/agents/
  planner.md           # Feature implementation planning
  architect.md         # System design decisions
  tdd-guide.md         # Test-driven development
  code-reviewer.md     # Quality/security review
  security-reviewer.md # Vulnerability analysis
  build-error-resolver.md
  e2e-runner.md
  refactor-cleaner.md
```

## 4. Rules and Memory

Your `.rules` folder holds `.md` files with best practices Claude should ALWAYS follow. Two approaches:

- Single CLAUDE.md - Everything in one file (user or project level)
- Rules folder - Modular `.md` files grouped by concern

## 5. MCPs (Model Context Protocol)

MCPs connect Claude to external services directly. Not a replacement for APIs - it's a prompt-driven wrapper around them, allowing more flexibility in navigating information.

> [!IMPORTANT]
> **Context Window Management**
> Be picky with MCPs. I keep all MCPs in user config but disable everything unused. Navigate to /plugins and scroll down or run /mcp.
> Your 200k context window before compacting might only be 70k with too many tools enabled. Performance degrades significantly.
> **Rule of thumb**: Have 20-30 MCPs in config, but keep under 10 enabled / under 80 tools active.

## 6. Plugins

Plugins package tools for easy installation instead of tedious manual setup. A plugin can be a skill + MCP combined, or hooks/tools bundled together.

```shell
# Add a marketplace
claude plugin marketplace add https://github.com/mixedbread-ai/mgrep

# Open Claude, run /plugins, find new marketplace, install from there
```

> [!IMPORTANT]
> **Key Takeaways**
>
> - Don't overcomplicate - treat configuration like fine-tuning, not architecture
> - Context window is precious - disable unused MCPs and plugins
> - Parallel execution - fork conversations, use git worktrees
> - Automate the repetitive - hooks for formatting, linting, reminders
> - Scope your subagents - limited tools = focused execution

## 7. Context & Memory management

For sharing memory across sessions, a skill or command that summarizes and checks in on progress then saves to a `.tmp` file in your `.claude` folder and appends to it until the end of your session is the best set.

Claude creates a file summarizing current state. Review it, ask for edits if needed, then start fresh. For the new conversation, just provide the file path. Particularly useful when you're hitting context limits and need to continue complex worktree.

**Clearing context strategically**

Once you have your plan set and context cleared (default), you can work from the plan. For strategic compacting, disable auto compact. Manually compact at logical intervals or create a skill that does so for you or suggests upon some defined criteria.

**Strategic compact skill**

Hook it to PreToolUse on Edit/Write operations.

```shell
#!/bin/bash
# Strategic Compact Suggester
# Runs on PreToolUse to suggest manual compaction at logical intervals
#
# Why manual over auto-compact:
# - Auto-compact happens at arbitrary points, often mid-task
# - Strategic compacting preserves context through logical phases
# - Compact after exploration, before execution
# - Compact after completing a milestone, before starting next

COUNTER_FILE="/tmp/claude-tool-count-$$"
THRESHOLD=${COMPACT_THRESHOLD:-50}

# Initialize or increment counter
if [ -f "$COUNTER_FILE" ]; then
  count=$(cat "$COUNTER_FILE")
  count=$((count + 1))
  echo "$count" > "$COUNTER_FILE"
else
  echo "1" > "$COUNTER_FILE"
  count=1
fi

# Suggest compact after threshold tool calls
if [ "$count" -eq "$THRESHOLD" ]; then
  echo "[StrategicCompact] $THRESHOLD tool calls reached - consider /compact if transitioning phases" >&2
fi
```

**Advanced: Dynamic system prompt injection**

Instead of solely putting everything in CLAUDE.md (user.scope) or `.claude/rules` (project scope) which loads every session, use CLI flags to inject context dynamically.

```shell
claude --system-prompt "$(cat memory.md)"
```

**Advanced: Memory persistence hooks**

```ascii
SESSION 1                              SESSION 2
─────────                              ─────────

[Start]                                [Start]
   │                                      │
   ▼                                      ▼
┌──────────────┐                    ┌──────────────┐
│ SessionStart │ ◄─── reads ─────── │ SessionStart │◄── loads previous
│    Hook      │     nothing yet    │    Hook      │    context
└──────┬───────┘                    └──────┬───────┘
       │                                   │
       ▼                                   ▼
   [Working]                           [Working]
       │                               (informed)
       ▼                                   │
┌──────────────┐                           ▼
│  PreCompact  │──► saves state       [Continue...]
│    Hook      │    before summary
└──────┬───────┘
       │
       ▼
   [Compacted]
       │
       ▼
┌──────────────┐
│  Stop Hook   │──► persists to ──────────►
│ (session-end)│    ~/.claude/sessions/
└──────────────┘
```

- PreCompact Hook: Before context compaction happens, save important state to a file
- SessionComplete Hook: On session end, persist learnings to a file
- SessionStart Hook: On new session, load previous context automatically

## 7. Continuous learning / memory

If you've had to repeat a prompt multiple times and Claude ran into the same problem or gave you a response you've heard before this is applicable to you. You can automatically do this by simply telling Claude to remember it or add it to your rules, or you can have a skill that does exactly that.

**The Problem**: Wasted tokens, wasted context, wasted time, your cortisol spikes as you frustratingly yell at claude to not do something that you already had told it not to do in a previous session.

**The Solution**: When Claude Code discovers something that isn't trivial- a debugging technique, a workaround, some project-specific pattern - it saves that knowledge as a new skill. Next time a similar problem comes up, the skill gets loaded automatically.

> WIP
