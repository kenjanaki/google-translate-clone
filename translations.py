import io
import pytesseract
from flask import Flask, render_template, jsonify, request
from deep_translator import GoogleTranslator
from PIL import Image
from ocr import extract_text_from_pdf

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('google.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        input_text = data.get("text", "")
        source_lang = data.get("source", "auto")
        target_lang = data.get("target", "hi")

        google_source_lang = source_lang[:2] if source_lang != "auto" else source_lang
        google_target_lang = target_lang[:2]

        translated = GoogleTranslator(source=google_source_lang, target=google_target_lang).translate(input_text)
        return jsonify({"translation": translated})
    except Exception as e:
        print(f"Error in translation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/ocr', methods=['POST'])
def ocr_and_translate():
    try:
        file = request.files['file']
        input_lang = request.form['inputLang']
        output_lang = request.form['outputLang'] 

        google_input_lang = input_lang[:2] if input_lang != "auto" else "auto"
        google_output_lang = output_lang[:2]
        tesseract_input_lang = input_lang[:3]
        tesseract_output_lang = output_lang[:3]

        file_stream = io.BytesIO(file.read())

        file_extension = file.filename.split('.')[-1].lower()

        extracted_text = ""

        if file_extension == 'pdf':
            extracted_text = extract_text_from_pdf(file_stream, tesseract_input_lang)

        elif file_extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
            img = Image.open(file_stream)
            img = img.convert('L')
            img = img.point(lambda p: p > 200 and 255)
            extracted_text = pytesseract.image_to_string(img, lang=tesseract_input_lang)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        try:
            translated_text = GoogleTranslator(source=google_input_lang, target=google_output_lang).translate(extracted_text)
            return jsonify({"extracted_text": extracted_text, "translated_text": translated_text})
        except Exception as e:
            print(f"Error in translation: {str(e)}")
            return jsonify({"error": f"Translation error: {str(e)}"}), 500
    except Exception as e:
        print(f"Error in OCR processing: {str(e)}")
        return jsonify({"error": f"OCR error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)