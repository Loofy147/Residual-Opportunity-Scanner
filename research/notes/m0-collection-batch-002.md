# M0 collection batch 002

Date: 2026-09-17

## Scope

Added 9 verified deprecation/API lifecycle cases to the M0 corpus:

- Cloudflare Zone Settings Batch API
- Cloudflare Account Roles API
- Cloudflare Workers KV legacy namespace routes
- Cloudflare legacy Registrar domain management API
- Google Ad Manager SOAP API v202511
- Google Ads API v22
- DV360 SDF API v9
- Atlassian Cloud Admin v1 Users/Groups APIs
- SAP IBP Security Audit Log Services API

The corpus also restores the 10 cases that existed before the accidental replacement of the corpus file and retains the 2 Google Maps cases added in batch 001.

## Evidence policy

Official vendor/developer documentation is treated as primary evidence for deprecation dates, replacement endpoints, and lifecycle conditions. Consumer demand and willingness to pay are not inferred from deprecation alone.

## Current observation

The new API cases strengthen the existence of **migration pressure** as an observable phenomenon. They do not yet establish buyer willingness to pay or sufficient consumer density for a product in each case.

Several cases are especially useful because the migration burden differs:

- Cloudflare Workers KV: mostly mechanical path migration.
- Cloudflare Account Roles: identifier/schema remapping.
- Cloudflare Zone Settings Batch: change from batching to per-setting operations.
- Cloudflare Registrar: broader resource/API surface replacement.
- Google versioned APIs: recurring lifecycle pressure with published schedules.

This variation is important for validating whether migration pain, rather than deprecation age alone, predicts opportunity.

## Correction note

An earlier commit accidentally replaced the original 10-case corpus when adding the first Google cases. The corpus was reconstructed from commit `f5987e22268e3c11741174903173709d1dc69a93` and then extended. No case was intentionally discarded.

## Next sampling requirement

Do not keep adding API cases indefinitely. Next batches should increase:

1. package/project namespace cases;
2. historical web/infrastructure relationship cases;
3. negative controls where deprecation/abandonment exists but no credible intervention is apparent.
