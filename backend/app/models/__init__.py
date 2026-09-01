"""
CareerOS — SQLAlchemy Models Initialization

Import all models here so Alembic can discover them.
"""
from app.core.database import Base
from app.models.user import User
from app.models.resume import (
    Resume, ResumeVersion, ResumeSection, PersonalInfo, Experience, 
    Education, Project, Skill, Certification, Achievement, 
    Publication, Link, CustomSection, SectionType
)

# This ensures Base and all models are imported for metadata
__all__ = [
    "Base", "User", "Resume", "ResumeVersion", "ResumeSection",
    "PersonalInfo", "Experience", "Education", "Project", "Skill",
    "Certification", "Achievement", "Publication", "Link", "CustomSection"
]
