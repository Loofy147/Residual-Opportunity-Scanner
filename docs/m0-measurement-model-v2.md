# M0 Measurement Model v2

## Why v2 exists

M0 learned that a single opportunity score conflated two different things:

1. **Structural value** — how reusable, differentiating, or leverage-rich a residual asset/pattern might be.
2. **Current opportunity** — whether there is present pressure and a concrete intervention worth pursuing now.

Historical controls demonstrated that structural value can remain high after current pressure disappears. The model therefore keeps these quantities separate.

## Signals

All signals use a 0–5 ordinal scale and require evidence or an explicit `UNKNOWN`/low score.

### Need / present pressure

- `current_pressure`: current lifecycle/operational pressure caused by the residual state.
- `dependency`: observed dependence on the subject by existing software/users/registry relationships.
- `demand_signal`: direct or strong public evidence that someone currently wants the problem solved.

### Solution fit

- `substitution_gap`: how incomplete, costly, or incompatible the available replacement is.
- `intervention_specificity`: how clearly a concrete intervention can be defined.
- `reuse_leverage`: how much existing state/capability reduces implementation cost.
- `differentiation`: how difficult the intervention would be to commoditize or replace immediately.

### Friction

- `legal_friction`: ownership/authorization/license barrier.
- `verification_cost`: cost of proving the relevant facts.
- `delivery_complexity`: implementation/operations burden of the intervention.

## Derived scores

### Current opportunity

```text
need =
  0.45 * current_pressure
+ 0.35 * dependency
+ 0.20 * demand_signal

solution_fit =
  0.30 * substitution_gap
+ 0.30 * intervention_specificity
+ 0.20 * reuse_leverage
+ 0.20 * differentiation

friction =
  0.45 * legal_friction
+ 0.30 * verification_cost
+ 0.25 * delivery_complexity

current_opportunity =
  need * solution_fit * (1 - friction)
```

Values are normalized to 0–100.

Hard rule:

```text
current_pressure == 0 -> current_opportunity == 0
```

This prevents historical controls from looking commercially current merely because they are structurally interesting.

### Structural value

Structural value is reported separately from current opportunity. It measures reuse leverage, differentiation, substitution gap, and intervention specificity. It does not imply present demand.

### Confidence

Confidence remains a separate evidence judgment. It is never silently multiplied into opportunity score.

## Decision discipline

The score ranks investigation priority. It does not create a commercial conclusion.

A `PURSUE` case still requires:

- a named target user/buyer class;
- a concrete pain statement;
- a concrete intervention;
- current-pressure evidence;
- demand evidence or a clearly marked `UNKNOWN` state;
- explicit ownership/authorization/license assessment.

## Controls

M0 must include historical and negative controls. At least 15% of the final 100-case corpus should be controls, distributed across the three strata where practical.

Examples:

- historical transition with no current pressure;
- deprecation with trivial replacement;
- stale namespace with no defensible intervention;
- technical reachability but no authorization;
- evidence that fails to establish the claimed dependency;
- problem already solved by the first-party replacement.

## Interpretation rule

The scanner is successful only if it can distinguish these classes reliably:

```text
interesting residual state
        !=
current opportunity
        !=
commercial opportunity
```
