import streamlit as st
import os
import json
import importlib.util
import pandas as pd

# === 📁 Chemins ===
TRANSFORMATION_DIR = "modules/kalista/kalista_transformations"

# === 🔁 Chargement dynamique des transformations ===
TAGGING_METHODS = []

for filename in os.listdir(TRANSFORMATION_DIR):
    if filename.endswith(".py") and not filename.startswith("__"):
        module_path = os.path.join(TRANSFORMATION_DIR, filename)
        module_name = filename[:-3]
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            if hasattr(mod, "apply"):
                TAGGING_METHODS.append((module_name, mod.apply))
        except Exception as e:
            st.warning(f"⚠️ Erreur de chargement dans {filename} : {e}")

# === 🧠 Interface principale KALISTA ===
def run_kalista():
    st.subheader("🏷️ KALISTA – Thématisation intelligente des phrases")

    uploaded_file = st.file_uploader("📤 Importer un fichier JSON (issu d’EKKO)", type=["json"])

    if uploaded_file:
        try:
            raw_data = json.load(uploaded_file)
            if not isinstance(raw_data, list):
                st.error("❌ Le fichier JSON doit contenir une liste d'objets.")
                return

            st.success(f"✅ {len(raw_data)} phrases importées depuis le fichier.")

            st.markdown("### 🛠️ Choisir les méthodes de tagging à appliquer")
            selected_methods = []
            for method_name, method_func in TAGGING_METHODS:
                if st.checkbox(f"Activer {method_name}", value=True):
                    selected_methods.append((method_name, method_func))

            max_phrases = st.number_input("🔢 Nombre maximal de phrases à traiter", min_value=1, max_value=len(raw_data), value=min(10, len(raw_data)))

            if st.button("🚀 Lancer la thématisation"):

                results = []
                for entry in raw_data[:max_phrases]:
                    nb = entry.get("NbPhrase", "–")
                    for k in entry:
                        if k.startswith("Transfo"):
                            texte = entry[k]
                            result_row = {
                                "NbPhrase": nb,
                                "Transformation": k,
                                "Texte": texte
                            }
                            for method_name, method_func in selected_methods:
                                try:
                                    output = method_func(texte)
                                    # Convertir si liste de dicts (cas ML)
                                    if isinstance(output, list) and all(isinstance(el, dict) and "tag" in el for el in output):
                                        tags_str = ", ".join(f"{t['tag']} ({t.get('score', '-')})" for t in output)
                                        result_row[f"Tags_{method_name}"] = tags_str
                                    elif isinstance(output, list):
                                        result_row[f"Tags_{method_name}"] = ", ".join(output)
                                    else:
                                        result_row[f"Tags_{method_name}"] = str(output)
                                except Exception as e:
                                    result_row[f"Tags_{method_name}"] = f"Erreur : {e}"

                            results.append(result_row)

                st.markdown("### 📊 Résultats de la thématisation")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)

                st.download_button(
                    label="💾 Télécharger le fichier JSON des résultats",
                    data=json.dumps(results, indent=2, ensure_ascii=False),
                    file_name="kalista_tagged_results.json",
                    mime="application/json"
                )

        except Exception as e:
            st.error(f"❌ Erreur lors du traitement : {e}")
