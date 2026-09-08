# app.py
# Interface web NORYX avec Streamlit

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
from pipeline import NoryxPipeline
from data.api_provider import get_fixtures

# Configuration de la page
st.set_page_config(
    page_title="NORYX - Intelligence Football",
    page_icon="🧠",
    layout="wide"
)

# Titre
st.title("🧠 NORYX - Intelligence Footballistique")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Contrôle")
    if st.button("🔄 Analyser les matchs du jour"):
        with st.spinner("Analyse en cours..."):
            pipeline = NoryxPipeline()
            today = datetime.now().strftime("%Y-%m-%d")
            fixtures = get_fixtures(date=today)
            if fixtures:
                for fixture in fixtures[:5]:
                    try:
                        pipeline.analyze_fixture(fixture['fixture']['id'])
                    except Exception as e:
                        st.error(f"Erreur : {e}")
                st.success("✅ Analyse terminée !")
            else:
                st.warning("Aucun match aujourd'hui.")

    st.markdown("---")
    st.markdown("### 📊 Navigation")
    page = st.radio(
        "Choisir une vue",
        ["📈 Dashboard", "📋 Matchs récents", "📊 Performances"]
    )

# Fonction pour charger les données
def load_predictions():
    conn = sqlite3.connect("noryx.db")
    df = pd.read_sql_query("""
        SELECT 
            match_date, home_team, away_team, league,
            pred_home, pred_draw, pred_away,
            prediction, confidence, risk_level,
            over_2_5, under_2_5, btts_yes, btts_no,
            actual_result
        FROM predictions
        ORDER BY created_at DESC
        LIMIT 50
    """, conn)
    conn.close()
    return df

df = load_predictions()

# --- PAGE DASHBOARD ---
if page == "📈 Dashboard":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total analyses", len(df))
    with col2:
        if 'actual_result' in df.columns:
            correct = df[df['prediction'] == df['actual_result']].shape[0]
            accuracy = correct / len(df) if len(df) > 0 else 0
            st.metric("✅ Précision", f"{accuracy:.1%}")
        else:
            st.metric("✅ Précision", "N/A")
    with col3:
        avg_conf = df['confidence'].mean() if not df.empty else 0
        st.metric("🔒 Confiance moyenne", f"{avg_conf:.1%}")
    with col4:
        risk_counts = df['risk_level'].value_counts()
        if not risk_counts.empty:
            st.metric("⚠️ Risque élevé", risk_counts.get("ÉLEVÉ", 0))
        else:
            st.metric("⚠️ Risque élevé", 0)
    
    st.markdown("---")
    
    # Graphique des prédictions
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Distribution des prédictions")
            pred_counts = df['prediction'].map({'home': 'Domicile', 'draw': 'Nul', 'away': 'Extérieur'}).value_counts()
            fig = px.pie(values=pred_counts.values, names=pred_counts.index, title="Répartition des prédictions")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Niveau de confiance")
            fig = px.histogram(df, x='confidence', nbins=20, title="Distribution de la confiance")
            st.plotly_chart(fig, use_container_width=True)

# --- PAGE MATCHS RÉCENTS ---
elif page == "📋 Matchs récents":
    st.subheader("📋 Derniers matchs analysés")
    if not df.empty:
        # Afficher les colonnes pertinentes
        display_df = df[['match_date', 'home_team', 'away_team', 'prediction', 'confidence', 'risk_level']].copy()
        display_df['prediction'] = display_df['prediction'].map({'home': '🏠 Domicile', 'draw': '🤝 Nul', 'away': '✈️ Extérieur'})
        display_df.columns = ['Date', 'Domicile', 'Extérieur', 'Prédiction', 'Confiance', 'Risque']
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("Aucun match analysé pour le moment.")

# --- PAGE PERFORMANCES ---
elif page == "📊 Performances":
    st.subheader("📊 Performance des prédictions")
    if 'actual_result' in df.columns and not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Précision par niveau de risque
            st.write("**Précision par niveau de risque**")
            risk_accuracy = df.groupby('risk_level').apply(
                lambda x: (x['prediction'] == x['actual_result']).mean()
            ).reset_index()
            risk_accuracy.columns = ['Risque', 'Précision']
            fig = px.bar(risk_accuracy, x='Risque', y='Précision', title="Précision selon le risque")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Précision globale
            correct = df[df['prediction'] == df['actual_result']].shape[0]
            total = len(df)
            st.metric("✅ Précision globale", f"{correct/total:.1%}", f"{correct}/{total}")
            
            # Matrice de confusion simplifiée
            st.write("**Matrice de confusion**")
            confusion = pd.crosstab(df['prediction'], df['actual_result'])
            st.dataframe(confusion, use_container_width=True)
    else:
        st.info("Pas encore assez de données pour évaluer les performances.")

st.markdown("---")
st.caption("🧠 NORYX - Intelligence Footballistique | Données en temps réel")