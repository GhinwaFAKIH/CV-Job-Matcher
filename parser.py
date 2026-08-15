import fitz


def extract_text(pdf_path: str) -> str:
    """Extract text from a PDF file."""

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()
        text += "\n"

    document.close()

    return text
