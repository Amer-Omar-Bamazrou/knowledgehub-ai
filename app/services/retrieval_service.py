from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding

RELEVANCE_THRESHOLD = 0.50

def search_similar_chunks(
        question: str,
        user_id: int,
        db: Session,
        limit: int = 5,
) -> list[tuple[DocumentChunk, float]]:
    question_embedding = generate_embedding(question)


    distance = DocumentChunk.embedding.cosine_distance(question_embedding)

    statement = (
        select(DocumentChunk, distance.label("distance"))
        .join(DocumentChunk.document)
        .where(
            DocumentChunk.document.has(user_id=user_id)
        )
        .order_by(
            distance
        )
        .limit(limit)
    )

    results = db.execute(statement).all()

    relevant_chunks = [
        (chunk, float(distance_value))
        for chunk, distance_value in results
        if distance_value <= RELEVANCE_THRESHOLD
    ]

    return relevant_chunks