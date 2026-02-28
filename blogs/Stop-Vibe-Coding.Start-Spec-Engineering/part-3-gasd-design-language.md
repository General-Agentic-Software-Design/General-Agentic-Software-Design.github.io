# GASD — The Design Language That Keeps AI Agents Honest

> *What if your architecture document was also your agent's instruction set?*

---

Parts 1 and 2 of this 6-part series established the problem and the philosophy. Now the practical question:

*What does a spec that drives AI code generation actually look like?*

Natural language is too ambiguous. Markdown docs aren't machine-readable. UML is too heavyweight. OpenAPI only covers API surfaces. Something purpose-built is needed.

That's **GASD** — the General Agentic Software Design Language.

## What GASD Is

GASD is a **Design Bridge Language**: built for humans and AI agents to collaborate on software architecture. It is for capturing architectural decisions, type contracts, component interfaces, and behavioral flows — with enough precision that an AI agent generates consistent, deterministic code every time it reads the spec.

Not a programming language — you can't run GASD.
Not a requirements format — you don't write user stories in GASD.
Not documentation — it doesn't describe what already exists.

GASD captures *how to architect a system*, at the precision needed to eliminate agent interpretation variance.

## The Three-Layer Model

```
User Stories         →    GASD Spec           →    Code
─────────────────         ──────────────            ──────────────
"As a user, I want        "AuthService uses         def login(...):
 to log in..."             JWT, bcrypt cost=12,         token = jwt.encode(...)
                           ENSURE attempts < 5"         if attempts >= 5:
                                                            raise ForbiddenException
```

- **Layer 1**: *What* — user stories, product requirements. GASD doesn't replace this.
- **Layer 2**: *How* — architecture decisions. This is where drift happens, and where GASD operates.
- **Layer 3**: *Runnable* — code, generated from the GASD spec by AI agents.

GASD is the missing middle. It turns product intent into engineering precision.

## What GASD Captures

### `DECISION` — Lock Architectural Choices

The most powerful construct. Once written, an architectural choice never varies between generations.

```gasd
DECISION "Password Storage":
    CHOSEN: "bcrypt (cost=12)"
    RATIONALE: "Industry standard, constant-time comparison, widely supported"
    ALTERNATIVES: ["argon2", "PBKDF2"]
    AFFECTS: [AuthService.register, AuthService.login]
```

Without this: AI picks bcrypt today, argon2 tomorrow. With this: always bcrypt, cost 12, rationale on record.

### `TYPE` — Contracts, Not Prose

Data structures with explicit validation constraints — structured annotations that compile directly to validation code.

```gasd
TYPE LoginRequest:
    email:    String @format("email") @max_length(255)
    password: String @min_length(8) @sensitive
```

`@sensitive` — this field must never appear in logs.
`@format("email")` — generate email validation.
Not suggestions. Contracts.

### `COMPONENT` — Architecture Topology

What depends on what. What each component exposes. Enough for the AI to generate properly layered, dependency-injected code.

```gasd
COMPONENT AuthService:
    PATTERN: "Service"
    DEPENDENCIES: [UserRepository, TokenService]
    INTERFACE:
        login(req: LoginRequest) -> SessionToken
        register(req: RegistrationRequest) -> UUID
```

### `FLOW` — Constrained Behavioral Design

Step-by-step operation design with exact guard clauses, error types, and execution modifiers. This is where AI freedom is most tightly constrained.

```gasd
FLOW login(req: LoginRequest) -> SessionToken:
    @error_strategy("Exception-based")
    1. VALIDATE req
    2. ACHIEVE "Fetch user by email" via UserRepository
        ON_ERROR: THROW UnauthorizedException("Invalid credentials")
    3. ENSURE password_matches(req.password, user.password_hash)
        OTHERWISE THROW UnauthorizedException("Invalid credentials")
    4. ENSURE user.failed_attempts < 5
        OTHERWISE THROW ForbiddenException("Account locked")
    5. CREATE SessionToken from user
    6. RETURN SessionToken
```

### `CONSTRAINT` / `INVARIANT` — Global Rules

```gasd
CONSTRAINT: "All public methods must have input validation"
CONSTRAINT: "Use Dependency Injection for all external services"
INVARIANT: "A user's failed_attempts counter must never exceed 5 before locking"
```

These are not comments. A GASD-compliant transpiler validates them before generating code.

## What GASD Intentionally Does NOT Capture

- **Business logic** — discount percentages, business rules. Those live in user stories and config.
- **Implementation code** — `ACHIEVE` deliberately leaves implementation to the agent.
- **Infrastructure** — Kubernetes, Terraform, migrations. Downstream of design.

Knowing what *not* to put in GASD is as important as knowing what to put in it.

## Contract, Not Document

A document describes. A contract obligates.

When you merge a GASD spec change, you change the contract your entire engineering pipeline operates under — code must be regenerated, tests must be regenerated, and any deviation is a violation to fix, not a style preference to tolerate.

That's what makes GASD the single source of truth. Not authoritative by convention (like a wiki), but authoritative by enforcement (like a type system).

## Before and After

| Without GASD | With GASD |
|---|---|
| Ad-hoc natural language prompts | Structured `FLOW` and `DECISION` blocks |
| Architecture decisions in Confluence | `DECISION` blocks in version control |
| Inconsistent error handling across modules | `@error_strategy` + `CONSTRAINT` |
| Scattered type validation | `TYPE` with `@format`, `@range`, `@min_length` |
| "I think we decided on bcrypt?" | `DECISION "Password Storage": CHOSEN: "bcrypt"` |

## Start Small

You don't need to spec an entire system at once. Start with one module:

- One `DECISION` block for the architectural choice you keep re-making
- One `TYPE` for the data structure that keeps being validated inconsistently  
- One `FLOW` for the operation every new developer asks about

Run it through a GASD-aware agent. Compare the output to your existing code. Expand from there.

---

*GASD is the missing layer between your product requirements and your AI's output. It's how you keep agents accountable.*

---

**Part 3 of 6** · **Previous**: [Part 2 — Spec-Driven Development](./part-2-spec-driven-development.md) · **Next**: [Part 4 — From User Story to Working Code ⭐](./part-4-user-story-to-code-walkthrough.md)
