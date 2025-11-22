"""
SQLAlchemy database model for tasks.
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UUID, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from data.database import Base
import uuid



class TaskModel(Base):
    """SQLAlchemy model for Task table."""
    __tablename__ = "tasks"

    uuid: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="todo", nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    # Relationship to project
    project = relationship("ProjectModel", back_populates="tasks")

    def __repr__(self):
        return f"<TaskModel(uuid={self.uuid}, title={self.title}, status={self.status})>"