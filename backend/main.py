from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline.graph import run_investigation

app = FastAPI(title="TrueLens API")

# Allow React frontend to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request format
class AnalyzeRequest(BaseModel):
    input_type: str  # "text" or "url"
    content: str     # article text or URL

@app.get("/health")
def health():
    return {"status": "TrueLens backend is running"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    print(f"\n{'='*50}")
    print(f"New investigation started")
    print(f"Input type: {request.input_type}")
    print(f"Content preview: {request.content[:100]}...")
    print(f"{'='*50}")

    result = run_investigation(request.input_type, request.content)

    return {
        "verdict":          result["verdict"],
        "verdict_type":     result["verdict_type"],
        "total_score":      result["total_score"],
        "confidence":       result["confidence"],
        "fact_check_score": result["fact_check_score"],
        "image_score":      result["image_score"],
        "language_score":   result["language_score"],
        "explanation":      result["explanation"],
        "flags":            result["flags"]
    }