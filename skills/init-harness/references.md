# Authoritative References

The following resources inform what goes into each generated file:

## Foundations
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — initializer agents, init.sh, self-verification, handoff artifacts
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — task state, evaluator design
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — architectural constraints, repo-local instructions, telemetry
- [Harness Engineering — Thoughtworks](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) — context engineering, architectural constraints, entropy management
- [Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) — weak results are often harness problems, not model problems

## Context & Memory
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — context window as working memory budget
- [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) — durable, repo-local instructions

## Constraints & Guardrails
- [Beyond permission prompts](https://www.anthropic.com/engineering/claude-code-sandboxing) — sandboxing, policy design
- [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — safe, inspectable tool boundaries
- [12 Factor Agents](https://www.humanlayer.dev/blog/12-factor-agents) — explicit prompts, state ownership, pause-resume behavior
- [Mitigating Prompt Injection Attacks](https://openhands.dev/blog/mitigating-prompt-injection-attacks-in-software-agents) — confirmation mode, analyzers, hard policies

## Specs & Workflow
- [AGENTS.md format](https://github.com/agentsmd/agents.md) — portable cross-runtime instruction format
- [GitHub Spec Kit](https://github.com/github/spec-kit) — spec-driven development toolkit
- [12-Factor AgentOps](https://www.12factoragentops.com/) — context discipline, validation, reproducible workflows

## Evals & Observability
- [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — what to measure in agent systems
- [OpenTelemetry Semantic Conventions for GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — portable observability conventions
- [Testing Agent Skills Systematically](https://developers.openai.com/blog/eval-skills/) — JSONL logs, deterministic checks

**Full curated list:** https://github.com/walkinglabs/awesome-harness-engineering
