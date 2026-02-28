# Stop Vibe Coding. Start Spec Engineering

> *AI can write code faster than any human. So why do teams keep getting burned?*

---

The productivity gains are real. AI coding tools genuinely accelerate output — boilerplate disappears, scaffolding takes minutes, not hours. We're not here to argue against that.

We're here to talk about what comes after the demo.

## "Plausible" ≠ "Correct"

AI coding tools are optimized for one thing: generating plausible code from a natural language description. Extraordinary capability. But "plausible" and "correct" are not the same thing — and "fast" and "consistent" are not synonyms.

The enterprise software industry is beginning to discover this the hard way.

## Vibe Coding vs. Engineering

**Vibe Coding**: prompt the AI with a rough idea, accept whatever comes out, fix what breaks, ship it. For a weekend project? Delightful. For software that processes payroll, handles medical records, or manages financial transactions? A liability dressed as a productivity tool.

The problem isn't speed. It's what gets silently decided at speed.

## Agent Drift

Ask any LLM to build a user authentication service. Close the chat. Open a new session. Ask again.

You get a different architecture.

First response: JWT with Redis. Second: opaque tokens in Postgres. Both valid in isolation. Both reflecting completely different architectural decisions that cascade through your entire system.

This is **Agent Drift** — the phenomenon where repeated generation from the same intent produces structurally divergent implementations. It's not a bug. It's the fundamental nature of probabilistic text generation. The model isn't trying to be consistent. It's generating a plausible next token.

At scale, Agent Drift compounds. Different modules, different assumptions. Different error strategies. The codebase becomes a patchwork of micro-architectures — each sensible alone, incoherent together.

## The Debt Accelerator

As the 2025 DORA report notes, AI acts as an **amplifier** — a mirror reflecting back the good, bad, and ugly of your entire pipeline. Speed was never the bottleneck. Design quality was.

When a senior engineer writes code manually, every decision is deliberate. When an AI generates code, decisions are implicit — buried in statistical patterns from millions of repositories of varying quality. The faster you generate, the faster implicit-decision debt accumulates. You ship faster. You break faster. You refactor more.

The velocity gain evaporates in maintenance.

## No Single Source of Truth

This is the deeper problem the "AI makes you faster" narrative ignores:

**In a vibe-coded workflow, there is no single source of truth for design decisions.**

Why does the auth service use JWT and not opaque tokens? Check the chat history? The PR description? The comments — if any were generated? These are ephemeral, unsearchable, non-authoritative. The next developer (or agent) who touches that code has no reliable way to know what constraints the original decision was made under.

AI makes this dramatically worse. The volume of implicit decisions explodes alongside the volume of generated code.

## The Fix: Discipline Before Velocity

The teams succeeding at AI-assisted engineering at scale share one trait: they establish **discipline** before deploying **velocity**.

They answer the architectural questions in writing before a prompt is written. They treat AI as a highly capable *implementer* — given a precise brief, it produces consistent, high-quality results. Given an ambiguous one, it produces inconsistent, surprising results. Just like any implementer.

**Before you prompt an AI to write meaningful code, answer three questions in writing:**

1. **What design decisions are locked?** (auth strategy, error handling, transaction model)
2. **What types and constraints must hold?** (validation rules, edge cases, invariants)
3. **What is explicitly out of scope?** (what the AI must not do, even if it seems plausible)

Without answers in a stable, machine-readable form — you're vibe coding, and accumulating invisible debt with every generation.

---

*Code is cheap. Design decisions are gold.*

---

**Part 1 of 6** · **Next**: [Part 2 — Spec-Driven Development](./part-2-spec-driven-development.md)
