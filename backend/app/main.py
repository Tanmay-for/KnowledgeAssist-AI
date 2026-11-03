
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.api.upload import router as upload_router
from backend.app.api.chat import router as chat_router
from backend.app.api.graph import router as graph_router
from backend.app.api.documents import router as documents_router


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Intelligent Document-Based Knowledge Assistant",
    version="1.0.0"
)


# Allow communication with React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(graph_router)
app.include_router(documents_router)

# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to KnowledgeAssist AI!",
        "status": "Backend is running"
    }


# Health check route
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": settings.APP_NAME
    }
