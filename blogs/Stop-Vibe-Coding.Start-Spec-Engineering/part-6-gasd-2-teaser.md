# What's Next — A Glimpse at GASD 2.0

> *One agent, one spec: solved. Ten agents, one codebase: welcome to the next problem.*

---

GASD 1.0 answers a specific question: *how do you ensure a single AI agent generates consistent, deterministic code from a design spec?*

The answer — a structured Design Bridge Language with locked decisions, typed contracts, annotated flows, and global invariants — works. Using GASD 1.0 today ensures fewer re-generation surprises, more consistent codebases, and a cleaner product-to-engineering handoff.

But a harder question is emerging.

## The Next Problem: Multi-Agent Coordination

The future of software development isn't one developer with one AI assistant. It's teams of engineers working alongside *fleets of AI agents*, building in parallel across shared codebases.

Five agents implementing five microservices simultaneously, all reading the same GASD specs. Each follows the spec faithfully. Integration fails.

Why?

Agent A chose UUID v4 for entity IDs. Agent B chose UUID v7. Both valid. Neither explicitly specified. The services can't interoperate.

Agent C generated async code for a notification service. Agent D assumed synchronous. The integration error is subtle and hard to trace.

This is the **Coordination Tax** — incompatibilities that emerge when multiple agents, each individually correct, produce outputs that don't work together.

GASD 1.0 doesn't solve this. GASD 2.0 is being designed to.

## The Bigger Vision

In a traditional team, a spec is a document humans write and humans read. It informs development but doesn't drive it.

In an agentic team, the spec is the *coordination protocol* — the shared contract that keeps humans and agents aligned, keeps agents aligned with each other, and keeps today's implementation aligned with tomorrow's maintenance.

GASD is working toward becoming that protocol: not just a Design Bridge for one developer and one agent, but the **lingua franca of collaborative, human-supervised, multi-agent software engineering**.

## Start Spec Engineering Today

GASD 1.0 is available now. It transforms user stories into structured designs that ensure your AI agents generate production-ready code with minimal drift.

### The 3-Step Workflow

1. **Draft**: Provide your User Stories or SRS to an agent to generate an initial GASD design.
2. **Review & Refine**: Humans review the GASD file for architectural correctness, security, and specific constraints.
3. **Generate**: Provide the finalized GASD to the agent with a `TARGET` (e.g., Python, Rust) to get consistent code.

---

### Resources

- 📖 [Read the GASD 1.0 Specification](https://github.com/General-Agentic-Software-Design/General-Agentic-Software-Design-Language/blob/main/GASD_Specification.md)
- ⭐ [Try the full walkthrough](./part-4-user-story-to-code-walkthrough.md)
- 🌟 [Join the Discussion on GitHub](https://github.com/General-Agentic-Software-Design/General-Agentic-Software-Design-Language/discussions)
- [A Full Example: Graphical Calculator](https://github.com/General-Agentic-Software-Design/Example_Graphical-Calculator)

**Part 6 of 6** · **Next**: Starting your first project? [Back to Part 1](./part-1-vibe-coding-vs-rigorous-engineering.md)
