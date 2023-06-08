from flask_openapi3 import FileStorage
from pydantic import BaseModel, Field


class PageModel(BaseModel):
    page: int = Field(1, ge=1, description="Page")
    page_size: int = Field(15, ge=1, description="Page size")


class IdModel(BaseModel):
    id: int = Field(..., description="ID")


class FileModel(BaseModel):
    file: FileStorage


class JsonResponse(BaseModel):
    code: int = Field(default=0, description="Code")
    message: str = Field(default="ok", description="Message")
