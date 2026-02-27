from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline.graph import run_investigation
import os

app = FastAPI(title="TrueLens API")

# ---- CORS (allow your local + Vercel frontend) ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",            # Vite local
        "http://localhost:3000",            # React local (if used)
        "https://truelens-silk.vercel.app",  # Vercel prod
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Request Schema ----
class AnalyzeRequest(BaseModel):
    input_type: str  # "text" or "url"
    content: str     # article text or URL

# ---- Health Check ----
@app.get("/health")
def health():
    return {"status": "TrueLens backend is running"}

# ---- Main API ----
@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    print("\n" + "=" * 50)
    print("New investigation started")
    print(f"Input type: {request.input_type}")
    print(f"Content preview: {request.content[:100]}...")
    print("=" * 50)

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

# ---- Local run (Render will use its own start command) ----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
