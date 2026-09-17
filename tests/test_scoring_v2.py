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


def test_historical_control_has_zero_current_opportunity():
    signals = base_signals()
    historical = SignalsV2(
        current_pressure=0,
        dependency=signals.dependency,
        demand_signal=signals.demand_signal,
        substitution_gap=signals.substitution_gap,
        intervention_specificity=signals.intervention_specificity,
        reuse_leverage=signals.reuse_leverage,
        differentiation=signals.differentiation,
        legal_friction=signals.legal_friction,
        verification_cost=signals.verification_cost,
        delivery_complexity=signals.delivery_complexity,
    )
    scores = score_v2(historical)
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
