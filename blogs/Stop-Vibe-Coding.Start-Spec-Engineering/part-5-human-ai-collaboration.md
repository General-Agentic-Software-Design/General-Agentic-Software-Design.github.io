# Human + AI — The New Collaboration Model

> *The AI writes the code. The human writes the architecture. Neither does it alone.*

---

Every conversation about AI-assisted development arrives at the same question: *what happens to software engineers?*

Wrong question. AI and engineers are not competing for the same job.

The right question: **in a world where AI can generate code from a design, what is the most valuable thing a software engineer can do?**

The answer is what engineers were always supposed to be doing: making good architectural decisions.

## The Role Shift

The most experienced engineers — the ones with the deepest understanding of trade-offs, failure modes, and long-term consequences — spend a disproportionate amount of time writing routine implementation code. Not because it requires their expertise, but because there's no other way to get it done.

AI changes this equation.

If a well-specified design generates production-quality implementation code, then the scarce resource is no longer code — it's *design*. The bottleneck moves upstream, from "can we write the code?" to "can we make the right architectural decisions?"

That's not deskilling engineering. It's a **promotion** of the most valuable engineering work.

## The Collaboration Lifecycle

```
Product Team          Architect (Human)          AI Agent
─────────────         ──────────────────          ──────────────
Write User Stories →  Author/Review GASD     →  Generate Code
                      Make design decisions       Generate Tests
                      Resolve QUESTION blocks     Generate Docs
                      APPROVE the spec            Attach EVIDENCE
                                                  Open PR
                      Review Evidence         ←  Submit for merge
                      Merge or request changes
```

### Stage 1 — Product Defines What

User stories, acceptance criteria, business rules. GASD sits downstream of this, not as a replacement for it.

### Stage 2 — Architect Defines How

The architect authors the GASD spec — or a GASD-aware AI drafts it and the architect reviews. Either way, the architect is **the authority on every design decision**:

- Which authentication strategy
- Which error handling approach
- What the type contracts look like
- What invariants must hold globally

This is where senior engineering expertise is most valuable. Not writing the tenth CRUD endpoint — deciding what constraints every CRUD endpoint must satisfy.

### Stage 3 — AI Generates

Once the spec is approved, the agent implements. The spec eliminates the agent's degrees of freedom on every design dimension addressed. It's not free-styling — it's implementing a blueprint.

Same GASD spec → same implementation. Every time.

### Stage 4 — Blocking Ambiguity Surfaces

No spec is perfect. When the agent hits a gap, it raises a `QUESTION` block instead of guessing:

```gasd
QUESTION: "Should a successful login reset the failed_attempts counter?"
    BLOCKING: true
    CONTEXT: AuthService.login
    RAISED_BY: "agent-codex-v3"
```

`BLOCKING: true` — the agent stops. Human decides. Spec updated. Agent resumes. Decision permanently recorded.

The AI's question and the human's answer are both in the spec. Next quarter, "why does login reset the counter?" has an answer — in the file, not in anyone's memory.

### Stage 5 — Formal Approval

Significant decisions are formally approved:

```gasd
APPROVE "Token Format":
    STATUS: APPROVED
    BY: "Lead Architect"
    DATE: "2026-02-22"
    NOTES: "Stateless JWT is appropriate for MVP; revisit if we need server-side invalidation"
```

Not bureaucracy — an audit trail. When the token format changes in 18 months, the next architect can see who decided, when, why, and what was anticipated.

### Stage 6 — Evidence Embedded

When the agent finishes, it attaches an `EVIDENCE` block:

```gasd
EVIDENCE AuthService.login:
    TEST_COVERAGE: "94%"
    TESTS_PASSED: "12/12"
    VALIDATION_DATE: "2026-02-22T18:00:00Z"
    AGENT_ID: "agent-codex-v3"
    LINKED_TESTS: ["UT-AUTH-001", "UT-AUTH-002", "UT-AUTH-003"]
    NOTES: "Anti-enumeration constraint validated in UT-AUTH-002"
```

Proof embedded in the spec. A CI/CD pipeline can parse `EVIDENCE` blocks to enforce merge gates automatically.

### Stage 7 — Review and Merge

The human reviews the evidence and generated code. Because design decisions were already reviewed at Stage 2, the code review is a **sanity check** — not a design session. This makes reviews dramatically faster.

## GASD as Institutional Memory

One of the most corrosive problems in software teams: architectural decisions made by engineers who've since left become invisible. "Why did we do it this way?" becomes unanswerable.

GASD makes institutional memory explicit. Every decision is:

- **Recorded** — in a version-controlled file
- **Dated** — `APPROVE` captures when
- **Attributed** — who made the call
- **Rationale-bearing** — the `RATIONALE` field captures why

When a new AI agent is onboarded to maintain a GASD-specced codebase, it reads the spec. The knowledge is in the file, not in anyone's head.

## The Two Fears — Answered

**"Will GASD replace senior developers?"**

No. GASD replaces *routine implementation work* that senior developers shouldn't be doing anyway. It raises the value of what they do best: trade-off analysis and architectural constraint-setting.

**"Will junior developers still learn?"**

Yes — arguably more. When architectural decisions are explicit and reasoned in the spec, junior developers can read them, challenge them, propose alternatives. `DECISION` blocks are positions with rationale, not authority by fiat. That's how junior engineers become architects.

## The New Measure of Senior Engineering

In a GASD-driven team, a senior engineer's output is measured not in lines of code but in quality of design decisions:

- How well does the GASD spec eliminate ambiguity?
- How thoroughly do `DECISION` blocks capture architectural trade-offs?
- How precisely do `TYPE` contracts prevent misuse?
- How clearly do `FLOW` steps guide the agent to the correct implementation?

These are the skills that separate great engineers from good ones. GASD just makes them the primary deliverable — exactly where they belong.

---

*GASD turns one-time AI conversations into permanent architectural contracts. It makes senior engineers the design authorities they always should have been.*

---

**Part 5 of 6** · **Previous**: [Part 4 — From User Story to Working Code](./part-4-user-story-to-code-walkthrough.md) · **Next**: [Part 6 — GASD 2.0](./part-6-gasd-2-teaser.md)
