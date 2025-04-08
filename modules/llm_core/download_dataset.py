from datasets import load_dataset

dataset = load_dataset("OpenLLM-France/Lucie-Training-Dataset")
print(f"Nombre d'exemples : {len(dataset['train'])}")
print(dataset['train'][0])
