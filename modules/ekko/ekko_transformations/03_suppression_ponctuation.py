import re

def apply(text: str) -> str:
    """
    Supprime toute ponctuation et tout caractère spécial, à l'exception :
    - des lettres accentuées (français)
    - des chiffres
    - des espaces
    - des symboles % et €
    """
    # Autorise : lettres latines accentuées (unicode), chiffres, espace, %, €
    cleaned_text = re.sub(r"[^a-zA-Z0-9\u00C0-\u017F\s%€]", "", text)

    # Réduction des espaces multiples
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    return cleaned_text