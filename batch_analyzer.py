# batch_analyzer.py
# Analyse tous les matchs du jour et génère un rapport de synthèse

import logging
import sqlite3
from datetime import datetime
from data.api_provider import get_fixtures
from pipeline import NoryxPipeline
import os

# Créer le dossier reports s'il n'existe pas
os.makedirs("reports", exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_batch_analysis(limit=None):
    """
    Analyse tous les matchs du jour (ou limités) et génère un rapport.
    """
    print("\n" + "="*60)
    print("   🧠  NORYX - BATCH ANALYSIS")
    print("="*60 + "\n")

    pipeline = NoryxPipeline()
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Matchs du {today}")

    fixtures = get_fixtures(date=today)
    if not fixtures:
        print("❌ Aucun match trouvé aujourd'hui.")
        return

    # Limiter si demandé
    if limit:
        fixtures = fixtures[:limit]

    print(f"🔍 {len(fixtures)} match(s) à analyser...\n")

    report_lines = []
    report_lines.append(f"RAPPORT NORYX - {today}")
    report_lines.append("="*50)

    for idx, fixture in enumerate(fixtures, 1):
        fixture_id = fixture['fixture']['id']
        home = fixture['teams']['home']['name']
        away = fixture['teams']['away']['name']
        
        print(f"{idx}/{len(fixtures)} ⚽ {home} vs {away}")
        
        try:
            result = pipeline.analyze_fixture(fixture_id)
            risk = result['risk']
            pred_label = risk['prediction']
            pred_map = {"home": home, "draw": "Nul", "away": away}
            pred_text = pred_map.get(pred_label, pred_label)
            prob = risk['probability']
            confidence = risk['confidence']
            risk_level = risk['risk_level']
            
            line = f"{home} vs {away} : {pred_text} ({prob*100:.1f}%) | Confiance {confidence*100:.1f}% | Risque {risk_level}"
            report_lines.append(line)
            print(f"   ✅ {line}")
            
        except Exception as e:
            error_line = f"❌ {home} vs {away} : Erreur - {e}"
            report_lines.append(error_line)
            print(f"   {error_line}")

        print("-" * 40)

    # Sauvegarder le rapport
    filename = f"reports/batch_{today}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    print(f"\n✅ Rapport batch enregistré : {filename}")
    print(f"📊 {len(fixtures)} match(s) analysés.")
    
    # Afficher un résumé rapide
    print("\n📋 RÉSUMÉ RAPIDE")
    print("-" * 40)
    for line in report_lines[:10]:  # Afficher les 10 premiers
        print(line)
    if len(report_lines) > 10:
        print(f"... et {len(report_lines)-10} autres matchs.")
    print("="*60)

if __name__ == "__main__":
    run_batch_analysis()