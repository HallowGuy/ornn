import streamlit as st
import os
import json
import importlib.util
import pandas as pd

# 📦 Chargement dynamique des modules de transformation
TRANSFORMATION_DIR = "modules/ekko/ekko_transformations"
AVAILABLE_TRANSFORMATIONS = []

for filename in sorted(os.listdir(TRANSFORMATION_DIR)):
    if filename.endswith(".py") and not filename.startswith("__"):
        module_path = os.path.join(TRANSFORMATION_DIR, filename)
        module_name = filename[:-3]
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "apply"):
            AVAILABLE_TRANSFORMATIONS.append((module_name, mod.apply))

def run_ekko():
    st.subheader("🧠 EKKO – Analyse contextuelle des phrases")

    uploaded_file = st.file_uploader("📤 Importer un fichier JSON HEXGATE", type=["json"])

    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)

            st.success("✅ Fichier chargé avec succès.")
            st.markdown(f"**Client :** `{data.get('meta', {}).get('client', 'inconnu')}`")
            st.markdown(f"**Document :** `{data.get('meta', {}).get('document_name', 'non spécifié')}`")
            st.markdown(f"**Contexte :** {data.get('meta', {}).get('contexte', '–')}`")

            phrases = data.get("phrases", [])
            if not phrases:
                st.warning("⚠️ Aucun contenu trouvé dans le champ 'phrases'.")
                return

            # 🧰 Sélection des transformations
            st.markdown("### 🧰 Choix des transformations à appliquer")
            selected = []
            for module_name, _ in AVAILABLE_TRANSFORMATIONS:
                if st.checkbox(f"✔️ {module_name}", value=False, key=module_name):
                    selected.append(module_name)

            selected_transforms = [f for name, f in AVAILABLE_TRANSFORMATIONS if name in selected]

            # 🔢 Nombre de phrases à transformer
            max_count = st.number_input("Nombre de phrases à traiter :", min_value=1, max_value=len(phrases), value=min(100, len(phrases)))

            if st.button("🚀 Lancer les transformations"):
                st.markdown("### 📊 Résultats des transformations")
                results = []

                for idx, phrase in enumerate(phrases[:int(max_count)], start=1):
                    row = {
                        "NbPhrase": idx,
                        "Phrase originale": phrase.get("text", "")
                    }

                    transformed = phrase.get("text", "")
                    for trans_idx, transformation in enumerate(selected_transforms, start=1):
                        try:
                            transformed = transformation(transformed)
                            row[f"Transfo {trans_idx}"] = transformed
                        except Exception as e:
                            row[f"Transfo {trans_idx}"] = f"[Erreur : {e}]"

                    results.append(row)

                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)

                # 📥 Export du JSON
                st.download_button(
                    label="📁 Télécharger le résultat JSON",
                    data=json.dumps(results, ensure_ascii=False, indent=2),
                    file_name="ekko_transformed.json",
                    mime="application/json"
                )

        except Exception as e:
            st.error(f"❌ Erreur de chargement ou traitement du fichier : {e}")
