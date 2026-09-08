# engines/telegram_alert.py
# Envoi d'alertes Telegram

import requests
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramAlert:
    def __init__(self):
        # Récupérer les infos depuis .env ou config
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.token and self.chat_id)

    def send_message(self, message: str):
        """Envoie un message Telegram."""
        if not self.enabled:
            logger.warning("Telegram non configuré. Message ignoré.")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info("📱 Message Telegram envoyé.")
            else:
                logger.error(f"Erreur Telegram : {response.text}")
        except Exception as e:
            logger.error(f"Erreur d'envoi Telegram : {e}")

    def send_alert(self, home_team: str, away_team: str, alert_type: str, message: str, confidence: float):
        """Formate et envoie une alerte spécifique."""
        emojis = {
            "SURE_BET": "🔒",
            "OVER": "⚽",
            "BTTS": "🤝",
            "TIGHT": "⚖️",
            "UNCERTAINTY": "⚠️"
        }
        emoji = emojis.get(alert_type, "📢")
        
        full_message = f"""
{emoji} <b>ALERTE NORYX</b>

🏟️ <b>{home_team} vs {away_team}</b>

📌 {message}

📊 Confiance : {confidence*100:.1f}%
🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """
        self.send_message(full_message.strip())