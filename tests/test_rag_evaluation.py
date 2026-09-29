from app.db.database import SessionLocal
from app.services.retrieval_service import search_similar_chunks


def test_rag_retrieves_expected_information():
    db = SessionLocal()

    evaluation_cases = [
        {
            "question": "What framework is used to build the API?",
            "expected": "FastAPI",
        },
        {
            "question": "What database system is used?",
            "expected": "PostgreSQL",
        },
        {
            "question": "What is SQLAlchemy used for?",
            "expected": "SQLAlchemy",
        },
    ]

    try:
        for case in evaluation_cases:
            chunks = search_similar_chunks(
                question=case["question"],
                user_id=1,
                db=db,
                limit=3,
            )

            assert len(chunks) > 0
            assert any(
                case["expected"] in chunk.content
                for chunk in chunks
            )

    finally:
        db.close()


def test_rag_rejects_unknown_information():
    db = SessionLocal()

    try:

        chunks = search_similar_chunks(
            question="Who is the president of the United States?",
            user_id = 1,
            db=db,
            limit=3,
        )

        assert chunks == []

    finally:
        db.close()
