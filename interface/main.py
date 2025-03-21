import streamlit as st
import os
from datetime import datetime

from core.session import init_session
from core.enhancer import enhance_user_prompt
from core.models import LLM_MODELS
from generator.image import generate_image
from database.json_db import add_entry, generate_uid, get_all_entries

from interface.layout.sidebar_history import display_sidebar_history
from interface.layout.model_selector import model_selector
from interface.layout.prompt_section import prompt_input_section
from interface.layout.viewer import show_generation_view

def main():
    """
    Main interface logic for the Streamlit app.
    Displays either the main prompt interface or the generation viewer.
    """
    st.set_page_config(page_title="Générateur d'Images IA", layout="wide")

    entries_to_display = get_all_entries()
    if "last_entry" in st.session_state:
        if not any(e["uid"] == st.session_state.last_entry["uid"] for e in entries_to_display):
            entries_to_display.append(st.session_state.last_entry)

    with st.sidebar:
        display_sidebar_history(entries_to_display)

    if st.session_state.get("view_mode") == "view_generation":
        show_generation_view()
        return

    st.title("🎨 Générateur d'Images avec Prompts Améliorés")

    if "client_novita" not in st.session_state:
        st.session_state.client_novita, st.session_state.client_nebius = init_session()

    model_choice = model_selector()
    prompt = prompt_input_section()

    if prompt:
        uid = generate_uid()
        directory_path = os.path.join("image_generated", uid)

        entry = {
            "uid": uid,
            "prompt": prompt,
            "date": datetime.now().isoformat()
        }
        st.session_state.last_entry = entry
        st.session_state.generated_prompts = []

        st.write("### Étapes en cours")

        enhance_box = st.empty()
        save_box = st.empty()
        image_boxes = [st.empty() for _ in range(5)]

        with st.spinner("Amélioration du prompt..."):
            try:
                enhanced_json = enhance_user_prompt(
                    st.session_state.client_novita, prompt, model_choice
                )
            except Exception as e:
                st.error(f"Erreur lors de l'amélioration du prompt : {e}")
                st.stop()
        enhance_box.success("✅ Prompt amélioré avec succès")

        st.session_state.generated_prompts = enhanced_json["enhanced_prompts"]

        with st.spinner("Enregistrement du prompt..."):
            add_entry(prompt, uid)
        save_box.success("✅ Prompt enregistré")

        for i, enhanced_prompt in enumerate(st.session_state.generated_prompts):
            with st.spinner(f"Génération de l’image {i+1}..."):
                try:
                    generate_image(
                        st.session_state.client_nebius,
                        enhanced_prompt,
                        f"output_{i}",
                        directory_path
                    )
                    image_boxes[i].success(f"✅ Image {i+1} générée")
                except Exception as e:
                    image_boxes[i].error(f"❌ Erreur pour l'image {i+1} : {e}")

        st.session_state.view_mode = "view_generation"
        st.session_state.view_entry = entry
        st.rerun()

def run_interface():
    """
    Entry point for running the interface.
    """
    main()

if __name__ == "__main__":
    run_interface()
