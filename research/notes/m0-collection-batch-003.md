# M0 Collection Batch 003

Date: 2026-09-17

## Scope

Added 25 new cases in `research/cases/m0-corpus-003.jsonl`:

- 10 deprecated API / migration cases
- 7 package namespace / registry-governance cases
- 8 residual web / infrastructure cases

## Selection method

The batch follows the lessons from prior batches:

1. Prefer first-party or registry-maintained documentation for lifecycle claims.
2. Use public issue reports as USER_REPORTED evidence when the claim concerns observed downstream pain, owner access, or ecosystem behavior not independently established by the registry.
3. Keep historical control cases when useful; do not treat age alone as opportunity.
4. Include negative/control cases deliberately so the corpus is not pre-filtered for positive outcomes.
5. Do not infer ownership, authorization, or legal reuse from reachability.
6. Treat aggregate measurements as experimental evidence with stated sampling limitations.
7. Score as a prioritization signal only; score does not prove demand or willingness to pay.

## New recurring patterns

### Migration pressure

The strongest API cases combine a dated sunset, a named replacement, and concrete interface differences. Examples include Google Maps client IDs, Google Merchant API v1beta, Microsoft Graph retirements, and GitHub REST changes.

### Namespace residue

The package-registry cases repeatedly show that stale identity can create:

- canonical-name friction;
- user-install confusion;
- inability to configure trusted publishing;
- supply-chain risk;
- governance workload.

The recurring product path is more often monitoring/governance than direct reuse.

### Relationship residue

The MCP registry cases show measurable state surviving after the underlying relationship changes:

- orphaned GitHub namespaces after account/org renames;
- stale remote URLs after deletion;
- repository references returning 404;
- endpoints that answer HTTP but no longer implement the advertised protocol;
- successful publications remaining invisible to direct lookup/search.

These are candidates for registry-health and lifecycle intelligence rather than appropriation of third-party resources.

## Current experimental interpretation

`PURSUE` signals are clustering around **migration tooling** and **infrastructure/registry health** rather than abandoned-asset acquisition.

This remains a hypothesis until the M0 sample is complete and the rates are calculated across all strata.
