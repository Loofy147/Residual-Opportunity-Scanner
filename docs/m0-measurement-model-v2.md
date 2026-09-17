# M0 Measurement Model v2

## Why v2 exists

M0 learned that a single opportunity score conflated two different things:

1. **Structural value** — how reusable, differentiating, or leverage-rich a residual asset/pattern might be.
2. **Current opportunity** — whether there is present pressure and a concrete intervention worth pursuing now.

Historical controls demonstrated that structural value can remain high after current pressure disappears. The model therefore keeps these quantities separate.

## Signals

All signals use a 0–5 ordinal scale. `null` means **UNKNOWN** and must be preserved when the evidence does not establish a defensible value. Unknown is not equivalent to zero.

- `current_pressure`: current lifecycle/operational pressure caused by the residual state.
- `dependency`: observed dependence on the subject by existing software/users/registry relationships.
- `demand_signal`: direct or strong public evidence that someone currently wants the problem solved.
- `substitution_gap`: how incomplete, costly, or incompatible the available replacement is.
- `intervention_specificity`: how clearly a concrete intervention can be defined.
- `reuse_leverage`: how much existing state/capability reduces implementation cost.
- `differentiation`: how difficult the intervention would be to commoditize or replace immediately.
- `legal_friction`: ownership/authorization/license barrier.
- `verification_cost`: cost of proving the relevant facts.
- `delivery_complexity`: implementation/operations burden of the intervention.

## Unknown propagation

A migration must not invent missing signal values.

Therefore:

```text
current_pressure = 0
    -> current_opportunity = 0

current_pressure = UNKNOWN
    -> current_opportunity = UNKNOWN

current_pressure > 0
+ any required need/solution/friction input UNKNOWN
    -> current_opportunity = UNKNOWN
```

Structural value and friction remain independently calculable when their own inputs are known.

## Derived scores

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

Structural value is reported separately from current opportunity:

```text
structural_value =
  0.35 * reuse_leverage
+ 0.25 * differentiation
+ 0.20 * substitution_gap
+ 0.20 * intervention_specificity
```

Confidence remains a separate evidence judgment. It is never silently multiplied into opportunity score.

## Decision discipline

The score ranks investigation priority. It does not create a commercial conclusion.

`PURSUE` additionally requires:

- a named target user/buyer class;
- a concrete pain statement;
- a concrete intervention;
- established current-pressure evidence;
- a positive demand signal backed by buyer/pain evidence;
- known ownership state;
- acceptable authorization/license/lawful-reuse state.

A high score alone never creates `PURSUE`.

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

The scanner is successful only if it can distinguish:

```text
interesting residual state
        !=
current opportunity
        !=
commercial opportunity
```
