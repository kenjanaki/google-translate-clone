from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\Users\hiran\Downloads\poppler-24.08.0\Library\bin"

def extract_text_from_pdf(file_stream, input_lang):
    text = ""

    images = convert_from_bytes(file_stream.read(), poppler_path=poppler_path)
    
    for img in images:
        img = img.convert('L')
        img = img.point(lambda p: p > 200 and 255)
        page_text = pytesseract.image_to_string(img, lang=input_lang)
        text += page_text + "\n"
    
    return text
