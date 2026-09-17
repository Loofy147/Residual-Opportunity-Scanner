"""M0 measurement model v2.

This model separates present pressure from structural value. It is a
prioritization aid, not a probability of commercial success.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignalsV2:
    current_pressure: int
    dependency: int
    demand_signal: int
    substitution_gap: int
    intervention_specificity: int
    reuse_leverage: int
    differentiation: int
    legal_friction: int
    verification_cost: int
    delivery_complexity: int

    def validate(self) -> None:
        for name, value in self.__dict__.items():
            if not 0 <= value <= 5:
                raise ValueError(f"{name} must be between 0 and 5")


def score_v2(signals: SignalsV2) -> dict[str, float]:
    """Return separate current-opportunity, structural-value, and friction scores.

    A current opportunity is explicitly gated by current_pressure. A historical
    case with zero present pressure therefore cannot receive a non-zero current
    opportunity score merely from structural interest.
    """

    signals.validate()

    need = (
        0.45 * signals.current_pressure
        + 0.35 * signals.dependency
        + 0.20 * signals.demand_signal
    ) / 5.0

    solution_fit = (
        0.30 * signals.substitution_gap
        + 0.30 * signals.intervention_specificity
        + 0.20 * signals.reuse_leverage
        + 0.20 * signals.differentiation
    ) / 5.0

    friction = (
        0.45 * signals.legal_friction
        + 0.30 * signals.verification_cost
        + 0.25 * signals.delivery_complexity
    ) / 5.0

    structural = (
        0.35 * signals.reuse_leverage
        + 0.25 * signals.differentiation
        + 0.20 * signals.substitution_gap
        + 0.20 * signals.intervention_specificity
    ) / 5.0

    current = 0.0
    if signals.current_pressure > 0:
        current = 100.0 * need * solution_fit * max(0.0, 1.0 - friction)

    return {
        "current_opportunity": round(min(100.0, max(0.0, current)), 2),
        "structural_value": round(min(100.0, max(0.0, 100.0 * structural)), 2),
        "friction": round(min(100.0, max(0.0, 100.0 * friction)), 2),
    }
