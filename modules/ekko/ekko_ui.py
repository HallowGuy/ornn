
import streamlit as st
import json
import re

def clean_text(text):
    # Nettoyage simple : suppression de ponctuation, espaces multiples, minuscules
    text = re.sub(r"[\n\r\t]", " ", text)
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", "", text)  # garder lettres, chiffres, accents
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

def run_ekko():
    st.subheader("📄 EKKO – Nettoyage de phrases extraites")

    uploaded_file = st.file_uploader("📥 Charger un JSON issu de HEXGATE", type=["json"])
    
    if uploaded_file:
        raw_data = json.load(uploaded_file)
        phrases = raw_data.get("content", [])
        
        st.success(f"✅ {len(phrases)} phrases chargées depuis {raw_data['metadata'].get('document_name', 'Document')}")

        cleaned_phrases = []
        for entry in phrases:
            original = entry["text"]
            cleaned = clean_text(original)
            cleaned_phrases.append({
                "original": original,
                "nettoyé": cleaned
            })

        st.markdown("### 🧹 Résultat du nettoyage")
        for i, item in enumerate(cleaned_phrases):
            st.markdown(f"**Phrase {i+1}**")
            st.code(f"Avant : {item['original']}")
            st.code(f"Après : {item['nettoyé']}")

        final_output = {
            "metadata": raw_data.get("metadata", {}),
            "nettoyage": "standard",
            "content": [
                {"phrase_number": i+1, "text_cleaned": item["nettoyé"], "text_original": item["original"]}
                for i, item in enumerate(cleaned_phrases)
            ]
        }

        st.markdown("### 📦 JSON nettoyé final :")
        st.json(final_output)

        json_data = json.dumps(final_output, indent=2, ensure_ascii=False)
        st.download_button("📤 Télécharger le JSON nettoyé", data=json_data, file_name="ekko_output.json", mime="application/json")
