
import streamlit as st

# 1️⃣ Configuration de la page
st.set_page_config(
    page_title="ORNN – Interface d’accueil",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2️⃣ Imports standards Python
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 3️⃣ Charger .env
load_dotenv()

# 4️⃣ Ajouter le chemin pour accéder à config/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 5️⃣ Importer les paramètres de configuration
from config.settings import settings

# 🎨 Personnalisation du style
st.markdown(
    """
    <style>
        body {
            background-color: #ffffff;
            color: #000000;
        }
        .main {
            background-color: #ffffff;
        }
        .sidebar .sidebar-content {
            background-color: #4B1D3F;
            color: white;
        }
        .sidebar .sidebar-content a {
            color: #ffffff;
        }
        .sidebar .sidebar-content a:hover {
            color: #ffdddd;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🧭 Menu latéral
st.sidebar.title("🧭 Navigation")
st.sidebar.markdown(f"👤 Utilisateur : `{settings.USERNAME}`")

# Ajout de fonctionnalités supplémentaires
if st.sidebar.button("♻️ Réinitialiser la session"):
    st.cache_data.clear()
    st.rerun()

debug_mode = st.sidebar.checkbox("🛠️ Mode développeur", value=settings.DEBUG)

menu = st.sidebar.radio("Choisir une page :", [
    "🏠 Accueil",
    "📝 Importer un document",
    "🔍 Analyser",
    "📤 Exporter",
    "⚙️ Paramètres"
])

# 🖥️ En-tête principal
st.markdown("<h1 style='color: #4B1D3F;'>Bienvenue sur ORNN</h1>", unsafe_allow_html=True)
st.write("Ce module est le point d’entrée pour vos traitements intelligents de texte.")

# 🔁 Navigation principale
if menu == "🏠 Accueil":
    st.subheader("Page d’accueil")
    st.write(f"Session ouverte le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    st.write("Utilisez le menu à gauche pour importer, analyser ou exporter un document.")
    if debug_mode:
        st.info("✅ Mode développeur activé")

elif menu == "📝 Importer un document":
    st.subheader("Importation")
    uploaded_file = st.file_uploader("Importer un fichier texte ou JSON", type=["txt", "json"])
    if uploaded_file:
        st.success("Fichier importé avec succès.")
        st.text(uploaded_file.read().decode("utf-8")[:500])

elif menu == "🔍 Analyser":
    st.subheader("Analyse (placeholder)")
    st.info("Cette section sera prochainement alimentée par votre moteur de traitement.")
    if debug_mode:
        st.code("Fonctionnalité à développer...")

elif menu == "📤 Exporter":
    st.subheader("Export (placeholder)")
    st.warning("Module d’export non encore implémenté.")

elif menu == "⚙️ Paramètres":
    st.subheader("Configuration")
    st.write("Ici, vous pourrez définir les options globales du module ORNN.")
    if debug_mode:
        st.json({
            "username": settings.USERNAME,
            "email": settings.EMAIL,
            "roles": settings.ROLES,
            "groups": settings.GROUPS,
            "input_path": settings.INPUT_PATH,
            "output_path": settings.OUTPUT_PATH
        })
