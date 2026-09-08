# report_generator.py
# Génération de rapports PDF pour les analyses NORYX

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NoryxPDFReport:
    def __init__(self, db_path="noryx.db"):
        self.db_path = db_path
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)

    def _setup_custom_styles(self):
        """Crée des styles personnalisés avec des noms uniques."""
        # Utiliser des noms préfixés pour éviter les conflits
        self.styles.add(ParagraphStyle(
            name='NoryxTitle',
            parent=self.styles['Title'],
            fontSize=20,
            alignment=TA_CENTER,
            spaceAfter=24,
            textColor=colors.HexColor('#1a237e')
        ))
        self.styles.add(ParagraphStyle(
            name='NoryxSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.HexColor('#283593')
        ))
        self.styles.add(ParagraphStyle(
            name='NoryxSectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            textColor=colors.HexColor('#0d47a1')
        ))
        self.styles.add(ParagraphStyle(
            name='NoryxHighlight',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#e65100'),
            alignment=TA_LEFT
        ))

    def generate_report(self, fixture_id: int, output_filename: str = None):
        """Génère un rapport PDF pour un match donné."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Récupérer les données du match
        cursor.execute("""
            SELECT 
                match_date, home_team, away_team, league,
                home_lambda, away_lambda,
                pred_home, pred_draw, pred_away,
                prediction, confidence, risk_level, signal,
                over_2_5, under_2_5, btts_yes, btts_no
            FROM predictions
            WHERE fixture_id = ?
        """, (fixture_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            logger.error(f"Match {fixture_id} introuvable dans la base.")
            return None

        # Extraire les données
        (match_date, home_team, away_team, league,
         home_lambda, away_lambda,
         pred_home, pred_draw, pred_away,
         prediction, confidence, risk_level, signal,
         over_2_5, under_2_5, btts_yes, btts_no) = row

        # Nom du fichier
        if output_filename is None:
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_home = home_team.replace(" ", "_")
            safe_away = away_team.replace(" ", "_")
            output_filename = f"{self.reports_dir}/NORYX_{safe_home}_vs_{safe_away}_{date_str}.pdf"

        # Créer le PDF
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            topMargin=2*cm,
            bottomMargin=2*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        story = []

        # --- TITRE ---
        story.append(Paragraph(f"🧠 NORYX - RAPPORT D'ANALYSE", self.styles['NoryxTitle']))
        story.append(Paragraph(f"{home_team} VS {away_team}", self.styles['NoryxSubtitle']))
        story.append(Spacer(1, 0.5*cm))

        # --- INFOS MATCH ---
        story.append(Paragraph(f"📅 Date : {match_date}", self.styles['Normal']))
        story.append(Paragraph(f"🏆 Compétition : {league}", self.styles['Normal']))
        story.append(Spacer(1, 0.5*cm))

        # --- STATISTIQUES ---
        story.append(Paragraph("📊 STATISTIQUES", self.styles['NoryxSectionHeader']))
        data = [
            ["", "Domicile", "Extérieur"],
            ["λ (moy. buts)", f"{home_lambda:.2f}", f"{away_lambda:.2f}"],
        ]
        t = Table(data, colWidths=[4*cm, 3*cm, 3*cm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3f2fd')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.5*cm))

        # --- 1X2 ---
        story.append(Paragraph("🎯 PRÉDICTION 1X2", self.styles['NoryxSectionHeader']))
        pred_map = {"home": home_team, "draw": "Nul", "away": away_team}
        prediction_name = pred_map.get(prediction, prediction)
        story.append(Paragraph(f"✅ Prédiction : <b>{prediction_name}</b>", self.styles['NoryxHighlight']))
        story.append(Paragraph(f"📊 Probabilité : {confidence*100:.1f}%", self.styles['Normal']))
        story.append(Paragraph(f"⚠️  Risque : {risk_level} (Signal {signal})", self.styles['Normal']))
        story.append(Spacer(1, 0.2*cm))

        # Tableau des probabilités 1X2
        data2 = [
            ["", home_team, "Nul", away_team],
            ["Probabilité", f"{pred_home*100:.1f}%", f"{pred_draw*100:.1f}%", f"{pred_away*100:.1f}%"]
        ]
        t2 = Table(data2, colWidths=[3*cm, 3*cm, 2*cm, 3*cm])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f5e9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(t2)
        story.append(Spacer(1, 0.5*cm))

        # --- OVER/UNDER ---
        story.append(Paragraph("⚽ OVER/UNDER", self.styles['NoryxSectionHeader']))
        data3 = [
            ["", "Oui", "Non"],
            ["Over 2.5", f"{over_2_5*100:.1f}%", f"{under_2_5*100:.1f}%"]
        ]
        t3 = Table(data3, colWidths=[3*cm, 3*cm, 3*cm])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fff3e0')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(t3)
        story.append(Spacer(1, 0.5*cm))

        # --- BTTS ---
        story.append(Paragraph("🤝 BTTS (Both Teams To Score)", self.styles['NoryxSectionHeader']))
        data4 = [
            ["Oui", "Non"],
            [f"{btts_yes*100:.1f}%", f"{btts_no*100:.1f}%"]
        ]
        t4 = Table(data4, colWidths=[3*cm, 3*cm])
        t4.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8eaf6')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        story.append(t4)
        story.append(Spacer(1, 0.5*cm))

        # --- MÉTHODOLOGIE ---
        story.append(Paragraph("📐 MÉTHODOLOGIE", self.styles['NoryxSectionHeader']))
        story.append(Paragraph(
            "L'analyse combine les moteurs suivants :",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "• Poisson : distribution des buts",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "• ELO : force relative des équipes",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "• Monte Carlo : simulation du match",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "• Forme récente : 5 derniers matchs",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "• Consensus : accord entre les modèles",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 0.5*cm))

        # --- PIED DE PAGE ---
        story.append(Paragraph(
            f"Rapport généré par NORYX AI le {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
            self.styles['Normal']
        ))
        story.append(Paragraph(
            "🔬 NORYX — Intelligence Footballistique",
            self.styles['Normal']
        ))

        # Générer le PDF
        doc.build(story)
        logger.info(f"✅ Rapport PDF généré : {output_filename}")
        return output_filename

    def generate_report_from_last(self):
        """Génère un rapport pour le dernier match analysé."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT fixture_id FROM predictions ORDER BY created_at DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return self.generate_report(row[0])
        else:
            logger.error("Aucun match trouvé.")
            return None

    def generate_batch_reports(self, limit=5):
        """Génère des rapports pour les derniers matchs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT fixture_id FROM predictions ORDER BY created_at DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        files = []
        for (fixture_id,) in rows:
            filename = self.generate_report(fixture_id)
            if filename:
                files.append(filename)
        return files


if __name__ == "__main__":
    # Test : générer un rapport
    generator = NoryxPDFReport()
    generator.generate_report_from_last()