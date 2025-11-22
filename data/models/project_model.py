"""
SQLAlchemy database model for project.
"""
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, BigInteger
from sqlalchemy.orm import relationship
from data.database import Base


class ProjectModel(Base):
    """SQLAlchemy model for Project table."""
    __tablename__ = "projects"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    # Relationship to tasks
    tasks = relationship("TaskModel", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProjectModel(id={self.id}, name={self.name})>"