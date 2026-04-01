# Agent responsibly

Source: <https://vercel.com/blog/agent-responsibly>

- False confidence:
  - Agent-generated code is dangerously convincing, but an agent doesn't understand your production environment.
  - The gap between "this PR looks correct" and "this PR is safe to ship" has always existed.
- Leveraging vs. relying:
  - Relying means assuming that if the agent wrote it and the tests pass, it's ready to ship. The author never builds a mental model of the change.
  - Leveraging means using agents to iterate quickly while maintaining complete ownership of the output.
- Guarding production:
  - Sefl-driving deployments: Every change rolls out incrementally through gated pipelines. If a canary deployment degrades, the rollout stops and rolls back automatically.
  - Continuous validation: This infrastructure tests itself continuously, not just a deploy.
  - Executable guardrails: encode operational knowledge as runnable tools instead of documentation.
- Guardrails:
  - Stronger guardrails around shared infra, with runtime validation at every stage of the deployment pipeline
  - Stricter static checks at PR time, especially around feature flags
  - Production-mirroring end-to-end testing in staging
  - Read-only agents that continuously verify system invariants in production, using specialized agents to audit the assumptions made by generative agents
  - Metrics like defect-commit vs. defect-escape ratios to surface when risk is increasing across the platform
- Leverage agents, don't rely on them. Before you open your next PR, ask yourself:
  - What does this do? How does it behave once rolled out?
  - How can this adversely impact production or customers?
  - Am I comfortable owning an incident tied to this code?


