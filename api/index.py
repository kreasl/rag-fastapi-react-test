import os.path
import uuid
from http.client import HTTPException

from fastapi import Depends, FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db
from .models import Application

models.Application.metadata.create_all(bind=engine)

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

@app.get("/api/applications")
def get_applications(db: Session = Depends(get_db)):
    applications = crud.get_applications(db)
    return applications

@app.get("/api/application/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = crud.get_application(db, application_id)
    return application

@app.post("/api/application")
async def create_application(name: str = Form(...), description: str = Form(...), file: UploadFile = None):
    path = f"{uuid.uuid4()}.pdf"

    upload_file_path = f"{UPLOAD_PATH}/{path}"

    try:
        with open(upload_file_path, "wb") as out_file:
            while content := await file.read():
                out_file.write(content)

        db = SessionLocal()
        application = Application(
            name=name,
            description=description,
            path=path
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return {"message": "Application created", "application": application}
    except Exception as e:
        if os.path_exists(upload_file_path):
            os.remove(upload_file_path)

        raise HTTPException(500, str(e))
    finally:
        db.close()

@app.get("/api/cv/{path}")
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

