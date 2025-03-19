from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import re
import json
import time

def init_session():
    """
    Initialize the session by loading environment variables and creating InferenceClient objects.
    
    Returns:
        tuple: A tuple containing two InferenceClient objects for Novita and Nebius.
    """
    print("[LOADING ENVIRONMENT VARIABLES]")
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

def validate_json_structure(json_data):
    """
    Validate if the given JSON follows the expected structure.
    
    Args:
        json_data (dict): The JSON object to validate.
    
    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(json_data, dict):
        return False
    if "enhanced_prompts" not in json_data or not isinstance(json_data["enhanced_prompts"], list):
        return False
    return all(isinstance(prompt, str) for prompt in json_data["enhanced_prompts"])

def extract_json(text):
    """
    Extracts a JSON object from the text using regex.
    
    Args:
        text (str): The text to extract JSON from.
    
    Returns:
        dict or None: Extracted JSON object or None if extraction fails.
    """
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None

def clean_answer(answer):
    """
    Clean the answer and ensure it is a valid JSON object.
    
    Args:
        answer (str): The answer to be cleaned.
    
    Returns:
        dict: The cleaned answer as a JSON object.
    """
    answer = answer.replace("```json", "").replace("```", "").strip()
    json_data = extract_json(answer)

    if json_data and validate_json_structure(json_data):
        return json_data

    print("Erreur: L'IA n'a pas renvoyé un JSON valide.")
    print("Réponse brute reçue:", answer)
    exit(1)

def ask_until_valid_json(client, messages):
    """
    Continually asks the AI for a JSON response until a valid one is received.
    
    Args:
        client (InferenceClient): The AI client to use.
        messages (list): The conversation history including the system and user messages.
    
    Returns:
        dict: The valid JSON response.
    """
    for attempt in range(3):  # Maximum 3 tentatives
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
            messages=messages,
            max_tokens=1000,
        )
        response = completion.choices[0].message.content
        json_data = extract_json(response)

        if json_data and validate_json_structure(json_data):
            return json_data

        print(f"[ATTEMPT {attempt+1}/3] L'IA a échoué à générer un JSON valide. Nouvelle tentative...")
        messages.append({"role": "system", "content": "Your response was not a valid JSON. Please try again."})
        time.sleep(1)

    print("L'IA a échoué après 3 tentatives.")
    exit(1)

def enhance_user_prompt(client):
    """
    Enhance the user prompt by generating five different variations.
    
    Args:
        client (InferenceClient): The AI client to use.
    
    Returns:
        dict: The enhanced prompts as a JSON object.
    """
    user_prompt = input("Please enter a prompt to generate an image:\n> ")
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant that enhances user prompts for generating high-quality AI-generated media. "
                "Your ONLY response format should be a valid JSON object, with NO additional text before or after. "
                "The JSON format should be as follows:\n"
                "{ \"enhanced_prompts\": [ \"Improved prompt 1\", \"Improved prompt 2\", \"Improved prompt 3\", \"Improved prompt 4\", \"Improved prompt 5\"] }\n\n"
                "DO NOT include markdown formatting (e.g., ```json) in your response."
            )
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    
    return ask_until_valid_json(client, messages)

def generate_image(client, prompt, image_name):
    """
    Generate an image based on the provided prompt and save it to a file.
    
    Args:
        client (InferenceClient): The AI client to use for image generation.
        prompt (str): The prompt to use for generating the image.
        image_name (str): The name of the file to save the generated image.
    """
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev",
    )
    image.save(image_name+".png")

def main():
    """
    The main function that orchestrates the process.
    It initializes the session, enhances the user prompt, generates enhanced prompts,
    and creates an image for each enhanced prompt.
    """
    client_novita, client_nebius = init_session()
    print("[SESSION INITIALIZED]")
    print("[ASKING FOR PROMPT]")
    enhanced_prompt_json = enhance_user_prompt(client_novita)
    print("[PROMPT ENHANCED]")

    for i, prompt in enumerate(enhanced_prompt_json['enhanced_prompts']):
        print(f"[GENERATING IMAGE {i+1}/{len(enhanced_prompt_json['enhanced_prompts'])}]")
        generate_image(client_nebius, prompt, f"output_{i}")
    
if __name__ == "__main__":
    main()
