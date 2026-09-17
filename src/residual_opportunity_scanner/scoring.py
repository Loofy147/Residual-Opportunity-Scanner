"""Deterministic M0 opportunity scoring.

The scorer is intentionally simple and inspectable. It ranks candidates; it does
not establish truth, ownership, legality, or commercial demand.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Signals:
    dependency: int
    migration_pressure: int
    substitution_gap: int
    reuse_leverage: int
    differentiation: int = 0
    legal_friction: int = 0
    verification_cost: int = 0

    def validate(self) -> None:
        for name, value in self.__dict__.items():
            if not 0 <= value <= 5:
                raise ValueError(f"{name} must be between 0 and 5")


def opportunity_score(signals: Signals) -> float:
    """Return a 0..100 prioritization score.

    Positive signals receive equal weight for M0. Friction is a bounded
    penalty. The result is deliberately not a probabilistic claim.
    """

    signals.validate()
    positive = (
        signals.dependency
        + signals.migration_pressure
        + signals.substitution_gap
        + signals.reuse_leverage
        + signals.differentiation
    ) / 25.0
    penalty = (signals.legal_friction + signals.verification_cost) / 10.0
    return round(max(0.0, min(100.0, (positive - penalty) * 100.0)), 2)
