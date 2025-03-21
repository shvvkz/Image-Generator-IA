import re
import json

def validate_json_structure(json_data):
    """
    Validate if the given JSON follows the expected structure.
    Args:
        json_data (dict): JSON object
    Returns:
        bool: True if valid, False otherwise.
    """
    return isinstance(json_data, dict) and "enhanced_prompts" in json_data and isinstance(json_data["enhanced_prompts"], list)

def extract_json(text):
    """
    Extracts a JSON object from the text using regex.
    Args:
        text (str): Text to extract JSON from.
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
