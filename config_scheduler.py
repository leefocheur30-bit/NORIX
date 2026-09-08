# config_scheduler.py
# Configuration du planificateur NORYX

# Heures d'analyse (format 24h)
SCHEDULE_TIMES = ["08:00", "12:00", "18:00"]

# Ligue à analyser (None = toutes les ligues)
LEAGUE_ID = None  # Exemple: 39 pour Premier League

# Limite de matchs par analyse (None = tous)
MAX_MATCHES = None

# Activer les logs détaillés
VERBOSE_LOGS = True