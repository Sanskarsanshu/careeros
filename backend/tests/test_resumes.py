import uuid
import pytest
from httpx import AsyncClient

# Helper function to create a user and return their auth headers
async def get_auth_headers(async_client: AsyncClient, email: str, password: str = "password123"):
    register_response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Test User"
        }
    )
    if register_response.status_code != 201:
        # If already exists, just login
        pass
        
    login_response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio(loop_scope="session")
async def test_resume_crud(async_client: AsyncClient):
    headers = await get_auth_headers(async_client, f"user_crud_{uuid.uuid4()}@example.com")
    
    # Create
    create_resp = await async_client.post(
        "/api/v1/resumes",
        headers=headers,
        json={"title": "My Resume"}
    )
    assert create_resp.status_code == 201
    resume_id = create_resp.json()["id"]
    
    # List
    list_resp = await async_client.get("/api/v1/resumes", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1
    
    # Get Full
    get_resp = await async_client.get(f"/api/v1/resumes/{resume_id}", headers=headers)
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["title"] == "My Resume"
    assert data["personal_info"]["full_name"] == "New Resume"
    assert len(data["sections"]) == 10
    
    # Update
    update_resp = await async_client.put(
        f"/api/v1/resumes/{resume_id}",
        headers=headers,
        json={"title": "Updated Resume"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "Updated Resume"
    
    # Update Personal Info
    personal_resp = await async_client.put(
        f"/api/v1/resumes/{resume_id}/personal",
        headers=headers,
        json={"full_name": "John Doe", "email": "john@example.com"}
    )
    assert personal_resp.status_code == 200
    assert personal_resp.json()["full_name"] == "John Doe"

@pytest.mark.asyncio(loop_scope="session")
async def test_experience_crud(async_client: AsyncClient):
    headers = await get_auth_headers(async_client, f"user_exp_{uuid.uuid4()}@example.com")
    create_resp = await async_client.post("/api/v1/resumes", headers=headers, json={"title": "Exp Resume"})
    resume_id = create_resp.json()["id"]
    
    # Create
    exp_resp = await async_client.post(
        f"/api/v1/resumes/{resume_id}/experience",
        headers=headers,
        json={"company": "Acme Corp", "position": "Developer"}
    )
    assert exp_resp.status_code == 201
    exp_id = exp_resp.json()["id"]
    
    # Update
    update_resp = await async_client.put(
        f"/api/v1/resumes/{resume_id}/experience/{exp_id}",
        headers=headers,
        json={"company": "Acme Corp 2"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["company"] == "Acme Corp 2"
    
    # Delete
    del_resp = await async_client.delete(f"/api/v1/resumes/{resume_id}/experience/{exp_id}", headers=headers)
    assert del_resp.status_code == 204

@pytest.mark.asyncio(loop_scope="session")
async def test_education_crud(async_client: AsyncClient):
    headers = await get_auth_headers(async_client, f"user_edu_{uuid.uuid4()}@example.com")
    create_resp = await async_client.post("/api/v1/resumes", headers=headers, json={"title": "Edu Resume"})
    resume_id = create_resp.json()["id"]
    
    edu_resp = await async_client.post(
        f"/api/v1/resumes/{resume_id}/education",
        headers=headers,
        json={"institution": "MIT", "degree": "BS"}
    )
    assert edu_resp.status_code == 201
    
    edu_id = edu_resp.json()["id"]
    update_resp = await async_client.put(
        f"/api/v1/resumes/{resume_id}/education/{edu_id}",
        headers=headers,
        json={"degree": "MS"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["degree"] == "MS"
    
    del_resp = await async_client.delete(f"/api/v1/resumes/{resume_id}/education/{edu_id}", headers=headers)
    assert del_resp.status_code == 204

@pytest.mark.asyncio(loop_scope="session")
async def test_project_crud(async_client: AsyncClient):
    headers = await get_auth_headers(async_client, f"user_proj_{uuid.uuid4()}@example.com")
    create_resp = await async_client.post("/api/v1/resumes", headers=headers, json={"title": "Proj Resume"})
    resume_id = create_resp.json()["id"]
    
    proj_resp = await async_client.post(
        f"/api/v1/resumes/{resume_id}/projects",
        headers=headers,
        json={"name": "CareerOS"}
    )
    assert proj_resp.status_code == 201
    
    proj_id = proj_resp.json()["id"]
    update_resp = await async_client.put(
        f"/api/v1/resumes/{resume_id}/projects/{proj_id}",
        headers=headers,
        json={"role": "Lead"}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["role"] == "Lead"
    
    del_resp = await async_client.delete(f"/api/v1/resumes/{resume_id}/projects/{proj_id}", headers=headers)
    assert del_resp.status_code == 204

@pytest.mark.asyncio(loop_scope="session")
async def test_other_entities(async_client: AsyncClient):
    # Condensing remaining entities into one test for brevity
    headers = await get_auth_headers(async_client, f"user_others_{uuid.uuid4()}@example.com")
    create_resp = await async_client.post("/api/v1/resumes", headers=headers, json={"title": "Other Resume"})
    resume_id = create_resp.json()["id"]
    
    # Skills
    r = await async_client.post(f"/api/v1/resumes/{resume_id}/skills", headers=headers, json={"category": "Lang", "name": "Python"})
    assert r.status_code == 201
    await async_client.delete(f"/api/v1/resumes/{resume_id}/skills/{r.json()['id']}", headers=headers)
    
    # Certifications
    r = await async_client.post(f"/api/v1/resumes/{resume_id}/certifications", headers=headers, json={"name": "AWS"})
    assert r.status_code == 201
    await async_client.delete(f"/api/v1/resumes/{resume_id}/certifications/{r.json()['id']}", headers=headers)

    # Achievements
    r = await async_client.post(f"/api/v1/resumes/{resume_id}/achievements", headers=headers, json={"title": "Award"})
    assert r.status_code == 201
    await async_client.delete(f"/api/v1/resumes/{resume_id}/achievements/{r.json()['id']}", headers=headers)

    # Publications
    r = await async_client.post(f"/api/v1/resumes/{resume_id}/publications", headers=headers, json={"title": "Paper"})
    assert r.status_code == 201
    await async_client.delete(f"/api/v1/resumes/{resume_id}/publications/{r.json()['id']}", headers=headers)

    # Links
    r = await async_client.post(f"/api/v1/resumes/{resume_id}/links", headers=headers, json={"name": "Blog", "url": "http://x.com"})
    assert r.status_code == 201
    await async_client.delete(f"/api/v1/resumes/{resume_id}/links/{r.json()['id']}", headers=headers)

    # Custom
    r = await async_client.post(f"/api/v1/resumes/{resume_id}/custom-sections", headers=headers, json={"title": "Custom"})
    assert r.status_code == 201
    await async_client.delete(f"/api/v1/resumes/{resume_id}/custom-sections/{r.json()['id']}", headers=headers)

@pytest.mark.asyncio(loop_scope="session")
async def test_ordering(async_client: AsyncClient):
    headers = await get_auth_headers(async_client, f"user_ord_{uuid.uuid4()}@example.com")
    create_resp = await async_client.post("/api/v1/resumes", headers=headers, json={"title": "Ord Resume"})
    resume_id = create_resp.json()["id"]
    
    # Reorder sections
    ord_resp = await async_client.put(
        f"/api/v1/resumes/{resume_id}/sections/order",
        headers=headers,
        json={"sections": ["education", "experience", "projects", "personal", "summary", "skills", "certifications", "achievements", "publications", "links", "custom"]}
    )
    assert ord_resp.status_code == 204
    
    # Verify
    get_resp = await async_client.get(f"/api/v1/resumes/{resume_id}", headers=headers)
    sections = get_resp.json()["sections"]
    sections_sorted = sorted(sections, key=lambda s: s["display_order"])
    assert sections_sorted[0]["section_type"] == "education"
    assert sections_sorted[1]["section_type"] == "experience"

    # Reorder entries
    exp1 = await async_client.post(f"/api/v1/resumes/{resume_id}/experience", headers=headers, json={"company": "C1", "position": "P1"})
    exp2 = await async_client.post(f"/api/v1/resumes/{resume_id}/experience", headers=headers, json={"company": "C2", "position": "P2"})
    
    id1 = exp1.json()["id"]
    id2 = exp2.json()["id"]
    
    ord_entries_resp = await async_client.put(
        f"/api/v1/resumes/{resume_id}/sections/experience/entries/order",
        headers=headers,
        json={"entry_ids": [id2, id1]}
    )
    assert ord_entries_resp.status_code == 204
    
    get_resp2 = await async_client.get(f"/api/v1/resumes/{resume_id}", headers=headers)
    exps = get_resp2.json()["experiences"]
    exp1_fetched = next(e for e in exps if e["id"] == id1)
    exp2_fetched = next(e for e in exps if e["id"] == id2)
    assert exp2_fetched["display_order"] == 0
    assert exp1_fetched["display_order"] == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_versions(async_client: AsyncClient):
    headers = await get_auth_headers(async_client, f"user_ver_{uuid.uuid4()}@example.com")
    create_resp = await async_client.post("/api/v1/resumes", headers=headers, json={"title": "Ver Resume"})
    resume_id = create_resp.json()["id"]
    
    # Add experience
    await async_client.post(f"/api/v1/resumes/{resume_id}/experience", headers=headers, json={"company": "Old Corp", "position": "Dev"})
    
    # Create version
    ver_resp = await async_client.post(f"/api/v1/resumes/{resume_id}/versions", headers=headers, json={"label": "V1"})
    assert ver_resp.status_code == 201
    version_id = ver_resp.json()["id"]
    assert ver_resp.json()["version_number"] == 1
    
    # Modify live resume
    await async_client.post(f"/api/v1/resumes/{resume_id}/experience", headers=headers, json={"company": "New Corp", "position": "Dev"})
    
    # Get version and check snapshot
    get_ver = await async_client.get(f"/api/v1/resumes/{resume_id}/versions/{version_id}", headers=headers)
    assert get_ver.status_code == 200
    
    snapshot = get_ver.json()["snapshot"]
    # Snapshot should only have 1 experience
    assert len(snapshot["experiences"]) == 1
    assert snapshot["experiences"][0]["company"] == "Old Corp"
    
    # List versions
    list_ver = await async_client.get(f"/api/v1/resumes/{resume_id}/versions", headers=headers)
    assert list_ver.status_code == 200
    assert len(list_ver.json()) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_authorization(async_client: AsyncClient):
    headers_a = await get_auth_headers(async_client, f"user_a_{uuid.uuid4()}@example.com")
    headers_b = await get_auth_headers(async_client, f"user_b_{uuid.uuid4()}@example.com")
    
    # User A creates a resume
    create_resp = await async_client.post("/api/v1/resumes", headers=headers_a, json={"title": "Resume A"})
    resume_a_id = create_resp.json()["id"]
    
    # User A creates an experience
    exp_resp = await async_client.post(
        f"/api/v1/resumes/{resume_a_id}/experience",
        headers=headers_a,
        json={"company": "Acme A", "position": "Dev"}
    )
    exp_a_id = exp_resp.json()["id"]
    
    # User B attempts to access Resume A
    get_b = await async_client.get(f"/api/v1/resumes/{resume_a_id}", headers=headers_b)
    assert get_b.status_code == 404
    
    put_b = await async_client.put(f"/api/v1/resumes/{resume_a_id}", headers=headers_b, json={"title": "Hacked"})
    assert put_b.status_code == 404
    
    del_b = await async_client.delete(f"/api/v1/resumes/{resume_a_id}", headers=headers_b)
    assert del_b.status_code == 404
    
    # User B attempts to access Experience A
    put_exp_b = await async_client.put(f"/api/v1/resumes/{resume_a_id}/experience/{exp_a_id}", headers=headers_b, json={"company": "Hacked"})
    assert put_exp_b.status_code == 404

    # Validate deleting resume deletes child
    await async_client.delete(f"/api/v1/resumes/{resume_a_id}", headers=headers_a)
    
    # The resume should be gone
    get_after_del = await async_client.get(f"/api/v1/resumes/{resume_a_id}", headers=headers_a)
    assert get_after_del.status_code == 404
