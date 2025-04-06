import os
import json
import streamlit as st
from typing import List, Dict
from jinja2 import Template
import ast

from modules.aurelion.aurelion_transformations.rewrite_final_transformation import rewrite

def regrouper_par_phrase(data: List[Dict]) -> Dict[int, List[Dict]]:
    regroupement = {}
    for item in data:
        num = item.get("NbPhrase")
        if num not in regroupement:
            regroupement[num] = []
        regroupement[num].append(item)
    return regroupement

def choisir_meilleure_transformation(versions: List[Dict]) -> Dict:
    for version in sorted(versions, key=lambda v: v.get("Transformation", ""), reverse=True):
        if "à supprimer" not in version.get("Tags_02_rule_based_tagging", "").lower():
            return version
    return versions[-1]

def classer_par_section(tags_ml: str, tag_themes: Dict[str, int]) -> str:
    tags_all = tags_ml.lower() + " " + " ".join(tag_themes.keys()).lower()
    if "objectif" in tags_all:
        return "Objectifs"
    elif "introduction" in tags_all:
        return "Introduction"
    else:
        return "Thèmes"

def charger_template() -> Template:
    CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    template_path = os.path.join(CURRENT_DIR, "data", "templates", "aurelion_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return Template(f.read())

def run_aurelion():
    st.subheader("🧩 AURELION – Génération structurée")

    uploaded_file = st.file_uploader("📤 Importer un fichier JSON depuis KALISTA", type=["json"])
    debug_mode = st.checkbox("🪵 Activer les logs détaillés")

    if uploaded_file:
        try:
            raw_data = json.load(uploaded_file)
            st.success("✅ Données chargées.")

            regroupes = regrouper_par_phrase(raw_data)
            template = charger_template()

            sections = {
                "Introduction": [],
                "Objectifs": [],
                "Thèmes": {}
            }

            for num, versions in regroupes.items():
                meilleure = choisir_meilleure_transformation(versions)
                texte_source = meilleure.get("Texte", "")
                texte_reformule = rewrite(texte_source)

                try:
                    tags_theme = ast.literal_eval(meilleure.get("Tags_01_match_themes", "{}"))
                except Exception:
                    tags_theme = {"Thème inconnu": 1}

                tags_ml = meilleure.get("Tags_03_ml_tagging", "")
                section = classer_par_section(tags_ml, tags_theme)

                if section in ["Introduction", "Objectifs"]:
                    sections[section].append(texte_reformule)
                else:
                    for theme in tags_theme.keys():
                        if theme not in sections["Thèmes"]:
                            sections["Thèmes"][theme] = []
                        sections["Thèmes"][theme].append(texte_reformule)

                if debug_mode:
                    st.markdown(f"### 🔎 Phrase {num}")
                    st.markdown(f"- **Transformation retenue :** {meilleure.get('Transformation')}")
                    st.markdown(f"- **Texte brut :** {texte_source}")
                    st.markdown(f"- **Texte reformulé :** {texte_reformule}")
                    st.markdown(f"- **Tags ML :** `{tags_ml}`")
                    st.markdown(f"- **Thèmes :** `{tags_theme}`")
                    st.markdown("---")

            html_final = template.render(
                titre_document="Livrable Structuré – AURELION",
                client="Client inconnu",
                date="Date inconnue",
                introduction=sections["Introduction"],
                objectif=sections["Objectifs"],
                themes=sections["Thèmes"]
            )

            st.markdown("### 🧾 Aperçu du livrable final")
            st.components.v1.html(html_final, height=800, scrolling=True)

            st.download_button(
                label="📥 Télécharger le livrable HTML",
                data=html_final,
                file_name="livrable_aurelion.html",
                mime="text/html"
            )

        except Exception as e:
            st.error(f"❌ Erreur lors du traitement : {e}")
