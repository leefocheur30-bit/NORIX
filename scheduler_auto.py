# scheduler_auto.py
# Planificateur automatique NORYX

import schedule
import time
import logging
from datetime import datetime
from batch_analyzer import run_batch_analysis

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def job():
    """Tâche programmée : lance l'analyse batch."""
    logger.info("🔄 Lancement de l'analyse batch programmée...")
    try:
        run_batch_analysis()
        logger.info("✅ Analyse batch terminée.")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'analyse batch : {e}")

def run_scheduler():
    """Démarre le scheduler."""
    # Planifier le job tous les jours à 8h00
    schedule.every().day.at("08:00").do(job)
    logger.info("⏰ Scheduler NORYX démarré. Prochaine exécution à 08:00.")
    
    # Option : exécuter immédiatement au démarrage (pour tester)
    # job()

    while True:
        schedule.run_pending()
        time.sleep(60)  # Vérifier toutes les minutes

if __name__ == "__main__":
    run_scheduler()