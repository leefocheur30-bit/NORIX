# engines/risk.py
# Évaluation du risque et de la confiance

class RiskEngine:
    def __init__(self):
        self.name = "Risk"

    def evaluate(self, fusion_result: dict, agreement_info: dict) -> dict:
        """
        Calcule le niveau de risque.
        fusion_result : dict home/draw/away
        agreement_info : dict retourné par ConsensusEngine
        """
        # 1. Prédiction (le résultat avec le plus de chances)
        prediction = max(fusion_result, key=fusion_result.get)
        probability = fusion_result[prediction]

        # 2. Marge (différence entre 1er et 2ème)
        sorted_probs = sorted(fusion_result.values(), reverse=True)
        margin = sorted_probs[0] - sorted_probs[1] if len(sorted_probs) > 1 else 0.0

        # 3. Accord (1.0 ou 0.0)
        agreement_score = agreement_info.get("score", 0.0)

        # 4. Calcul de la confiance globale (entre 0 et 1)
        # 60% la probabilité, 20% la marge, 20% l'accord
        confidence = (0.60 * probability) + (0.20 * margin) + (0.20 * agreement_score)
        confidence = min(1.0, max(0.0, confidence))

        # 5. Niveaux
        if confidence >= 0.70:
            risk_level = "FAIBLE"
            signal = "FORT"
        elif confidence >= 0.50:
            risk_level = "MODÉRÉ"
            signal = "MOYEN"
        else:
            risk_level = "ÉLEVÉ"
            signal = "FAIBLE"

        return {
            "prediction": prediction,          # "home", "draw" ou "away"
            "probability": probability,        # probabilité de cette prédiction
            "margin": margin,                  # écart entre 1er et 2nd
            "agreement_score": agreement_score,# 1 ou 0
            "confidence": confidence,          # score de confiance global
            "risk_level": risk_level,          # FAIBLE / MODÉRÉ / ÉLEVÉ
            "signal": signal                   # FORT / MOYEN / FAIBLE
        }