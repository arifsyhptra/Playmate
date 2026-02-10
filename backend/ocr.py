import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def run_ocr(image_path):
    """
    Menerima path gambar, mengembalikan hasil OCR sebagai string
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="eng")  # Bisa ganti lang sesuai kebutuhan
        return text
    except Exception as e:
        return f"Error: {e}"
