from app.services.document_parser import extract_text_from_txt


def test_extract_text_from_txt(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text(
        "FastAPI is a Python web framework.",
        encoding="utf-8",
    )

    text = extract_text_from_txt(str(file))

    assert text == "FastAPI is a Python web framework."