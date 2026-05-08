from pypdf import PdfReader

def extract_pdf_text(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text