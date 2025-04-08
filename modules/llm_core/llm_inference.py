from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "gpt2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID)

def generate(prompt: str, max_tokens: int = 120) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    input_length = inputs["input_ids"].shape[1]  # nombre de tokens dans le prompt

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        pad_token_id=tokenizer.eos_token_id
    )

    generated_tokens = outputs[0][input_length:]  # on coupe le prompt
    return tokenizer.decode(generated_tokens, skip_special_tokens=True)