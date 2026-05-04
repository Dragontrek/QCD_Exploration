from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.api import router as api_router
import os

app = FastAPI(title="QCD API")

# Include the backend API routes
app.include_router(api_router, prefix="/api")

# Get absolute path to frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

# Serve specific HTML files
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/add")
async def serve_add():
    return FileResponse(os.path.join(FRONTEND_DIR, "add.html"))

# Mount the static files (css, js, images) from the frontend directory
app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
