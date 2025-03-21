import streamlit as st
import os
import re

from core.session import init_session
from core.enhancer import enhance_user_prompt
from core.models import LLM_MODELS
from generator.image import generate_image

st.set_page_config(page_title="Générateur d'Images IA", layout="wide")
st.title("🎨 Générateur d'Images avec Prompts Améliorés")

if "client_novita" not in st.session_state:
    st.session_state.client_novita, st.session_state.client_nebius = init_session()

model_labels = [f"{model['name']} ({model['description']})" for model in LLM_MODELS]
model_choice_label = st.selectbox("🧠 Choisissez le modèle LLM pour améliorer le prompt :", model_labels)
model_choice = next(model["name"] for model in LLM_MODELS if model["name"] in model_choice_label)

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

    directory_name = re.sub(r'\s+', '_', user_prompt.strip().lower())
    directory_path = os.path.join("image_generated", directory_name)

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
                cols[i % 5].image(img_path, caption=f"Image {i+1}", use_container_width=True)
            except Exception as e:
                st.error(f"Erreur lors de la génération de l’image {i+1} : {e}")
else:
    st.info("📝 Entrez un prompt ci-dessus puis cliquez sur '✨ Générer les images'")
