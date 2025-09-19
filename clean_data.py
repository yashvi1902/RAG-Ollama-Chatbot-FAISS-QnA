import json
import re

def clean_text(text):
    """
    Remove unwanted characters like \u00a0 and multiple spaces from a string.
    """
    if isinstance(text, str):  # Ensure the input is a string
        # Decode any unicode escape sequences in the string
        text = bytes(text, 'utf-8').decode('unicode_escape')
        # Remove any remaining unicode escape sequences that didn't get decoded
        text = re.sub(r'\\u[0-9A-Fa-f]{4}', '', text)  # Remove all \uXXXX escape sequences
        # Replace multiple spaces with a single space
        cleaned_text = re.sub(r'\s+', ' ', text)  
        # Remove unwanted characters like newlines and tabs
        unwanted_chars = ['\n', '\t']
        for char in unwanted_chars:
            cleaned_text = cleaned_text.replace(char, ' ')
        return cleaned_text.strip()
    return text  # Return as is if not a string

def clean_json_data(json_data):
    """
    Recursively clean all string fields in a JSON object.
    """
    if isinstance(json_data, dict):  # If the data is a dictionary
        return {key: clean_json_data(value) for key, value in json_data.items()}
    elif isinstance(json_data, list):  # If the data is a list
        return [clean_json_data(item) for item in json_data]
    elif isinstance(json_data, str):  # If the data is a string
        return clean_text(json_data)
    return json_data  # Return as is if not a string, dict, or list

def process_json_file(input_file, output_file):
    """
    Read a JSON file, clean all text fields, and write the cleaned data to another file.
    """
    with open(input_file, 'r') as file:
        data = json.load(file)

    cleaned_data = clean_json_data(data)

    with open(output_file, 'w') as file:
        json.dump(cleaned_data, file, indent=4)

    print(f"Cleaned data saved to {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "tokenized_data_new.json"  # Path to your input JSON file
    output_file = "clean_data_pdf.json"  # Path to save the cleaned JSON file

    process_json_file(input_file, output_file)
