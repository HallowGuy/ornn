#!/bin/bash

echo "🧼 Nettoyage & préparation Git..."

# Créer le fichier .gitignore si non existant
if [ ! -f .gitignore ]; then
    echo "📄 Création de .gitignore..."
    curl -s https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore -o .gitignore
fi

# Ajout ciblé
echo "➕ Ajout des fichiers utiles..."
git add app/ modules/ config/ data/ resources/ run.sh README.md requirements.txt .gitignore

# Commit
echo "✅ Commit..."
git commit -m '🔁 Commit automatique – clean & push'

# Push
echo "🚀 Envoi vers GitHub..."
git push origin main

echo "🎉 Fait !"
