from residual_opportunity_scanner.scoring import Signals, opportunity_score


def test_score_is_bounded():
    assert 0 <= opportunity_score(Signals(0, 0, 0, 0)) <= 100
    assert opportunity_score(Signals(5, 5, 5, 5, 5)) == 100


def test_friction_reduces_score():
    base = opportunity_score(Signals(4, 4, 4, 4, 4, 0, 0))
    penalized = opportunity_score(Signals(4, 4, 4, 4, 4, 5, 5))
    assert penalized < base


def test_invalid_signal_rejected():
    try:
        opportunity_score(Signals(6, 0, 0, 0))
    except ValueError:
        return
    raise AssertionError("out-of-range signal was accepted")
