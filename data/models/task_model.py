"""
SQLAlchemy database model for tasks.
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, BigInteger
from sqlalchemy.orm import relationship
from data.database import Base



class TaskModel(Base):
    """SQLAlchemy model for Task table."""
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="todo", nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    # Relationship to project
    project = relationship("ProjectModel", back_populates="tasks")

    def __repr__(self):
        return f"<TaskModel(id={self.id}, title={self.title}, status={self.status})>"