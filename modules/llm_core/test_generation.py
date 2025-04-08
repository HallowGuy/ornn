from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "gpt2"  # modèle minuscule pour test

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

prompt = "Explique le rôle d'une GED dans une mairie :"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
