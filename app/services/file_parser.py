import PyPDF2
from docx import Document


def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    return text


def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_text_from_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")