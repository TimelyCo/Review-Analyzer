from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

from agents.orchestrator import analyze_business

app = FastAPI(
    title="Review-Analyzer",
    description="API for business review analysis using Gemini and RAG",
    version="1.0.0"
)

# Configure CORS to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    business_name: str
    location: str = ""

@app.post("/api/analyze")
async def analyze_endpoint(request: AnalyzeRequest):
    try:
        result = analyze_business(request.business_name, request.location)
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("summary"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
