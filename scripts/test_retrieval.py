from app.db.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.retrieval_service import search_similar_chunks


def main():
    db = SessionLocal()

    try:
        chunks = search_similar_chunks(
            question="What framework is used to build the API?",
            user_id=1,
            db=db,
            limit=3,
        )

        print(f"Found {len(chunks)} relevant chunks.")

        for chunk in chunks:
            print("\n--- Chunk ---")
            print(f"ID: {chunk.id}")
            print(f"Document ID: {chunk.document_id}")
            print(f"Distance: not displayed yet")
            print(f"Content: {chunk.content}")

    finally:
        db.close()


if __name__ == "__main__":
    main()