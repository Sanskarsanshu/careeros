import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SectionType(str, enum.Enum):
    personal = "personal"
    summary = "summary"
    experience = "experience"
    education = "education"
    projects = "projects"
    skills = "skills"
    certifications = "certifications"
    achievements = "achievements"
    publications = "publications"
    links = "links"
    custom = "custom"


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    target_job_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    template_id: Mapped[str] = mapped_column(String(255), default="classic", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="resumes")
    versions: Mapped[list["ResumeVersion"]] = relationship("ResumeVersion", back_populates="resume", cascade="all, delete-orphan")
    sections: Mapped[list["ResumeSection"]] = relationship("ResumeSection", back_populates="resume", cascade="all, delete-orphan")
    personal_info: Mapped["PersonalInfo"] = relationship("PersonalInfo", back_populates="resume", cascade="all, delete-orphan", uselist=False)
    experiences: Mapped[list["Experience"]] = relationship("Experience", back_populates="resume", cascade="all, delete-orphan")
    educations: Mapped[list["Education"]] = relationship("Education", back_populates="resume", cascade="all, delete-orphan")
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="resume", cascade="all, delete-orphan")
    skills: Mapped[list["Skill"]] = relationship("Skill", back_populates="resume", cascade="all, delete-orphan")
    certifications: Mapped[list["Certification"]] = relationship("Certification", back_populates="resume", cascade="all, delete-orphan")
    achievements: Mapped[list["Achievement"]] = relationship("Achievement", back_populates="resume", cascade="all, delete-orphan")
    publications: Mapped[list["Publication"]] = relationship("Publication", back_populates="resume", cascade="all, delete-orphan")
    links: Mapped[list["Link"]] = relationship("Link", back_populates="resume", cascade="all, delete-orphan")
    custom_sections: Mapped[list["CustomSection"]] = relationship("CustomSection", back_populates="resume", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Resume id={self.id} title={self.title} user_id={self.user_id}>"


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    label: Mapped[str | None] = mapped_column(Text, nullable=True)
    snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="versions")

    __table_args__ = (
        UniqueConstraint("resume_id", "version_number", name="uq_resume_version_number"),
    )


class ResumeSection(Base):
    __tablename__ = "resume_sections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    section_type: Mapped[SectionType] = mapped_column(Enum(SectionType, name="sectiontype"), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="sections")


class PersonalInfo(Base):
    __tablename__ = "personal_info"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    professional_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(Text, nullable=True)
    linkedin: Mapped[str | None] = mapped_column(Text, nullable=True)
    github: Mapped[str | None] = mapped_column(Text, nullable=True)
    website: Mapped[str | None] = mapped_column(Text, nullable=True)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="personal_info")


class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    company: Mapped[str] = mapped_column(Text, nullable=False)
    position: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    bullets: Mapped[list | dict | None] = mapped_column(JSONB, default=list, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="experiences")


class Education(Base):
    __tablename__ = "educations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    institution: Mapped[str] = mapped_column(Text, nullable=False)
    degree: Mapped[str | None] = mapped_column(Text, nullable=True)
    field: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    gpa: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="educations")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str | None] = mapped_column(Text, nullable=True)
    technologies: Mapped[list | dict | None] = mapped_column(JSONB, nullable=True)
    link: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    bullets: Mapped[list | dict | None] = mapped_column(JSONB, default=list, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="projects")


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    proficiency: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="skills")


class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    issuer: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_issued: Mapped[date | None] = mapped_column(Date, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="certifications")


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="achievements")


class Publication(Base):
    __tablename__ = "publications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    publisher: Mapped[str | None] = mapped_column(Text, nullable=True)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="publications")


class Link(Base):
    __tablename__ = "links"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="links")


class CustomSection(Base):
    __tablename__ = "custom_sections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    resume: Mapped["Resume"] = relationship("Resume", back_populates="custom_sections")
