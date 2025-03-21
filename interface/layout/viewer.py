import streamlit as st
import os

def show_generation_view():
    """
    Display the detailed view of a generated image set.
    """
    st.markdown(
        """<style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child { display: none; }</style>""",
        unsafe_allow_html=True
    )

    entry = st.session_state.get("view_entry")
    prompts = st.session_state.get("generated_prompts")

    if not entry or not prompts:
        st.error("Aucune génération à afficher.")
        return

    st.title(f"🖼️ Résultat du {entry['date'].split('T')[0]}")
    st.markdown(f"**Prompt original :** {entry['prompt']}")

    img_folder = os.path.join("image_generated", entry["uid"])
    cols = st.columns(5)

    for i, _ in enumerate(prompts):
        img_path = os.path.join(img_folder, f"output_{i}.png")
        if os.path.exists(img_path):
            cols[i % 5].image(img_path, use_container_width=True)

    if st.button("🔙 Retour"):
        st.session_state.view_mode = None
        st.session_state.view_entry = None
        st.session_state.generated_prompts = None
        st.rerun()
