import os
import json

# Déterminer le chemin vers le fichier thesaurus_ekko.json
THESAURUS_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "data", "glossary", "thesaurus_ekko.json"
    )
)

# Chargement du thésaurus JSON (clé = mot original, valeur = équivalent recommandé)
def load_thesaurus():
    if not os.path.isfile(THESAURUS_PATH):
        raise FileNotFoundError(f"Thesaurus introuvable : {THESAURUS_PATH}")
    with open(THESAURUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

THESAURUS = load_thesaurus()

def apply(phrase: str) -> str:
    """
    Remplace les mots par leur équivalent du thésaurus, uniquement si une correspondance exacte existe.
    La phrase est supposée déjà nettoyée et lemmatisée.
    """
    tokens = phrase.split()
    new_tokens = []
    for token in tokens:
        remplacement = THESAURUS.get(token.lower())
        new_tokens.append(remplacement if remplacement else token)
    return " ".join(new_tokens)
