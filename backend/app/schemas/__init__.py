from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    seclevel: str = "user"

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None
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
    source: Optional[str] = None
    destination: Optional[str] = None
    date: datetime
    content: Optional[str] = None
    priority: str = "normal"
    notes: Optional[str] = None

class DocumentUpdate(BaseModel):
    subject: Optional[str] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None

class DocumentResponse(BaseModel):
    id: int
    doc_type: str
    doc_number: str
    subject: str
    source: Optional[str] = None
    destination: Optional[str] = None
    date: datetime
    content: Optional[str] = None
    priority: str
    notes: Optional[str] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    status: str
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True
