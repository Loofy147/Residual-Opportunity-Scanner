# M0 State Audit — 2026-09-17

## 1. Research frontier

The project began with a broad question:

> What internet primitives have survived for 10–30 years, what residual state/identity/relationships remain, and can those remnants be reused to create present-day value?

The working hypothesis evolved into a narrower opportunity question:

> Where does residual infrastructure create current, defensible friction for a present user, and can that friction be converted into a concrete intervention?

This is a better M0 target because age alone is not value.

## 2. Initial goal vs operational equivalent

### Initial research goal

Discover and understand forgotten/obsolete digital primitives and the forms of residual value they retain.

### Current research goal

Estimate whether residual infrastructure contains a repeatable density of evidence-backed opportunities after accounting for current pressure, surviving dependency, intervention fit, friction, and lawful reuse constraints.

### Engineering equivalent

Build an evidence-first case engine that can:

`discover -> verify -> model lifecycle -> measure current pressure -> identify intervention -> score/prioritize -> reject weak cases`

The scanner itself is not yet the product. The M0 artifact is the **measurement and evidence kernel** needed to determine whether a product should exist.

## 3. Current corpus state

Current committed corpus on `feat/m0-opportunity-case`:

- `m0-corpus-001.jsonl`: 12 cases
- `m0-corpus-002.jsonl`: 5 cases
- `m0-corpus-003.jsonl`: 25 cases
- total: **42 cases**

Current strata:

- deprecated APIs / datasets: **16**
- package / project namespace cases: **16**
- historical web / infrastructure cases: **10**

M0 target remains 100 cases at 40 / 30 / 30.

Current decision labels across the 42 cases:

- `PURSUE`: 11
- `WATCH`: 26
- `RESEARCH`: 5
- `KILL`: 0

This distribution is not yet an opportunity-rate result. The zero `KILL` count is itself a sampling/control deficiency that must be corrected before interpretation.

## 4. What the corpus has actually taught us

### A. Migration pressure is the strongest recurring commercial signal

The strongest current candidates combine:

- a dated or concrete lifecycle transition;
- surviving dependency or an installed consumer base;
- a named replacement;
- non-trivial interface/schema/identity differences;
- a plausible intervention such as compatibility, migration automation, monitoring, or normalization.

### B. Namespace residue is mostly a governance/identity problem

Package-name cases repeatedly produce:

- canonical-name friction;
- install/import mismatch;
- user confusion;
- trusted-publishing ownership problems;
- supply-chain risk;
- registry governance workload.

The evidence does **not** support treating abandoned names as directly reusable assets. A safer and more general product pattern is namespace/registry intelligence.

### C. Relationship residue is promising

Registry cases show that relationships can outlive the resource or identity that created them:

- renamed GitHub accounts/organizations;
- stale registry namespaces;
- deleted resources with surviving URL references;
- 404 repositories still referenced by registries;
- endpoints that answer HTTP but no longer implement the advertised protocol;
- publication records that remain inconsistent with discoverability.

This points toward lifecycle/registry-health intelligence rather than appropriation.

### D. Legacy artifacts are useful controls even when they are not opportunities

The DSEWiki/AP Chemistry cases demonstrate persistent residual state, but they do not by themselves establish a lawful or commercial reuse path. They belong in the research corpus as architectural/archaeological controls.

### E. The current scorer is not yet a valid opportunity measure

The existing scorer averages positive structural signals and subtracts friction. This creates a failure mode:

- a historical case with **zero current migration pressure** can still receive a high opportunity score because dependency/reuse/differentiation remain high.

Example: the YouTube Analytics v1->v2 historical control was scored high despite current migration pressure being zero.

Therefore the current numeric score must not be used for M0 opportunity-rate claims.

## 5. What must change before more discovery

### 5.1 Separate current pressure from structural value

Do not collapse these into one number.

Required dimensions:

- `current_pressure`
- `dependency`
- `demand_signal`
- `substitution_gap`
- `intervention_specificity`
- `reuse_leverage`
- `differentiation`
- `legal_friction`
- `verification_cost`
- `delivery_complexity`

A historical control with `current_pressure = 0` must not obtain a non-zero **current-opportunity priority** merely because its structural value is interesting.

### 5.2 Add explicit buyer/user evidence

API deprecation documentation proves lifecycle pressure; it does not prove willingness to pay.

Every `PURSUE` case should identify:

- likely user/buyer;
- observed pain or operational consequence;
- evidence that the user population exists;
- the concrete intervention;
- why the intervention is preferable to doing nothing or using the official replacement.

Buyer willingness can remain `UNKNOWN` in M0; it must not be silently inferred.

### 5.3 Add ownership/legal gates as state, not only numeric penalty

Technical reachability must never be treated as authorization.

The case model needs explicit fields for:

- ownership status;
- authorization status;
- license status;
- lawful reuse status.

Unknown should remain unknown.

### 5.4 Increase negative/control coverage

M0 currently has zero `KILL` cases. This is inadequate for testing a discovery/scoring system.

Before final M0 interpretation, target at least **15 negative/control cases** across the three strata, including:

- no surviving dependency;
- historical-only pressure;
- trivial migration with no defensible intervention;
- legal/ownership blocker;
- evidence failure;
- already-solved problem with no substitution gap.

Controls must be intentionally sampled rather than fabricated.

### 5.5 Add corpus integrity checks

Before interpreting the dataset, the repository must automatically verify:

- unique `case_id` across all corpus files;
- schema validity;
- evidence URI validity as syntax;
- required evidence fields;
- score reproducibility;
- no impossible score/label combinations;
- expected stratum counts;
- explicit negative/control coverage.

### 5.6 Keep source provenance immutable

Each batch remains append-only. A later correction creates a new revision or replacement artifact with a documented reason; it must not silently overwrite historical evidence.

The earlier corpus overwrite incident demonstrated why this matters.

## 6. M0 target, revised

The target is still 100 cases, but completion now means more than reaching 100.

M0 exits only when all are true:

1. 40 / 30 / 30 stratified corpus is present.
2. At least 15 cases are negative/historical/control cases.
3. 100% of cases pass schema and corpus-integrity validation.
4. Every `PURSUE` case has a concrete intervention and identified user/buyer class.
5. Every `PURSUE` case has current-pressure evidence, not just age/deprecation evidence.
6. Historical controls with zero current pressure score zero for current-opportunity priority.
7. Evidence cost can be measured per case.
8. We can report verified-opportunity, actionable-opportunity, and commercially-plausible-opportunity rates separately.
9. The strongest failure modes are documented.
10. The strongest opportunity class survives a counterfactual test against existing official replacements.

## 7. What we should NOT do yet

- Do not build a large crawler.
- Do not build an autonomous agent swarm.
- Do not treat abandoned infrastructure as an acquisition pool.
- Do not claim commercial opportunity from lifecycle evidence alone.
- Do not optimize for the highest numeric score before the score model is validated.

## 8. Near-term implementation sequence

1. Introduce the v2 case/scoring model.
2. Backfill only the fields required for already-collected cases; preserve unknowns instead of inventing values.
3. Add corpus validator and score-reproduction tests.
4. Re-score all existing cases under v2.
5. Add negative/control strata.
6. Continue collection toward 100.
7. Calculate M0 rates and failure modes.
8. Select one opportunity class for a small prototype.

## 9. Success criterion beyond M0

The meaningful equivalent of the original idea is not:

> "We found many old things."

It is:

> "We can repeatedly identify a current, evidence-backed problem caused by residual infrastructure, explain the causal chain, and produce a defensible intervention with measurable value."

That is the threshold for moving from archaeology to a real opportunity scanner.

## 10. Measurement-hardening correction — 2026-09-17

The first v2 implementation contained a contract contradiction: the documentation required missing evidence to remain `UNKNOWN`, while the v2 signal schema accepted only integers `0..5`. This would have forced the 42-case migration either to invent values or to collapse UNKNOWN into zero.

This was corrected before corpus migration.

### Implemented

- v2 signals now accept `null` for UNKNOWN.
- UNKNOWN is not equivalent to zero.
- `current_pressure = 0` remains a hard invariant: `current_opportunity = 0`.
- `current_pressure = UNKNOWN` propagates to `current_opportunity = UNKNOWN`.
- Missing solution/friction inputs propagate UNKNOWN instead of producing a partial numeric score.
- `structural_value` and `friction` independently remain UNKNOWN when their own required inputs are missing.
- The v2 schema now permits nullable measurement outputs where reproducibility is impossible.
- Added strict corpus validation for schema, duplicate IDs, evidence URI syntax, score reproducibility, strata, controls, and impossible `PURSUE` states.
- Added unit tests for unknown propagation, legal/demand gates, malformed JSON, duplicate IDs, and score reproduction.
- Added GitHub Actions workflow for unit tests and canonical schema validation.

### Verification boundary

The updated measurement/validator code was executed in the analysis environment and passed **12 tests**.

The GitHub commit `1726b08bee7b9900739d6f1537104e67e53169bd` is now the head of the open PR. GitHub currently reports no workflow runs or status checks for that commit, so CI execution is not yet treated as independently verified.

### Corpus boundary

The committed 42-case corpus remains the historical v1 material. It has **not** been silently rewritten into v2 by this hardening commit. The next step is an explicit v1 -> v2 migration artifact that preserves unknowns, recomputes scores deterministically, and records the migration provenance before any M0 opportunity-rate interpretation.
