import os.path
import uuid
from http.client import HTTPException

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base

### Create FastAPI instance with custom docs and openapi url

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))
UPLOAD_PATH = f"{ROOT_PATH}/uploads/"
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


engine = create_engine(f"sqlite:///{ROOT_PATH}/db/db.sqlite", echo=True)

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    return {"message": "Hello from FastAPI"}

@app.get("/api/cv")
def get_all_cvs():
    return {
        "cvs": [
            {"id":"1", "name": "First CV", "path": "api/cv/download/0d9c50ac-5c51-4b18-9524-59382ce2ce18.pdf"},
            {"id":"2", "name": "Second CV", "path": "api/cv/download/2"},
            {"id":"3", "name": "Third CV", "path": "api/cv/download/3"},
            {"id":"4", "name": "Fourth CV", "path": "api/cv/download/4"},
        ],
    }

@app.get("/api/cv/{id}")
def get_cv(id: str):
    return {
        "id": "1",
        "name": "First CV",
        "description": "This is the first CV",
        "path": "/api/cv/download/4",
    }

@app.post("/api/cv")
async def post_cv(name: str, description: str, file: UploadFile):
    path = f"{uuid.uuid4()}.pdf"

    upload_file_path = f"{UPLOAD_PATH}/{path}"
    with open(upload_file_path, "wb") as out_file:
        while content := await file.read():
            out_file.write(content)

    return {"message": "CV created", "path": upload_file_path}

@app.get("/api/cv/download/{path}")
async def download_cv(path: str):
    file_location = os.path.join(UPLOAD_PATH, path)

    if not os.path.exists(file_location):
        raise HTTPException(404, "Not found")

    try:
        return FileResponse(
            file_location,
            media_type="application/octet-stream",
            filename=os.path.basename(path)  # Original filename for download
        )
    except Exception as e:
        raise HTTPException(500, str(e))

