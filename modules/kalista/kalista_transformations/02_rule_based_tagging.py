import os
import json

# 🔍 Définir le chemin absolu vers le fichier JSON de règles
RULES_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "data", "glossary", "rules_thematiques_kalista.json")
)

# 📥 Chargement des règles depuis le fichier JSON
def load_rules():
    try:
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors du chargement des règles : {e}")
        return []

# Initialisation des règles globales
RULES = load_rules()

# ⚙️ Fonction principale d'application des règles
def apply(text: str):
    matched_tags = []

    for rule in RULES:
        mot_cle = rule.get("mot_cle", "").strip().lower()
        theme = rule.get("theme", "").strip()

        if mot_cle and theme and mot_cle in text.lower():
            matched_tags.append(theme)

    return matched_tags
