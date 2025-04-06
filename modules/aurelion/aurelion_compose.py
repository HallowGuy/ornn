import json
from typing import List, Dict


def select_best_transformation(phrase_data: Dict) -> Dict:
    """
    Sélectionne la meilleure transformation parmi Transfo 6 à Transfo 1,
    en s'appuyant sur une stratégie simple : priorité à la transformation la plus affinée,
    sauf si un tag 'à supprimer' est détecté.

    Retourne :
        - La phrase retenue
        - Le numéro de transformation retenu
    """
    for i in range(6, 0, -1):  # De Transfo 6 à 1
        transfo_key = f"Transfo {i}"
        if transfo_key in phrase_data:
            # Si la phrase est marquée à supprimer, on l'écarte
            all_tags = phrase_data.get("tags", []) + phrase_data.get("tags_regles", []) + phrase_data.get("tags_ml", [])
            all_tag_labels = [t["tag"] if isinstance(t, dict) else t for t in all_tags]
            if "à supprimer" not in all_tag_labels:
                return {
                    "text": phrase_data[transfo_key],
                    "source_transfo": transfo_key,
                    "tags": all_tag_labels
                }
    return {
        "text": phrase_data.get("Phrase originale", ""),
        "source_transfo": "Phrase originale",
        "tags": []
    }


def generate_structured_output(phrases: List[Dict]) -> Dict:
    """
    Produit une structure de document basée sur les tags :
    - Introduction
    - Objectif
    - Thèmes (groupe par tag)
    """
    final = {
        "introduction": [],
        "objectif": [],
        "themes": {}
    }

    for phrase in phrases:
        best = select_best_transformation(phrase)
        tags = best["tags"]

        if not tags:
            final["introduction"].append(best["text"])
        elif any(tag in ["objectif", "but", "enjeu"] for tag in tags):
            final["objectif"].append(best["text"])
        else:
            for tag in tags:
                if tag not in final["themes"]:
                    final["themes"][tag] = []
                final["themes"][tag].append(best["text"])

    return final
