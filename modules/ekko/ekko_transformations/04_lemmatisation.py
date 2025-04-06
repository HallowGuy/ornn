import spacy
import re

# Chargement du modèle français
try:
    nlp = spacy.load("fr_core_news_sm")
except:
    import sys
    print("❌ Le modèle spaCy 'fr_core_news_sm' est manquant. Installez-le avec :")
    print("   python -m spacy download fr_core_news_sm")
    sys.exit(1)

# Expression régulière pour détecter les dates au format YYYY-MM-DD
DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")

def apply(text: str) -> str:
    """
    Lemmatisation du texte sans altérer les dates formatées.
    """
    if not text.strip():
        return text

    doc = nlp(text)
    lemmatized_tokens = []

    for token in doc:
        if DATE_PATTERN.fullmatch(token.text):
            # Préserver les dates
            lemmatized_tokens.append(token.text)
        elif token.is_alpha:
            # Appliquer la lemmatisation sur les mots
            lemmatized_tokens.append(token.lemma_)
        else:
            # Garder tel quel pour les autres tokens (ponctuation, chiffres, etc.)
            lemmatized_tokens.append(token.text)

    return " ".join(lemmatized_tokens)
