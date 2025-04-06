import re
from datetime import datetime

# Expressions régulières pour les différents formats de dates fréquents
DATE_PATTERNS = [
    (r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})", "%d-%m-%Y"),  # 01/01/2023 ou 01-01-23
    (r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", "%Y-%m-%d"),    # 2023-01-01
    (r"(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})", "%d %B %Y"),  # 1 janvier 2023
]

# Conversion des mois français en anglais pour `datetime.strptime`
FRENCH_MONTHS = {
    "janvier": "January", "février": "February", "mars": "March", "avril": "April",
    "mai": "May", "juin": "June", "juillet": "July", "août": "August",
    "septembre": "September", "octobre": "October", "novembre": "November", "décembre": "December"
}

def normalize_dates(text: str) -> str:
    result = text

    for pattern, fmt in DATE_PATTERNS:
        matches = re.findall(pattern, result, flags=re.IGNORECASE)
        for match in matches:
            try:
                original_str = " ".join(match) if isinstance(match, tuple) else match

                # Remplacement du mois en français si nécessaire
                if fmt == "%d %B %Y":
                    jour, mois_fr, annee = match
                    mois_en = FRENCH_MONTHS.get(mois_fr.lower())
                    if not mois_en:
                        continue
                    original_str = f"{jour} {mois_en} {annee}"

                date_obj = datetime.strptime(original_str, fmt)
                iso_date = date_obj.strftime("%Y-%m-%d")
                result = re.sub(re.escape(" ".join(match)), iso_date, result)
            except Exception:
                continue

    return result

def apply(text: str) -> str:
    return normalize_dates(text)
