
import streamlit as st
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Ajout du chemin vers les modules et le core ORNN
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import settings

# Configuration de la page (doit être tout en haut)
st.set_page_config(
    page_title="ORNN – Plateforme Intelligente",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌈 Mise en forme CSS
st.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            background-color: #4B1D3F;
            color: white;
        }
        .sidebar .sidebar-content a {
            color: white;
        }
        .sidebar .sidebar-content a:hover {
            color: #ffdddd;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🧭 Menu principal
st.sidebar.title("🧠 ORNN – Plateforme Intelligente")
st.sidebar.markdown(f"👤 Utilisateur : `{settings.USERNAME}`")
main_menu = st.sidebar.radio("Modules disponibles :", [
    "🏠 Accueil ORNN",
    "📄 EKKO – Prétraitement",
    "🏷️ KALISTA – Thématisation",
    "🧩 AURELION – Structuration",
    "📁 HEXGATE – Contexte",
    "📝 Export",
    "⚙️ Paramètres"
])

# 🎯 Navigation dynamique
if main_menu == "🏠 Accueil ORNN":
    st.markdown("<h1 style='color: #4B1D3F;'>Bienvenue sur ORNN</h1>", unsafe_allow_html=True)
    st.write("Interface unifiée pour la gestion intelligente des documents.")
    st.write(f"Session active depuis le {datetime.now().strftime('%d/%m/%Y à %H:%M')}.")

elif main_menu == "📄 EKKO – Prétraitement":
    st.header("📄 EKKO – Nettoyage & Extraction")
    with st.expander("➡️ Lancer EKKO"):
        from modules.ekko.ekko_ui import run_ekko
        run_ekko()

elif main_menu == "🏷️ KALISTA – Thématisation":
    st.header("🏷️ KALISTA – Tagging multi-thèmes")
    with st.expander("➡️ Lancer KALISTA"):
        from modules.kalista.kalista_ui import run_kalista
        run_kalista()

elif main_menu == "🧩 AURELION – Structuration":
    st.header("🧩 AURELION – Génération structurée")
    with st.expander("➡️ Lancer AURELION"):
        from modules.aurelion.aurelion_ui import run_aurelion
        run_aurelion()

elif main_menu == "📁 HEXGATE – Contexte":
    st.header("📁 HEXGATE – Métadonnées et contexte")
    with st.expander("➡️ Lancer HEXGATE"):
        from modules.hexgate.hexgate_ui import run_hexgate
        run_hexgate()

elif main_menu == "📝 Export":
    st.header("📝 Export du livrable")
    st.info("Module d'export JSON + PDF en cours d'intégration.")

elif main_menu == "⚙️ Paramètres":
    st.header("⚙️ Paramètres de l’application")
    st.write("Email :", settings.EMAIL)
    st.write("Rôles :", settings.ROLES)
    st.write("Groupes :", settings.GROUPS)
    st.json(settings.dict())
