import pytest

@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_db_health_check(async_client):
    response = await async_client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "database" in response.json()["services"]
