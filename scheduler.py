# automation/scheduler.py (extrait)
import schedule
import time
from update_results import update_results
from evaluate_performance import compute_metrics

def job():
    print("⏰ Exécution du job programmé...")
    update_results()
    compute_metrics()
    print("✅ Job terminé.")

# Planifier tous les jours à minuit
schedule.every().day.at("00:05").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)