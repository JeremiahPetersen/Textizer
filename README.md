![demo screenshot textizer](https://github.com/JeremiahPetersen/Textizer/assets/118206017/f28c681a-6c1c-4d29-985e-fa2f4cf94a32)

![demo screenshot 2 textizer](https://github.com/JeremiahPetersen/Textizer/assets/118206017/c9d23c47-acf9-42c8-8b62-b3ccdfd8297f)


# Textizer
Text cleanup multi tool for removing whitespaces and line breaks, anonymizing identifiable information, and checking token count for use with ChatGPT or other Large Language Models.  There is also a decode feature to decode a previously anonymized text.  This project leverages the capabilities of the Hugging Face Transformers library and React library.

## How to Use

1. Clone the repository.
2. Navigate to the directory containing `app.py` and run `python app.py` to start the Flask API at http://localhost:5000.
3. Navigate to the directory containing `App.js` and run `npm install` followed by `npm start`. This starts the React application on http://localhost:3000.
4. Open http://localhost:3000 in your web browser.
5. Enter your text in the input text area.
6. Click the 'Anonymize' button to replace all named entities with anonymized labels.
7. Click the 'Remove Spaces' button to remove all spaces and line breaks.

Remember - 'Anonymize' and 'Remove Spaces' operations are performed independently. To decode the anonymized text, you need to use the `/decode` endpoint from the backend API.

## Changing Modes

The application provides different modes for various text-related operations:

- Anonymize Mode: Use this mode by clicking the 'Anonymize' button. This mode uses the Named Entity Recognition (NER) model from the Hugging Face Transformers library to anonymize the text.
- Decode Mode: The logic is built and working for this mode, use by calling the `/decode` endpoint from the backend API. This mode decodes the anonymized text to its original form.  (Add a Decode Button in App.js for front end functionality)
- Remove Spaces and Line Breaks Mode: Use this mode by clicking the 'Remove Spaces' button. This mode removes all spaces and line breaks from the text.

## Code Explanation

This app includes a backend Flask API and a frontend built using React.

### Defining the HTTP endpoints

The Flask API offers the following four HTTP endpoints:

- `/anonymize`: This endpoint receives a POST request with the text to be anonymized. It uses the Named Entity Recognition (NER) model from the Hugging Face Transformers library for anonymization.
- `/decode`: This endpoint receives a POST request with anonymized text and a mapping of anonymized entities to their original entities. It decodes the text by replacing the anonymized entities with their originals.
- `/removeSpacesAndLineBreaks`: This endpoint receives a POST request with the text and returns the text with all spaces and line breaks removed.
- `/getCharAndTokenCount`: This endpoint receives a POST request with the text and returns the character count and token count of the text.

### Defining the React Components

The frontend is built using the React library. The main component is TextModifier, which maintains several states, including input text, output text, mapping of original entities to their replacements, and character/token counts for both the input and output text. These states are updated based on user interaction and the responses from the Flask API.

### Applying CSS Styling

The frontend uses CSS for styling. Flexbox is used for layout, and several containers and items are defined and aligned within them. The CSS file also defines styles for text areas, buttons, and character/token count displays.

Enjoy and feel free to contribute!

# TODO

- [ ] Build logic to remove comments from code.  Add button on front end. (This will lower token input for larger codebases)
- [ ] Continue working on "Decode" functionality
- [ ] Adjust "Anonymizer" function to work with lower case names, places, etc
- [ ] Continue testing various names/places and add to list of edge cases for ones that do not transform as expected
- [ ] Build Tests

