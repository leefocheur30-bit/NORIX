# bot.py
from pipeline import NoryxPipeline
from data.api_provider import get_fixtures
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("\n" + "="*60)
    print("   🧠  NORYX - INTELLIGENCE FOOTBALL  🧠")
    print("="*60 + "\n")

    try:
        pipeline = NoryxPipeline()
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"📅 Matchs du {today}")

        fixtures = get_fixtures(date=today)
        if not fixtures:
            print("❌ Aucun match trouvé pour aujourd'hui.")
            return

        print(f"🔍 {len(fixtures)} match(s) trouvés. Analyse du premier uniquement.\n")

        fixture = fixtures[0]
        fixture_id = fixture['fixture']['id']
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']

        print(f"⚽ {home_team} vs {away_team}")
        print("-" * 60)

        # Analyse
        report = pipeline.analyze_fixture(fixture_id)

        # 1. 1X2
        risk = report['risk']
        pred_map = {"home": home_team, "draw": "Nul", "away": away_team}
        prediction_name = pred_map.get(risk['prediction'], risk['prediction'])

        print(f"\n🎯 PRÉDICTION 1X2")
        print(f"   Résultat : {prediction_name}")
        print(f"   Probabilité : {risk['probability']*100:.1f}%")
        print(f"   Confiance : {risk['confidence']*100:.1f}%")
        print(f"   Risque : {risk['risk_level']} (Signal {risk['signal']})")

        fusion = report['fusion']
        print(f"   Détails : Domicile {fusion['home']*100:.1f}% | Nul {fusion['draw']*100:.1f}% | Extérieur {fusion['away']*100:.1f}%")

        # 2. Over/Under
        over_under = report['over_under']
        print(f"\n⚽ OVER/UNDER")
        print(f"   Over 0.5 : {over_under['over_0.5']*100:.1f}% | Under 0.5 : {over_under['under_0.5']*100:.1f}%")
        print(f"   Over 1.5 : {over_under['over_1.5']*100:.1f}% | Under 1.5 : {over_under['under_1.5']*100:.1f}%")
        print(f"   Over 2.5 : {over_under['over_2.5']*100:.1f}% | Under 2.5 : {over_under['under_2.5']*100:.1f}%")
        print(f"   Over 3.5 : {over_under['over_3.5']*100:.1f}% | Under 3.5 : {over_under['under_3.5']*100:.1f}%")

        # 3. BTTS
        btts = report['btts']
        print(f"\n🤝 BTTS")
        print(f"   Oui : {btts['btts_yes']*100:.1f}% | Non : {btts['btts_no']*100:.1f}%")

        # 4. Alertes (AJOUT)
        if report.get('alerts'):
            print(f"\n🔔 ALERTES DÉTECTÉES")
            for alert in report['alerts']:
                print(f"   {alert['message']}")

        # 5. Lambdas
        lambdas = report['lambdas']
        print(f"\n📊 MOYENNES DE BUTS")
        print(f"   Domicile : {lambdas['home']:.2f} | Extérieur : {lambdas['away']:.2f}")

        # Génération du PDF (optionnelle)
        print("\n" + "="*60)
        print("   📄 GÉNÉRATION DU RAPPORT PDF")
        print("="*60)
        try:
            from report_generator import NoryxPDFReport
            generator = NoryxPDFReport()
            pdf_file = generator.generate_report(fixture_id)
            if pdf_file:
                print(f"✅ Rapport PDF : {pdf_file}")
            else:
                print("❌ Échec de la génération du PDF.")
        except ImportError:
            print("⚠️  Module report_generator non trouvé (reportlab installé ?).")
        except Exception as e:
            print(f"❌ Erreur PDF : {e}")

        print("\n" + "="*60)
        print("✅ Analyse terminée.")
        print("="*60)

    except Exception as e:
        logger.error(f"❌ Erreur fatale : {e}", exc_info=True)
        print(f"\n❌ Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()