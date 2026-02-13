from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import aiofiles

from app.db.database import get_db
from app.models import Document, DocumentHistory
from app.schemas import DocumentCreate, DocumentUpdate, DocumentResponse, DocumentSearch
from app.api.dependencies import get_current_user, get_current_admin
from app.models import User

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """إنشاء مستند جديد (وارد أو صادر)"""

    # Check if doc_number already exists
    existing = db.query(Document).filter(Document.doc_number == document.doc_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رقم المستند موجود بالفعل"
        )

    new_doc = Document(
        **document.model_dump(),
        created_by=current_user.id
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Add to history
    history = DocumentHistory(
        document_id=new_doc.id,
        action="created",
        action_by=current_user.id,
        new_value=f"Document created: {new_doc.subject}"
    )
    db.add(history)
    db.commit()

    return DocumentResponse.model_validate(new_doc)


@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    doc_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """عرض جميع المستندات"""

    query = db.query(Document)

    if doc_type:
        query = query.filter(Document.doc_type == doc_type)

    return query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/search", response_model=List[DocumentResponse])
def search_documents(
    doc_type: Optional[str] = None,
    search_term: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """بحث متقدم في المستندات"""

    query = db.query(Document)

    if doc_type:
        query = query.filter(Document.doc_type == doc_type)

    if search_term:
        pattern = f"%{search_term}%"
        query = query.filter(
            or_(
                Document.subject.ilike(pattern),
                Document.content.ilike(pattern),
                Document.source.ilike(pattern),
                Document.destination.ilike(pattern),
                Document.doc_number.ilike(pattern)
            )
        )

    if date_from:
        query = query.filter(Document.date >= date_from)

    if date_to:
        query = query.filter(Document.date <= date_to)

    if priority:
        query = query.filter(Document.priority == priority)

    if status:
        query = query.filter(Document.status == status)

    return query.order_by(Document.created_at.desc()).all()


@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """عرض تفاصيل مستند"""

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستند غير موجود"
        )

    return DocumentResponse.model_validate(doc)


@router.put("/{doc_id}", response_model=DocumentResponse)
def update_document(
    doc_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """تعديل مستند"""

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستند غير موجود"
        )

    # Store old values for history
    old_values = f"subject: {doc.subject}, status: {doc.status}, priority: {doc.priority}"

    # Update fields
    update_data = document.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(doc, key):
            setattr(doc, key, value)

    db.commit()
    db.refresh(doc)

    # Add to history
    history = DocumentHistory(
        document_id=doc.id,
        action="updated",
        action_by=current_user.id,
        old_value=old_values,
        new_value=f"Updated: {update_data}"
    )
    db.add(history)
    db.commit()

    return DocumentResponse.model_validate(doc)


@router.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """حذف مستند (مدير فقط)"""

    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="المستند غير موجود"
        )

    # Delete history first
    db.query(DocumentHistory).filter(DocumentHistory.document_id == doc_id).delete()
    db.delete(doc)
    db.commit()

    return {"message": "تم حذف المستند بنجاح"}


@router.get("/{doc_id}/history")
def get_document_history(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """عرض سجل تعديلات المستند"""

    history = db.query(DocumentHistory).filter(DocumentHistory.document_id == doc_id).all()
    return history