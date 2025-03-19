from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import re
import json

def init_session():
    """
    Initialize the session by performing the following steps:
        - Load environment variables from a .env file.
        - Create and configure InferenceClient objects for two AI providers: Novita and Nebius.
    Args:
        None

    Returns:
        tuple: A tuple containing two InferenceClient objects:
            - client_novita (InferenceClient): Configured for the 'novita' provider using the NOVITA_API_KEY. 
            - client_nebius (InferenceClient): Configured for the 'nebius' provider using the NEBIUS_API_KEY. 
    """
    print("[LOADING ENVIRONMENT VARIABLES]")
    load_dotenv()

    client_novita = InferenceClient(
        provider='novita',
        api_key= os.getenv('NOVITA_API_KEY')
    )
    client_nebius = InferenceClient(
        provider="nebius",
        api_key=os.getenv("NEBIUS_API_KEY"),
    )
    return (client_novita, client_nebius)

def clean_answer(answer):
    """
    Clean the answer by removing unnecessary characters and converting it to a JSON object.
    Warning: Can raise a ValueError if the answer made by deepseek-ai is not a valid JSON object.
    
    Args:
        answer (str): The answer to be cleaned.
        
    Returns:
        dict: The cleaned answer as a JSON object.
    """
    cleaned_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL)
    cleaned_answer = cleaned_answer.replace("\n", "")
    cleaned_answer = cleaned_answer.replace("\\", "")
    cleaned_answer = cleaned_answer.replace("```json", "")
    cleaned_answer = cleaned_answer.replace("```", "")
    try:
        return json.loads(cleaned_answer)
    except json.JSONDecodeError as e:
        raise ValueError("Erreur lors de la conversion en JSON (l'IA intermédiaire n'a pas généré un json valide):") from e
    
def enhance_user_prompt(client):
    """
    Enhance the user prompt by generating five different variations of the prompt.
    
    Args:
        client (InferenceClient): The InferenceClient object to use for generating the enhanced prompts.
        
    Returns:
        str: The enhanced prompts as a JSON object.
    """
    user_prompt = input("Please enter a prompt to generate an image:\n> ")
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that enhances user prompts for generating high-quality AI-generated media. Your goal is to take a " + 
                       "simple prompt provided by the user and improve it by adding more details, context, and creative elements. Your output must be a JSON object" + 
                       "containing five enhanced prompts, each offering a different variation while keeping the core idea intact. The final output should be formatted" +
                       "as follows: { \"enhanced_prompts\": [ \"Improved prompt 1\", \"Improved prompt 2\", \"Improved prompt 3\", \"Improved prompt 4\", \"Improved prompt 5\"]" +
                       "\n}\n\nEnsure that the descriptions are vivid, precise, and provide sufficient details for AI models to generate high-quality images."
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    completion = client.chat.completions.create(
        model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
        messages = messages,
        max_tokens = 1000,
    )
    return completion.choices[0].message.content

def generate_image(client, prompt, image_name):
    """
    Generate an image based on the provided prompt and save it to a file.
    
    Args:
        client (InferenceClient): The InferenceClient object to use for generating the image.
        prompt (str): The prompt to use for generating the image.
        image_name (str): The name of the file to save the generated image.
        
    Returns:
        None
    """
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev",
    )
    image.save(image_name+".png")

def main():
    """
    The main function of the script that orchestrates the entire process.
    It initializes the session, enhances the user prompt, generates five enhanced prompts,
    and generates an image for each enhanced prompt.
    """
    client_novita, client_nebius = init_session()
    print("[SESSION INITIALIZED]")
    print("[ASKING FOR PROMPT]")
    enhanced_prompt_raw = enhance_user_prompt(client_novita)
    print("[PROMPT ENHANCED]")
    enhanced_prompt_json = clean_answer(enhanced_prompt_raw)
    for i, prompt in enumerate(enhanced_prompt_json['enhanced_prompts']):
        print(f"[GENERATING IMAGE {i+1}/{len(enhanced_prompt_json['enhanced_prompts'])}]")
        generate_image(client_nebius, prompt, f"output_{i}")
    
if __name__ == "__main__":
    main()