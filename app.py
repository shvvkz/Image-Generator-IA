import streamlit as st
import os
import re

from core.session import init_session
from core.enhancer import enhance_user_prompt
from core.models import LLM_MODELS
from generator.image import generate_image
from database.json_db import add_entry, generate_uid, get_all_entries

st.set_page_config(page_title="Générateur d'Images IA", layout="wide")
st.title("🎨 Générateur d'Images avec Prompts Améliorés")

# ===========================
# 📚 HISTORIQUE DANS LE MENU LATÉRAL
# ===========================

with st.sidebar:
    st.markdown("## 📚 Historique")
    entries = get_all_entries()

    if not entries:
        st.info("Aucune image générée pour le moment.")
    else:
        for entry in reversed(entries):  # Afficher du plus récent au plus ancien
            label = f"{entry['date'].split('T')[0]} - {entry['prompt'][:50]}..."
            with st.expander(label):
                st.markdown(f"**Prompt complet :** {entry['prompt']}")
                img_folder = os.path.join("image_generated", entry["uid"])
                if os.path.exists(img_folder):
                    images = sorted([f for f in os.listdir(img_folder) if f.endswith(".png")])
                    cols = st.columns(5)
                    for i, img in enumerate(images):
                        img_path = os.path.join(img_folder, img)
                        cols[i % 5].image(img_path, use_container_width=True)  # 👈 plus de caption ici

# ===========================
# 🧠 INITIALISATION DES CLIENTS
# ===========================

if "client_novita" not in st.session_state:
    st.session_state.client_novita, st.session_state.client_nebius = init_session()

# Choix du modèle
model_labels = [f"{model['name']} ({model['description']})" for model in LLM_MODELS]
model_choice_label = st.selectbox("🧠 Choisissez le modèle LLM pour améliorer le prompt :", model_labels)
model_choice = next(model["name"] for model in LLM_MODELS if model["name"] in model_choice_label)

# ===========================
# ✍️ SAISIE DU PROMPT
# ===========================

user_prompt = st.text_input("💬 Entrez un prompt :", placeholder="A beautiful futuristic city at sunset")

if st.button("✨ Générer les images") and user_prompt.strip():
    with st.spinner("Amélioration du prompt..."):
        try:
            enhanced_json = enhance_user_prompt(st.session_state.client_novita, user_prompt, model_choice)
        except Exception as e:
            st.error(f"Erreur lors de l'amélioration du prompt : {e}")
            st.stop()

    st.success("✅ Prompts améliorés générés !")
    st.json(enhanced_json)

    uid = generate_uid()
    directory_path = os.path.join("image_generated", uid)
    add_entry(user_prompt, uid)

    st.write("🖼️ Génération des images en cours...")
    cols = st.columns(5)

    for i, prompt in enumerate(enhanced_json["enhanced_prompts"]):
        with st.spinner(f"Image {i+1}..."):
            try:
                img_path = generate_image(
                    st.session_state.client_nebius,
                    prompt,
                    f"output_{i}",
                    directory_path
                )
                cols[i % 5].image(img_path, use_container_width=True)  # 👈 plus de caption ici aussi
            except Exception as e:
                st.error(f"Erreur lors de la génération de l’image {i+1} : {e}")
else:
    st.info("📝 Entrez un prompt ci-dessus puis cliquez sur '✨ Générer les images'")
