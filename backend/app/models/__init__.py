from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    seclevel = Column(String(20), nullable=False, default="user")
    full_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password: str):
        from app.core.security import get_password_hash
        self.password = get_password_hash(password)

    def verify_password(self, password: str) -> bool:
        from app.core.security import verify_password
        return verify_password(password, self.password)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_type = Column(String(20), nullable=False, index=True)  # 'warid' (وارد) or 'sadir' (صادر)
    doc_number = Column(String(50), nullable=False, unique=True, index=True)
    subject = Column(Text, nullable=False)
    source = Column(String(200), nullable=True)
    destination = Column(String(200), nullable=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    content = Column(Text, nullable=True)
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_type = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False, default="new")
    priority = Column(String(20), nullable=False, default="normal")  # low, normal, high, urgent
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    creator = relationship("User", backref="documents")

    def __repr__(self):
        return f"<Document {self.doc_number} - {self.doc_type}>"


class DocumentHistory(Base):
    __tablename__ = "document_history"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False)  # created, updated, deleted, status_changed
    action_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    document = relationship("Document", backref="history")
    actor = relationship("User", foreign_keys=[action_by])

    def __repr__(self):
        return f"<History {self.action} on doc {self.document_id}>"