from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_get_timeline_posts(client):
    mock_posts = [{"id": 1, "name": "Test", "email": "t@t.com", "content": "Hello", "created_at": "2026-01-01T00:00:00"}]
    with patch("app.routes.api.get_all_posts", new_callable=AsyncMock, return_value=mock_posts):
        response = await client.get("/api/timeline_post")
    assert response.status_code == 200
    data = response.json()
    assert "timeline_posts" in data
    assert len(data["timeline_posts"]) == 1


@pytest.mark.asyncio
async def test_post_timeline_post(client):
    mock_post = {"id": 1, "name": "Test User", "email": "test@example.com", "content": "Hello world", "created_at": "2026-01-01T00:00:00"}
    with patch("app.routes.api.create_post", new_callable=AsyncMock, return_value=mock_post):
        response = await client.post(
            "/api/timeline_post",
            data={"name": "Test User", "email": "test@example.com", "content": "Hello world"},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["content"] == "Hello world"
    assert "id" in data


@pytest.mark.asyncio
async def test_post_timeline_post_invalid_name(client):
    response = await client.post(
        "/api/timeline_post",
        data={"name": "", "email": "test@example.com", "content": "Hello"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_post_timeline_post_invalid_email(client):
    response = await client.post(
        "/api/timeline_post",
        data={"name": "Test", "email": "invalid", "content": "Hello"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_post_timeline_post_invalid_content(client):
    response = await client.post(
        "/api/timeline_post",
        data={"name": "Test", "email": "test@example.com", "content": ""},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_ci_endpoint(client):
    response = await client.get("/api/test-ci")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_metrics(client):
    response = await client.get("/metrics")
    assert response.status_code == 200
