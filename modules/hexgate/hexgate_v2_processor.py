import re
import json
import spacy
from datetime import datetime
from typing import List, Dict

# Charger le modèle spaCy français
nlp = spacy.load("fr_core_news_lg")
FR_VOCAB = set(nlp.vocab.strings)  # Dictionnaire intégré à spaCy

def clean_text_lines(lines):
    cleaned_lines = []
    for line in lines:
        line = line.strip()

        if not line or re.fullmatch(r"\W+", line):
            continue  # Ignore lignes vides ou symboles

        if (
            cleaned_lines
            and not re.search(r"[.!?…]\s*$", cleaned_lines[-1])
            and line and line[0].islower()
        ):
            cleaned_lines[-1] += " " + line
        else:
            cleaned_lines.append(line)
    return cleaned_lines

def normalize_dates(text: str) -> str:
    months = {
        "janvier": "01", "février": "02", "mars": "03", "avril": "04",
        "mai": "05", "juin": "06", "juillet": "07", "août": "08",
        "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
    }
    pattern = re.compile(r"(\d{1,2})\s+(%s)\s+(\d{4})" % "|".join(months.keys()), re.IGNORECASE)
    
    def replace_date(match):
        day, month, year = match.groups()
        return f"{year}{months[month.lower()]:0>2}{int(day):02}"
    
    return pattern.sub(replace_date, text)

def extract_phrases(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if len(sent.text.strip().split()) >= 3]

def tag_unknown_terms(phrases: List[str]) -> Dict[str, List[str]]:
    tagged = {}
    for phrase in phrases:
        doc = nlp(phrase)
        unknown = set()
        for token in doc:
            if token.is_alpha and token.text not in FR_VOCAB and not token.is_stop:
                if token.text[0].isupper() or token.text.isupper():
                    unknown.add(token.text)
        tagged[phrase] = sorted(unknown)
    return tagged

def detect_dates_in_phrase(text: str) -> List[str]:
    # Recherches multiples formats de dates
    patterns = [
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",    # ex: 04/12/2024
        r"\b\d{4}-\d{2}-\d{2}\b",          # ex: 2024-12-04
        r"\b\d{1,2}\s+[a-zéû]+\s+\d{4}\b", # ex: 4 décembre 2024
    ]
    found_dates = []
    for pat in patterns:
        found_dates += re.findall(pat, text, flags=re.IGNORECASE)
    return found_dates

def process_document(text: str) -> Dict:
    lines = text.splitlines()
    lines = clean_text_lines(lines)
    full_text = normalize_dates(" ".join(lines))
    phrases = extract_phrases(full_text)
    tagged = tag_unknown_terms(phrases)

    return {
        "meta": {
            "processed_at": datetime.now().strftime("%Y%m%d"),
            "source": "HEXGATEv2"
        },
        "phrases": [
            {
                "position": idx + 1,
                "text": p,
                "tags": tagged.get(p, []),
                "date_detected": detect_dates_in_phrase(p)
            }
            for idx, p in enumerate(phrases)
        ]
    }

# 🔧 Exécution manuelle pour test
if __name__ == "__main__":
    with open("sample_cctp.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    result = process_document(raw_text)

    with open("hexgate_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("✅ HEXGATE v2 : traitement terminé.")
