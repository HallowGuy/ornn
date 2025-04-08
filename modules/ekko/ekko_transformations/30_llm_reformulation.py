from modules.llm_core.llm_inference import generate

def apply(text: str) -> str:
    prompt = f"Oui. La phrase signifie que {text.lower()}."
    return generate(prompt, max_tokens=60)