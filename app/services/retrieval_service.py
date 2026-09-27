from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding

def search_similar_chunks(
        question: str,
        user_id: int,
        db: Session,
        limit: int = 5,
) -> list[DocumentChunk]:
    question_embedding = generate_embedding(question)

    statment = (
        select(DocumentChunk)
        .join(DocumentChunk.document)
        .where(
            DocumentChunk.document.has(user_id=user_id)
        )
        .order_by(
            DocumentChunk.embedding.cosine_distance(question_embedding)
        )
        .limit(limit)
    )

    return list(db.scalars(statment).all())

