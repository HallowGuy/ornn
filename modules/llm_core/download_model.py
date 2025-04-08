from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "OpenLLM-France/Lucie-7B"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", trust_remote_code=True)

print("Modèle et tokenizer téléchargés.")
