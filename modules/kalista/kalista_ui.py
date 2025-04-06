import streamlit as st
import os
import json
import importlib.util

# 📁 Répertoire contenant les transformations KALISTA
TRANSFORMATION_DIR = "modules/kalista/kalista_transformations"

# 🔁 Chargement dynamique des modules ayant une fonction apply()
AVAILABLE_TRANSFORMATIONS = []
for filename in sorted(os.listdir(TRANSFORMATION_DIR)):
    if filename.endswith(".py") and not filename.startswith("__"):
        module_path = os.path.join(TRANSFORMATION_DIR, filename)
        module_name = filename[:-3]
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            if hasattr(mod, "apply"):
                AVAILABLE_TRANSFORMATIONS.append({
                    "name": module_name,
                    "function": mod.apply
                })
        except Exception as e:
            st.warning(f"⚠️ Erreur de chargement dans {filename} : {e}")

def run_kalista():
    st.subheader("🏷️ KALISTA – Thématisation intelligente des phrases")

    uploaded_file = st.file_uploader("📤 Importer un fichier JSON (issu d’EKKO)", type=["json"])

    if uploaded_file is not None:
        try:
            raw_data = json.load(uploaded_file)
            phrases = raw_data if isinstance(raw_data, list) else raw_data.get("phrases", [])

            if not phrases:
                st.warning("⚠️ Aucune phrase trouvée dans le fichier.")
                return

            st.success(f"✅ {len(phrases)} phrases importées depuis le fichier.")

            st.markdown("### 🛠️ Choisir les méthodes de tagging à appliquer")
            selected_transfos = st.multiselect(
                "Méthodes disponibles :", 
                options=[t["name"] for t in AVAILABLE_TRANSFORMATIONS],
                default=[t["name"] for t in AVAILABLE_TRANSFORMATIONS]
            )

            nb_phrases = st.number_input(
                "🔢 Nombre de phrases à traiter",
                min_value=1,
                max_value=len(phrases),
                value=min(5, len(phrases)),
                step=1
            )

            if st.button("🚀 Lancer la transformation"):
                st.markdown("### 🧠 Résultats")
                results = []

                for i, item in enumerate(phrases[:nb_phrases]):
                    phrase = item.get("text", item if isinstance(item, str) else "")
                    result_row = {"nb_phrase": i + 1, "original": phrase}

                    for t in AVAILABLE_TRANSFORMATIONS:
                        if t["name"] in selected_transfos:
                            try:
                                tags = t["function"](phrase)
                                result_row[t["name"]] = tags
                            except Exception as e:
                                result_row[t["name"]] = [{"tag": "erreur", "score": 0.0, "debug": str(e)}]

                    results.append(result_row)

                # Affichage dans un tableau Streamlit
                for row in results:
                    with st.expander(f"📝 Phrase {row['nb_phrase']}"):
                        st.markdown(f"**Texte original :** {row['original']}")
                        for key, value in row.items():
                            if key not in ["nb_phrase", "original"]:
                                st.markdown(f"**Méthode : `{key}`**")
                                for tag in value:
                                    st.markdown(f"- {tag['tag']} (score : {tag.get('score', '-')})")

                # 📤 Export JSON
                st.markdown("### 📤 Export des résultats")
                export_json = json.dumps(results, indent=2, ensure_ascii=False)
                st.download_button(
                    label="💾 Télécharger le JSON des résultats",
                    data=export_json,
                    file_name="kalista_tagging_results.json",
                    mime="application/json"
                )

        except Exception as e:
            st.error(f"❌ Erreur lors du traitement : {e}")
