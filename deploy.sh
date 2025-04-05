#!/bin/bash

# --- CONFIGURATION ---
GITHUB_USER="HallowGuy"
GITHUB_REPO="ornn"
BRANCH="main"

# ⚠️ Token stocké dans variable d'environnement pour éviter de l'exposer en clair
if [ -z "$GITHUB_PAT" ]; then
  echo "❌ Le token GitHub n'est pas défini. Exécute : export GITHUB_PAT=ton_token"
  exit 1
fi

# --- COMMIT & PUSH ---
echo "📦 Commit & push vers GitHub ($GITHUB_REPO)..."

git add .
git commit -m "📤 Déploiement automatique via deploy.sh"
git push https://$GITHUB_USER:$GITHUB_PAT@github.com/$GITHUB_USER/$GITHUB_REPO.git $BRANCH

echo "✅ Déploiement terminé."
