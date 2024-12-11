# google-translate-clone
_Web-based translator application inspired by Google Translate_

An ongoing effort at cloning Google Translate. Includes language auto-detection and OCR to upload any kind of document to translate. Hosted locally.

### Challenges:
- Extracting text from images and PDFs with high accuracy.
- Auto detection of language from extracted text.
 
### Tech Stack:
- Software platform: Python  
- Frontend: HTML, CSS
- Backend: Flask
- Interactivity: JavaScript
- Libraries: pytesseract, deep_translator, PIL, pdf2image, poppler, io

### Input:
- Input and output language entries must contain the first three or more letters of the language name.
- There is a limit of 5000 characters in a single translation.
