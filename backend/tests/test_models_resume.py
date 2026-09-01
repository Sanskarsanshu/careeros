import pytest
import uuid
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.resume import (
    Resume, PersonalInfo, Experience, Project, Skill, ResumeVersion,
    SectionType, ResumeSection
)


@pytest.fixture
async def test_user(db_session):
    user = User(email=f"test_{uuid.uuid4()}@example.com", full_name="Test User")
    db_session.add(user)
    await db_session.commit()
    return user


@pytest.mark.asyncio(loop_scope="session")
async def test_create_resume(db_session, test_user):
    resume = Resume(
        user_id=test_user.id,
        title="Software Engineer Resume",
        target_job_title="Backend Engineer",
        summary="A passionate developer"
    )
    db_session.add(resume)
    await db_session.commit()

    assert resume.id is not None
    assert resume.title == "Software Engineer Resume"
    assert resume.user_id == test_user.id


@pytest.mark.asyncio(loop_scope="session")
async def test_personal_info_one_to_one(db_session, test_user):
    resume = Resume(user_id=test_user.id, title="Test")
    db_session.add(resume)
    await db_session.commit()

    # Create PersonalInfo
    pi1 = PersonalInfo(
        resume_id=resume.id,
        full_name="John Doe",
        email="john@example.com"
    )
    db_session.add(pi1)
    await db_session.commit()

    # Attempt to create second PersonalInfo should fail due to unique constraint
    pi2 = PersonalInfo(
        resume_id=resume.id,
        full_name="Jane Doe",
        email="jane@example.com"
    )
    db_session.add(pi2)
    with pytest.raises(IntegrityError):
        await db_session.commit()
    await db_session.rollback()


@pytest.mark.asyncio(loop_scope="session")
async def test_experience_and_display_order(db_session, test_user):
    resume = Resume(user_id=test_user.id, title="Test")
    db_session.add(resume)
    await db_session.commit()

    exp1 = Experience(
        resume_id=resume.id,
        company="Company A",
        position="Dev",
        display_order=1
    )
    exp2 = Experience(
        resume_id=resume.id,
        company="Company B",
        position="Senior Dev",
        display_order=2
    )
    db_session.add_all([exp1, exp2])
    await db_session.commit()

    result = await db_session.execute(
        select(Experience).where(Experience.resume_id == resume.id).order_by(Experience.display_order)
    )
    experiences = result.scalars().all()
    assert len(experiences) == 2
    assert experiences[0].company == "Company A"
    assert experiences[1].company == "Company B"


@pytest.mark.asyncio(loop_scope="session")
async def test_jsonb_roundtrip_projects(db_session, test_user):
    resume = Resume(user_id=test_user.id, title="Test")
    db_session.add(resume)
    await db_session.commit()

    proj = Project(
        resume_id=resume.id,
        name="CareerOS",
        technologies=["Python", "FastAPI", "PostgreSQL"],
        bullets=["Built backend", "Configured Docker"]
    )
    db_session.add(proj)
    await db_session.commit()

    assert isinstance(proj.technologies, list)
    assert proj.technologies == ["Python", "FastAPI", "PostgreSQL"]
    assert proj.bullets == ["Built backend", "Configured Docker"]


@pytest.mark.asyncio(loop_scope="session")
async def test_skills(db_session, test_user):
    resume = Resume(user_id=test_user.id, title="Test")
    db_session.add(resume)
    await db_session.commit()

    skill = Skill(resume_id=resume.id, category="Languages", name="Python")
    db_session.add(skill)
    await db_session.commit()

    assert skill.name == "Python"
    assert skill.category == "Languages"
    assert skill.proficiency is None


@pytest.mark.asyncio(loop_scope="session")
async def test_resume_versions(db_session, test_user):
    resume = Resume(user_id=test_user.id, title="Test")
    db_session.add(resume)
    await db_session.commit()

    v1 = ResumeVersion(
        resume_id=resume.id,
        version_number=1,
        snapshot={"title": "Draft 1"}
    )
    v2 = ResumeVersion(
        resume_id=resume.id,
        version_number=2,
        snapshot={"title": "Draft 2"}
    )
    db_session.add_all([v1, v2])
    await db_session.commit()

    # Attempt to add v2 again to test unique constraint
    v_dup = ResumeVersion(
        resume_id=resume.id,
        version_number=2,
        snapshot={}
    )
    db_session.add(v_dup)
    with pytest.raises(IntegrityError):
        await db_session.commit()
    await db_session.rollback()


@pytest.mark.asyncio(loop_scope="session")
async def test_cascade_deletes(db_session, test_user):
    # Create resume
    resume = Resume(user_id=test_user.id, title="Test Cascade")
    db_session.add(resume)
    await db_session.commit()

    # Create associated records
    pi = PersonalInfo(resume_id=resume.id, full_name="Cascade Test")
    exp = Experience(resume_id=resume.id, company="Cascade Co", position="Test")
    rv = ResumeVersion(resume_id=resume.id, version_number=1, snapshot={})
    
    db_session.add_all([pi, exp, rv])
    await db_session.commit()

    # Delete the user which should cascade to resume which should cascade to children
    await db_session.delete(test_user)
    await db_session.commit()

    # Verify everything is deleted
    assert (await db_session.execute(select(Resume).where(Resume.id == resume.id))).scalar_one_or_none() is None
    assert (await db_session.execute(select(PersonalInfo).where(PersonalInfo.resume_id == resume.id))).scalar_one_or_none() is None
    assert (await db_session.execute(select(Experience).where(Experience.resume_id == resume.id))).scalar_one_or_none() is None
    assert (await db_session.execute(select(ResumeVersion).where(ResumeVersion.resume_id == resume.id))).scalar_one_or_none() is None


@pytest.mark.asyncio(loop_scope="session")
async def test_user_resume_relationship(db_session, test_user):
    r1 = Resume(user_id=test_user.id, title="R1")
    r2 = Resume(user_id=test_user.id, title="R2")
    db_session.add_all([r1, r2])
    await db_session.commit()

    # Refresh user to load resumes
    result = await db_session.execute(
        select(User).options(selectinload(User.resumes)).where(User.id == test_user.id)
    )
    user_with_resumes = result.scalar_one()
    
    assert len(user_with_resumes.resumes) == 2
    titles = [r.title for r in user_with_resumes.resumes]
    assert "R1" in titles
    assert "R2" in titles
