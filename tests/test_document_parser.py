from app.services.document_parser import extract_text_from_txt


def test_extract_text_from_txt():
    contents = b"FastAPI is a Python web framework."

    text = extract_text_from_txt(contents)

    assert text == "FastAPI is a Python web framework."
