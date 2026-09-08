from dataclasses import dataclass
from typing import Any


@dataclass
class AnalysisResult:
    """
    Résultat complet d'une analyse NORYX.
    """

    match: Any

    poisson: dict
    elo: dict
    monte_carlo: dict

    consensus: dict
    risk: dict

    best_score: str
    best_score_probability: float