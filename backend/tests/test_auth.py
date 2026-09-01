import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_and_login(async_client: AsyncClient):
    # Register
    register_response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@careeros.com",
            "password": "strongpassword123",
            "full_name": "Test User"
        }
    )
    assert register_response.status_code == 201
    user_data = register_response.json()
    assert user_data["email"] == "test@careeros.com"

    # Login
    login_response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@careeros.com",
            "password": "strongpassword123"
        }
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data

    # Get Me
    me_response = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token_data['access_token']}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "test@careeros.com"

@pytest.mark.asyncio
async def test_unauthenticated_me(async_client: AsyncClient):
    me_response = await async_client.get("/api/v1/auth/me")
    assert me_response.status_code == 401
