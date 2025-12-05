import io
from PIL import Image
import pytesseract
import PyPDF2

# Point this to your tesseract exe if on Windows, e.g.:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            extract = page.extract_text()
            if extract:
                text += extract + "\n"
        return text
    except Exception as e:
        return ""

def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from an image using Tesseract OCR."""
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Tesseract does the 'OCR' part (reading the pixels)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return ""

def extract_text(filename: str, file_bytes: bytes) -> str:
    """Router to choose the right extraction method."""
    if filename.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
        return extract_text_from_image(file_bytes)
    else:
        # Assume text file
        return file_bytes.decode("utf-8", errors="ignore")