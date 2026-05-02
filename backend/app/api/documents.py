from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin, get_current_user
from app.db.database import get_db
from app.models import Document, DocumentHistory, User
from app.schemas import DocumentCreate, DocumentResponse, DocumentUpdate

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/", response_model=DocumentResponse)
def create_document(document: DocumentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(Document).filter(Document.doc_number == document.doc_number).first():
        raise HTTPException(status_code=400, detail="رقم المستند موجود بالفعل")
    new_doc = Document(**document.model_dump(), created_by=current_user.id)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    db.add(DocumentHistory(document_id=new_doc.id, action="created", action_by=current_user.id, new_value=new_doc.subject))
    db.commit()
    return DocumentResponse.model_validate(new_doc)


@router.get("/", response_model=list[DocumentResponse])
def list_documents(doc_type: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = db.query(Document)
    if doc_type:
        q = q.filter(Document.doc_type == doc_type)
    return q.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/search", response_model=list[DocumentResponse])
def search_documents(doc_type: str | None = None, search_term: str | None = None, priority: str | None = None, doc_status: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = db.query(Document)
    if doc_type:
        q = q.filter(Document.doc_type == doc_type)
    if search_term:
        p = f"%{search_term}%"
        q = q.filter(or_(Document.subject.ilike(p), Document.content.ilike(p), Document.source.ilike(p), Document.destination.ilike(p), Document.doc_number.ilike(p)))
    if priority:
        q = q.filter(Document.priority == priority)
    if doc_status:
        q = q.filter(Document.status == doc_status)
    return q.order_by(Document.created_at.desc()).all()


@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="المستند غير موجود")
    return DocumentResponse.model_validate(doc)


@router.put("/{doc_id}", response_model=DocumentResponse)
def update_document(doc_id: int, document: DocumentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="المستند غير موجود")
    old = f"status:{doc.status}, priority:{doc.priority}"
    for key, value in document.model_dump(exclude_unset=True).items():
        setattr(doc, key, value)
    db.commit()
    db.refresh(doc)
    db.add(DocumentHistory(document_id=doc.id, action="updated", action_by=current_user.id, old_value=old))
    db.commit()
    return DocumentResponse.model_validate(doc)


@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="المستند غير موجود")
    db.query(DocumentHistory).filter(DocumentHistory.document_id == doc_id).delete()
    db.delete(doc)
    db.commit()
    return {"message": "تم حذف المستند بنجاح"}


@router.get("/{doc_id}/history")
def get_document_history(doc_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(DocumentHistory).filter(DocumentHistory.document_id == doc_id).all()
