import os
import json
import joblib
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

# 📁 Mise à jour du chemin relatif basé sur la position actuelle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Ce dossier = kalista_transformations
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))  # Racine du projet

# 📍 Chemins vers les fichiers dans data/
MODEL_PATH = os.path.join(ROOT_DIR, "data", "models", "kalista_logreg_model.pkl")
LABELS_PATH = os.path.join(ROOT_DIR, "data", "models", "kalista_labels.json")

# 🧠 Chargement du modèle ML
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle ML : {e}")

# 🏷️ Chargement des étiquettes
try:
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        LABELS = json.load(f)
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement des labels ML : {e}")

# ⚙️ Initialisation de l'encodeur (doit correspondre à l'entraînement)
encoder = SentenceTransformer("distiluse-base-multilingual-cased-v2")

# 📌 Fonction d'application
def apply(phrase: str) -> List[Dict[str, object]]:
    """
    Utilise un modèle ML pour taguer une phrase.
    Retourne une liste de tags avec un score associé.
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