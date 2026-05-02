from datetime import datetime

from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str | None = None
    seclevel: str = "user"

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str | None = None
    seclevel: str
    created_at: datetime
    is_active: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class DocumentCreate(BaseModel):
    doc_type: str
    doc_number: str
    subject: str
    source: str | None = None
    destination: str | None = None
    date: datetime
    content: str | None = None
    priority: str = "normal"
    notes: str | None = None

class DocumentUpdate(BaseModel):
    subject: str | None = None
    source: str | None = None
    destination: str | None = None
    content: str | None = None
    status: str | None = None
    priority: str | None = None
    notes: str | None = None

class DocumentResponse(BaseModel):
    id: int
    doc_type: str
    doc_number: str
    subject: str
    source: str | None = None
    destination: str | None = None
    date: datetime
    content: str | None = None
    priority: str
    notes: str | None = None
    file_name: str | None = None
    file_type: str | None = None
    status: str
    created_by: int
    created_at: datetime
    updated_at: datetime | None = None
    class Config:
        from_attributes = True
