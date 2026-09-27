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
You are an AI assistant for KnowledgeHub AI.

Answer the user's question using only the provided documents context.

If the answer cannot be found in the provided context, say:
"I could not find the answer in your documents."

Document context:
{context}

User question:
{question}
"""

    return generate_response(prompt)