import streamlit as st
from core.models import LLM_MODELS

def model_selector():
    """
    Display a selectbox to choose a LLM model from the available list.

    Returns:
        str: The name of the selected LLM model.
    """
    model_labels = [
        f"{model['name']} ({model['description']})" for model in LLM_MODELS
    ]
    selected_label = st.selectbox("🧠 Choisissez le modèle LLM :", model_labels)
    return next(model["name"] for model in LLM_MODELS if model["name"] in selected_label)
