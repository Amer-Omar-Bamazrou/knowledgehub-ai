from sqlalchemy.orm import Session

from app.services.ai_service import generate_response
from app.services.retrieval_service import search_similar_chunks


def ask_knowledge_base(
    question: str,
    user_id: int,
    db: Session,
) -> tuple[str, list[dict]]:
    chunks = search_similar_chunks(
        question=question,
        user_id=user_id,
        db=db,
        limit=5,
    )

    if not chunks:
        return (
            "I could not find the answer in your documents.",
            [],
        )

    context = "\n\n".join(
        f"Document: {chunk.document.title}\n"
        f"Document chunk:\n{chunk.content}"
        for chunk, _distance in chunks
    )

    prompt = f"""
Use the document context below to answer the user's question.

Document context:
{context}

Question:
{question}

Answer briefly using only the document context.
"""

    response = generate_response(prompt)

    sources = [
        {
            "document_id": chunk.document_id,
            "document_title": chunk.document.title,
            "chunk_id": chunk.id,
            "distance": distance,
        }
        for chunk, distance in chunks
    ]

    return response, sources