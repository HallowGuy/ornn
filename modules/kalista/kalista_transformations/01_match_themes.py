import json
import os
import re
from typing import List, Dict

# Définir le chemin vers le fichier de thèmes
THEMES_PATH = os.path.join("data", "glossary", "themes_collectivites.json")

# Charger les thèmes avec leurs mots-clés
with open(THEMES_PATH, "r", encoding="utf-8") as f:
    THEMES_DICT: Dict[str, List[str]] = json.load(f)

def clean_text(text: str) -> str:
    """Nettoie le texte pour un matching plus cohérent."""
    text = text.lower()
    text = re.sub(r"[^\w\s%€]", "", text)
    return text

def apply(phrase: str) -> Dict[str, float]:
    """
    Tag une phrase selon les mots-clés présents dans le dictionnaire de thèmes.
    Retourne un dictionnaire de tags avec un score simple basé sur le nombre de mots-clés retrouvés.
    """
    cleaned = clean_text(phrase)
    tags_scores = {}

    for theme, keywords in THEMES_DICT.items():
        score = sum(1 for kw in keywords if kw.lower() in cleaned)
        if score > 0:
            tags_scores[theme] = score

    # Si aucun mot-clé ne correspond, on propose un tag "À supprimer"
    if not tags_scores:
        tags_scores["À supprimer"] = 1

    return tags_scores
