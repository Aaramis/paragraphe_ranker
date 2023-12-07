import fitz
from ebooklib import epub
from bs4 import BeautifulSoup as bs 
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r' +', ' ', text)

    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text


def extract_text_from_epub(epub_path: str) -> str:
    """
    Extract text content from an EPUB file using ebooklib.

    Parameters:
    - epub_path (str): Path to the EPUB file.

    Returns:
    - str: Extracted text content.
    """
    book = epub.read_epub(epub_path)

    content = []
    for item in book.get_items_of_type(epub.ebooklib.ITEM_DOCUMENT):
        content.append(item.content)

    # Decode binary content and concatenate
    decoded_content = ''.join(c.decode('utf-8') for c in content)

    # Use BeautifulSoup to parse HTML
    soup = bs(decoded_content, "html.parser")

    # Extract text
    text = soup.get_text(separator=' ')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' +', ' ', text)

    return text


def extract_text_from_document(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".epub"):
        return extract_text_from_epub(file_path)
    else:
        print("Unsupported file format", "Please provide a PDF or EPUB file.")
