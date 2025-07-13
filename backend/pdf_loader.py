import pdfplumber
import os
import re


def load_pdf_context(pdf_path: str) -> str:
    """Carga y extrae el texto de un archivo PDF con mejor precisión usando pdfplumber"""
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        text_content = []
        # Open the PDF file and extract text from each page
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text and text.strip():
                    cleaned = clean_extracted_text(text)
                    if cleaned:
                        text_content.append(f"Page {page_num}:\n{cleaned}")
        
        if not text_content:
            raise ValueError("No text content found in PDF")

        full_text = "\n\n".join(text_content)
        print(f"PDF loaded successfully. Total length: {len(full_text)} characters")
        return full_text

    except Exception as e:
        print(f"Error loading PDF: {e}")
        return "Error loading PDF content"

def clean_extracted_text(text: str) -> str:
    """Limpia el texto extraído del PDF"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.,;:!?()"\'-]', '', text)
    return text.strip()

