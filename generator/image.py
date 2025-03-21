import os

def generate_image(client, prompt, image_name, directory_path):
    """
    Generate an image based on the provided prompt and save it to a file.
    
    Args:
        client (InferenceClient): The AI client to use for image generation.
        prompt (str): The prompt to use for generating the image.
        image_name (str): The name of the file to save the generated image.
        directory_path (str): The full path to the directory where the image should be saved.
    Returns:
        str: The path to the saved image file.
    """
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-dev",
    )

    os.makedirs(directory_path, exist_ok=True)
    image_path = os.path.join(directory_path, image_name + ".png")

    image.save(image_path)
    return image_path
