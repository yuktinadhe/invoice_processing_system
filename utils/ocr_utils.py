import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os
from config import DATA_DIR

# 🔹 Poppler ka bin path (Windows ke liye zaroori)
POPPLER_PATH = r"C:\Users\yukti\Zenith Tech\invoice_mvp\Release-25.07.0-0\poppler-25.07.0\Library\bin"

# 🔹 Tesseract ka path agar alag install kiya ho (default install location)
# Agar tumne tesseract default jagah pe install kiya hai to ye line enable karo:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def pdf_to_image(pdf_path: str, out_dir: str = DATA_DIR) -> str:
    """
    Convert first page of PDF to image using poppler.
    Returns the path of saved image.
    """
    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    os.makedirs(out_dir, exist_ok=True)
    img_path = os.path.join(out_dir, "tmp_page1.png")
    images[0].save(img_path, "PNG")
    return img_path


def run_ocr(file_path: str):
    """
    Run OCR on image or PDF.
    Returns extracted text and engine used.
    """
    if file_path.lower().endswith(".pdf"):
        img_path = pdf_to_image(file_path)
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        return text, "tesseract (pdf)"
    else:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text, "tesseract (image)"


# 🔹 Wrapper functions (for compatibility with rag_pipeline.py)
def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image file using Tesseract.
    """
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF (first page) using Tesseract.
    """
    img_path = pdf_to_image(pdf_path)
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img)
    return text
