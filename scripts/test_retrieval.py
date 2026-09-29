from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding


def run_retrieval_test(question: str):
    db = SessionLocal()

    try:
        question_embedding = generate_embedding(question)

        distance = DocumentChunk.embedding.cosine_distance(question_embedding)

        statement = (
            select(DocumentChunk, distance.label("distance"))
            .join(DocumentChunk.document)
            .where(
                DocumentChunk.document.has(user_id=1)
            )
            .order_by(distance)
            .limit(3)
        )

        results = db.execute(statement).all()

        print(f"\nQuestion: {question}")

        for chunk, distance_value in results:
            print("\n--- Result ---")
            print(f"Chunk ID: {chunk.id}")
            print(f"Distance: {distance_value:.4f}")
            print(f"Content: {chunk.content}")

    finally:
        db.close()


if __name__ == "__main__":
    run_retrieval_test("What framework is used to build the API?")
    run_retrieval_test("What database does the application use?")
    run_retrieval_test("What ORM is used in the project?")
    run_retrieval_test("What programming language is mentioned?")
    run_retrieval_test("What is the capital of France?")
    run_retrieval_test("How do I make a chocolate cake?")
    run_retrieval_test("What is the weather today?")