import time
from core.utils import extract_json, validate_json_structure

def ask_until_valid_json(client, messages, model):
    """
    Continually asks the AI for a JSON response until a valid one is received.
    Args:
        client (InferenceClient): The InferenceClient object.
        messages (list): A list of messages to send to the AI.
        model (str): The model to use for generating the response
    Returns:
        dict: The valid JSON response.
    """
    for attempt in range(3):
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1000,
        )
        response = completion.choices[0].message.content
        json_data = extract_json(response)

        if json_data and validate_json_structure(json_data):
            return json_data

        messages.append({"role": "system", "content": "Your response was not a valid JSON. Please try again."})
        time.sleep(1)

    raise ValueError("L'IA a échoué après 3 tentatives.")

def enhance_user_prompt(client, user_prompt, model):
    """
    Enhance the user prompt by generating five different variations.
    Args:
        client (InferenceClient): The InferenceClient object.
        user_prompt (str): The user prompt to enhance.
        model (str): The model to use for enhancing the prompt.
    Returns:
        dict: The enhanced prompts as a JSON object.
    """
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
    
    return ask_until_valid_json(client, messages, model)
