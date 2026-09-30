from unittest.mock import patch

from app.services.document_parser import extract_text_from_pdf


def test_extract_text_from_pdf():
    fake_pages = [
        "FastAPI is a Python web framework.",
        "PostgreSQL is a relational database.",
    ]

    mock_pages = [
        type(
            "MockPage",
            (),
            {
                "extract_text": lambda self, text=text: text,
            },
        )()
        for text in fake_pages
    ]

    mock_reader = type(
        "MockReader",
        (),
        {
            "pages": mock_pages,
        },
    )

    with patch(
        "app.services.document_parser.PdfReader",
        return_value=mock_reader(),
    ):
        text = extract_text_from_pdf(b"fake pdf contents")

    assert "FastAPI is a Python web framework." in text
    assert "PostgreSQL is a relational database." in text