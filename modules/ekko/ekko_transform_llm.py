from modules.llm_core.llm_inference import generate

def ekko_llm_transform(phrase: str) -> str:
    prompt = f"Reformule la phrase suivante en langage structuré et formel : {phrase}"
    return generate(prompt, max_tokens=100)