---
name: review-protocol
description: Shared review behavior for auto-review and auto-review-integration. Load when reviewing code completion, quality, or plan-vs-implementation compliance. Provides the evidence standard, review range, severity model, and return format; routes to specialized references for security, thermo-nuclear, or simplify passes.
---

# Review Protocol

Shared review behavior for auto-review and auto-review-integration.

Every finding gets proof. Be pragmatic, not pedantic. Do not duplicate what static analyzers already cover.

## Core Rules

- Focus on bugs, completion gaps, regressions, and real maintainability issues before style
- Be pragmatic, not pedantic
- Follow the project brief, planner output, success criteria, and repository AGENTS.md standards
- Do not flag issues that ruff, pyright, or ordinary static checks already cover
- Be specific: `file_path:line_number`, problem, concrete fix suggestion
- **Report findings only when >80% confident** it is a real problem. Zero findings is a valid result.
- **Proof gate for Critical/High findings:** Confirm you can cite the exact line, describe the concrete failure mode, and have read the surrounding context before flagging. If you cannot satisfy all three, downgrade or drop.
- **False-positive blacklist:** Do not flag generic "add error handling" without caller tracing. Do not flag magic-number false alarms where the number has domain meaning. Do not flag missing docstrings on self-documenting code. Do not flag intended fire-and-forget patterns with explicit inline comments.

## Review Scope and Range

The task prompt declares a **Review Scope**: `full` or `fix-delta`. The scope determines what the review examines and how the report is structured.

### Full scope (default)

The first review of any planned work runs at full scope. The task prompt includes a **Review Base** SHA. Examine:
1. `git diff <review-base>...HEAD` — all committed changes since plan start
2. `git diff HEAD` — any uncommitted changes

If no Review Base is provided, fall back to `git diff HEAD` (uncommitted) or `git diff main..HEAD` (full branch).

### Fix-delta scope (follow-up after review fixes)

A follow-up review after review fixes runs at fix-delta scope. The task prompt includes **Prior Findings**, the **Snapshot SHA** the previous review examined, and the **Fix Diff** (`git diff <snapshot>...HEAD` plus uncommitted changes). Examine only:

1. Each carried finding against the current code — report `resolved`, `unresolved`, or `regressed` with file:line proof
2. The changed files since the snapshot — regressions the fixes may have introduced
3. Validation evidence the caller ran after the fixes

Do not re-run the full completion, plan-coverage, or code-quality pass. Do not hunt for new findings outside the supplied findings and the changed files. New Critical/Major regressions in the fix delta are still reported at full severity.

## Always: Completion Check

- Is every item in the approved plan actually implemented?
- Are the success criteria from the brief genuinely met — not just superficially?
- Is there any missing follow-through work required to call the task complete?
- Do the changed files match what the plan said would change?

## Always: Key Files Verification

The plan lists Key Files that must be created or modified. For each one:

1. **Existence**: Does the file exist?
2. **Substantive**: Is it real implementation, not a stub? Check for:
   - Returns `<div>Placeholder</div>` or `Response.json({ message: "Not implemented" })`
   - Contains only `TODO`, `FIXME`, or placeholder comments
   - Python: function/method with only `pass` or a docstring with no real body
   - Any language: primary path returns `None`/`null`, throws "Not implemented", or is intentionally empty
   - New file where every top-level declaration is a stub

If missing or stub: flag as INCOMPLETE.

## Always: Key Connections Verification

The plan lists Key Connections — how components must be wired together. For each:

1. **Import exists**: The consumer imports the provider
2. **Usage exists**: The consumer actually calls what it imports
3. **Data flows**: Output from one flows into the other (not just static returns)

Common stub patterns:
- Fetch called but response ignored (`fetch(...)` with no `.then`, `await`, or assignment)
- Query runs but static response returned (`await x.findMany()` then `return Response.json({ ok: true })`)
- Handler only prevents default (`onSubmit={(e) => e.preventDefault()}`)

If missing or broken: flag as INCOMPLETE.

## Always: Code Quality

Check the changed code for:
- **Bugs** — wrong conditionals, off-by-one, incorrect operators, null/None handling
- **Missing error handling** — uncaught exceptions on external calls, missing input validation, no fallback for failure paths. Only flag when there is a concrete caller-visible failure mode.
- **Logic correctness** — does the implementation do what was asked?
- **Over-engineering** — unnecessary abstractions, classes that should be functions, layers that add no value
- **File size** — did the diff push a file past ~1000 lines? Flag as Major and ask whether decomposition is warranted.
- **Branching complexity** — ad-hoc conditionals or special cases inserted into busy code paths belong behind their own abstraction
- **AGENTS.md compliance** — does the code follow the project's stated patterns and conventions?
- **Regressions** — does anything that was working before now break?
- **Defensive noise** — validation, null checks, error handling, wrappers, or fallbacks added without a concrete failure path. Flag as Major.
- **Adjacent refactors** — changes outside the task scope. Flag as Major.
- **Hypothetical abstractions** — abstractions added for future use cases that don't exist yet. Flag as Major.

## Always: AI Code Quality

Check for AI-specific issues that static analyzers miss:
- **Dead code** — new functions/classes/exports never called outside the diff itself
- **Hallucinated API** — calls to methods or imports that do not exist in the installed library. **Critical** — code will not compile or run.
- **Reinventing stdlib / project helpers** — custom utilities where a built-in or existing helper already fits
- **Reinventing third-party library** — custom utilities where an existing PyPI/npm package covers the case. Verify the library exists via Context7/PyPI/webfetch before flagging; do not invent libraries.
- **Comment quality** — comments that merely paraphrase code (`# increment counter` above `i += 1`). Flag as Minor.
- **Style drift** — mixed conventions introduced mid-file without reason

## Always: Review Guard Check

When the task prompt contains a `Review Guard` block, verify:
- **Invariants satisfied** — each named invariant holds in the delivered code. Cite file/line. Severity: Critical if broken.
- **Forbidden bypasses absent** — the diff contains none of the named forbidden bypasses, unless the plan approved the exact exception with compensating evidence. Unapproved bypass: Major.
- **Evidence produced** — the named evidence artifacts, counters, or commands exist or pass. Missing evidence: Major.

When no Review Guard is provided, skip this section silently.

## Conditional: Project Contract Check

Trigger only when the project `AGENTS.md` declares a `## Project Contract` marker with `Status: active` or `draft`, or the plan carries a `Contract Context` block. Load the `project-contract` skill and:

1. **Checker evidence** — run the structural checker and confirm the status is valid `active`, `opted-out`, or `not-required`. Missing/draft/invalid: Critical.
2. **Clause and decision coverage** — confirm the plan builds on the relevant contract sections and decision IDs named in its `Contract Context`.
3. **Amendment coverage** — if the diff changes contract files, confirm the approved plan declared `Contract impact: amend` and the user approved it. Unplanned material boundary changes: Major, return to plan.
4. **No laundering** — confirm no contract file was rewritten to match the implementation it enabled. Contract edits that justify changed code without a plan amendment: Critical.

Populate `Project Contract Check` in the return format. When no contract marker is present and the plan carries no Contract Context, omit this section silently.

## Always: Quality-Gate / Suppression Check

Always active. Inspect the diff for source-level suppressions and quality-gate changes:
- `# noqa`, `# type: ignore`, `# nosec` on new or changed lines
- `filterwarnings`, `warnings.filterwarnings`, `ignore_warnings` parameter changes
- `--ignore`, `--disable` flags on linters, type checkers, or validators
- Changes to lint/typecheck configuration (`.ruff.toml`, `pyproject.toml` tool sections, `noxfile.py` sessions)
- Removal, weakening, or conditional bypass of a previously enforced validation command

For each finding:
- If the Review Guard names this exact suppression with compensating evidence: **Positive** — plan-approved.
- If no plan approval: **Major** — unapproved suppression.

## Severity Model

- **Critical** — broken requested behavior, serious regression, security issue, missing core scope
- **Major** — logic error, missing validation on external input, meaningful maintainability problem, incomplete implementation
- **Minor** — limited high-value cleanup, max 3 per review
- **Advisory** — structural simplification worth considering; not a blocker
- **Positive** — good patterns worth preserving

## Conditional: Silent Failures

Check for swallowed errors when the diff touches error handling, file ops, subprocess, network, or database:

- [ ] No bare `except:` or `except Exception: pass` that silently consumes errors without logging or re-raising
- [ ] No `try/except` that only logs without recovery or re-raise — logging without action is still silent failure
- [ ] No `subprocess.run()` with `check=False` that ignores non-zero exit codes
- [ ] No file operations without error handling (`open()`, `read()`, `write()`, `unlink()`, `os.remove()`) outside a try block unless known-safe
- [ ] No None/null propagation — functions that can return `None`/`null` are checked before use downstream
- [ ] No `requests.get()`/`post()` without explicit `timeout` and status code verification
- [ ] For Node/TS: Promise chains or `async` calls without `.catch()` or try/catch

Do not flag: debug code, test files, or intentional no-ops with explicit inline comments.

## Conditional: Security

Load `references/security.md` from this skill when the changed code touches any of:
- user input, form data, or external API responses
- authentication, authorization, or session management logic
- database queries or resource access where object ownership matters
- file system operations (reads, writes, uploads)
- API endpoints exposed to the internet (especially auth, signup, upload, or high-cost)
- sensitive or personal data

Skip for internal utility functions, config changes, test-only changes, or documentation.

## Conditional: Plan-vs-Implementation

Use the plan provided in the task prompt and verify the implementation against it. Trigger when the prompt contains a plan and mode is `plan`. Skip silently if no plan is provided.

For each plan item:
1. **Task coverage** — every numbered Task is `done`, `partial`, or `missing`. Cite file/line. A task is `done` only when its success criterion is verifiably met.
2. **Build deviations** — for each `# decision:` annotation in the diff, evaluate whether the choice was justified by a genuine plan gap. Flag silent deviation from plan-specified values, names, or contracts. Severity: Major if it changes observable behavior; Minor if cosmetic.
3. **Plan gaps** — tasks too underspecified for faithful implementation (pseudocode referencing unverified APIs, config values without defaults, ambiguous contracts). These are plan-quality findings, not build findings.
4. **File-size and structural** — if the diff pushed any file past 800 lines, flag as Major regardless of plan mention.
5. **Plan file freshness** — if the plan header timestamp is >24h old relative to the diff, warn it may not be current.

## Conditional: Thermo-Nuclear

Load `references/thermo-nuclear.md` from this skill when the task prompt contains `--thermo`. This is an exceptionally harsh maintainability pass. Do not load automatically.

## Conditional: Simplify

Load `references/simplify.md` from this skill when the task prompt contains `--simplify`. This produces a tagged delete-list of over-engineered code. Do not load automatically.

## Reference Routing

| Signal | Reference | When |
|--------|-----------|------|
| Security surfaces in diff | `references/security.md` | auto-review detects auth, input, file, DB, or internet-exposed code |
| `--thermo` in task prompt | `references/thermo-nuclear.md` | exceptionally harsh maintainability review |
| `--simplify` in task prompt | `references/simplify.md` | tagged delete-list for over-engineering |

Each reference is loaded on demand. Do not load references proactively.

## Return Format

```md
Review Scope
- full | fix-delta

Review Range
- base: <SHA or "uncommitted"> → HEAD (<N> files changed)

Completion Status
- complete | incomplete — summary

Findings Resolution (fix-delta scope only)
- [Resolved/Unresolved/Regressed] <finding> file:line — proof

Plan Coverage
- task 1: done / missing / partial

Success Criteria Check
- criterion: met / not met — reason

Key Files Check
- path: exists + substantive | stub | missing

Key Connections Check
- consumer → provider: wired | partial | not wired

Findings
- [Critical/Major/Minor] file:line — description → fix

Security Notes (omit if not triggered)
- [Severity][Category] file:line — description → fix

Silent Failures Notes (omit if none)
- [Severity][Pattern] file:line — description → fix

Test Quality Notes (omit if test-quality skill not loaded)
- [Severity][Anti-Pattern] file:line — description → fix

Build Deviations (omit if plan-vs-impl not triggered)
- [Severity] file:line — what deviated → fix

Plan Gaps (omit if plan-vs-impl not triggered)
- task — what was underspecified → plan amendment

Review Guard Check (omit if no Review Guard provided)
- [Critical/Major/Positive] invariant/bypass/evidence — status → fix

Project Contract Check (omit if no contract marker and no Contract Context)
- [Critical/Major/Positive] checker/coverage/amendment/laundering — status → fix

Quality-Gate / Suppression Check (always present)
- [Major/Positive] file:line — suppression type → plan-approved / unapproved

Positive
- patterns worth preserving

Required Next Actions
- (empty if complete)

Plan Decision Required (omit if none)
- file:line — finding → why scope or contract is affected
```

## Iteration Guidance

If `Completion Status` is `incomplete` or `Required Next Actions` is non-empty: the calling agent should not call the work done. Hand specific next actions back for fixes and re-run review after.

If `Completion Status` is `complete` with no findings: the calling agent can proceed to docs and git finalization.

If findings exist: the calling agent fixes all safe findings (clear, single-location fixes within plan scope), re-runs validation, then re-runs review at **fix-delta** scope — carrying the prior findings, the snapshot SHA, and the fix diff. The follow-up verifies resolution of the carried findings and regressions from the fixes; it is not a full re-review. Only findings requiring architectural or scope decisions are escalated as `⚠ Plan Decision Required`.

Fix-delta loops terminate: any third or later pass also runs at fix-delta scope for unresolved carried findings only; if findings remain unresolved after that pass, stop and report — do not loop. If a fix-delta review surfaces a new Critical/Major regression or the fixes expand into a new integration boundary, the calling agent applies the full-review escalation rules (a new full review instead of looping).

Do not make code changes. Do not produce vague or purely stylistic criticism. Do not repeat findings ruff or pyright already surface.
