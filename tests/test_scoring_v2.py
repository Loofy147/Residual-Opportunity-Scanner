from residual_opportunity_scanner.scoring_v2 import SignalsV2, score_v2


def base_signals() -> SignalsV2:
    return SignalsV2(
        current_pressure=4,
        dependency=4,
        demand_signal=3,
        substitution_gap=3,
        intervention_specificity=3,
        reuse_leverage=4,
        differentiation=3,
        legal_friction=0,
        verification_cost=1,
        delivery_complexity=1,
    )


def test_zero_current_pressure_is_hard_zero_even_with_unknown_other_signals():
    signals = SignalsV2(
        current_pressure=0,
        dependency=None,
        demand_signal=None,
        substitution_gap=3,
        intervention_specificity=3,
        reuse_leverage=4,
        differentiation=3,
        legal_friction=0,
        verification_cost=1,
        delivery_complexity=1,
    )
    scores = score_v2(signals)
    assert scores["current_opportunity"] == 0.0
    assert scores["structural_value"] == 67.0


def test_unknown_current_pressure_propagates_to_current_opportunity():
    signals = SignalsV2(
        current_pressure=None,
        dependency=4,
        demand_signal=3,
        substitution_gap=3,
        intervention_specificity=3,
        reuse_leverage=4,
        differentiation=3,
        legal_friction=0,
        verification_cost=1,
        delivery_complexity=1,
    )
    scores = score_v2(signals)
    assert scores["current_opportunity"] is None
    assert scores["structural_value"] == 67.0


def test_missing_solution_or_friction_input_prevents_current_score():
    solution_unknown = SignalsV2(
        current_pressure=4,
        dependency=4,
        demand_signal=3,
        substitution_gap=None,
        intervention_specificity=3,
        reuse_leverage=4,
        differentiation=3,
        legal_friction=0,
        verification_cost=1,
        delivery_complexity=1,
    )
    friction_unknown = SignalsV2(
        current_pressure=4,
        dependency=4,
        demand_signal=3,
        substitution_gap=3,
        intervention_specificity=3,
        reuse_leverage=4,
        differentiation=3,
        legal_friction=None,
        verification_cost=1,
        delivery_complexity=1,
    )
    assert score_v2(solution_unknown)["current_opportunity"] is None
    assert score_v2(friction_unknown)["current_opportunity"] is None


def test_historical_control_has_zero_current_opportunity():
    scores = score_v2(
        SignalsV2(
            current_pressure=0,
            dependency=4,
            demand_signal=3,
            substitution_gap=3,
            intervention_specificity=3,
            reuse_leverage=4,
            differentiation=3,
            legal_friction=0,
            verification_cost=1,
            delivery_complexity=1,
        )
    )
    assert scores["current_opportunity"] == 0.0
    assert scores["structural_value"] > 0.0


def test_more_current_pressure_increases_current_opportunity():
    low = score_v2(
        SignalsV2(
            current_pressure=1,
            dependency=4,
            demand_signal=3,
            substitution_gap=3,
            intervention_specificity=3,
            reuse_leverage=4,
            differentiation=3,
            legal_friction=0,
            verification_cost=1,
            delivery_complexity=1,
        )
    )
    high = score_v2(base_signals())
    assert high["current_opportunity"] > low["current_opportunity"]


def test_friction_reduces_current_opportunity_but_not_structural_value():
    low_friction = score_v2(base_signals())
    high_friction = score_v2(
        SignalsV2(
            current_pressure=4,
            dependency=4,
            demand_signal=3,
            substitution_gap=3,
            intervention_specificity=3,
            reuse_leverage=4,
            differentiation=3,
            legal_friction=5,
            verification_cost=5,
            delivery_complexity=5,
        )
    )
    assert high_friction["current_opportunity"] < low_friction["current_opportunity"]
    assert high_friction["structural_value"] == low_friction["structural_value"]


def test_invalid_signal_is_rejected():
    invalid = SignalsV2(
        current_pressure=6,
        dependency=0,
        demand_signal=0,
        substitution_gap=0,
        intervention_specificity=0,
        reuse_leverage=0,
        differentiation=0,
        legal_friction=0,
        verification_cost=0,
        delivery_complexity=0,
    )
    try:
        score_v2(invalid)
    except ValueError:
        return
    raise AssertionError("out-of-range signal was accepted")
