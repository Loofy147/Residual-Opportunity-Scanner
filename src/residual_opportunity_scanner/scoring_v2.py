"""M0 measurement model v2.

Signals may be unknown (``None``). Unknown is preserved as unknown rather than
being silently converted to zero. Scores that cannot be computed reproducibly
are returned as ``None``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

Score: Final = float | None


@dataclass(frozen=True)
class SignalsV2:
    current_pressure: int | None
    dependency: int | None
    demand_signal: int | None
    substitution_gap: int | None
    intervention_specificity: int | None
    reuse_leverage: int | None
    differentiation: int | None
    legal_friction: int | None
    verification_cost: int | None
    delivery_complexity: int | None

    def validate(self) -> None:
        for name, value in self.__dict__.items():
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an integer between 0 and 5 or null")
            if not 0 <= value <= 5:
                raise ValueError(f"{name} must be between 0 and 5")


def _weighted(values: tuple[int | None, ...], weights: tuple[float, ...]) -> float | None:
    if any(value is None for value in values):
        return None
    return sum(value * weight for value, weight in zip(values, weights, strict=True))


def _normalize(value: float | None) -> float | None:
    if value is None:
        return None
    return value / 5.0


def _bounded(value: float | None) -> float | None:
    if value is None:
        return None
    return round(min(100.0, max(0.0, value)), 2)


def score_v2(signals: SignalsV2) -> dict[str, Score]:
    """Return reproducible v2 measurement components.

    ``current_opportunity`` is:
    - exactly 0 when current pressure is explicitly 0;
    - unknown when current pressure or another required input is unknown;
    - otherwise the normalized need × solution-fit × (1 - friction) score.

    ``structural_value`` and ``friction`` remain independently computable when
    their own required inputs are known.
    """

    signals.validate()

    need_raw = _weighted(
        (signals.current_pressure, signals.dependency, signals.demand_signal),
        (0.45, 0.35, 0.20),
    )
    solution_raw = _weighted(
        (
            signals.substitution_gap,
            signals.intervention_specificity,
            signals.reuse_leverage,
            signals.differentiation,
        ),
        (0.30, 0.30, 0.20, 0.20),
    )
    friction_raw = _weighted(
        (signals.legal_friction, signals.verification_cost, signals.delivery_complexity),
        (0.45, 0.30, 0.25),
    )
    structural_raw = _weighted(
        (
            signals.reuse_leverage,
            signals.differentiation,
            signals.substitution_gap,
            signals.intervention_specificity,
        ),
        (0.35, 0.25, 0.20, 0.20),
    )

    friction_normalized = _normalize(friction_raw)
    friction = None if friction_normalized is None else _bounded(100.0 * friction_normalized)

    if signals.current_pressure == 0:
        current = 0.0
    elif signals.current_pressure is None:
        current = None
    elif need_raw is None or solution_raw is None or friction_raw is None:
        current = None
    else:
        need = _normalize(need_raw)
        solution_fit = _normalize(solution_raw)
        friction_ratio = _normalize(friction_raw)
        assert need is not None
        assert solution_fit is not None
        assert friction_ratio is not None
        current = _bounded(100.0 * need * solution_fit * max(0.0, 1.0 - friction_ratio))

    structural_normalized = _normalize(structural_raw)
    structural = None if structural_normalized is None else _bounded(100.0 * structural_normalized)

    return {
        "current_opportunity": current,
        "structural_value": structural,
        "friction": friction,
    }
