
import streamlit as st
import json
import re

def apply_simple_theming(phrase):
    tags = []
    phrase_lower = phrase.lower()
    if "archivage" in phrase_lower or "conservation" in phrase_lower:
        tags.append("Archivage")
    if "sécurité" in phrase_lower or "confidentiel" in phrase_lower:
        tags.append("Sécurité")
    if "workflow" in phrase_lower or "processus" in phrase_lower:
        tags.append("Workflow")
    if "signature" in phrase_lower:
        tags.append("Signature")
    if "portail" in phrase_lower or "interface" in phrase_lower:
        tags.append("UI/UX")
    return tags if tags else ["Autre"]

def run_kalista():
    st.subheader("🏷️ KALISTA – Tagging par règles simples")

    uploaded_file = st.file_uploader("📥 Charger un JSON issu de EKKO", type=["json"])
    
    if uploaded_file:
        raw_data = json.load(uploaded_file)
        phrases = raw_data.get("content", [])
        
        st.success(f"✅ {len(phrases)} phrases analysées")

        tagged_phrases = []
        for entry in phrases:
            original = entry.get("text_original") or entry.get("text", "")
            cleaned = entry.get("text_cleaned", original)
            tags = apply_simple_theming(cleaned)
            tagged_phrases.append({
                "text": cleaned,
                "tags": tags
            })

        st.markdown("### 🏷️ Résultats de la thématisation")
        for i, item in enumerate(tagged_phrases):
            st.markdown(f"**Phrase {i+1}** — *{', '.join(item['tags'])}*")
            st.code(item["text"])

        final_output = {
            "metadata": raw_data.get("metadata", {}),
            "tagging_method": "rule_based",
            "content": [
                {"phrase_number": i+1, "text": item["text"], "tags": item["tags"]}
                for i, item in enumerate(tagged_phrases)
            ]
        }

        st.markdown("### 📦 JSON taggué :")
        st.json(final_output)

        json_data = json.dumps(final_output, indent=2, ensure_ascii=False)
        st.download_button("📤 Télécharger le JSON taggué", data=json_data, file_name="kalista_output.json", mime="application/json")
