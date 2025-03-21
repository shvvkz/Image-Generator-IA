import streamlit as st

def prompt_input_section():
    """
    Display a text input and a button to submit a prompt.

    Returns:
        str or None: The user-entered prompt if submitted, otherwise None.
    """
    prompt = st.text_input("💬 Entrez un prompt :", placeholder="A beautiful futuristic city at sunset")
    if st.button("✨ Générer les images") and prompt.strip():
        return prompt
    return None
