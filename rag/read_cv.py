from PyPDF2 import PdfReader
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CV_MAP = {
    "1": os.path.join(BASE_DIR, "data", "Rajiv_Kumar_G.pdf"),
    "2": os.path.join(BASE_DIR, "data", "Rajiv_Kumar_M.pdf"),
}


def read_cv(choice="1"):
    try:
        path = CV_MAP.get(choice)

        if not path:
            print(f"⚠️ CV choice '{choice}' not found in CV_MAP")
            return "CV not found"

        if not os.path.exists(path):
            print(f"⚠️ CV file not found at: {path}")
            return f"CV file not found at {path}"

        reader = PdfReader(path)

        text = ""
        for page in reader.pages:
            try:
                text += page.extract_text() + "\n"
            except Exception as e:
                print(f"⚠️ Error reading page: {e}")
                continue

        if not text:
            return "CV file is empty or unreadable"

        return text[:3000]  # limit for LLM
    
    except Exception as e:
        print(f"💥 CV Read Error: {e}")
        return f"Error reading CV: {str(e)}"