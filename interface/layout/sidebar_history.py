import streamlit as st
import os

def display_sidebar_history(entries):
    """
    Display a list of past generations in the sidebar and handle selection.

    Args:
        entries (list): List of generation entries containing 'uid', 'prompt', and 'date'.
    """
    st.markdown("## 📚 Historique")

    if not entries:
        st.info("Aucune image générée pour le moment.")
    else:
        for entry in reversed(entries):
            label = f"{entry['date'].split('T')[0]} - {entry['prompt'][:50]}..."
            if st.button(label, key=f"history_{entry['uid']}"):
                st.session_state.view_mode = "view_generation"
                st.session_state.view_entry = entry
                st.session_state.generated_prompts = ["" for _ in range(5)]
                st.rerun()
