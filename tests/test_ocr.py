# ocr_test.py
from PIL import Image
import pytesseract
import os, sys

# If Python can't find tesseract, uncomment and set path exactly:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IMAGE = "sample.jpg"
if not os.path.exists(IMAGE):
    print(f"Error: {IMAGE} not found in this folder.")
    sys.exit(1)

img = Image.open(IMAGE)
text = pytesseract.image_to_string(img, lang="eng")
print("---- OCR OUTPUT ----")
print(text)
print("---- END ----")
