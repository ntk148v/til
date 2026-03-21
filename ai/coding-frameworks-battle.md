# The Complete Guide to AI Coding Meta-Frameworks: Oh-My-OpenCode, Get-Shit-Done, and Superpowers

Raw AI coding assistants are powerful, but they suffer from structural bottlenecks during long sessions: context window rot, forgotten requirements, and a tendency to take shortcuts. To solve this, the engineering community created "meta-frameworks" or "harnesses." These tools sit on top of base AI CLIs (like OpenCode or Claude Code) to enforce memory management, execution rules, and multi-agent coordination.

Here is the complete, detailed breakdown of the three leading paradigms in agentic development, how they work under the hood, and how to choose the right one for your repository.

---

### 1. Oh-My-OpenCode (OmO): The Multi-Agent Swarm

Oh-My-OpenCode is a heavy, highly customizable orchestration toolkit designed to turn a single AI instance into an entire engineering department. It relies on asynchronous, parallel sub-agents to handle complex scoping.

**Core Architecture & Mechanisms**

- **The Sisyphus Protocol:** The primary coding agent is named "Sisyphus." It includes a "Todo Continuation Enforcer" that prevents the AI from stopping halfway through a massive refactor. If it tries to quit before the checklist is complete, the framework forces it back to work.
- **Async Background Agents:** While Sisyphus writes the core logic, OmO spins up parallel sub-agents. The _Librarian_ agent reads official documentation or GitHub repositories, the _Explorer_ agent runs fast contextual grep searches to map the codebase, and the _Oracle_ agent steps in for complex debugging.
- **Native LSP & AST-Grep:** It uses built-in Language Server Protocol (LSP) tools and Abstract Syntax Tree (AST) grep for surgical, deterministic refactoring, rather than relying on simple text replacement.

**Pros:**

- Handles massive codebase scaffolding and complex open-source framework integration effortlessly.
- Keeps the main agent's context lean by delegating exploration to background agents.
- Extremely customizable terminal UI with zero screen flicker and Tmux integration.

**Cons:**

- Massive token consumption. Running 3 to 4 models in parallel drains API budgets quickly.
- High complexity to configure and master.

**Best For:** Developers starting greenfield projects who want maximum automation, parallel processing, and have the API budget to support it.

---

### 2. Get-Shit-Done (GSD): The Spec-Driven Orchestrator

Get-Shit-Done (specifically the GSD-2 architecture) is an aggressive context-engineering framework. Its sole purpose is to eradicate "Context Rot"—the degradation of AI intelligence that happens when a context window fills with chat history and irrelevant files.

**Core Architecture & Mechanisms**

- **Thin Orchestrator, Fat Executors:** GSD uses a main orchestration agent that consumes only 10% to 15% of the context window. It plans, coordinates, and verifies, but it never writes code. When work is required, it spawns a fresh sub-agent with a completely empty 200k context window dedicated entirely to one specific task.
- **Files as Long-Term Memory:** It relies heavily on Markdown files (`ROADMAP.md`, specific phase specs) as persistent memory. When a sub-agent spawns, it only reads the spec files relevant to its immediate task.
- **Goal-Backward Verification:** GSD will not commit code simply because it generated it. It runs a planner-to-checker loop, actively verifying that the required artifacts exist, are wired correctly, and pass tests before declaring a milestone complete.

**Pros:**

- Zero context rot. Task 50 gets the exact same model intelligence and attention to detail as Task 1.
- Produces highly reliable, atomic Git commits.
- Forces you to think systematically through its "discuss-phase" before execution begins.

**Cons:**

- Can feel slow. You must write and review specification files before any actual code is generated.
- Generates a lot of metadata files that you must manage via `.gitignore`.

**Best For:** Long-running projects, complex feature additions in mature codebases, and developers who prioritize system stability over rapid prototyping.

---

### 3. Superpowers: The Rigor & Discipline Enforcer

Superpowers is a lightweight skills library. Instead of parallel swarms or heavy markdown files, Superpowers focuses on psychological constraints. It treats the base model like a junior engineer that needs strict supervision to prevent it from taking shortcuts.

**Core Architecture & Mechanisms**

- **Skill-Based Injections:** It operates via a directory of "Skills" (Markdown workflows with deterministic flowcharts). When you issue a prompt, Superpowers scans its library and injects the exact rules required for that specific task.
- **Iron Law of TDD:** Superpowers enforces strict Test-Driven Development. It demands a Red-Green-Refactor loop. If the agent attempts to write implementation logic before writing a failing test, Superpowers will automatically delete the code and force a restart.
- **Socratic Brainstorming:** Before acting, it triggers a Socratic design phase. It forces the AI to interrogate your prompt, identify edge cases, and propose a design document. It will not execute until you approve the design.

**Pros:**

- Highly token-efficient. It does not run background swarms or heavy context loops; it only triggers specific skills when needed.
- Produces incredibly high-quality, tested, and reliable code.
- Stays out of your way until you explicitly need it.

**Cons:**

- Requires heavy human involvement. You are constantly reviewing test outputs and approving Socratic design questions.
- Lacks the autonomous, unattended background processing capabilities of OmO or GSD.

**Best For:** Day-to-day debugging, routine bug fixes, and hands-on developers who want a clean, test-first safety net without altering their entire workflow.

---

### Summary Matrix

| Metric                 | Oh-My-OpenCode                | Get-Shit-Done             | Superpowers                  |
| :--------------------- | :---------------------------- | :------------------------ | :--------------------------- |
| **Primary Philosophy** | Parallel Sub-Agent Delegation | Context Isolation & Specs | TDD & Execution Rigor        |
| **Context Strategy**   | Delegates to background tools | Aggressive memory wipes   | Socratic alignment prompts   |
| **Token Cost**         | Very High                     | Medium                    | Low                          |
| **Human Involvement**  | Low (Fire and forget)         | Medium (Reviewing specs)  | High (Reviewing tests)       |
| **Execution State**    | Asynchronous / Parallel       | Sequential Waves          | Sequential / Skill-triggered |

**The Final Verdict**
If you want to build an application while you sleep, install **Oh-My-OpenCode**. If you are managing a complex architecture over several weeks and cannot afford AI hallucinations, implement **Get-Shit-Done**. If you just want your AI to stop writing sloppy code and write tests first, use **Superpowers**.
