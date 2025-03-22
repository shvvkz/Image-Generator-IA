import time
from core.utils import extract_json, validate_json_structure

def ask_until_valid_json(client, messages, model_name):
    """
    Continually asks the AI for a JSON response until a valid one is received.

    Args:
        client (InferenceClient): The InferenceClient object.
        messages (list): A list of messages to send to the AI.
        model_name (str): The name of the LLM to use.

    Returns:
        dict: The valid JSON response.
    """
    for attempt in range(3):
        completion = client.chat.completions.create(
            model=messages[0].get("model", model_name),
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

def enhance_user_prompt(client, user_prompt, model_name, num_images=5, style=None):
    """
    Enhance the user prompt by generating a specified number of variations, with optional style.

    Args:
        client (InferenceClient): The InferenceClient object.
        user_prompt (str): The user prompt to enhance.
        model_name (str): The name of the LLM to use.
        num_images (int): Number of image prompts to generate.
        style (str): Artistic style to apply.

    Returns:
        dict: The enhanced prompts as a JSON object.
    """
    style_instruction = f" Apply the '{style}' artistic style to each prompt." if style else ""

    system_prompt = (
        f"You are an AI assistant that enhances user prompts for generating high-quality AI-generated media. "
        f"Generate exactly {num_images} variations of the user's prompt."
        f"{style_instruction} "
        "Your ONLY response format should be a valid JSON object, with NO additional text before or after. "
        "The JSON format should be as follows:\n"
        "{ \"enhanced_prompts\": [ \"Improved prompt 1\", ..., \"Improved prompt N\"] }\n\n"
        "DO NOT include markdown formatting (e.g., ```json) in your response."
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    return ask_until_valid_json(client, messages, model_name)
