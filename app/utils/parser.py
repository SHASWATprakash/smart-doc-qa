import fitz  # PyMuPDF
import docx

def parse_pdf(path):
    doc = fitz.open(path)
    return " ".join([page.get_text() for page in doc])

def parse_docx(path):
    doc = docx.Document(path)
    return " ".join([p.text for p in doc.paragraphs])