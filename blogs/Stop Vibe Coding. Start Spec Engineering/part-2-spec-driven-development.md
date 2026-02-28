# Spec-Driven Development — The Idea AI Just Made Urgent

> *Specs aren't new. What's new is that AI agents need them to work reliably.*

---

Specs predate the term "software engineer." From punched-card specifications in the 1940s to 10,000-page defense contract requirements in the 1980s, specifying what a system must do before building it is as old as the discipline itself.

So why is Spec-Driven Development suddenly the most discussed topic in AI-assisted engineering?

Because the audience has changed.

## The Spec Graveyard — A Brief History

**Formal Methods (1970s–90s)**: Z notation, VDM, TLA+. Mathematically rigorous, provably correct, and almost entirely unused in commercial software. Written for humans to verify, not machines to execute.

**UML (1990s–2000s)**: Visual design language, widely adopted, widely abandoned. Maintaining UML diagrams alongside living code cost more than the value they delivered.

**OpenAPI (2010s)**: Finally — spec-driven development that *stuck*. Specify your API before implementing it; generate client SDKs, server stubs, validation middleware, and docs from a single source. It worked because the spec drove tooling, not just humans.

**The AI Era (now)**: OpenAPI proved that a machine-readable spec can generate real artifacts — not just documentation, but executable code. LLMs have made this possible at the *entire application design level*. The question is no longer "can we generate code from a spec?" The question is: "what kind of spec do you need for consistent, high-quality results?"

## The Spec-First Shift

The core idea: **the specification is the authoritative source of truth, above the code**.

In traditional workflows, specs drift immediately. Code diverges as requirements change and pragmatic decisions accumulate. Within months, the spec is archaeology.

Spec-First flips this. The spec is not documentation written *after* decisions — it's the *medium in which decisions are made*. Code is derived from the spec, not the other way around.

For AI-assisted development this is critical:

- **AI has no memory across sessions.** Every new prompt starts from zero. A persistent spec gives agents the context to make consistent decisions — session after session, agent after agent.
- **Code reviews become design reviews.** A spec change required for a code change makes the design decision explicit, traceable, and reviewable — not buried in a diff.
- **Onboarding is instant.** A new engineer (or new agent) reads the spec and understands the architecture in minutes, not weeks.

## The Industry Is Converging Here

This isn't academic. Three significant bets are being placed on spec-first AI development right now.

**Amazon Kiro** — an agentic IDE (VS Code fork, Claude Sonnet 4.0) that builds SDD into the development loop itself. Requirements → structured user stories → technical design docs → task breakdown → implementation, triggered step by step. "Steering Files" lock in project conventions for every agent session. "Hooks" keep specs, docs, and tests synchronized as code evolves.

**Tessl** — founded by Guy Podjarny (Snyk). Not an IDE — a Spec Registry, like npm but for AI agent knowledge. Over 10,000 pre-built usage specs for popular libraries stop agents from hallucinating APIs or version-mixing. Teams publish internal specs to distribute architectural knowledge across their entire agent fleet. Tessl's vision: eventually, comprehensive specs + tests make *code itself largely disposable* — just regenerate it.

**Spec-kit frameworks** — open-source DSLs for capturing design intent in machine-readable formats, layerable on existing workflows without switching IDEs or platforms.

Three different approaches. One shared conclusion: **the spec is the source of truth. The code is the output.**

## "Isn't This Just Documentation?" — Answered

The objection is fair. Documentation rots. We've all been burned by it.

But **executable documentation doesn't rot the same way**. When a spec drives code generation — when changing the spec regenerates different code — spec and implementation are coupled. They can't diverge silently. A team that modifies code without updating the spec creates a visible, explicit gap. The spec remains the authority.

This is exactly how OpenAPI works. You don't change API behavior and update the spec as an afterthought. The spec *is* the API.

## The Design Bridge

```
User Stories  →  Design Bridge (Spec)  →  Code
   "What"              "How"               "Runnable"
```

The Design Bridge sits between product requirements and implementation. It captures the architectural *how* — at a precision that eliminates interpretation variance when handed to an AI agent.

It doesn't replace user stories. It doesn't replace code. It's the missing middle layer that turns a rough product requirement into a deterministic engineering blueprint.

## SDD Isn't New. The Urgency Is

Three things have changed:

1. **AI agents need machine-readable design context** to produce consistent results — and they now exist at production scale
2. **Generation speed has outpaced review speed** — the cost of specless AI coding is higher than ever
3. **Multi-agent workflows are emerging** — requiring shared, authoritative design contracts that all agents can read

SDD has been theoretically sound for decades. AI just made ignoring it expensive.

In the next part, we introduce **GASD** — the General Agentic Software Design Language — a Design Bridge purpose-built for AI-assisted development.

---

*The spec is the prompt that never drifts.*

---

**Part 2 of 6** · **Previous**: [Part 1 — Stop Vibe Coding](./part-1-vibe-coding-vs-rigorous-engineering.md) · **Next**: [Part 3 — GASD: A Design Language for the Agentic Era](./part-3-gasd-design-language.md)
