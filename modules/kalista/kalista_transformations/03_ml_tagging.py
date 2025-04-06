import os
import json
import joblib
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

# 🔍 Localisation du répertoire courant (où se trouve ce fichier)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔄 Nouveau chemin vers les fichiers déplacés
MODEL_PATH = os.path.join(CURRENT_DIR, "models", "kalista_logreg_model.pkl")
LABELS_PATH = os.path.join(CURRENT_DIR, "models", "kalista_labels.json")

# 📥 Chargement du modèle
model = joblib.load(MODEL_PATH)

# 📥 Chargement des étiquettes
with open(LABELS_PATH, "r", encoding="utf-8") as f:
    LABELS = json.load(f)

# ⚙️ Encodeur BERT
encoder = SentenceTransformer("distiluse-base-multilingual-cased-v2")

def apply(phrase: str) -> List[Dict[str, object]]:
    """
    Utilise un modèle ML pour taguer une phrase et retourne les tags avec leur probabilité.
    """
    try:
        embedding = encoder.encode([phrase])
        probs = model.predict_proba(embedding)[0]

        tags_with_scores = [
            {"tag": LABELS[i], "score": float(round(score, 4))}
            for i, score in enumerate(probs) if score > 0.2
        ]

        if not tags_with_scores:
            tags_with_scores.append({"tag": "à supprimer", "score": 1.0})

        return sorted(tags_with_scores, key=lambda x: -x["score"])

    except Exception as e:
        return [{"tag": "erreur_ml", "score": 1.0, "debug": str(e)}]
