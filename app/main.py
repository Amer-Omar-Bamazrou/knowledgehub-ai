from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.api.auth import router as auth_router



app = FastAPI(
    title="KnowledgeHub AI",
    description="Production-ready AI Backend",
    version="0.1.0"
)

app.include_router(documents_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to KnowledgeHub AI!"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }