import pytest
import sys
import os
from httpx import AsyncClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app


# Test user signup and login
@pytest.mark.asyncio
async def test_auth():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Signup
        response = await client.post("/auth/signup", json={
            "email": "testuser@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        })
        assert response.status_code == 201
        assert "access_token" in response.json()

        # Login
        response = await client.post("/auth/login", json={
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

# Test getting user data (requires auth)
@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        # Login to get token
        response = await client.post("/auth/login", json={
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        token = response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/users/me", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["email"] == "testuser@example.com"


