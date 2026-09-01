import uuid
from typing import Any, Dict, List, Optional, Sequence, TypeVar

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import (
    Achievement,
    Certification,
    CustomSection,
    Education,
    Experience,
    Link,
    PersonalInfo,
    Project,
    Publication,
    Resume,
    ResumeSection,
    ResumeVersion,
    SectionType,
    Skill,
)
from app.repositories.resume_repository import ResumeRepository
from app.schemas.resume import (
    AchievementCreate,
    AchievementUpdate,
    CertificationCreate,
    CertificationUpdate,
    CustomSectionCreate,
    CustomSectionUpdate,
    EducationCreate,
    EducationUpdate,
    EntryOrderUpdate,
    ExperienceCreate,
    ExperienceUpdate,
    LinkCreate,
    LinkUpdate,
    PersonalInfoCreate,
    PersonalInfoUpdate,
    ProjectCreate,
    ProjectUpdate,
    PublicationCreate,
    PublicationUpdate,
    ResumeCreate,
    ResumeUpdate,
    SectionOrderUpdate,
    SkillCreate,
    SkillUpdate,
)

ModelType = TypeVar("ModelType")


class ResumeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ResumeRepository(db)

    def _require_ownership(self, obj: Any, name: str = "Resource"):
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{name} not found.",
            )
        return obj

    # ------------------------------------------------------------------------
    # Resume Operations
    # ------------------------------------------------------------------------

    async def create_resume(self, user_id: str, obj_in: ResumeCreate) -> Resume:
        resume = await self.repo.create_resume(user_id, obj_in)
        
        # Create default PersonalInfo
        await self.repo.create_or_update_personal_info(
            resume_id=resume.id,
            obj_in=PersonalInfoCreate(full_name="New Resume")
        )
        
        # Create default sections
        default_sections = [
            SectionType.personal,
            SectionType.summary,
            SectionType.experience,
            SectionType.education,
            SectionType.projects,
            SectionType.skills,
            SectionType.certifications,
            SectionType.achievements,
            SectionType.publications,
            SectionType.links,
        ]
        
        for i, section_type in enumerate(default_sections):
            await self.repo.create_resume_section(
                resume_id=resume.id,
                section_type=section_type,
                display_order=i
            )

        await self.db.commit()
        await self.db.refresh(resume)
        return resume

    async def get_resume(self, resume_id: uuid.UUID, user_id: str) -> Resume:
        resume = await self.repo.get_resume(resume_id, user_id)
        return self._require_ownership(resume, "Resume")

    async def get_full_resume(self, resume_id: uuid.UUID, user_id: str) -> Resume:
        resume = await self.repo.get_full_resume(resume_id, user_id)
        return self._require_ownership(resume, "Resume")

    async def list_resumes(self, user_id: str) -> Sequence[Resume]:
        return await self.repo.list_resumes(user_id)

    async def update_resume(
        self, resume_id: uuid.UUID, user_id: str, obj_in: ResumeUpdate
    ) -> Resume:
        resume = await self.get_resume(resume_id, user_id)
        updated_resume = await self.repo.update_resume(resume, obj_in)
        await self.db.commit()
        await self.db.refresh(updated_resume)
        return updated_resume

    async def delete_resume(self, resume_id: uuid.UUID, user_id: str) -> None:
        resume = await self.get_resume(resume_id, user_id)
        await self.repo.delete_resume(resume)
        await self.db.commit()

    # ------------------------------------------------------------------------
    # Personal Info
    # ------------------------------------------------------------------------

    async def get_personal_info(self, resume_id: uuid.UUID, user_id: str) -> PersonalInfo:
        # Check resume ownership first, since get_personal_info returns None if empty
        await self.get_resume(resume_id, user_id) 
        
        info = await self.repo.get_personal_info(resume_id, user_id)
        if not info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Personal info not found"
            )
        return info

    async def update_personal_info(
        self, resume_id: uuid.UUID, user_id: str, obj_in: PersonalInfoUpdate
    ) -> PersonalInfo:
        await self.get_resume(resume_id, user_id)
        info = await self.repo.create_or_update_personal_info(resume_id, obj_in)
        await self.db.commit()
        await self.db.refresh(info)
        return info

    # ------------------------------------------------------------------------
    # Generic Entity Handlers
    # ------------------------------------------------------------------------

    async def _create_entity(self, repo_method, resume_id: uuid.UUID, user_id: str, obj_in: Any):
        await self.get_resume(resume_id, user_id)
        entity = await repo_method(resume_id, obj_in)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def _update_entity(
        self, get_repo_method, update_repo_method, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: Any
    ):
        entity = await get_repo_method(entity_id, resume_id, user_id)
        self._require_ownership(entity)
        updated_entity = await update_repo_method(entity, obj_in)
        await self.db.commit()
        await self.db.refresh(updated_entity)
        return updated_entity

    async def _delete_entity(self, get_repo_method, delete_repo_method, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        entity = await get_repo_method(entity_id, resume_id, user_id)
        self._require_ownership(entity)
        await delete_repo_method(entity)
        await self.db.commit()

    # ------------------------------------------------------------------------
    # Experience
    # ------------------------------------------------------------------------
    async def create_experience(self, resume_id: uuid.UUID, user_id: str, obj_in: ExperienceCreate):
        return await self._create_entity(self.repo.create_experience, resume_id, user_id, obj_in)

    async def update_experience(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: ExperienceUpdate):
        return await self._update_entity(self.repo.get_experience, self.repo.update_experience, entity_id, resume_id, user_id, obj_in)

    async def delete_experience(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_experience, self.repo.delete_experience, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Education
    # ------------------------------------------------------------------------
    async def create_education(self, resume_id: uuid.UUID, user_id: str, obj_in: EducationCreate):
        return await self._create_entity(self.repo.create_education, resume_id, user_id, obj_in)

    async def update_education(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: EducationUpdate):
        return await self._update_entity(self.repo.get_education, self.repo.update_education, entity_id, resume_id, user_id, obj_in)

    async def delete_education(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_education, self.repo.delete_education, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------------
    async def create_project(self, resume_id: uuid.UUID, user_id: str, obj_in: ProjectCreate):
        return await self._create_entity(self.repo.create_project, resume_id, user_id, obj_in)

    async def update_project(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: ProjectUpdate):
        return await self._update_entity(self.repo.get_project, self.repo.update_project, entity_id, resume_id, user_id, obj_in)

    async def delete_project(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_project, self.repo.delete_project, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Skills
    # ------------------------------------------------------------------------
    async def create_skill(self, resume_id: uuid.UUID, user_id: str, obj_in: SkillCreate):
        return await self._create_entity(self.repo.create_skill, resume_id, user_id, obj_in)

    async def update_skill(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: SkillUpdate):
        return await self._update_entity(self.repo.get_skill, self.repo.update_skill, entity_id, resume_id, user_id, obj_in)

    async def delete_skill(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_skill, self.repo.delete_skill, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Certifications
    # ------------------------------------------------------------------------
    async def create_certification(self, resume_id: uuid.UUID, user_id: str, obj_in: CertificationCreate):
        return await self._create_entity(self.repo.create_certification, resume_id, user_id, obj_in)

    async def update_certification(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: CertificationUpdate):
        return await self._update_entity(self.repo.get_certification, self.repo.update_certification, entity_id, resume_id, user_id, obj_in)

    async def delete_certification(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_certification, self.repo.delete_certification, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Achievements
    # ------------------------------------------------------------------------
    async def create_achievement(self, resume_id: uuid.UUID, user_id: str, obj_in: AchievementCreate):
        return await self._create_entity(self.repo.create_achievement, resume_id, user_id, obj_in)

    async def update_achievement(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: AchievementUpdate):
        return await self._update_entity(self.repo.get_achievement, self.repo.update_achievement, entity_id, resume_id, user_id, obj_in)

    async def delete_achievement(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_achievement, self.repo.delete_achievement, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Publications
    # ------------------------------------------------------------------------
    async def create_publication(self, resume_id: uuid.UUID, user_id: str, obj_in: PublicationCreate):
        return await self._create_entity(self.repo.create_publication, resume_id, user_id, obj_in)

    async def update_publication(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: PublicationUpdate):
        return await self._update_entity(self.repo.get_publication, self.repo.update_publication, entity_id, resume_id, user_id, obj_in)

    async def delete_publication(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_publication, self.repo.delete_publication, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Links
    # ------------------------------------------------------------------------
    async def create_link(self, resume_id: uuid.UUID, user_id: str, obj_in: LinkCreate):
        return await self._create_entity(self.repo.create_link, resume_id, user_id, obj_in)

    async def update_link(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: LinkUpdate):
        return await self._update_entity(self.repo.get_link, self.repo.update_link, entity_id, resume_id, user_id, obj_in)

    async def delete_link(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_link, self.repo.delete_link, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Custom Sections
    # ------------------------------------------------------------------------
    async def create_custom_section(self, resume_id: uuid.UUID, user_id: str, obj_in: CustomSectionCreate):
        return await self._create_entity(self.repo.create_custom_section, resume_id, user_id, obj_in)

    async def update_custom_section(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str, obj_in: CustomSectionUpdate):
        return await self._update_entity(self.repo.get_custom_section, self.repo.update_custom_section, entity_id, resume_id, user_id, obj_in)

    async def delete_custom_section(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str):
        await self._delete_entity(self.repo.get_custom_section, self.repo.delete_custom_section, entity_id, resume_id, user_id)

    # ------------------------------------------------------------------------
    # Ordering
    # ------------------------------------------------------------------------

    async def update_section_order(
        self, resume_id: uuid.UUID, user_id: str, obj_in: SectionOrderUpdate
    ):
        await self.get_resume(resume_id, user_id)
        sections_str = [s.value for s in obj_in.sections]
        await self.repo.update_section_order(resume_id, sections_str)
        await self.db.commit()

    async def update_entry_order(
        self, resume_id: uuid.UUID, user_id: str, section_type: SectionType, obj_in: EntryOrderUpdate
    ):
        await self.get_resume(resume_id, user_id)
        
        model_map = {
            SectionType.experience: Experience,
            SectionType.education: Education,
            SectionType.projects: Project,
            SectionType.skills: Skill,
            SectionType.certifications: Certification,
            SectionType.achievements: Achievement,
            SectionType.publications: Publication,
            SectionType.links: Link,
            SectionType.custom: CustomSection,
        }
        
        model = model_map.get(section_type)
        if not model:
            raise HTTPException(status_code=400, detail="Cannot order this section type")
            
        await self.repo.update_entry_order(model, resume_id, obj_in.entry_ids)
        await self.db.commit()

    # ------------------------------------------------------------------------
    # Versioning
    # ------------------------------------------------------------------------
    
    def _build_snapshot_dict(self, resume: Resume) -> Dict[str, Any]:
        """Convert a full resume ORM object into a dictionary snapshot"""
        # A simple recursive or manual dump of all properties.
        def _dump_list(items):
            return [
                {col: getattr(item, col) for col in item.__table__.columns.keys() if col not in ["id", "resume_id", "created_at", "updated_at"]}
                for item in items
            ]
            
        snapshot = {
            "title": resume.title,
            "target_job_title": resume.target_job_title,
            "summary": resume.summary,
            "template_id": resume.template_id,
            "personal_info": None,
            "sections": _dump_list(resume.sections),
            "experiences": _dump_list(resume.experiences),
            "educations": _dump_list(resume.educations),
            "projects": _dump_list(resume.projects),
            "skills": _dump_list(resume.skills),
            "certifications": _dump_list(resume.certifications),
            "achievements": _dump_list(resume.achievements),
            "publications": _dump_list(resume.publications),
            "links": _dump_list(resume.links),
            "custom_sections": _dump_list(resume.custom_sections),
        }
        
        if resume.personal_info:
            snapshot["personal_info"] = {
                col: getattr(resume.personal_info, col) 
                for col in resume.personal_info.__table__.columns.keys() 
                if col not in ["id", "resume_id", "created_at", "updated_at"]
            }
            
        # JSON serializer compatibility for dates/UUIDs
        from fastapi.encoders import jsonable_encoder
        return jsonable_encoder(snapshot)

    async def create_version(self, resume_id: uuid.UUID, user_id: str, label: Optional[str] = None) -> ResumeVersion:
        resume = await self.get_full_resume(resume_id, user_id)
        snapshot = self._build_snapshot_dict(resume)
        
        version = await self.repo.create_version(resume_id, label, snapshot)
        await self.db.commit()
        await self.db.refresh(version)
        return version

    async def list_versions(self, resume_id: uuid.UUID, user_id: str) -> Sequence[ResumeVersion]:
        # Ownership check implicitly done by repo query JOIN, but let's be explicitly safe and clean:
        await self.get_resume(resume_id, user_id)
        return await self.repo.list_versions(resume_id, user_id)

    async def get_version(self, version_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> ResumeVersion:
        version = await self.repo.get_version(version_id, resume_id, user_id)
        return self._require_ownership(version, "Resume version")
