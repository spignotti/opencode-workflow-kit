---
name: project-contract
description: Create, validate, and maintain a compact opt-in technical contract for a project's accepted decisions and invariants. Load when setting up a project contract, or when a project AGENTS.md declares an active or draft Project Contract.
---

# Project Contract

A compact, opt-in, Git-versioned record of a project's accepted technical decisions and invariants. It is local, normative once `active`, and never activated automatically.

## When to load

- The user asks to set up, validate, or amend a project contract ("set up a project contract").
- A project-local `AGENTS.md` declares a Project Contract marker with `Status: active` or `draft`.
- A plan or review needs to verify contract compliance.

## Compact layout

```text
AGENTS.md  ## Project Contract
  ├─ Status: active | draft | opted-out | not-required
  ├─ Manifest: <path to TECHNICAL_CONTRACT.md>
  ├─ Activation reason: <manual | short reason>
  └─ Opt-out reason: <required when Status=opted-out>
TECHNICAL_CONTRACT.md        # single manifest, always read when active
```

The manifest records status, authority, accepted decisions, risk controls with required evidence, and open items. There is no module tree and no `docs/decisions/` requirement.

## Activation rules

| Signal | Status |
|---|---|
| No request, quick/standard project | `not-required` |
| Explicit "set up a project contract" | `draft` → user approval → `active` |
| User declines after offer | `opted-out` with a reason |

A contract is never silently active: it becomes `active` only after user approval of an explicit draft with no blocking open items.

## Structural validation

```bash
python3 <skill>/scripts/check_project_contract.py --root <project> [--json]
```

Exit codes:
- `0` — valid `not-required`, valid `active`, or explicit `opted-out` with reason.
- `2` — missing required active artifacts, `draft`, marker/manifest mismatch, or unsafe manifest path.

The checker proves shape and references only, never semantic validity.

## Lifecycle

- **Establish:** run the short interview (purpose, key risks, accepted decisions, required evidence), write a `draft`, present for approval, then set `active`. No external write-back.
- **Amend:** a material contract change is a plan-named, user-approved change; code follows in the same approved package.
- **Consume:** plans and reviews read the relevant sections and do not rewrite the contract.
- **Retire:** downgrading or completing a project never deletes contract history.

## Conflict protocol

Contract, code, config, and the brief disagreeing is a conflict, not a silent-winner decision. Do not rewrite the contract to match code, and do not ignore the contract for new work. Return to plan with:

```text
STOP — Project Contract Gate
Observed: <missing artifact or exact contradiction>
Boundary: <contract section and plan task>
Decision needed: <smallest planning decision>
```

## Content rules

- Record only decisions, invariants, risk controls, and required evidence.
- No project-scope prose, source-code explanations, or dependency-version lists.