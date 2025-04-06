import nlpaug.augmenter.sentence as nas

# Utilise un modèle de paraphrase léger compatible avec les environnements contraints
try:
    aug = nas.T5SentenceAug(model_path='ramsrigouthamg/t5_paraphraser', device='cpu')
except Exception as e:
    print(f"⚠️ Impossible de charger le paraphraser NLPaug : {e}")
    aug = None

def apply(text: str) -> str:
    """
    Paraphrase la phrase à l’aide d’un modèle T5 léger.
    Si le modèle échoue, retourne la phrase originale.
    """
    if not aug:
        return text

    try:
        augmented = aug.augment(text, n=1)
        if isinstance(augmented, list):
            return augmented[0]
        return augmented
    except Exception as e:
        print(f"⚠️ Erreur pendant le paraphrasing NLPaug : {e}")
        return text
