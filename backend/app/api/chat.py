from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.rag.rag_pipeline import answer_question

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    question: str
    mode: str = "simple"


@router.post("/")
def chat(request: ChatRequest):

    try:
        result = answer_question(
            question=request.question,
            mode=request.mode
        )

        return {
            "status": "success",
            "question": request.question,
            "mode": request.mode,
            "answer": result["answer"],
            "sources": result["sources"],
            "graph_context": result["graph_context"]
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {error}"
        )