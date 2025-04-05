
import streamlit as st
import fitz  # PyMuPDF
import json
import spacy

# Chargement du modèle français de spaCy
try:
    nlp = spacy.load("fr_core_news_md")
except:
    st.error("❌ Le modèle spaCy 'fr_core_news_md' n'est pas installé. Exécutez : \n\
             pip install spacy && python -m spacy download fr_core_news_md")
    st.stop()

def run_hexgate():
    st.subheader("📁 HEXGATE – Extraction par phrases + Métadonnées + Règles")

    uploaded_file = st.file_uploader("📄 Importer un document PDF", type=["pdf"])
    
    if uploaded_file is not None:
        st.success("✅ Document chargé : " + uploaded_file.name)

        # Lire le texte du PDF
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_doc:
            text += page.get_text()

        st.markdown("### 📝 Texte extrait :")
        st.text_area("Texte brut du PDF", text, height=300)

        # Métadonnées
        st.markdown("### 🗂️ Métadonnées manuelles")
        client = st.text_input("👤 Nom du client")
        date_reception = st.date_input("📅 Date de réception")
        auteur = st.text_input("✍️ Auteur du document")
        contexte = st.text_area("🧠 Contexte d’analyse")

        # Règles manuelles
        st.markdown("### 🧠 Règles manuelles d’interprétation")
        st.info("Exemple : 'GED' → 'Système de gestion documentaire'")
        default_rules = [{"motif": "GED", "remplacer_par": "Système de gestion documentaire"}]
        rules = st.data_editor(default_rules, num_rows="dynamic", key="rules_editor")

        # Application des règles
        for rule in rules:
            motif = rule.get("motif", "")
            remplacement = rule.get("remplacer_par", "")
            if motif and remplacement:
                text = text.replace(motif, remplacement)

        # Découpage en phrases
        doc = nlp(text)
        phrases = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        structured_json = [{"phrase_number": i+1, "text": phrase} for i, phrase in enumerate(phrases)]

        final_output = {
            "metadata": {
                "client": client,
                "date_reception": str(date_reception),
                "auteur": auteur,
                "contexte": contexte,
                "document_name": uploaded_file.name
            },
            "rules_appliquees": rules,
            "content": structured_json
        }

        st.markdown("### 📦 JSON structuré final :")
        st.json(final_output)

        json_data = json.dumps(final_output, indent=2, ensure_ascii=False)
        st.download_button("📥 Télécharger le JSON complet", data=json_data, file_name="hexgate_output.json", mime="application/json")
