def apply(text: str) -> str:
    # Supprimer les lignes vides ou ne contenant que des espaces/tabulations
    if not text.strip():
        return ""

    # Analyser le premier mot
    words = text.strip().split()
    if not words:
        return ""

    first_word = words[0]
    
    # Si le premier mot commence par une majuscule mais n'est pas tout en majuscules
    if first_word[0].isupper() and not first_word.isupper():
        # Transformer uniquement la première lettre du premier mot en minuscule
        first_word_corrected = first_word[0].lower() + first_word[1:]
        words[0] = first_word_corrected
        return " ".join(words)

    return text.strip()
