from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

def init_session():
    """
    Initialize the session by loading environment variables and creating InferenceClient objects.
    
    Returns:
        tuple: A tuple containing two InferenceClient objects for Novita and Nebius.
    """
    load_dotenv()
    client_novita = InferenceClient(
        provider='novita',
        api_key=os.getenv('NOVITA_API_KEY')
    )
    client_nebius = InferenceClient(
        provider="nebius",
        api_key=os.getenv("NEBIUS_API_KEY"),
    )
    return client_novita, client_nebius
