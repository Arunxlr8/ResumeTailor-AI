"""FastAPI application entry point.

Initializes the FastAPI application, registers CORS middleware, includes the
workflow router, and defines basic health check routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.workflow import router as workflow_router

app = FastAPI(
    title="Agentic Resume Tailor",
    version="1.0.0",
    description="An AI-powered agentic system that tailors resumes using LangGraph."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(workflow_router)


@app.get("/")
async def health() -> dict[str, str]:
    """Provide a basic health status check for the API service.

    Parameters:
        None.

    Returns:
        dict[str, str]: Status message showing the service status.
    """
    return {
        "status": "running",
        "service": "Agentic Resume Tailor"
    }