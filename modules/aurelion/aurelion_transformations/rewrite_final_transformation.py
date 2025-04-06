from transformers import pipeline
import re

# Paraphraseur local via HuggingFace pipeline (modèle français ou multilingue)
try:
    paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")
except Exception:
    paraphraser = None  # fallback

def rewrite(text: str) -> str:
    try:
        if not text or len(text.strip()) < 5:
            return "[Texte trop court]"

        # Fallback : transformation simple si modèle indisponible
        if paraphraser is None:
            return f"[Règle simple appliquée] {text}"

        # Nettoyage initial
        cleaned_text = re.sub(r"\s+", " ", text).strip()

        # Appel du paraphraseur
        response = paraphraser(f"paraphrase: {cleaned_text}", max_length=256, do_sample=False)
        new_text = response[0]["generated_text"]

        # Mise au propre
        if not new_text.endswith("."):
            new_text += "."

        return new_text[0].upper() + new_text[1:]

    except Exception as e:
        return f"[Erreur NLP] {text} – {e}"
