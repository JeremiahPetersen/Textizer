from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from tiktoken import get_encoding

app = Flask(__name__)
CORS(app)

enc = get_encoding("cl100k_base")  # or enc = tiktoken.encoding_for_model("gpt-4")

ner = pipeline('ner')

# This dictionary stores the mapping between original entities and their replacements
entity_mapping = {}

@app.route('/anonymize', methods=['POST'])
def anonymize():
    # Clear the entity_mapping dictionary at the beginning of each request
    entity_mapping.clear()

    text = request.json.get('text', '')
    out = ner(text)

    # Create a memory to remember which original entity corresponds to which placeholder
    memory = {}

    # Initialize counters for each type of entity
    name_counter = 1
    location_counter = 1
    organization_counter = 1

    # Sort entities by start offset in ascending order
    out.sort(key=lambda e: (e['start'], e['end']))

    # Group consecutive entities of the same type
    grouped_entities = []
    for entity in out:
        if not grouped_entities or grouped_entities[-1]['entity'] != entity['entity'] or grouped_entities[-1]['end'] != entity['start']:
            grouped_entities.append(entity)
        else:
            grouped_entities[-1]['end'] = entity['end']
            grouped_entities[-1]['word'] += ' ' + entity['word']

    # Sort grouped entities by start offset in descending order
    grouped_entities.sort(key=lambda e: (-e['start'], -e['end']))

    # Define a set of conjunctions that we won't replace
    conjunctions = {"and", "or"}

    # Replace named entities
    for entity in grouped_entities:
        # If the entity is a conjunction, skip it
        if entity['word'].lower() in conjunctions:
            continue

        # If the entity has already been replaced before, use the same replacement
        if entity['word'] in memory:
            replacement = memory[entity['word']]
        else:
            # Choose a new replacement based on entity type
            if entity['entity'] in ['B-PER', 'I-PER']:
                replacement = f"Name{name_counter}"
                name_counter += 1
            elif entity['entity'] in ['B-LOC', 'I-LOC']:
                replacement = f"Place{location_counter}"
                location_counter += 1
            elif entity['entity'] in ['B-ORG', 'I-ORG']:
                replacement = f"Group{organization_counter}"
                organization_counter += 1

            # Remember this replacement for future use
            memory[entity['word']] = replacement
            entity_mapping[replacement] = entity['word']

        # Replace the entity in the original text
        text = text[:entity['start']] + replacement + text[entity['end']:]
    
    return jsonify({'anonymizedText': text, 'mapping': entity_mapping, 'characterCount': len(text), 'tokenCount': len(enc.encode(text))})

@app.route('/decode', methods=['POST'])
def decode():
    text = request.json.get('text', '')
    mapping = request.json.get('mapping', {})
    for anonymized_entity, original_entity in mapping.items():
        text = text.replace(anonymized_entity, original_entity)
    
    # Clear the entity_mapping dictionary after decoding the text
    entity_mapping.clear()
    
    return jsonify({'decodedText': text, 'characterCount': len(text), 'tokenCount': len(enc.encode(text))})

@app.route('/removeSpacesAndLineBreaks', methods=['POST'])
def remove_spaces_and_line_breaks():
    data = request.get_json()
    input_text = data.get('text')
    
    # Remove whitespace and line breaks
    output_text = input_text.replace(" ", "").replace("\n", "")
    
    return jsonify({'text': output_text, 'characterCount': len(output_text), 'tokenCount': len(enc.encode(output_text))}), 200

@app.route('/getCharAndTokenCount', methods=['POST'])
def get_char_and_token_count():
    text = request.get_json()['text']
    char_count = len(text)
    token_count = len(enc.encode(text))
    return jsonify({'charCount': char_count, 'tokenCount': token_count})

if __name__ == "__main__":
    app.run(port=5000)