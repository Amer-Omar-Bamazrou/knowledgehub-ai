from app.db.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.retrieval_service import search_similar_chunks


EVALUATION_CASES = [
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
    {
        "question": "Who is the president of the United States?",
        "expected": None,
    },
]


def evaluate_rag():
    db = SessionLocal()

    passed = 0

    try:
        for case in EVALUATION_CASES:
            chunks = search_similar_chunks(
                question=case["question"],
                user_id=1,
                db=db,
                limit=3,
            )

            if case["expected"] is None:
                success = len(chunks) == 0
            else:
                success = any(
                    case["expected"] in chunk.content
                    for chunk in chunks
                )

            if success:
                passed += 1
                print(f"PASS: {case['question']}")
            else:
                print(f"FAIL: {case['question']}")

    finally:
        db.close()

    total = len(EVALUATION_CASES)
    accuracy = (passed / total) * 100

    print()
    print("RAG Evaluation")
    print("--------------")
    print(f"Total cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Retrieval accuracy: {accuracy:.1f}%")


if __name__ == "__main__":
    evaluate_rag()
