
import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.router import route_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM Request Router API",
    description="Client-facing API for the AI assistant",
    version="1.0.0",
)

# Allow the GitHub Pages website and local development.
allowed_origins = [
    "https://srinivasmalla1980.github.io",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# Optionally configure additional origins through an environment variable.
extra_origin = os.getenv("FRONTEND_ORIGIN")
if extra_origin:
    allowed_origins.append(extra_origin.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    answer: str
    route: str
    reason: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question.",
        )

    try:
        result = route_request(question)

        return ChatResponse(
            answer=str(result.get("answer", "")),
            route=str(result.get("route", "UNKNOWN")),
            reason=str(result.get("reason", "")),
        )

    except Exception:
        # Keep internal errors and implementation details out of
        # the public response. Full details remain in server logs.
        logger.exception("Failed to process chat request")

        raise HTTPException(
            status_code=502,
            detail="The AI service could not process your request. Please try again.",
        )
