# check_alerts.py
# Affiche les alertes sauvegardées

from engines.alert_engine import AlertEngine

if __name__ == "__main__":
    alert = AlertEngine()
    alert.display_alerts()