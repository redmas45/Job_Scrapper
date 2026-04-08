from PyPDF2 import PdfReader
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CV_MAP = {
    "1": os.path.join(BASE_DIR, "data", "Rajiv_Kumar_G.pdf"),
    "2": os.path.join(BASE_DIR, "data", "Rajiv_Kumar_M.pdf"),
}


def read_cv(choice="1"):
    path = CV_MAP.get(choice)

    if not path or not os.path.exists(path):
        print("⚠️ CV not found")
        return ""

    reader = PdfReader(path)

    text = ""
    for page in reader.pages:
        try:
            text += page.extract_text() + "\n"
        except:
            continue

    return text[:3000]  # limit for LLM