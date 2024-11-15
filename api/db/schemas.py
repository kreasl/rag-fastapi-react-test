from pydantic import BaseModel

class ApplicationBase(BaseModel):
    name: str
    path: str

class ApplicationCreate(ApplicationBase):
    pass
