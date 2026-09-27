from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.chunking_service import chunk_text
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/", response_model=DocumentResponse, status_code=201)
async def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_document = Document(
        title=document.title,
        content=document.content,
        user_id=current_user.id,
    )

    db.add(new_document)
    db.flush()

    chunks = chunk_text(document.content)

    for index, content in enumerate(chunks):
        embedding = generate_embedding(content)

        chunk = DocumentChunk(
            document_id=new_document.id,
            chunk_index=index,
            content=content,
            embedding=embedding,
        )

        db.add(chunk)

    db.commit()
    db.refresh(new_document)

    return new_document


@router.get(
    "/",
    response_model=list[DocumentResponse],
)
async def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = db.execute(
        select(Document).where(
            Document.user_id == current_user.id
        )
    )

    return result.scalars().all()


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == current_user.id,
        )
    ).scalar_one_or_none()

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return document