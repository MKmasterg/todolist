"""
SQLAlchemy database model for project.
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from data.database import Base


class ProjectModel(Base):
    """SQLAlchemy model for Project table."""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    # Relationship to tasks
    tasks = relationship("TaskModel", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProjectModel(id={self.id}, name={self.name})>"