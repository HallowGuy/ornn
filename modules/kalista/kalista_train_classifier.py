import json
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# 🔁 Chemin vers le fichier d'entraînement
TRAINING_FILE = "data/training/kalista_training_sample.json"
MODEL_OUTPUT = "modules/kalista/model/kalista_logreg_model.pkl"

# 📦 Chargement des données
def load_training_data(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    phrases = [entry["phrase"] for entry in data]
    labels = [entry["theme"] for entry in data]
    return phrases, labels

# 🧠 Encodage avec BERT multilingue
def encode_phrases(phrases, model_name='distiluse-base-multilingual-cased-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(phrases, show_progress_bar=True)
    return embeddings

# 🏗️ Entraînement du classifieur
def train_classifier(X, y):
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X, y)
    return clf

# 📊 Évaluation du modèle
def evaluate_model(clf, X_test, y_test):
    y_pred = clf.predict(X_test)
    print("\n📈 Rapport de classification :")
    print(classification_report(y_test, y_pred))

# ▶️ Point d’entrée
if __name__ == "__main__":
    print("📥 Chargement des données...")
    phrases, labels = load_training_data(TRAINING_FILE)

    print("🔤 Encodage des phrases avec BERT...")
    embeddings = encode_phrases(phrases)

    print("🔀 Séparation des données...")
    X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.2, random_state=42)

    print("🎓 Entraînement du modèle...")
    clf = train_classifier(X_train, y_train)

    print("📊 Évaluation...")
    evaluate_model(clf, X_test, y_test)

    print(f"💾 Sauvegarde du modèle : {MODEL_OUTPUT}")
    joblib.dump(clf, MODEL_OUTPUT)
    print("✅ Modèle sauvegardé avec succès.")
