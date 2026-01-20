# Agent Skills

Source:

- <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>
- <https://agentskills.io/integrate-skills>

## 1. Overview

- A simple, open format for giving agents new capabilities and expertise.
- Agent Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently.
- What can Agent skills enable?
  - Domain expertise: Package specialized knowledge into reusable instructions, from legal review processes to data analysis pipelines.
  - New capabilities: Give agents new capabilities (e.g. creating presentations, building MCP servers, analyzing datasets).
  - Repeatable workflows: Turn multi-step tasks into consistent and auditable workflows.
  - Interoperability: Reuse the same skill across different skills-compatible agent products.

## What are skills?

A skill is a folder containing a `SKILL.md` file.

```shell
my-skill/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

Skills use **progressive disclosure** to manage context efficiently:

- Discovery: At startup, agents load only the name and description of each available skill, just enough to know when it might be relevant.
- Activation: When a task matches a skill’s description, the agent reads the full SKILL.md instructions into context.
- Execution: The agent follows the instructions, optionally loading referenced files or executing bundled code as needed.

The SKILL.md file

```markdown
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
---

# PDF Processing

## When to use this skill

Use this skill when the user needs to work with PDF files...

## How to extract text

1. Use pdfplumber for text extraction...

## How to fill forms

...
```
