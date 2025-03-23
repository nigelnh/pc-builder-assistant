from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import components, nlp, compatibility

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
@app.get("/")
def read_root():
    return {"message": "Welcome to the PC Builder API!"}