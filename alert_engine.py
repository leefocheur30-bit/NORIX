# engines/alert_engine.py
# Système d'alertes automatiques NORYX

import logging
import sqlite3
from datetime import datetime, timedelta
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertEngine:
    def __init__(self, db_path="noryx.db"):
        self.db_path = db_path
        self.alerts_file = "alerts.json"
        self._load_alerts()

    def _load_alerts(self):
        """Charge les alertes précédentes pour éviter les doublons."""
        if os.path.exists(self.alerts_file):
            with open(self.alerts_file, 'r') as f:
                try:
                    self.previous_alerts = json.load(f)
                except:
                    self.previous_alerts = {}
        else:
            self.previous_alerts = {}

    def _save_alerts(self):
        """Sauvegarde les alertes envoyées."""
        with open(self.alerts_file, 'w') as f:
            json.dump(self.previous_alerts, f)

    def check_match(self, fixture_id: int, fixture_data: dict, fusion_result: dict, risk_result: dict, over_under: dict, btts: dict) -> list:
        """
        Vérifie si un match déclenche des alertes.
        Retourne une liste d'alertes.
        """
        alerts = []
        alert_key = f"{fixture_id}"

        # Vérifier si déjà alerté
        if alert_key in self.previous_alerts:
            already_sent = self.previous_alerts[alert_key]
            # Si l'alerte a déjà été envoyée récemment (24h), on ne renvoie pas
            last_sent = datetime.fromisoformat(already_sent)
            if (datetime.now() - last_sent).total_seconds() < 86400:
                return alerts

        home_team = fixture_data['teams']['home']['name']
        away_team = fixture_data['teams']['away']['name']

        # --- SEUILS D'ALERTE ---

        # 1. Confiance élevée (> 75%) ET risque faible
        if risk_result['confidence'] >= 0.75 and risk_result['risk_level'] == 'FAIBLE':
            alerts.append({
                "type": "SURE_BET",
                "message": f"🔒 {home_team} vs {away_team} : Confiance {risk_result['confidence']*100:.1f}% - Risque FAIBLE",
                "priority": 1,
                "prediction": risk_result['prediction'],
                "confidence": risk_result['confidence']
            })

        # 2. Over 2.5 > 60%
        if over_under.get('over_2.5', 0) >= 0.60:
            alerts.append({
                "type": "OVER",
                "message": f"⚽ {home_team} vs {away_team} : Over 2.5 à {over_under['over_2.5']*100:.1f}%",
                "priority": 2,
                "prediction": "over_2.5",
                "confidence": over_under['over_2.5']
            })

        # 3. BTTS Oui > 60%
        if btts.get('btts_yes', 0) >= 0.60:
            alerts.append({
                "type": "BTTS",
                "message": f"🤝 {home_team} vs {away_team} : BTTS Oui à {btts['btts_yes']*100:.1f}%",
                "priority": 3,
                "prediction": "btts_yes",
                "confidence": btts['btts_yes']
            })

        # 4. Désaccord des modèles ET confiance moyenne
        if risk_result['confidence'] < 0.50 and risk_result['signal'] == 'FAIBLE':
            alerts.append({
                "type": "UNCERTAINTY",
                "message": f"⚠️ {home_team} vs {away_team} : Désaccord des modèles - À éviter",
                "priority": 5,
                "prediction": None,
                "confidence": risk_result['confidence']
            })

        # 5. Bonus : match très serré
        fusion = fusion_result
        margin = max(fusion.values()) - min(fusion.values())
        if margin < 0.10 and risk_result['confidence'] >= 0.50:
            alerts.append({
                "type": "TIGHT",
                "message": f"⚖️ {home_team} vs {away_team} : Match très équilibré (marge {margin*100:.1f}%) - Nul possible",
                "priority": 4,
                "prediction": "draw",
                "confidence": risk_result['confidence']
            })

        # Marquer comme alerté
        self.previous_alerts[alert_key] = datetime.now().isoformat()
        self._save_alerts()

        return alerts

    def get_alerts(self, limit=10, min_priority=3):
        """Récupère les dernières alertes de la base."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Créer la table des alertes si elle n'existe pas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fixture_id INTEGER,
                alert_type TEXT,
                message TEXT,
                priority INTEGER,
                prediction TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        cursor.execute("""
            SELECT alert_type, message, prediction, confidence, created_at
            FROM alerts
            WHERE priority <= ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (min_priority, limit))
        rows = cursor.fetchall()
        conn.close()

        return rows

    def save_alert(self, fixture_id, alert):
        """Sauvegarde une alerte en base."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alerts (fixture_id, alert_type, message, priority, prediction, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            fixture_id,
            alert['type'],
            alert['message'],
            alert['priority'],
            alert.get('prediction', ''),
            alert.get('confidence', 0.0)
        ))
        conn.commit()
        conn.close()

    def display_alerts(self, limit=10):
        """Affiche les alertes en console."""
        alerts = self.get_alerts(limit=limit)
        if not alerts:
            print("\n🔔 Aucune alerte pour le moment.")
            return

        print("\n" + "="*60)
        print("   🔔  ALERTES NORYX")
        print("="*60)
        for alert_type, message, prediction, confidence, created_at in alerts:
            print(f"📌 {message}")
            print(f"   Type: {alert_type} | Confiance: {confidence*100:.1f}% | {created_at}")
            print("-"*50)
        print("="*60)


if __name__ == "__main__":
    # Test
    alert = AlertEngine()
    alert.display_alerts()