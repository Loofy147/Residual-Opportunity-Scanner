# Residual Opportunity Scanner

Evidence-first discovery of reusable value in residual, obsolete, deprecated, or historically persistent digital infrastructure.

## Current objective

M0 is not a general internet crawler. It tests whether a small, auditable corpus can reveal commercially actionable residual opportunities.

We currently investigate three classes:

1. **Migration archaeology** — deprecated APIs/datasets with surviving consumers and replacement gaps.
2. **Namespace archaeology** — abandoned or contested package/project identities with current demand.
3. **Residual graph** — historical web/infrastructure relationships whose surviving references create actionable information.

## Core principle

> The opportunity is usually not the obsolete object itself. It is the current friction created by its surviving state, identity, relationships, or dependencies.

## M0 experiment

Target corpus: 100 cases.

- 40 deprecated APIs/datasets
- 30 package/project namespaces
- 30 historical web/infrastructure cases

Every case must be evidence-backed and scored through the same schema. A high score is not a claim of value; it is a prioritization signal for manual verification.

## Evidence status

Use: `ESTABLISHED`, `EXPERIMENTALLY_SUPPORTED`, `USER_REPORTED`, `INFERENCE`, `HYPOTHESIS`, `CONTRADICTED`, `UNKNOWN`, `OPEN`.

## Planned pipeline

```text
Discovery -> Verification -> Enrichment -> Scoring -> Manual audit -> Decision
```

Raw observations, claims, evidence, scores, and decisions remain distinct objects.

## Non-goals for M0

- No opportunistic takeover or exploitation of third-party infrastructure.
- No large crawler before the scoring model is validated.
- No autonomous agent swarm.
- No claim that an identified resource is legally reusable without explicit evidence.

## Repository layout

```text
schema/        canonical case schema
src/           deterministic scoring/domain logic
tests/         unit tests
fixtures/      small synthetic examples
research/      evidence and experiment notes
docs/          protocol and design decisions
```
