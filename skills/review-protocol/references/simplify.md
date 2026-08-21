---
name: simplify
description: Over-engineering review producing a tagged delete-list with tags: delete, stdlib, native, yagni, shrink, defensive, noise. Load only when `--simplify` is in the task prompt.
---

# Simplify Review — Over-Engineering Delete-List

Use this skill when explicitly requested via `--simplify` mode. This is not a general code review — it is a focused hunt for code that should be deleted or replaced, not rearranged or polished.

Do NOT load automatically. It is too aggressive for routine review.

## Purpose

Find code in the current diff that exists only because:
- Generated code was not cleaned up after the first working version
- An abstraction was introduced before it needed to exist
- A library or framework capability was hand-rolled instead of used
- A pattern from one project was carried over where it doesn't pull its weight
- Type, config, or wiring overhead exists that the current code does not justify

## Tag System

Every finding must carry exactly one tag:

| Tag | Meaning | When to use |
|-----|---------|-------------|
| `delete` | Delete entirely | Function/class/module/helper that is unnecessary, unused, or duplicated |
| `stdlib` | Replace with stdlib | Custom code doing what Python/Node/Go stdlib already does better |
| `native` | Replace with framework-native | Wrappers, adapters, or indirection that mirror what the framework already provides natively |
| `yagni` | You Aint Gonna Need It | Config, parameters, branching, abstraction that supports a hypothetical future that hasn't materialized |
| `shrink` | Consolidate | Multiple scattered pieces that should be a single helper or inline expression |
| `defensive` | Defensive Programming audit | Redundant None/Key guards, paranoid checks, LBYL where EAFP fits, missing boundary validation |
| `noise` | Remove or rewrite comment | Comment adds no signal: paraphrases code, states obvious, contains misplaced info (design rationale, bare TODO, dead code) |

## What to Flag

Flag code where any of these hold:

- **Unnecessary wrapper**: a function/class that merely delegates to another with no behavioral change or meaningful contract enforcement
- **Unused parameter**: a function parameter or config key that has exactly one call site and that call site passes a hardcoded value
- **Abstract-everything-ism**: an interface/abstract class/trait with exactly one implementation and no plan for a second
- **Tiny helper**: a function ≤3 lines used at exactly one call site — it should be inlined
- **Config over code**: a runtime config knob for something that never changes between environments or runs
- **Copy-paste hook**: a React hook, middleware, decorator, or interceptor that exists because a pattern was abstracted before it repeated
- **Dead parameter**: a parameter accepted but never read on any code path
- **Unnecessary enum/class**: a one-member enum or a class with one method and no state
- **Decorator bloat**: a decorator/annotation whose entire body could be one line in the decorated function
- **Over-normalized**: splitting data/config across files or models when a single dict/object would suffice
- **Optionality creep**: fields/params that are always provided but declared optional, or fields that are always `None` at construction
- **Wrapper around stdlib**: `def flatten(lst): return [x for sub in lst for x in sub]` instead of `itertools.chain.from_iterable`
- **Wrapper around library**: a thin composition that faithfully re-exports a library function with the same signature
- **Duplicate validation across layers**: the same `if x is None` or `if key in d` pattern appears in ≥2 functions in the same call chain; upstream already validated → delete downstream copies
- **Phantom default**: `dict.get(key, fallback)` where the caller immediately before does `d[key]` and would raise before `get` ever exercised its default
- **LBYL-to-EAFP**: `if key in d: return d[k]` is verbose safety where `try: return d[k]\nexcept KeyError:` is idiomatic Python — unless performance profiling proved the check matters
- **Guard after guarantee**: `if x is None: raise` immediately following a function that would itself raise if x were None
- **isinstance paranoia**: runtime type-check on a parameter that already carries a type hint and reached this code through typed boundaries

## What NOT to Flag

Do not flag:
- Correctness issues (that's for the main review)
- Security issues (that's for the security reference)
- Performance before profiling (unless there is clear O(n²) or N+1 in the diff)
- Missing tests or documentation
- API design or naming
- Code style, formatting, or linting
- Anything the review agent already flagged
- **Pydantic/typed-model validation at system boundaries** — first ingress point where untrusted data enters; that's the canonical place for it
- **`try/except` around external IO** — `requests`, `open()`, `subprocess.run()` — defence at the network/filesystem boundary is not redundant
- **Security validations** — auth checks, path-traversal guards, SQL injection escapes — these belong in security-review, not simplify
- **Code with an explicit `# defensive:` or `# boundary guard:` comment** — the author consciously decided the check is necessary

If a finding could also be a correctness bug, report it as a correctness finding instead — do not dilute the simplify list. If a defensive finding is both redundant AND a correctness risk, report it as a correctness finding — not as `[defensive]`.

## Output Format

Each finding is a single line: `[tag] file:line — why delete/replace → what to use instead or how to inline`

Examples:
```
[delete] src/utils/flatten.py:12 — custom flatten, used exactly once → inline itertools.chain
[stdlib] src/utils/parse_csv.py:3 — custom CSV parser → use csv.DictReader
[native] src/api/client.py:21 — httpx client wrapper that adds no auth/retry/header logic → use httpx directly
[yagni] src/config.py:42 — FORCE_HTTPS env var, always true in every env → hardcode True
[shrink] src/handlers/user.py:14-19 + order.py:28-33 — duplicated validate_positive → single helper in shared/
[noise] src/handler.py:15 — paraphrase: "# Increment counter" above `i += 1` → delete
[noise] src/cache.py:23 — bare TODO without ticket → replace with `# TODO(#1425): add retry with exponential backoff`
```

## Defensive Programming Audit (tag: `[defensive]`)

This pass inspects every None/KeyError/TypeError guard, default, and type-check the diff adds. The goal is not just "remove the check" but to classify each guard so the author keeps the real safety and drops the reflexive AI paranoia.

### System Boundary Map

Start by locating all **trust boundaries** in the diff — places where untrusted data enters the system:

| Input source | Where it first hits code | Boundary? |
|---|---|---|
| HTTP/REST request body | endpoint handler, middleware, serializer deserialize | YES — boundary |
| CLI args / env vars | `argparse`, `os.environ`, config loader | YES — boundary |
| File/Database read | `open()`, DB query result | YES — boundary |
| Internal function call | inside the same process, same trust boundary | NO — internal |
| Library return value | post-deserialization, after library validated its contract | NO — library internal |

**Rule:** Guards at YES boundaries are necessary (keep). Guards at NO boundaries are likely redundant — the caller already guarantees the contract.

### Findings buckets

Every DP finding goes into exactly one bucket:

#### Redundant (drop)

A guard that cannot fire because the caller or an upstream layer already guarantees the invariant. Tag `[defensive]` with a one-line justification citing what upstream already ensures.

```
[defensive] src/process.py:38 — `if data is None: return` is redundant; parse_input() on line 12 already throws for None
```

Look for:
- Same `is None` / `in dict` check in ≥2 layers of the same call chain
- `dict.get(key, fallback)` where the call site uses `d[key]` and would KeyError before `get` is meaningful
- Raising or returning early when the input was already validated by the entry-point contract
- Guard that shadows a type hint the caller must satisfy — the type checker is the guard, not the `if`

#### EAFP opportunity (refactor)

A LBYL guard that the code could replace with EAFP **without changing behavior**. Tag `[defensive]` with the EAFP alternative.

```
[defensive] src/io.py:91 — LBYL: `if key in d: return d[key]` → EAFP: `try: return d[key]\nexcept KeyError: raise`
```

Typical EAFP-opportunity patterns:
- `if key in d: ... else: ...` where the else/default is a simple fallback
- `if x is not None: x.method()` where calling `.method()` on None would be the real signal
- `if hasattr(obj, 'attr'): obj.attr` — Python idioms prefer EAFP for attribute access

Do NOT flag EAFP when: the guard prevents an expensive or destructive operation, the exception would be hard to distinguish from a real error, or the code is performance-critical.

#### Missing at boundary (advisory)

A place where data crosses a trust boundary without validation, and the diff should probably add one. **Advisory only** — no tag, never a blocker.

```
src/endpoint.py:6 — `json.loads(raw)` with no schema validation; data enters here from HTTP POST
```

Only flag at YES boundaries (see system boundary map). Do not invent missing guards at NO boundaries.

### Detection Heuristics

1. **Same-check-in-chain:** grep for the same pattern (`is None`, `in dict`, `isinstance`) across functions in the same call chain. If it appears in ≥2, the downstream one is Redundant unless the upstream guard is conditional.

2. **Phantom-default:** flag `dict.get(key, X)` when within the same function or immediate caller, `d[key]` (bare access) also appears. The bare access will KeyError before `get` executes — the default is dead code unless `d[key]` is inside an `if key in d` block.

3. **Guard-after-guarantee:** `if x is None: raise/return` directly after a function call that would itself raise/return None on invalid input. The function is the guard — the `if` is redundant.

4. **Type-hint bound:** `isinstance(x, T)` where `x` has a type hint `T` (not `Union[T, ...]`, not `Optional[T]`) and entered through typed code. The caller cannot pass `~T` without a type-checker warning. Flag as Redundant.

5. **LBYL-to-EAFP heuristic:** `if guard-condition then body` where `body` has an idiomatic EAFP equivalent and no performance-sensitive loop surrounds it → EAFP opportunity.

6. **Boundary inventory:** scan added lines for `json.loads`, `parse`, `from_bytes`, `Pydantic.model_validate`, `BaseModel.__init__`, CLI parser `.parse_args()`, `open()`, `request.json()`, `request.form`. These are boundary points → check for validation immediately after.

## Comment Audit (tag: `[noise]`)

This pass inspects every comment in the diff — inline, block, docstring, TODO. AI agents over-comment by default. The goal is not to delete every comment, but to keep only those that explain *why* — never *what*.

**Core rule:** If removing the comment and reading the code alone produces the same understanding, the comment is noise.

### Detection Heuristics

| # | Pattern | Example (bad) | Action |
|---|---|---|---|
| H1 | **Paraphrase** | `i += 1  # Increment counter` | delete |
| H2 | **Obvious construct** | `# Import the os module` above `import os` | delete |
| H3 | **Section-label / ASCII-art** | `# ===== INITIALIZATION =====` above 3 lines | delete; extract function if needed |
| H4 | **Commented-out dead code** | `# old_handler()` with no note | delete; if needed, `# See commit abc123` |
| H5 | **Closing-bracket / end-marker** | `# end if`, `# end for` | delete |
| H6 | **Redundant docstring** | `"""Tests for foo."""` — name only, no semantic content | delete or expand with intent |
| H7 | **Bare TODO** | `# TODO: fix this` without ticket | rewrite: `# TODO(#1425): fix this` |
| H8 | **Initialize-variable block** | `# Initialize variables` above `x = 0; y = None` | delete |
| H9 | **Verbose preamble** | 5-line prose above a 3-line comprehension | delete; rename helper |
| H10 | **Misplaced rationale** | "We chose Postgres over Mongo because..." in code | delete; move to ADR / project docs |

Concrete finding format:

```
[noise] src/handler.py:15 — paraphrase (H1): "# Increment counter" above `i += 1` → delete
[noise] src/cache.py:23 — bare TODO (H7): "# TODO: add retry" without ticket → # TODO(#1425): add retry with exponential backoff
[noise] src/db.py:7 — misplaced rationale (H10): architecture-decision prose in code → delete; move to docs/adr/
```

Some `[noise]` findings are *replacements*, not pure deletions. Always prefer the more useful form over the bare one — but if the replacement is just as long as the original, the comment is not worth keeping. Delete and trust the docs / commit history.

### What NOT to Flag

- `# shortcut:` marker (project convention)
- `# decision:` marker for implementation-level choices (project convention)
- `# defensive:` / `# boundary guard:` (already protected in general What NOT to Flag)
- Non-obvious logic: bit tricks, algorithmic intuition, magic-number rationale
- Performance tradeoffs: `# linear scan, not hash — N < 10, hash overhead dominates`
- Workaround notes tied to a bug/issue: `# Firefox 2 drops mouse events outside the window; see bug #1234`
- Source attribution for copied code: `# via https://stackoverflow.com/a/46018816`
- Block comments at function head explaining intent of a non-trivial operation that cannot be trivially extracted

### Budget

3–8 high-confidence `[noise]` findings per ~200 lines of diff. Stop when the heuristics have all been applied.

## Priority

Process findings in this order:

1. **Defensive Programming Audit** — run first: map boundaries, classify each guard as Redundant | EAFP-opportunity | Missing-at-boundary. This pass informs context for all subsequent findings.
2. **Comment Audit** — run after DP: classify each comment against H1–H10 heuristics. Findings are `[noise]`.
3. `delete` — highest value, zero maintenance cost
4. `stdlib` / `native` — reduces dependency surface and in-house code
5. `shrink` — reduces fragmentation
6. `yagni` — reduces cognitive load

Defensive findings: budget 3–6 high-confidence tags per ~200 lines of diff. General findings: stop when you have identified 5–8 high-confidence findings per ~200 lines of diff. More than that is noise.

## Tone

Brief, direct, factual. The output is a delete-list, not an essay.

Good:
- `[delete] src/helpers/auth.py:43 — AuthGuard wrapper adds no logic vs raw middleware → inline`
- `[stdlib] src/utils/datetime_helpers.py:7 — time parsing wrapper → use datetime.fromisoformat`

Not good:
- "This function seems like it might be unnecessary if we consider the broader design" → be direct
- Multi-paragraph justifications for each finding → keep to one line

## Integration with Review Agent

The `--simplify` mode in plan.md instructs spawning `auto-review` with `mode: --simplify`. The review agent loads this skill, runs the delete-list pass against the current diff, and appends findings under a `Simplify Notes` section in the return format.

The Defensive Programming Audit and Comment Audit each produce their own structured subsection. Start with boundary map and DP findings as tagged `[defensive]` items plus untagged Missing-at-boundary advisories, then list comment findings as tagged `[noise]` items.

```md
Simplify Notes
- [delete] ...

Defensive Programming Audit
- System boundaries: YES at endpoint.py:6 (HTTP POST raw), NO at process.py:21 (internal)
- [defensive] src/process.py:38 — redundant: upstream parse_input already throws for None
- Missing at boundary: src/endpoint.py:6 — raw json.loads after HTTP POST, no schema validation

Comment Audit
- [noise] src/handler.py:15 — paraphrase (H1) above `i += 1` → delete
- [noise] src/cache.py:23 — bare TODO (H7) → replace with `# TODO(#1425): add retry with exponential backoff`
- [noise] src/db.py:7 — misplaced rationale (H10) → delete; move to docs/adr/
```
