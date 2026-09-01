import uuid
from typing import Any, Dict, List, Optional, Sequence, Type, TypeVar

from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
    Skill,
)
from app.schemas.resume import (
    AchievementCreate,
    AchievementUpdate,
    CertificationCreate,
    CertificationUpdate,
    CustomSectionCreate,
    CustomSectionUpdate,
    EducationCreate,
    EducationUpdate,
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
    SkillCreate,
    SkillUpdate,
)

ModelType = TypeVar("ModelType")


class ResumeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # ------------------------------------------------------------------------
    # Resume Operations
    # ------------------------------------------------------------------------

    async def create_resume(self, user_id: str, resume_in: ResumeCreate) -> Resume:
        db_obj = Resume(user_id=user_id, **resume_in.model_dump())
        self.session.add(db_obj)
        await self.session.flush()  # To generate db_obj.id
        return db_obj

    async def get_resume(self, resume_id: uuid.UUID, user_id: str) -> Optional[Resume]:
        stmt = select(Resume).where(Resume.id == resume_id, Resume.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_full_resume(self, resume_id: uuid.UUID, user_id: str) -> Optional[Resume]:
        stmt = (
            select(Resume)
            .options(
                selectinload(Resume.personal_info),
                selectinload(Resume.sections),
                selectinload(Resume.experiences),
                selectinload(Resume.educations),
                selectinload(Resume.projects),
                selectinload(Resume.skills),
                selectinload(Resume.certifications),
                selectinload(Resume.achievements),
                selectinload(Resume.publications),
                selectinload(Resume.links),
                selectinload(Resume.custom_sections),
            )
            .where(Resume.id == resume_id, Resume.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_resumes(self, user_id: str) -> Sequence[Resume]:
        stmt = select(Resume).where(Resume.user_id == user_id).order_by(Resume.updated_at.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_resume(self, db_obj: Resume, obj_in: ResumeUpdate) -> Resume:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def delete_resume(self, db_obj: Resume) -> None:
        await self.session.delete(db_obj)
        await self.session.flush()

    # ------------------------------------------------------------------------
    # Personal Info
    # ------------------------------------------------------------------------

    async def get_personal_info(self, resume_id: uuid.UUID, user_id: str) -> Optional[PersonalInfo]:
        stmt = select(PersonalInfo).join(Resume).where(
            PersonalInfo.resume_id == resume_id, Resume.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_or_update_personal_info(
        self, resume_id: uuid.UUID, obj_in: PersonalInfoCreate | PersonalInfoUpdate
    ) -> PersonalInfo:
        # Assumes ownership is verified before calling
        stmt = select(PersonalInfo).where(PersonalInfo.resume_id == resume_id)
        result = await self.session.execute(stmt)
        db_obj = result.scalar_one_or_none()

        update_data = obj_in.model_dump(exclude_unset=True)

        if db_obj:
            for field, value in update_data.items():
                setattr(db_obj, field, value)
        else:
            db_obj = PersonalInfo(resume_id=resume_id, **update_data)
        
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    # ------------------------------------------------------------------------
    # Generic Child Entity Operations
    # ------------------------------------------------------------------------
    
    async def _get_child(self, model: Type[ModelType], entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[ModelType]:
        stmt = select(model).join(Resume).where(
            model.id == entity_id,
            model.resume_id == resume_id,
            Resume.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        
    async def _create_child(self, model: Type[ModelType], resume_id: uuid.UUID, obj_in: Any) -> ModelType:
        # Ownership of resume_id must be verified before calling
        data = obj_in.model_dump()
        db_obj = model(resume_id=resume_id, **data)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj
        
    async def _update_child(self, db_obj: ModelType, obj_in: Any) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj
        
    async def _delete_child(self, db_obj: ModelType) -> None:
        await self.session.delete(db_obj)
        await self.session.flush()

    # Experience
    async def create_experience(self, resume_id: uuid.UUID, obj_in: ExperienceCreate) -> Experience:
        return await self._create_child(Experience, resume_id, obj_in)

    async def get_experience(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[Experience]:
        return await self._get_child(Experience, entity_id, resume_id, user_id)

    async def update_experience(self, db_obj: Experience, obj_in: ExperienceUpdate) -> Experience:
        return await self._update_child(db_obj, obj_in)

    async def delete_experience(self, db_obj: Experience) -> None:
        await self._delete_child(db_obj)

    # Education
    async def create_education(self, resume_id: uuid.UUID, obj_in: EducationCreate) -> Education:
        return await self._create_child(Education, resume_id, obj_in)

    async def get_education(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[Education]:
        return await self._get_child(Education, entity_id, resume_id, user_id)

    async def update_education(self, db_obj: Education, obj_in: EducationUpdate) -> Education:
        return await self._update_child(db_obj, obj_in)

    async def delete_education(self, db_obj: Education) -> None:
        await self._delete_child(db_obj)

    # Project
    async def create_project(self, resume_id: uuid.UUID, obj_in: ProjectCreate) -> Project:
        return await self._create_child(Project, resume_id, obj_in)

    async def get_project(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[Project]:
        return await self._get_child(Project, entity_id, resume_id, user_id)

    async def update_project(self, db_obj: Project, obj_in: ProjectUpdate) -> Project:
        return await self._update_child(db_obj, obj_in)

    async def delete_project(self, db_obj: Project) -> None:
        await self._delete_child(db_obj)

    # Skill
    async def create_skill(self, resume_id: uuid.UUID, obj_in: SkillCreate) -> Skill:
        return await self._create_child(Skill, resume_id, obj_in)

    async def get_skill(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[Skill]:
        return await self._get_child(Skill, entity_id, resume_id, user_id)

    async def update_skill(self, db_obj: Skill, obj_in: SkillUpdate) -> Skill:
        return await self._update_child(db_obj, obj_in)

    async def delete_skill(self, db_obj: Skill) -> None:
        await self._delete_child(db_obj)

    # Certification
    async def create_certification(self, resume_id: uuid.UUID, obj_in: CertificationCreate) -> Certification:
        return await self._create_child(Certification, resume_id, obj_in)

    async def get_certification(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[Certification]:
        return await self._get_child(Certification, entity_id, resume_id, user_id)

    async def update_certification(self, db_obj: Certification, obj_in: CertificationUpdate) -> Certification:
        return await self._update_child(db_obj, obj_in)

    async def delete_certification(self, db_obj: Certification) -> None:
        await self._delete_child(db_obj)

    # Achievement
    async def create_achievement(self, resume_id: uuid.UUID, obj_in: AchievementCreate) -> Achievement:
        return await self._create_child(Achievement, resume_id, obj_in)

    async def get_achievement(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[Achievement]:
        return await self._get_child(Achievement, entity_id, resume_id, user_id)

    async def update_achievement(self, db_obj: Achievement, obj_in: AchievementUpdate) -> Achievement:
        return await self._update_child(db_obj, obj_in)

    async def delete_achievement(self, db_obj: Achievement) -> None:
        await self._delete_child(db_obj)

    # Publication
    async def create_publication(self, resume_id: uuid.UUID, obj_in: PublicationCreate) -> Publication:
        return await self._create_child(Publication, resume_id, obj_in)

    async def get_publication(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[Publication]:
        return await self._get_child(Publication, entity_id, resume_id, user_id)

    async def update_publication(self, db_obj: Publication, obj_in: PublicationUpdate) -> Publication:
        return await self._update_child(db_obj, obj_in)

    async def delete_publication(self, db_obj: Publication) -> None:
        await self._delete_child(db_obj)

    # Link
    async def create_link(self, resume_id: uuid.UUID, obj_in: LinkCreate) -> Link:
        return await self._create_child(Link, resume_id, obj_in)

    async def get_link(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[Link]:
        return await self._get_child(Link, entity_id, resume_id, user_id)

    async def update_link(self, db_obj: Link, obj_in: LinkUpdate) -> Link:
        return await self._update_child(db_obj, obj_in)

    async def delete_link(self, db_obj: Link) -> None:
        await self._delete_child(db_obj)

    # Custom Section
    async def create_custom_section(self, resume_id: uuid.UUID, obj_in: CustomSectionCreate) -> CustomSection:
        return await self._create_child(CustomSection, resume_id, obj_in)

    async def get_custom_section(self, entity_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[CustomSection]:
        return await self._get_child(CustomSection, entity_id, resume_id, user_id)

    async def update_custom_section(self, db_obj: CustomSection, obj_in: CustomSectionUpdate) -> CustomSection:
        return await self._update_child(db_obj, obj_in)

    async def delete_custom_section(self, db_obj: CustomSection) -> None:
        await self._delete_child(db_obj)

    # ------------------------------------------------------------------------
    # Ordering
    # ------------------------------------------------------------------------

    async def update_section_order(self, resume_id: uuid.UUID, sections_order: List[str]) -> None:
        for index, section_type_str in enumerate(sections_order):
            stmt = (
                update(ResumeSection)
                .where(
                    ResumeSection.resume_id == resume_id,
                    ResumeSection.section_type == section_type_str
                )
                .values(display_order=index)
            )
            await self.session.execute(stmt)
        await self.session.flush()

    async def update_entry_order(self, model: Type[ModelType], resume_id: uuid.UUID, entry_ids: List[uuid.UUID]) -> None:
        for index, entity_id in enumerate(entry_ids):
            stmt = (
                update(model)
                .where(
                    model.id == entity_id,
                    model.resume_id == resume_id
                )
                .values(display_order=index)
            )
            await self.session.execute(stmt)
        await self.session.flush()

    # ------------------------------------------------------------------------
    # Resume Sections (Defaults)
    # ------------------------------------------------------------------------
    
    async def create_resume_section(self, resume_id: uuid.UUID, section_type: str, display_order: int) -> ResumeSection:
        db_obj = ResumeSection(
            resume_id=resume_id,
            section_type=section_type,
            display_order=display_order,
            is_visible=True
        )
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    # ------------------------------------------------------------------------
    # Versions
    # ------------------------------------------------------------------------

    async def create_version(self, resume_id: uuid.UUID, label: Optional[str], snapshot: Dict[str, Any]) -> ResumeVersion:
        # Get next version number
        stmt = select(func.max(ResumeVersion.version_number)).where(ResumeVersion.resume_id == resume_id)
        result = await self.session.execute(stmt)
        max_version = result.scalar() or 0
        next_version = max_version + 1

        db_obj = ResumeVersion(
            resume_id=resume_id,
            version_number=next_version,
            label=label,
            snapshot=snapshot
        )
        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def list_versions(self, resume_id: uuid.UUID, user_id: str) -> Sequence[ResumeVersion]:
        stmt = select(ResumeVersion).join(Resume).where(
            ResumeVersion.resume_id == resume_id,
            Resume.user_id == user_id
        ).order_by(ResumeVersion.version_number.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_version(self, version_id: uuid.UUID, resume_id: uuid.UUID, user_id: str) -> Optional[ResumeVersion]:
        stmt = select(ResumeVersion).join(Resume).where(
            ResumeVersion.id == version_id,
            ResumeVersion.resume_id == resume_id,
            Resume.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
