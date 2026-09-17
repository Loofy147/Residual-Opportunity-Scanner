# Residual Opportunity Scanner

Evidence-first discovery of reusable value in residual, obsolete, deprecated, or historically persistent digital infrastructure.

## Current objective

M0 is not a general internet crawler. It tests whether a small, auditable corpus can reveal repeatable, evidence-backed opportunities created by surviving residual state, identity, relationships, or dependencies.

The original research question was:

> What internet primitives have survived long enough to become overlooked, and what value remains when they are recomposed for present use?

The operational equivalent is narrower:

> Where does residual infrastructure create current, defensible friction for a present user, and can that friction be converted into a concrete intervention?

We currently investigate three classes:

1. **Migration archaeology** — deprecated APIs/datasets with surviving consumers and replacement gaps.
2. **Namespace archaeology** — abandoned or contested package/project identities with current demand or governance friction.
3. **Residual graph** — historical web/infrastructure relationships whose surviving references create actionable information.

## Core principle

> The opportunity is usually not the obsolete object itself. It is the current friction created by its surviving state, identity, relationships, or dependencies.

## M0 experiment

Target corpus: 100 cases.

- 40 deprecated APIs/datasets
- 30 package/project namespaces
- 30 historical web/infrastructure cases
- at least 15 negative/historical control cases across the strata

Current corpus snapshot: **42 cases** committed in three batches (16 APIs/datasets, 16 namespace cases, 10 web/infrastructure cases).

Every case must be evidence-backed and scored through the same schema. A high score is a prioritization signal only; it is not a claim of demand, ownership, legality, or commercial success.

## Measurement model

`OpportunityCase v2` separates:

- current pressure;
- dependency;
- demand signal;
- substitution gap;
- intervention specificity;
- structural reuse/differentiation;
- legal/verification/delivery friction;
- confidence.

Historical controls with zero current pressure must receive zero current-opportunity priority even when structurally interesting.

See `docs/m0-state-audit-2026-09-17.md` and `docs/m0-measurement-model-v2.md`.

## Evidence status

Use: `ESTABLISHED`, `EXPERIMENTALLY_SUPPORTED`, `USER_REPORTED`, `INFERENCE`, `HYPOTHESIS`, `CONTRADICTED`, `UNKNOWN`, `OPEN`.

## Planned pipeline

```text
Discovery -> Verification -> Enrichment -> Current-pressure assessment -> Scoring -> Manual audit -> Decision
```

Raw observations, claims, evidence, scores, and decisions remain distinct objects.

## Non-goals for M0

- No opportunistic takeover or exploitation of third-party infrastructure.
- No large crawler before the measurement model is validated.
- No autonomous agent swarm.
- No claim that an identified resource is legally reusable without explicit evidence.
- No commercial conclusion from lifecycle/deprecation evidence alone.

## Repository layout

```text
schema/        canonical case schemas
src/           deterministic scoring/domain logic
tests/         unit tests
fixtures/      small synthetic examples
research/      evidence, corpus, and experiment notes
docs/          protocol and design decisions
```
