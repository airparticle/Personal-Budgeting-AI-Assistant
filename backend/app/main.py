import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to allow 'app' to be recognized as a module
# regardless of where this script is executed from.
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.api import api_router
from app.ml.engine import predictor


# 1. Define Startup/Shutdown Logic (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    print("Startup: Initializing ML Models...")
    # The predictor is already instantiated in ml/engine.py, 
    # but we check its status here to ensure it loaded correctly.
    if predictor.model:
        print("ML Engine: Model loaded successfully.")
    else:
        print("ML Engine: Running in Mock Mode (No model file found).")

    yield  # The application runs here

    # --- Shutdown ---
    print("Shutdown: Cleaning up resources...")
    # Add any cleanup code here (e.g., closing DB pools if not handled by SQLAlchemy)


# 2. Initialize the App
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# 3. Configure CORS (Cross-Origin Resource Sharing)
# This is CRITICAL for your React Frontend to communicate with this Backend.
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],
)

# 4. Include the Routers
app.include_router(api_router, prefix=settings.API_V1_STR)


# 5. Root endpoint (Health Check)
@app.get("/")
def read_root():
    return {
        "message": "Finance AI Assistant API is running",
        "docs_url": "/docs"
    }