"""Residual Opportunity Scanner domain package."""

from .scoring import Signals, opportunity_score
from .scoring_v2 import SignalsV2, score_v2

__all__ = ["Signals", "opportunity_score", "SignalsV2", "score_v2"]
