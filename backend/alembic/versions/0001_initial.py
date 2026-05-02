"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-02 14:00:00.000000
"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("seclevel", sa.String(20), nullable=False, server_default="user"),
        sa.Column("full_name", sa.String(100)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "documents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("doc_type", sa.String(20), nullable=False, index=True),
        sa.Column("doc_number", sa.String(50), nullable=False, unique=True),
        sa.Column("subject", sa.Text, nullable=False),
        sa.Column("source", sa.String(200)),
        sa.Column("destination", sa.String(200)),
        sa.Column("date", sa.DateTime(timezone=True), nullable=False, index=True),
        sa.Column("content", sa.Text),
        sa.Column("file_path", sa.String(500)),
        sa.Column("file_name", sa.String(255)),
        sa.Column("file_type", sa.String(50)),
        sa.Column("status", sa.String(50), nullable=False, server_default="new"),
        sa.Column("priority", sa.String(20), nullable=False, server_default="normal"),
        sa.Column("notes", sa.Text),
        sa.Column("created_by", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )

    op.create_table(
        "document_history",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("document_id", sa.Integer, sa.ForeignKey("documents.id"), nullable=False, index=True),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("action_by", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("action_at", sa.DateTime(timezone=True), server_default=sa.func.now(), index=True),
        sa.Column("old_value", sa.Text),
        sa.Column("new_value", sa.Text),
        sa.Column("notes", sa.Text),
    )


def downgrade() -> None:
    op.drop_table("document_history")
    op.drop_table("documents")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")
