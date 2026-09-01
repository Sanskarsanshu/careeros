from datetime import date, datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, EmailStr, AnyUrl

from app.models.resume import SectionType


# ---------------------------------------------------------
# Base / Common Mixins
# ---------------------------------------------------------

class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class OrderedEntityUpdate(BaseModel):
    """Schema for updating a single entry's order or visibility"""
    display_order: Optional[int] = Field(None, ge=0)


class EntryOrderUpdate(BaseModel):
    """Schema for updating the order of multiple entries at once"""
    entry_ids: List[UUID]


class SectionOrderUpdate(BaseModel):
    """Schema for updating the order of sections"""
    sections: List[SectionType]


# ---------------------------------------------------------
# ResumeSection
# ---------------------------------------------------------

class ResumeSectionResponse(BaseModel):
    id: UUID
    section_type: SectionType
    display_order: int
    is_visible: bool

    model_config = ConfigDict(from_attributes=True)


class ResumeSectionUpdate(BaseModel):
    is_visible: Optional[bool] = None


# ---------------------------------------------------------
# PersonalInfo
# ---------------------------------------------------------

class PersonalInfoBase(BaseModel):
    full_name: str
    professional_title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class PersonalInfoCreate(PersonalInfoBase):
    pass


class PersonalInfoUpdate(BaseModel):
    full_name: Optional[str] = None
    professional_title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class PersonalInfoResponse(PersonalInfoBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Experience
# ---------------------------------------------------------

class ExperienceBase(BaseModel):
    company: str
    position: str
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None
    bullets: Optional[List[str]] = None


class ExperienceResponse(ExperienceBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Education
# ---------------------------------------------------------

class EducationBase(BaseModel):
    institution: str
    degree: Optional[str] = None
    field: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    gpa: Optional[str] = None
    description: Optional[str] = None


class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    gpa: Optional[str] = None
    description: Optional[str] = None


class EducationResponse(EducationBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Project
# ---------------------------------------------------------

class ProjectBase(BaseModel):
    name: str
    role: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    link: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    technologies: Optional[List[str]] = None
    link: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    bullets: Optional[List[str]] = None


class ProjectResponse(ProjectBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Skill
# ---------------------------------------------------------

class SkillBase(BaseModel):
    category: str
    name: str
    proficiency: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    proficiency: Optional[str] = None


class SkillResponse(SkillBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Certification
# ---------------------------------------------------------

class CertificationBase(BaseModel):
    name: str
    issuer: Optional[str] = None
    date_issued: Optional[date] = None
    url: Optional[str] = None


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    date_issued: Optional[date] = None
    url: Optional[str] = None


class CertificationResponse(CertificationBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Achievement
# ---------------------------------------------------------

class AchievementBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: Optional[date] = None


class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None


class AchievementResponse(AchievementBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Publication
# ---------------------------------------------------------

class PublicationBase(BaseModel):
    title: str
    publisher: Optional[str] = None
    date: Optional[date] = None
    url: Optional[str] = None
    description: Optional[str] = None


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(BaseModel):
    title: Optional[str] = None
    publisher: Optional[str] = None
    date: Optional[date] = None
    url: Optional[str] = None
    description: Optional[str] = None


class PublicationResponse(PublicationBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Link
# ---------------------------------------------------------

class LinkBase(BaseModel):
    name: str
    url: str


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None


class LinkResponse(LinkBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# CustomSection
# ---------------------------------------------------------

class CustomSectionBase(BaseModel):
    title: str
    description: Optional[str] = None


class CustomSectionCreate(CustomSectionBase):
    pass


class CustomSectionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class CustomSectionResponse(CustomSectionBase):
    id: UUID
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Resume (Parent Entity)
# ---------------------------------------------------------

class ResumeBase(BaseModel):
    title: str
    target_job_title: Optional[str] = None
    summary: Optional[str] = None
    template_id: str = "classic"
    is_active: bool = True


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    target_job_title: Optional[str] = None
    summary: Optional[str] = None
    template_id: Optional[str] = None
    is_active: Optional[bool] = None


class ResumeResponse(ResumeBase, TimestampSchema):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ResumeListItem(ResumeResponse):
    pass


class FullResumeResponse(ResumeResponse):
    personal_info: Optional[PersonalInfoResponse] = None
    sections: List[ResumeSectionResponse] = []
    experiences: List[ExperienceResponse] = []
    educations: List[EducationResponse] = []
    projects: List[ProjectResponse] = []
    skills: List[SkillResponse] = []
    certifications: List[CertificationResponse] = []
    achievements: List[AchievementResponse] = []
    publications: List[PublicationResponse] = []
    links: List[LinkResponse] = []
    custom_sections: List[CustomSectionResponse] = []

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------
# Resume Versioning
# ---------------------------------------------------------

class ResumeVersionCreate(BaseModel):
    label: Optional[str] = None


class ResumeVersionResponse(BaseModel):
    id: UUID
    version_number: int
    label: Optional[str] = None
    snapshot: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
