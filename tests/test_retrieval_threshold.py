from app.db.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.retrieval_service import search_similar_chunks


def test_relevant_question_returns_chunks():
    db = SessionLocal()

    try:
        chunks = search_similar_chunks(
            question="What framework is used to build the API?",
            user_id=1,
            db=db,
            limit=3,
        )

        assert len(chunks) > 0
        assert any("FastAPI" in chunk.content for chunk, distance in chunks)

    finally:
        db.close()


def test_irrelevant_question_returns_no_chunks():
    db = SessionLocal()

    try:
        chunks = search_similar_chunks(
            question="What is the capital of France?",
            user_id=1,
            db=db,
            limit=3,
        )

        assert chunks == []

    finally:
        db.close()