import json
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def tokenize_text(text):
    """
    Tokenize a string into sentences using SpaCy.
    """
    if isinstance(text, str):  # Ensure the input is a string
        doc = nlp(text)
        return [sent.text.strip() for sent in doc.sents]  # Extract sentences
    return text  # Return as is if not a string

def tokenize_json_data(json_data):
    """
    Recursively tokenize all string fields in a JSON object into sentences.
    """
    if isinstance(json_data, dict):  # If the data is a dictionary
        return {key: tokenize_json_data(value) for key, value in json_data.items()}
    elif isinstance(json_data, list):  # If the data is a list
        return [tokenize_json_data(item) for item in json_data]
    elif isinstance(json_data, str):  # If the data is a string
        return tokenize_text(json_data)  # Tokenize the string
    return json_data  # Return as is if not a string, dict, or list

def process_json_file(input_file, output_file):
    """
    Read a JSON file, tokenize all text fields, and write the tokenized data to another file.
    """
    with open(input_file, 'r') as file:
        data = json.load(file)

    tokenized_data = tokenize_json_data(data)

    with open(output_file, 'w') as file:
        json.dump(tokenized_data, file, indent=4)

    print(f"Tokenized data saved to {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "scraped_data_new.json"  # Path to your input JSON file
    output_file = "tokenized_data_new.json"  # Path to save the tokenized JSON file

    process_json_file(input_file, output_file)
