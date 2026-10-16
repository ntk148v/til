# Context Course

Source: <https://huggingface.co/learn/context-course>

## 1. Agent skills

> Without the right context, even a capable agent is working blind. It fills gaps with guesses, asks questions it shouldn’t need to ask, and wastes time on work that has to be redone. They can start failing on ordinary tasks instead of just hard tasks. Instead of needing a better model, the agent needs better context.

- A skill is a self-contained package of knowledge that makes an agent good at one specific task. Skills are portable across projects and agents, reusable once installed, structured in a format agents can parse, and extensible through links to scripts and APIs.
- A skill is essentially an onboarding document for an agent: the same kind of step-by-step guide you’d give a new colleague, but written so the agent can load it on demand.
- There’s a formal standard for how skills are structured, called the Agent Skills Specification, maintained at [agentskills.io](https://agentskills.io/).
- Directory structure:

```sh
skill-name/
├── SKILL.md              # Required: metadata + instructions
├── scripts/              # Optional: executable code
│   ├── validate.py
│   ├── deploy.sh
│   └── README.md
├── references/           # Optional: documentation links
│   ├── api-reference.md
│   └── examples.md
└── assets/               # Optional: templates, data
    ├── template.yaml
    └── config-example.json
```

- Rules:
  - Directory name must be lowercase with hyphens (skill-name, not SkillName)
  - Consecutive hyphens are NOT allowed (my—skill is invalid)
  - SKILL.md is required and must be in the root
  - Optional directories: scripts/, references/, assets/
  - All relative file paths are resolved from the skill root
- Every SKILL.md starts with YAML frontmatter that describes the skill. Here’s the complete specification:

```md
---
name: 'dataset-publishing'
description: 'Publish datasets to Hugging Face Hub. Use when uploading datasets, creating dataset cards, or managing dataset versions.'
license: 'Apache-2.0'
compatibility: 'Tested with Python 3.8+ and huggingface_hub 0.16+'
metadata:
  author: 'ml-team'
  version: '1.0.0'
allowed-tools: 'Bash(hf:*) Python(huggingface_hub:*)'
---
```

- The fastest way to debug a new skill is to test activation pressure directly:
  - Ask for the skill with an obvious prompt that should match its description.
  - Ask again with a vaguer prompt that a real user might write.
  - If only the first prompt works, tighten the `description` until both prompts reliably activate the skill.

## 2. Model Context Protocol (MCP)

- Model Context Protocol (MCP) is an open standard for letting AI applications interact with external data and tools. It sits between your agent and everything else: files, databases, APIs, services.
- Skills are great for fixed knowledge, but they can’t fetch new information or take live actions. MCP fills that gap by giving an agent **dynamic context**: it can call functions, read files, query databases, and interact with APIs through a single protocol.
  - Skills are perfect for teaching an AI how to do something (write prompts, analyze emails, code style guidelines).
  - MCP is perfect for giving an AI the ability to do something (read files, call APIs, query databases).
- Every MCP interaction involves three distinct roles:
  - **Host**: The host is the environment where a code agent runs
  - **Client**: The client is the protocol handler inside the host that communicates with MCP servers.
  - **Server**: The server is an external program that exposes capabilities through MCP
- MCP servers expose three kinds of capabilities to clients:
  - **Tools** are callable functions that agents invoke to perform actions or retrieve data.
  - **Resources** are read-only data sources that agents can access for information.
  - **Prompts** are instruction templates that agents can request to help guide their own behavior for specific contexts or domains.

## 3. Plugins

- Plugins are reusable extensions for code agents. They are pre-built context packs: curated, tested, and shareable bundles of knowledge and tools that save setup time and keep teams consistent.

## 4. Subagents

- Subagents are isolated agent instances spawned by a parent agent to handle subtasks, often in parallel. Each has its own context window, execution limits, and tool access, and reports back to the parent.
- Subagents enable parallel execution across multiple tasks simultaneously, give each task it own context window to prevent oeverflow, allow specialized tool access per agent, isolate failures so one crash doesn't take down the whole workflow, scale without slowing the parent, and decompose complexity naturally into manageable pieces.
- Avoid subagents for sequential dependent work where task B needs output from task A, same-file parallel edits that risk git conflicts, small quick tasks where spawn overhead exceeds the task itself, and workflows requiring more than five specialist agents where coordination becomes chaotic.
