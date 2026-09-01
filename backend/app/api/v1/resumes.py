import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db
from app.models.resume import SectionType
from app.models.user import User
from app.schemas.resume import (
    AchievementCreate,
    AchievementResponse,
    AchievementUpdate,
    CertificationCreate,
    CertificationResponse,
    CertificationUpdate,
    CustomSectionCreate,
    CustomSectionResponse,
    CustomSectionUpdate,
    EducationCreate,
    EducationResponse,
    EducationUpdate,
    EntryOrderUpdate,
    ExperienceCreate,
    ExperienceResponse,
    ExperienceUpdate,
    FullResumeResponse,
    LinkCreate,
    LinkResponse,
    LinkUpdate,
    PersonalInfoCreate,
    PersonalInfoResponse,
    PersonalInfoUpdate,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    PublicationCreate,
    PublicationResponse,
    PublicationUpdate,
    ResumeCreate,
    ResumeListItem,
    ResumeResponse,
    ResumeUpdate,
    ResumeVersionCreate,
    ResumeVersionResponse,
    SectionOrderUpdate,
    SkillCreate,
    SkillResponse,
    SkillUpdate,
)
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["resumes"])

# ------------------------------------------------------------------------
# Resume Operations
# ------------------------------------------------------------------------

@router.post("", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    resume_in: ResumeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_resume(str(current_user.id), resume_in)


@router.get("", response_model=List[ResumeListItem])
async def list_resumes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.list_resumes(str(current_user.id))


@router.get("/{id}", response_model=FullResumeResponse)
async def get_resume(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.get_full_resume(id, str(current_user.id))


@router.put("/{id}", response_model=ResumeResponse)
async def update_resume(
    id: uuid.UUID,
    resume_in: ResumeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_resume(id, str(current_user.id), resume_in)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_resume(id, str(current_user.id))


# ------------------------------------------------------------------------
# Personal Info
# ------------------------------------------------------------------------

@router.put("/{id}/personal", response_model=PersonalInfoResponse)
async def update_personal_info(
    id: uuid.UUID,
    personal_in: PersonalInfoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_personal_info(id, str(current_user.id), personal_in)


# ------------------------------------------------------------------------
# Experience
# ------------------------------------------------------------------------

@router.post("/{id}/experience", response_model=ExperienceResponse, status_code=status.HTTP_201_CREATED)
async def add_experience(
    id: uuid.UUID,
    obj_in: ExperienceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_experience(id, str(current_user.id), obj_in)


@router.put("/{id}/experience/{entry_id}", response_model=ExperienceResponse)
async def update_experience(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: ExperienceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_experience(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/experience/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_experience(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Education
# ------------------------------------------------------------------------

@router.post("/{id}/education", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
async def add_education(
    id: uuid.UUID,
    obj_in: EducationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_education(id, str(current_user.id), obj_in)


@router.put("/{id}/education/{entry_id}", response_model=EducationResponse)
async def update_education(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: EducationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_education(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/education/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_education(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Projects
# ------------------------------------------------------------------------

@router.post("/{id}/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def add_project(
    id: uuid.UUID,
    obj_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_project(id, str(current_user.id), obj_in)


@router.put("/{id}/projects/{entry_id}", response_model=ProjectResponse)
async def update_project(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_project(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/projects/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_project(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Skills
# ------------------------------------------------------------------------

@router.post("/{id}/skills", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def add_skill(
    id: uuid.UUID,
    obj_in: SkillCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_skill(id, str(current_user.id), obj_in)


@router.put("/{id}/skills/{entry_id}", response_model=SkillResponse)
async def update_skill(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: SkillUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_skill(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/skills/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_skill(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Certifications
# ------------------------------------------------------------------------

@router.post("/{id}/certifications", response_model=CertificationResponse, status_code=status.HTTP_201_CREATED)
async def add_certification(
    id: uuid.UUID,
    obj_in: CertificationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_certification(id, str(current_user.id), obj_in)


@router.put("/{id}/certifications/{entry_id}", response_model=CertificationResponse)
async def update_certification(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: CertificationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_certification(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/certifications/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_certification(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_certification(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Achievements
# ------------------------------------------------------------------------

@router.post("/{id}/achievements", response_model=AchievementResponse, status_code=status.HTTP_201_CREATED)
async def add_achievement(
    id: uuid.UUID,
    obj_in: AchievementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_achievement(id, str(current_user.id), obj_in)


@router.put("/{id}/achievements/{entry_id}", response_model=AchievementResponse)
async def update_achievement(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: AchievementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_achievement(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/achievements/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_achievement(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_achievement(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Publications
# ------------------------------------------------------------------------

@router.post("/{id}/publications", response_model=PublicationResponse, status_code=status.HTTP_201_CREATED)
async def add_publication(
    id: uuid.UUID,
    obj_in: PublicationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_publication(id, str(current_user.id), obj_in)


@router.put("/{id}/publications/{entry_id}", response_model=PublicationResponse)
async def update_publication(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: PublicationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_publication(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/publications/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_publication(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_publication(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Links
# ------------------------------------------------------------------------

@router.post("/{id}/links", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
async def add_link(
    id: uuid.UUID,
    obj_in: LinkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_link(id, str(current_user.id), obj_in)


@router.put("/{id}/links/{entry_id}", response_model=LinkResponse)
async def update_link(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: LinkUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_link(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/links/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_link(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Custom Sections
# ------------------------------------------------------------------------

@router.post("/{id}/custom-sections", response_model=CustomSectionResponse, status_code=status.HTTP_201_CREATED)
async def add_custom_section(
    id: uuid.UUID,
    obj_in: CustomSectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_custom_section(id, str(current_user.id), obj_in)


@router.put("/{id}/custom-sections/{entry_id}", response_model=CustomSectionResponse)
async def update_custom_section(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    obj_in: CustomSectionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.update_custom_section(entry_id, id, str(current_user.id), obj_in)


@router.delete("/{id}/custom-sections/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_custom_section(
    id: uuid.UUID,
    entry_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.delete_custom_section(entry_id, id, str(current_user.id))


# ------------------------------------------------------------------------
# Ordering
# ------------------------------------------------------------------------

@router.put("/{id}/sections/order", status_code=status.HTTP_204_NO_CONTENT)
async def update_section_order(
    id: uuid.UUID,
    obj_in: SectionOrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.update_section_order(id, str(current_user.id), obj_in)


@router.put("/{id}/sections/{section}/entries/order", status_code=status.HTTP_204_NO_CONTENT)
async def update_entry_order(
    id: uuid.UUID,
    section: SectionType,
    obj_in: EntryOrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    await service.update_entry_order(id, str(current_user.id), section, obj_in)


# ------------------------------------------------------------------------
# Versions
# ------------------------------------------------------------------------

@router.post("/{id}/versions", response_model=ResumeVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_version(
    id: uuid.UUID,
    obj_in: ResumeVersionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.create_version(id, str(current_user.id), obj_in.label)


@router.get("/{id}/versions", response_model=List[ResumeVersionResponse])
async def list_versions(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.list_versions(id, str(current_user.id))


@router.get("/{id}/versions/{version_id}", response_model=ResumeVersionResponse)
async def get_version(
    id: uuid.UUID,
    version_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ResumeService(db)
    return await service.get_version(version_id, id, str(current_user.id))
