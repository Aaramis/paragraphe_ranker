import fitz
import parser


def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
            text = text.replace("\n", " ")
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text


def extract_text_from_epub(epub_path: str) -> str:
    parsed = parser.from_file(epub_path, service='text')
    content = parsed["content"]
    return content


def extract_text_from_document(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".epub"):
        return extract_text_from_epub(file_path)
    else:
        print("Unsupported file format", "Please provide a PDF or EPUB file.")
