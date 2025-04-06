# 📚 ORNN – Pipeline d'Analyse Documentaire Intelligent

ORNN est une maquette fonctionnelle d’un pipeline d’analyse documentaire modulaire, fondé exclusivement sur des technologies **open source**. Il vise à extraire, reformuler, thématiser et restructurer l'information contenue dans des documents administratifs, techniques ou contractuels, en fournissant en sortie un **livrable structuré**.

Ce projet a pour but de valider une approche orientée produit, dans une optique de publication en open source. Une version "forkée" propriétaire pourra ensuite évoluer dans un cadre commercial.

---

## 🧩 Vue d'ensemble des modules

Le pipeline ORNN est organisé en **4 modules principaux**, exécutés dans l’ordre suivant :

| Étape | Nom du module | Description |
|------:|----------------|-------------|
| 1️⃣ | **HEXGATE** | Ingestion des documents bruts (TXT) et segmentation en phrases enrichies de métadonnées. |
| 2️⃣ | **EKKO** | Prétraitement linguistique et sémantique : nettoyage, reformulation, normalisation, enrichissement. |
| 3️⃣ | **KALISTA** | Application de tags thématiques selon 3 méthodes : mots-clés, règles métier, modèle ML. |
| 4️⃣ | **AURELION** | Regroupement des phrases, reformulation finale et génération d’un livrable HTML structuré. |

---

## 🛠️ Technologies et bibliothèques

- **NLP / IA :**
  - `spaCy` (segmentation, lemmatisation, détection de mots inconnus)
  - `sentence-transformers` (vectorisation sémantique)
  - `scikit-learn` (modèles ML)
  - `nlpaug` (paraphrasing)
  - `transformers` (paraphrasing LLM pour la version avancée)

- **Web et UI :**
  - `streamlit` pour l'interface utilisateur
  - `jinja2` pour les templates HTML du livrable

- **Outillage & persistance :**
  - `joblib` pour la persistance des modèles
  - `json` pour tous les formats d’échange

---

## 🚀 Lancer l'application

### 1. Création de l’environnement

```bash
cd Project_ORNN_clean
python3 -m venv .venv
source .venv/bin/activate


2. Installation des dépendances

pip install -r requirements.txt
python -m spacy download fr_core_news_sm


3. Lancer l'application Streamlit
streamlit run app/main.py


⚙️ Fonctionnalités par module
🧊 HEXGATE
Nettoyage du texte brut

Segmentation en phrases

Détection des dates

Identification des mots inconnus

🌀 EKKO
Prétraitement structural et grammatical

Application d’un thésaurus

Paraphrasing (simple + avancé)

Préparation des phrases pour le tagging

🏷️ KALISTA
Matching sur mots-clés avec themes_collectivites.json

Tagging via règles métier (rules_thematiques_kalista.json)

Classification ML via un modèle de logreg entraîné avec sentence-transformers

🧩 AURELION
Sélection de la meilleure reformulation

Regroupement des phrases par thème

Réécriture finale

Génération d’un livrable HTML stylisé via jinja2


-----------------

📌 Bonnes pratiques
Séparer les modules : chaque transformation est isolée, testable, réutilisable.

Garder la logique d’enchaînement claire (HEXGATE > EKKO > KALISTA > AURELION)

Utiliser un thésaurus et des règles métiers comme garde-fous avant tout ML.

Utiliser les modules comme briques de construction (framework modulaire).



-------------------
📜 Licence & publication
Ce projet est à publier sous licence open source permissive (MIT ou Apache 2.0).
Une version produit dérivée pourra être construite par fork, avec interface renforcée et intégration back-end.

-------------------
Conçu par : Hadi ABDALLAH 
