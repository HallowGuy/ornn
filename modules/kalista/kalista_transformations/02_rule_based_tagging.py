import os
import json

# Corriger le chemin vers le fichier de règles
CURRENT_DIR = os.path.dirname(__file__)
RULES_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", "..", "data", "glossary", "rules_thematiques_kalista.json"))

def load_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

try:
    RULES = load_rules()
except Exception as e:
    print(f"❌ Erreur lors du chargement des règles : {e}")
    RULES = {"rules": []}

def apply(phrase: str):
    matched_tags = []
    for rule in RULES.get("rules", []):
        tag = rule.get("tag")
        conditions = rule.get("conditions", [])
        for condition in conditions:
            if all(word.lower() in phrase.lower() for word in condition.get("contains", [])):
                matched_tags.append({"tag": tag, "source": "rule_based"})
                break
    return matched_tags
