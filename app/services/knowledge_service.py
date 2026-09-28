from sqlalchemy.orm import Session

from app.services.ai_service import generate_response
from app.services.retrieval_service import search_similar_chunks


def ask_knowledge_base(
        question: str,
        user_id: int,
        db: Session,
) -> str:
    chunks = search_similar_chunks(
        question=question,
        user_id=user_id,
        db=db,
        limit=5,
    )

    if not chunks:
        return "I could not find the answer in your documents."

    context = "\n\n".join(
        f"Document chunk:\n{chunk.content}"
        for chunk in chunks
    )

    prompt = f"""
Use the document context below to answer the user's question.

Document context:
{context}

Question:
{question}

Answer briefly using only the document context.
"""


    return generate_response(prompt)
