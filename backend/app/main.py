from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import components, nlp, compatibility, recommendation, builds, performance

app = FastAPI(
    title="PC Builder API",
    description="API for PC component compatibility and recommendations",
    version="0.1.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(components.router)
app.include_router(nlp.router)
app.include_router(compatibility.router)
app.include_router(recommendation.router)
app.include_router(builds.router)
app.include_router(performance.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the PC Builder API",
        "status": "running",
        "note": "If you're having issues with the frontend, ensure this backend server is running on http://localhost:8000 and CORS is enabled."
    }