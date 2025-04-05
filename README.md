
# 🧠 ORNN – Outil de Réécriture et de Normalisation des Narrations

ORNN est une plateforme modulaire d’analyse, transformation et structuration de documents métier en langage formel.  
Ce projet vise à industrialiser le traitement de texte intelligent avec une architecture décomposée en briques indépendantes.

---

## 🔧 Technologies utilisées

- **Python 3.11**
- **Streamlit** – Interface utilisateur rapide
- **Scikit-learn + Sentence Transformers** – Moteur d’analyse NLP
- **dotenv** – Gestion des paramètres et secrets
- **.NET Core (target)** – Cible future de déploiement
- **Intalio IAM + DMS + Case** – Interfaçage avec les modules officiels

---

## 🚀 Lancement du projet (mode prototype)

```bash
# Cloner le repo
git clone https://github.com/HallowGuy/ornn.git
cd ornn

# Activer l'environnement Python
python3 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application Streamlit
streamlit run app/main.py
```

---

## 🧩 Structure du projet

```bash
Project_ORNN_clean/
├── app/                  # Entrée principale Streamlit
├── core/                 # Composants partagés (UI, auth, API)
├── config/               # Paramètres globaux et settings
├── data/                 # Exemples d’entrée/sortie JSON
├── resources/            # Référentiels, glossaires, modèles
├── tests/                # Tests unitaires
├── .env                  # Variables utilisateur simulées
├── deploy.sh             # Script de push GitHub avec token
└── run.sh                # Lancement automatique du projet
```

---

## 📊 Diagramme d'architecture

![Architecture ORNN](https://via.placeholder.com/800x300.png?text=Diagramme+ORNN+à+intégrer)

_(Remplacer par un visuel issu de Lucidchart ou Draw.io exporté en PNG)_

---

## 👤 Auteur / Contact

**Hadi Abdallah**  
Responsable Avant-Vente France – Intalio  
📧 hadi.abdallah@intalio.com  
📱 +33 7 60 58 85 32  
[LinkedIn](https://www.linkedin.com/in/hadi-abdallah/)

---

## 📌 Statut du projet

> 🔧 En cours de prototypage (P1 – Streamlit)
>  
> 🎯 Cible Q2 2025 : migration vers .NET Core avec UI, IAM et Case Intalio intégrés

---

## ✅ Badges (à personnaliser)

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Made by](https://img.shields.io/badge/made%20by-Hadi%20Abdallah-blueviolet)

---

## 🛡️ Licence

Ce projet est distribué sous licence MIT – voir le fichier [LICENSE](LICENSE) pour plus d’informations.
