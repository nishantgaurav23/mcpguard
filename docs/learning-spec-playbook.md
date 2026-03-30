# Learning-Spec Playbook

A step-by-step guide for balancing learning and shipping across MCPGuard specs. Explains WHAT to do, WHEN, and WHY each pattern works for skill building.

---

## Table of Contents

1. [The Core Problem](#the-core-problem)
2. [The Decision Framework](#the-decision-framework)
3. [The Three Modes](#the-three-modes)
4. [Step-by-Step Workflows](#step-by-step-workflows)
5. [Applied to MCPGuard Roadmap](#applied-to-mcpguard-roadmap)
6. [Why This Pattern Works](#why-this-pattern-works)
7. [Progression Tracking](#progression-tracking)
8. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## The Core Problem

AI-assisted development creates a dangerous illusion: you feel productive because code ships fast, but you may not understand what was built. Six months later, you can't debug, extend, or explain your own codebase.

The solution is not to stop using AI. It is to use AI deliberately -- as a tutor when learning, and as a tool when shipping. The key is knowing which mode you're in for each task.

---

## The Decision Framework

Ask these questions in order for every spec:

```
Step 1: Is this spec already implemented?
  YES -> Paperwork Mode (create-spec + verify-spec)
  NO  -> Continue to Step 2

Step 2: Is the DOMAIN or TECHNOLOGY new to me?
  YES -> Continue to Step 3
  NO  -> Continue to Step 4

Step 3: How new is this to me?
  COMPLETELY NEW (never used the tech)
    -> Study First, then Learn Mode
       /learn-socratic <concept>
       /learn-spec <spec-id> <slug>

  SEEN SIMILAR (used analogous tech)
    -> Grill + Scaffold Mode
       /grillme <spec>
       /learn-mimic <task> phase 1

Step 4: Have I done this EXACT pattern before in this project?
  NO, FIRST TIME for this pattern
    -> Grill + Predict Mode
       /grillme <spec>
       /learn-predict <spec>
       /learn-mimic <task> phase 2

  YES, SECOND TIME (done one similar before)
    -> Verify + Build Mode
       /grillme <spec>
       /learn-mimic <task> phase 2 or 3

  YES, THIRD+ TIME (pattern is familiar)
    -> Ship Mode
       /start-spec-dev <spec-id> <slug>
       (or /learn-mimic <task> phase 3 if you want a light check)
```

---

## The Three Modes

### Mode 1: Learn Mode (2-3x time investment)

**When**: Technology or domain is new. You need to build mental models, not just ship code.

**Commands**:
```
/learn-socratic <concept>              # Understand prerequisites
/grillme <spec>                        # Prove you understand the problem
/learn-spec <spec-id> <slug>           # Full learning lifecycle
```

Or broken down manually:
```
/learn-socratic <concept>              # Step A: Understand the tech
/learn-predict <spec>                  # Step B: Design before seeing solution
/learn-mimic <task> phase 1            # Step C: See solution, rewrite from memory
/learn-explain                         # Step D: Understand key decisions
/learn-rebuild <module>                # Step E: Test retention (next day)
```

**Why this works**: Cognitive science calls this "desirable difficulty." Predicting before seeing, explaining after building, and rebuilding from memory create three separate encoding events for the same knowledge. Each retrieval strengthens the memory trace. Passive reading creates one weak trace; this approach creates multiple strong ones.

**Time**: 2-3x longer than just shipping.
**Retention**: High. You can debug and extend this code months later.

---

### Mode 2: Grill + Scaffold Mode (1.5x time investment)

**When**: Pattern is partially familiar. You've seen similar tech or done analogous work, but not this exact thing in this project.

**Commands**:
```
/grillme <spec>                        # Verify understanding, find gaps
/learn-predict <spec>                  # Design your approach
/learn-mimic <task> phase 2            # Signatures + hints, you fill logic
/learn-explain                         # Understand decisions (optional)
```

**Why this works**: The grill acts as a diagnostic. If you score READY, you skip the deep learning and go straight to building with light scaffolding. If you score NOT READY, you know exactly which gaps to fill before coding. This prevents both over-learning (wasting time on things you know) and under-learning (shipping code you don't understand).

**Time**: 1.5x longer than just shipping.
**Retention**: Good. You understand the structure and can modify it.

---

### Mode 3: Ship Mode (1x baseline time)

**When**: You've done this pattern 2+ times. The tech is familiar. The architecture is clear. You just need to execute.

**Commands**:
```
/start-spec-dev <spec-id> <slug>       # Full lifecycle, Claude does heavy lifting
```

Or with a light check:
```
/grillme easy <spec>                   # Quick sanity check (optional)
/learn-mimic <task> phase 3            # Pseudocode only, you implement fully
```

**Why this works**: Repeating the full learning cycle on familiar patterns has diminishing returns. Once you can implement from pseudocode (Phase 3) consistently, additional scaffolding is overhead, not learning. Ship it, and invest the saved time into learning the NEXT unfamiliar thing.

**Time**: Baseline.
**Retention**: Already solid from prior learning rounds.

---

### Paperwork Mode (for already-implemented specs)

**When**: Code is written and working, but spec folder and verification don't exist yet.

**Commands**:
```
/create-spec <spec-id> <slug>          # Create spec.md + checklist.md
/verify-spec <spec-id>                 # Audit: tests, lint, checklist, roadmap update
```

**Why separated**: Creating retroactive documentation is administrative, not learning. Don't waste learning energy on it. But DO still run verify -- it catches gaps (missing tests, lint errors) that you might have skipped during implementation.

---

## Step-by-Step Workflows

### Workflow A: Learning a New Technology (Learn Mode)

Use when a spec requires tech you've never used.

```
Step 1: STUDY the underlying concepts
  Command: /learn-socratic <technology or concept>
  Duration: 15-30 min
  Output: You can answer 3-5 concept questions correctly
  Why: You can't design a solution if you don't understand the primitives.
        Socratic method forces active recall, not passive reading.

Step 2: PROVE you understand the problem
  Command: /grillme <spec description>
  Duration: 15-20 min
  Output: Verdict (READY / ALMOST / NOT READY)
  Why: Exposes gaps between "I read about it" and "I can apply it."
        If NOT READY, loop back to Step 1 with targeted study.

Step 3: PREDICT your approach before seeing the solution
  Command: /learn-predict <spec>
  Duration: 10-15 min
  Output: Your design vs Claude's, with delta analysis
  Why: Prediction creates a "hook" in memory. When you see the actual
        solution, the differences stick because you have something to
        compare against. Without prediction, solutions wash over you.

Step 4: IMPLEMENT with full scaffolding
  Command: /learn-mimic <task> phase 1
  Duration: 30-60 min
  Output: Claude's version, then your rewrite from memory
  Why: Writing code after seeing it tests working memory. The 3 things
        you'll likely forget are exactly your learning edge.

Step 5: UNDERSTAND the decisions
  Command: /learn-explain
  Duration: 10 min
  Output: Key decisions, trade-offs, alternatives rejected
  Why: Knowing WHY prevents cargo-culting. Next time you face a
        similar decision, you'll reason from principles, not templates.

Step 6: VERIFY the spec
  Command: /verify-spec <spec-id>
  Duration: 5 min
  Output: Tests pass, lint clean, checklist complete, roadmap updated

Step 7: TEST RETENTION (next day or after 2-3 days)
  Command: /learn-rebuild <module>
  Duration: 15-20 min
  Output: Your rebuild vs original, gap analysis
  Why: Spaced retrieval is the strongest known memory technique.
        If you can rebuild it after a gap, you own it.
```

**Total time**: ~2-3 hours per spec
**Learning value**: Maximum. This is how you build expertise.

---

### Workflow B: Applying a Partially Familiar Pattern (Grill + Scaffold Mode)

Use when you know the tech but haven't applied it in this specific way.

```
Step 1: GRILL to diagnose gaps
  Command: /grillme <spec>
  Duration: 15 min
  Output: Verdict + specific gaps identified
  Why: Efficient triage. Spend learning time only on actual gaps,
        not things you already know.

Step 2: PREDICT your design
  Command: /learn-predict <spec>
  Duration: 10 min
  Output: Delta between your approach and optimal
  Why: Calibrates your intuition. Shows where your mental model
        diverges from best practice.

Step 3: IMPLEMENT with signatures + hints
  Command: /learn-mimic <task> phase 2
  Duration: 20-40 min
  Output: You fill in all logic from signatures
  Why: Phase 2 proves you can translate design into code.
        If you struggle, you need Phase 1 for this pattern.

Step 4: VERIFY
  Command: /verify-spec <spec-id>
  Duration: 5 min

Step 5 (optional): EXPLAIN decisions
  Command: /learn-explain
  Duration: 10 min
  Why: Only if you encountered surprising design choices.
```

**Total time**: ~1-1.5 hours per spec
**Learning value**: High for gap-filling. Efficient use of time.

---

### Workflow C: Repeating a Known Pattern (Ship Mode)

Use when you've done this exact pattern 2+ times and are confident.

```
Step 1: SHIP
  Command: /start-spec-dev <spec-id> <slug>
  Duration: 20-40 min
  Output: Spec created, implemented, verified

Step 2 (optional): LIGHT GRILL as sanity check
  Command: /grillme easy <spec>
  Duration: 5 min
  Why: Quick pulse check. If you score READY instantly,
        confirms you haven't forgotten anything.
```

**Total time**: ~30-45 min per spec
**Learning value**: Low (but that's fine -- you already learned this).

---

### Workflow D: Retroactive Spec Documentation (Paperwork Mode)

Use for already-implemented specs that need spec folders.

```
Step 1: CREATE spec folder
  Command: /create-spec <spec-id> <slug>
  Duration: 2 min
  Output: specs/spec-<id>-<slug>/spec.md + checklist.md

Step 2: VERIFY implementation
  Command: /verify-spec <spec-id>
  Duration: 5 min
  Output: Checklist marked, roadmap status updated
```

**Total time**: ~7 min per spec
**Learning value**: None (administrative). But verification catches quality gaps.

---

## Applied to MCPGuard Roadmap

### Phase 1: Project Foundation

| Spec | Domain | Familiarity | Recommended Workflow | Reasoning |
|------|--------|-------------|---------------------|-----------|
| S1.1 | Python packaging | Already done | **D (Paperwork)**: `/create-spec` + `/verify-spec` | Code exists, just needs spec folder |
| S1.2 | Makefile | Familiar | **C (Ship)**: `/start-spec-dev` | Makefiles are well-known territory |
| S1.3 | Pydantic config, env loading | Partially familiar | **B (Grill + Scaffold)**: `/grillme` + Phase 2 | Pydantic v2 settings have specific patterns worth learning |
| S1.4 | Package __init__ | Trivial | **C (Ship)**: `/start-spec-dev` | One-file spec, minimal logic |
| S1.5 | Logfire/structlog | New tech? | **A (Learn)** or **B (Scaffold)** | If Logfire is new: full learn mode. If structlog familiar: scaffold |

### Phase 2: Data Models

| Spec | Domain | Familiarity | Recommended Workflow | Reasoning |
|------|--------|-------------|---------------------|-----------|
| S2.1 | Pydantic models (findings) | Partially familiar | **B (Grill + Scaffold)** | First Pydantic model spec -- worth getting the pattern right |
| S2.2 | Pydantic models (semantic) | Pattern repeats | **C (Ship)** or Phase 3 mimic | Second model spec -- pattern is established |
| S2.3 | Tool definition model | Pattern repeats | **C (Ship)** | Third model spec |
| S2.4 | Scan events | Pattern repeats | **C (Ship)** | Fourth model spec |

### Phase 3: Detectors

| Spec | Domain | Familiarity | Recommended Workflow | Reasoning |
|------|--------|-------------|---------------------|-----------|
| First detector | BaseDetector ABC, regex | New pattern | **A (Learn)**: `/learn-spec` | First detector sets the pattern for all others. Invest heavily. |
| Second detector | Same ABC pattern | Partially familiar | **B (Scaffold)**: `/grillme` + Phase 2 | Prove you can apply the pattern to a different vulnerability class |
| Third+ detector | Same ABC pattern | Familiar | **C (Ship)**: `/start-spec-dev` | Pattern is internalized. Ship and invest time elsewhere. |

### Phase 4+: Agents, Formatters, CLI

| Spec | Domain | Familiarity | Recommended Workflow | Reasoning |
|------|--------|-------------|---------------------|-----------|
| PydanticAI semantic agent | PydanticAI agents | New domain | **A (Learn)**: `/learn-socratic` + `/learn-spec` | Agent framework is core to MCPGuard. Must understand deeply. |
| PydanticAI report agent | Same framework | Second time | **B (Scaffold)**: Phase 2 mimic | Apply agent pattern to different use case |
| Rich formatter | Rich library | Partially familiar | **B (Scaffold)** | Rich is well-documented but has specific patterns |
| SARIF formatter | SARIF spec | New format | **A (Learn)**: `/learn-socratic SARIF` first | SARIF is a complex spec with strict requirements |
| FastMCP server | FastMCP | New domain | **A (Learn)**: full learn mode | Dual-mode (CLI + MCP server) is architecturally significant |

---

## Why This Pattern Works

### 1. Desirable Difficulty (Bjork, 1994)

Learning that feels easy is often shallow. Predicting, getting grilled, and rebuilding from memory are harder than watching Claude code -- and that difficulty is exactly what creates durable learning.

**Applied here**: `/learn-predict` and `/grillme` create difficulty before implementation. `/learn-rebuild` creates difficulty after. The implementation itself (Phase 1-3 mimic) is the easiest part.

### 2. The Testing Effect (Roediger & Karpicke, 2006)

Retrieving information from memory strengthens it more than re-reading it. Every time you answer a grill question or rebuild from memory, you're practicing retrieval.

**Applied here**: `/grillme` is a retrieval test before coding. `/learn-rebuild` is a retrieval test after. `/learn-noai` (weekly) is a retrieval test across all recent work.

### 3. Spaced Repetition (Ebbinghaus, 1885)

Memory decays exponentially, but reviewing at increasing intervals resets the decay curve. The progression from Phase 1 -> Phase 2 -> Phase 3 -> Ship naturally spaces out your retrieval.

**Applied here**: First detector (Phase 1) -> second detector (Phase 2, days later) -> third detector (Phase 3/Ship, days later). Each revisit reinforces the pattern at a decreasing cost.

### 4. Zone of Proximal Development (Vygotsky, 1978)

You learn best when the task is slightly beyond your current ability, with support available. Too easy = boredom. Too hard = frustration.

**Applied here**: The Phase 1/2/3 progression self-adjusts difficulty. Phase 1 (full scaffolding) for new territory. Phase 3 (pseudocode only) when you're almost independent. The scaffolding is the "support" that keeps you in the productive zone.

### 5. Elaborative Interrogation (Pressley et al., 1987)

Asking "why?" about each decision creates deeper encoding than just seeing the decision.

**Applied here**: `/learn-explain` forces "why?" after every implementation. `/grillme` forces "why?" before. The combination creates a why-sandwich around every spec.

### 6. The Generation Effect (Slamecka & Graf, 1978)

Information you generate yourself is remembered better than information you read. Writing code (even imperfect code) beats reading perfect code.

**Applied here**: Every mode except Ship requires YOU to write or design something before seeing Claude's version. Even Phase 1 (full code then rewrite) requires you to generate the code from memory.

---

## Progression Tracking

Track your progression across specs to see yourself graduating:

```
| Spec  | Mode Used        | Mimic Phase | Grill Score | Notes                    |
|-------|------------------|-------------|-------------|--------------------------|
| S1.1  | Learn (Predict)  | Phase 2     | N/A         | 3 typos in pyproject.toml|
| S1.2  | Ship             | N/A         | N/A         | Familiar territory       |
| S1.3  | Scaffold         | Phase 2     | ALMOST      | pydantic_settings new    |
| ...   | ...              | ...         | ...         | ...                      |
```

**Signs of growth**:
- Grill scores trending from ALMOST -> READY
- Mimic phases trending from 1 -> 2 -> 3
- More specs in Ship mode, fewer in Learn mode
- `/learn-rebuild` scores improving (more SOLID, fewer GAPs)
- `/learn-noai gaps` finding fewer blind spots over time

**Signs of stagnation**:
- Staying in Ship mode for everything (not learning new things)
- Staying in Learn mode for everything (not graduating)
- Grill scores not improving across similar specs
- Can't rebuild a module you built last week

---

## Anti-Patterns to Avoid

### 1. "Learn Everything" Trap

**Symptom**: Running `/learn-spec` on every spec, including trivial ones.
**Problem**: Learning mode on a one-file `__init__.py` spec is waste. You already know this.
**Fix**: Use the decision framework. Trivial specs get Ship mode.

### 2. "Ship Everything" Trap

**Symptom**: Running `/start-spec-dev` on everything because it's faster.
**Problem**: You ship fast but can't debug, explain, or extend anything. You're a prompt operator, not an engineer.
**Fix**: If the tech is new, FORCE yourself into Learn mode. The 2x time investment pays for itself in debugging time saved later.

### 3. "Permanent Phase 1" Trap

**Symptom**: Always choosing Phase 1 mimic because it feels safer.
**Problem**: You're never testing whether you can actually build without seeing the answer first.
**Fix**: After doing Phase 1 for a pattern, you MUST do Phase 2 next time. Discomfort is the point.

### 4. "Skip the Grill" Trap

**Symptom**: Going straight to implementation without checking understanding.
**Problem**: You build on wrong assumptions, then debug for hours.
**Fix**: `/grillme` takes 15 minutes. Debugging a wrong assumption takes hours. Always grill on non-trivial specs.

### 5. "Never Review" Trap

**Symptom**: Never running `/learn-rebuild` or `/learn-noai gaps`.
**Problem**: You think you learned something, but it faded. No spaced retrieval means no retention.
**Fix**: Weekly `/learn-noai gaps`. `/learn-rebuild` on the previous week's most complex spec.

### 6. "Retroactive Learning" Trap

**Symptom**: Running `/learn-explain` on code you shipped weeks ago.
**Problem**: The context is gone. Learning is most effective immediately after building.
**Fix**: Run `/learn-explain` in the SAME session as implementation, not later.
