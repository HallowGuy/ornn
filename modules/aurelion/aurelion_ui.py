
import streamlit as st
import json
from datetime import datetime
import base64

LATEX_STYLE = """
<style>
body {
    font-family: 'Georgia', serif;
    margin: 40px;
    background-color: #fff;
    color: #111;
}
header {
    border-bottom: 2px solid #999;
    padding-bottom: 10px;
    margin-bottom: 40px;
    display: flex;
    align-items: center;
}
header img {
    height: 60px;
    margin-right: 20px;
}
header .meta {
    font-size: 0.9rem;
}
h1 {
    font-size: 1.6rem;
    margin: 0;
}
h2 {
    border-bottom: 1px solid #ccc;
    padding-bottom: 4px;
    margin-top: 30px;
}
p {
    text-align: justify;
    line-height: 1.6;
    font-size: 1.05rem;
    margin: 12px 0;
}
</style>
"""

def encode_image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

def structure_by_tags(content, plan_order):
    sections = {tag: [] for tag in plan_order}
    for entry in content:
        for tag in entry.get("tags", ["Autre"]):
            if tag in sections:
                sections[tag].append(entry["text"])
            else:
                sections.setdefault("Hors plan", []).append(entry["text"])
    return sections

def run_aurelion():
    st.subheader("🧩 AURELION – Structuration HTML + en-tête + logo")

    uploaded_file = st.file_uploader("📥 Charger un JSON issu de KALISTA", type=["json"])
    logo_file = st.file_uploader("🖼️ Logo de l'organisation (PNG/JPG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        raw_data = json.load(uploaded_file)
        content = raw_data.get("content", [])
        metadata = raw_data.get("metadata", {})

        st.success(f"✅ {len(content)} phrases taguées reçues")

        all_tags = set()
        for entry in content:
            all_tags.update(entry.get("tags", []))
        default_plan = sorted(all_tags)

        st.markdown("### 🧭 Définir un plan personnalisé")
        plan_order = st.multiselect("Ordre des sections :", options=default_plan, default=default_plan)
        section_titles = {tag: st.text_input(f"Titre pour '{tag}'", value=tag) for tag in plan_order}

        structured_sections = structure_by_tags(content, plan_order)

        # En-tête personnalisée
        client = metadata.get("client", st.text_input("👤 Client", value="Nom du client"))
        titre_doc = st.text_input("📄 Titre du document", value="Livrable structuré")
        date_gen = metadata.get("date_reception", str(datetime.now().date()))

        # Encodage du logo
        logo_base64 = ""
        if logo_file:
            logo_base64 = encode_image_to_base64(logo_file)

        html_output = LATEX_STYLE
        html_output += "<body><header>"
        if logo_base64:
            html_output += f"<img src='data:image/png;base64,{logo_base64}' alt='Logo'/>"
        html_output += f"<div class='meta'><h1>{titre_doc}</h1><p>Client : {client}<br>Date : {date_gen}</p></div>"
        html_output += "</header>"

        for tag in plan_order:
            phrases = structured_sections.get(tag, [])
            if not phrases:
                continue
            title = section_titles.get(tag, tag)
            html_output += f"<h2>{title}</h2>" + "".join(f"<p>{p}</p>" for p in phrases)

        html_output += "</body>"

        # Affichage et export
        st.markdown("### 📄 Aperçu HTML enrichi avec entête et logo")
        st.components.v1.html(html_output, height=600, scrolling=True)

        st.download_button("📥 Télécharger le livrable HTML (en-tête + style)", data=html_output, file_name="aurelion_livrable.html", mime="text/html")
