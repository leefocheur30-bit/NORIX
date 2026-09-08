# engines/fusion.py
# Fusion finale des 3 moteurs principaux avec poids dynamiques

import json
import os

class NoryxFusion:
    def __init__(self, use_optimized_weights=True):
        self.name = "Fusion"
        self.use_optimized_weights = use_optimized_weights
        self.weights = self._load_weights()

    def _load_weights(self) -> dict:
        """Charge les poids (optimisés ou par défaut)."""
        default_weights = {
            "poisson": 0.40,
            "elo": 0.30,
            "monte_carlo": 0.30
        }
        
        if not self.use_optimized_weights:
            return default_weights
        
        # Essayer de charger les poids optimisés
        try:
            if os.path.exists("optimized_weights.json"):
                with open("optimized_weights.json", "r") as f:
                    weights = json.load(f)
                    # Vérifier que toutes les clés sont présentes
                    if all(k in weights for k in default_weights):
                        print(f"📊 Utilisation des poids optimisés : {weights}")
                        return weights
        except Exception as e:
            print(f"⚠️ Erreur lors du chargement des poids optimisés : {e}")
        
        return default_weights

    def fuse(self, poisson: dict, elo: dict, monte_carlo: dict) -> dict:
        """
        Combine les 3 modèles en 1 résultat 1X2.
        """
        result = {"home": 0.0, "draw": 0.0, "away": 0.0}
        
        for key in result.keys():
            result[key] = (
                self.weights["poisson"] * poisson.get(key, 0.0) +
                self.weights["elo"] * elo.get(key, 0.0) +
                self.weights["monte_carlo"] * monte_carlo.get(key, 0.0)
            )

        # Normalisation
        total = sum(result.values())
        if total > 0:
            for key in result:
                result[key] = result[key] / total
        
        return result