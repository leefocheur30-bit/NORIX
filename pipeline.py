# pipeline.py
# Orchestre l'analyse complète d'un match avec sauvegarde en base, alertes, over/under, btts, forme récente

import logging
import sqlite3
from datetime import datetime

from data.api_provider import get_fixture, get_team_statistics
from data.match_adapter import MatchAdapter
from engines.lambda_engine import LambdaEngine
from engines.poisson import PoissonEngine
from engines.elo import EloEngine
from engines.monte_carlo import MonteCarloEngine
from engines.consensus import ConsensusEngine
from engines.fusion import NoryxFusion
from engines.risk import RiskEngine
from engines.over_under import OverUnderEngine
from engines.btts import BTTSEngine
from engines.alert_engine import AlertEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NoryxPipeline:
    def __init__(self):
        logger.info("🔧 Initialisation du pipeline NORYX...")
        self.adapter = MatchAdapter()
        self.lambda_engine = LambdaEngine()
        self.poisson = PoissonEngine()
        self.elo = EloEngine()
        self.monte_carlo = MonteCarloEngine()
        self.consensus = ConsensusEngine()
        self.fusion = NoryxFusion()
        self.risk = RiskEngine()
        self.over_under = OverUnderEngine()
        self.btts = BTTSEngine()
        self.alert = AlertEngine()  # Gestion des alertes
        logger.info("✅ Pipeline prêt.")

    def analyze_fixture(self, fixture_id: int) -> dict:
        logger.info(f"📊 Récupération du match ID {fixture_id}...")
        
        try:
            # 1. Données du match
            fixture_data = get_fixture(fixture_id)
            if not fixture_data:
                raise ValueError(f"Fixture {fixture_id} non trouvé (API).")

            home_name = fixture_data['teams']['home']['name']
            away_name = fixture_data['teams']['away']['name']
            logger.info(f"🏟️  {home_name} vs {away_name}")

            home_id = fixture_data['teams']['home']['id']
            away_id = fixture_data['teams']['away']['id']
            league_id = fixture_data['league']['id']
            season = fixture_data['league']['season']

            # 2. Statistiques (fallback automatique)
            home_stats = get_team_statistics(home_id, league_id, season)
            away_stats = get_team_statistics(away_id, league_id, season)

            if home_stats is None:
                logger.warning(f"Stats manquantes pour {home_name}, valeurs par défaut.")
                home_stats = self._default_stats(home_id, league_id)
            if away_stats is None:
                logger.warning(f"Stats manquantes pour {away_name}, valeurs par défaut.")
                away_stats = self._default_stats(away_id, league_id)

            # 3. Match (avec ID pour la forme)
            match = self.adapter.to_match(fixture_data, home_stats, away_stats)
            logger.info(f"✅ Match adapté : {match.home_team} vs {match.away_team}")

            # 4. Lambda avec date actuelle
            current_date = datetime.now().strftime("%Y-%m-%d")
            lambdas = self.lambda_engine.calculate(match, current_date)
            logger.info(f"📊 Lambda : home={lambdas['home']:.2f}, away={lambdas['away']:.2f}")

            # 5. Poisson
            poisson_result = self.poisson.calculate_1x2(lambdas['home'], lambdas['away'])

            # 6. ELO
            if hasattr(match, 'home_elo') and match.home_elo is not None:
                elo_result = self.elo.to_1x2(match.home_elo, match.away_elo)
            else:
                elo_result = self.elo.to_1x2(1500, 1500)

            # 7. Monte Carlo
            mc_result = self.monte_carlo.simulate(lambdas['home'], lambdas['away'])

            # 8. Consensus
            consensus_info = self.consensus.calculate_agreement(poisson_result, elo_result)

            # 9. Fusion
            fusion_result = self.fusion.fuse(poisson_result, elo_result, mc_result)

            # 10. Risk
            risk_result = self.risk.evaluate(fusion_result, consensus_info)

            # 11. Over/Under
            over_under_result = self.over_under.calculate(lambdas['home'], lambdas['away'])

            # 12. BTTS
            btts_result = self.btts.calculate(lambdas['home'], lambdas['away'])

            # 13. Alertes
            alert_results = self.alert.check_match(
                fixture_id, fixture_data,
                fusion_result, risk_result,
                over_under_result, btts_result
            )
            for alert in alert_results:
                self.alert.save_alert(fixture_id, alert)
                logger.info(f"🔔 Alerte : {alert['message']}")

            # 14. Sauvegarde en base
            self.save_prediction(
                fixture_id, fixture_data, lambdas,
                fusion_result, risk_result,
                over_under_result, btts_result
            )

            # Retour complet (avec alertes)
            return {
                "match": match,
                "lambdas": lambdas,
                "poisson": poisson_result,
                "elo": elo_result,
                "monte_carlo": mc_result,
                "consensus": consensus_info,
                "fusion": fusion_result,
                "risk": risk_result,
                "over_under": over_under_result,
                "btts": btts_result,
                "alerts": alert_results
            }

        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse du match {fixture_id} : {e}", exc_info=True)
            raise

    def _default_stats(self, team_id, league_id):
        """Retourne des statistiques minimales pour éviter les crashs."""
        return {
            "team_id": team_id,
            "league_id": league_id,
            "season": 2024,
            "matches_played": 10,
            "wins": 4,
            "draws": 3,
            "losses": 3,
            "goals_for": 12,
            "goals_against": 11,
            "goals_for_avg": 1.2,
            "goals_against_avg": 1.1
        }

    def save_prediction(self, fixture_id, fixture_data, lambdas, fusion_result, risk_result, over_under_result, btts_result):
        """Sauvegarde toutes les prédictions dans la base SQLite."""
        try:
            conn = sqlite3.connect("noryx.db")
            cursor = conn.cursor()

            # Vérifier si le match existe déjà
            cursor.execute("SELECT id FROM predictions WHERE fixture_id = ?", (fixture_id,))
            existing = cursor.fetchone()

            if existing:
                # Mise à jour
                cursor.execute("""
                    UPDATE predictions SET
                        match_date = ?,
                        home_team = ?,
                        away_team = ?,
                        league = ?,
                        home_lambda = ?,
                        away_lambda = ?,
                        pred_home = ?,
                        pred_draw = ?,
                        pred_away = ?,
                        prediction = ?,
                        confidence = ?,
                        risk_level = ?,
                        signal = ?,
                        over_2_5 = ?,
                        under_2_5 = ?,
                        btts_yes = ?,
                        btts_no = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE fixture_id = ?
                """, (
                    fixture_data['fixture']['date'],
                    fixture_data['teams']['home']['name'],
                    fixture_data['teams']['away']['name'],
                    fixture_data['league']['name'],
                    lambdas['home'],
                    lambdas['away'],
                    fusion_result['home'],
                    fusion_result['draw'],
                    fusion_result['away'],
                    risk_result['prediction'],
                    risk_result['confidence'],
                    risk_result['risk_level'],
                    risk_result['signal'],
                    over_under_result['over_2.5'],
                    over_under_result['under_2.5'],
                    btts_result['btts_yes'],
                    btts_result['btts_no'],
                    fixture_id
                ))
            else:
                # Insertion
                cursor.execute("""
                    INSERT INTO predictions (
                        fixture_id, match_date, home_team, away_team, league,
                        home_lambda, away_lambda,
                        pred_home, pred_draw, pred_away,
                        prediction, confidence, risk_level, signal,
                        over_2_5, under_2_5, btts_yes, btts_no
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fixture_id,
                    fixture_data['fixture']['date'],
                    fixture_data['teams']['home']['name'],
                    fixture_data['teams']['away']['name'],
                    fixture_data['league']['name'],
                    lambdas['home'],
                    lambdas['away'],
                    fusion_result['home'],
                    fusion_result['draw'],
                    fusion_result['away'],
                    risk_result['prediction'],
                    risk_result['confidence'],
                    risk_result['risk_level'],
                    risk_result['signal'],
                    over_under_result['over_2.5'],
                    over_under_result['under_2.5'],
                    btts_result['btts_yes'],
                    btts_result['btts_no']
                ))

            conn.commit()
            conn.close()
            logger.info(f"💾 Prédiction sauvegardée pour le match {fixture_id}.")

        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde : {e}")