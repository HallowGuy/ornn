import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 📦 Modèle léger et rapide pour paraphraser
MODEL_NAME = "google/flan-t5-base"

# 📥 Chargement du modèle
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
except Exception as e:
    print("❌ Erreur lors du chargement du modèle Flan-T5 :", e)
    tokenizer = None
    model = None

def apply(text: str) -> str:
    """
    Applique une reformulation intelligente à l’aide d’un modèle Flan-T5 léger.
    """
    if not tokenizer or not model:
        return text  # Fallback en cas d'erreur de chargement

    prompt = f"Reformule cette phrase de manière claire et professionnelle : {text}"
    inputs = tokenizer(prompt, return_tensors="pt", max_length=256, truncation=True)

    try:
        outputs = model.generate(
            inputs["input_ids"],
            max_new_tokens=128,
            num_beams=4,
            early_stopping=True
        )
        reformulated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return reformulated
    except Exception as e:
        print("❌ Erreur de reformulation :", e)
        return text
