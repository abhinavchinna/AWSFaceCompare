from fastapi import FastAPI
from api.endpoints import compare_faces
import uvicorn

app = FastAPI()

app.include_router(compare_faces.router, prefix="/api/v1/compare_faces", tags=["compare_faces"])
uvicorn.run(app, host="0.0.0.0", port=8000)