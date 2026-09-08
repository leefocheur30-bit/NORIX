# engines/consensus.py
# Moteur de consensus : indique l'accord entre Poisson et ELO

class ConsensusEngine:
    def __init__(self):
        self.name = "Consensus"

    def calculate_agreement(self, poisson_result: dict, elo_result: dict) -> dict:
        """
        Retourne :
          - agreement : True/False
          - score : 1.0 si accord, 0.0 si désaccord
        """
        # On trouve le favori (la clé avec la plus grande probabilité)
        poisson_fav = max(poisson_result, key=poisson_result.get)
        elo_fav = max(elo_result, key=elo_result.get)

        agreement = (poisson_fav == elo_fav)

        return {
            "agreement": agreement,
            "poisson_favorite": poisson_fav,
            "elo_favorite": elo_fav,
            "score": 1.0 if agreement else 0.0
        }