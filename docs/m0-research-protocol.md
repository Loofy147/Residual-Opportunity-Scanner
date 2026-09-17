# M0 Research Protocol

## Objective

Determine whether residual infrastructure can be converted into repeatable, evidence-backed opportunities with a plausible user and concrete intervention.

The experiment distinguishes three layers:

1. **Residual phenomenon** — a persistent state, identity, relationship, or capability exists.
2. **Current opportunity** — that residual condition creates present pressure/friction for a user.
3. **Commercial opportunity** — the problem has a plausible buyer/user, intervention, and defensible reason to pay or adopt.

M0 must not conflate these layers.

## Sampling frame

Target 100 cases:

- 40 deprecated APIs or public datasets
- 30 abandoned/contested package or project namespaces
- 30 historical web/infrastructure cases
- at least 15 negative/historical/control cases distributed across strata

Current corpus: 42 cases.

## Required evidence

Each case needs enough primary or high-quality secondary evidence to establish:

1. what the subject is;
2. what changed or became obsolete;
3. whether a live dependency, demand signal, or relationship remains;
4. what replacement or workaround exists;
5. what current friction remains;
6. what concrete intervention is plausible;
7. what lawful reuse/interaction path is plausible.

## Evidence discipline

A source supports only the claim it actually establishes. Separate direct observations from inferences. Ownership, authorization, licensing, and legal reusability must never be inferred from technical reachability.

For user/buyer pain, issue reports may be used as `USER_REPORTED`; they do not become established market evidence merely because they are public.

## Measurement

Use `OpportunityCase v2`.

The score separates:

- current pressure;
- dependency;
- demand signal;
- substitution gap;
- intervention specificity;
- structural reuse/differentiation;
- legal/verification/delivery friction;
- confidence.

A historical control with `current_pressure = 0` must have `current_opportunity = 0`.

## Opportunity paths

- direct reuse
- transformation
- aggregation
- inference
- automation
- migration
- monitoring
- research

## Decision labels

- `PURSUE`: evidence supports a concrete intervention worth prototyping.
- `WATCH`: signal exists but demand, ownership, substitution gap, or intervention specificity is insufficiently established.
- `RESEARCH`: the phenomenon is real and useful for learning, but the current product path is unclear.
- `KILL`: evidence fails, current need is absent, friction dominates, or no defensible intervention exists.

A high score alone must never produce `PURSUE`.

## Negative/control requirements

M0 must intentionally include negative and historical controls such as:

- historical transition with no current pressure;
- trivial replacement with low migration pain;
- residual identity with no defensible intervention;
- technically reachable but unauthorized third-party resource;
- evidence that fails to establish dependency;
- problem already solved sufficiently by the first-party replacement.

## M0 exit criteria

We do not graduate to large-scale discovery until the 100-case corpus can answer:

- verified residual-phenomenon rate;
- current-opportunity rate;
- actionable-opportunity rate;
- commercially-plausible-opportunity rate;
- negative/control separation rate;
- evidence cost per case;
- automation potential;
- strongest opportunity class;
- dominant failure modes;
- score-model false-positive patterns.
