from app.db.database import SessionLocal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.embedding_service import generate_embedding


def backfill_embeddings():
    db = SessionLocal()

    try:
        chunks = (
            db.query(DocumentChunk)
            .filter(DocumentChunk.embedding.is_(None))
            .all()
        )

        print(f"Found {len(chunks)} chunks without embeddings.")

        for chunk in chunks:
            print(f"Generating embedding for chunk {chunk.id}...")

            chunk.embedding = generate_embedding(chunk.content)

        db.commit()

        print("Embedding backfill completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    backfill_embeddings()