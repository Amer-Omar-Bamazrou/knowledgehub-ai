from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.ai import AIGenerateRequest, AIGenerateResponse
from app.services.ai_service import generate_response
from app.services.knowledge_service import ask_knowledge_base


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/generate",
    response_model=AIGenerateResponse,
)
def generate_ai_response(
    request: AIGenerateRequest,
    current_user: User = Depends(get_current_user),
):
    response = generate_response(request.prompt)

    return AIGenerateResponse(
        response=response,
    )


@router.post(
    "/ask",
    response_model=AIGenerateResponse,
)
def ask_ai(
    request: AIGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = ask_knowledge_base(
        question=request.prompt,
        user_id=current_user.id,
        db=db,
    )

    return AIGenerateResponse(
        response=response,
    )