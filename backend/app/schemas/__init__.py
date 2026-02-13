from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    seclevel: str = "user"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class DocumentBase(BaseModel):
    doc_type: str  # 'warid' or 'sadir'
    doc_number: str
    subject: str
    source: Optional[str] = None
    destination: Optional[str] = None
    date: datetime
    content: Optional[str] = None
    priority: str = "normal"
    notes: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    subject: Optional[str] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: int
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    status: str
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentSearch(BaseModel):
    doc_type: Optional[str] = None
    search_term: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class MessageResponse(BaseModel):
    message: str
    success: bool
    data: Optional[dict] = None