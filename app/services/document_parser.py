from io import BytesIO

from pypdf import PdfReader


def extract_text_from_txt(contents: bytes) -> str:
    with BytesIO(contents) as file:
        return file.read().decode("utf-8")


def extract_text_from_pdf(contents: bytes) -> str:
    with BytesIO(contents) as file:
        reader = PdfReader(file)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)