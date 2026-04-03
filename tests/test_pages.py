from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_index(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert "Abrar Habib" in response.text


@pytest.mark.asyncio
async def test_aboutme(client):
    response = await client.get("/aboutme")
    assert response.status_code == 200
    assert "About Me" in response.text


@pytest.mark.asyncio
async def test_work(client):
    mock_data = [{"title": "Shopify", "role": "Intern", "startdate": "Sep 2025", "enddate": "Present", "description": "Did stuff"}]
    with patch("app.routes.pages.get_work_experiences", new_callable=AsyncMock, return_value=mock_data):
        response = await client.get("/work")
    assert response.status_code == 200
    assert "Work Experiences" in response.text


@pytest.mark.asyncio
async def test_education(client):
    mock_data = [{"title": "CUNY", "startdate": "Aug 2022", "enddate": "Dec 2025", "description": "CS degree"}]
    with patch("app.routes.pages.get_education", new_callable=AsyncMock, return_value=mock_data):
        response = await client.get("/education")
    assert response.status_code == 200
    assert "Education" in response.text


@pytest.mark.asyncio
async def test_hobbies(client):
    mock_data = [{"title": "Soccer", "description": "Fun", "source": "https://example.com/img.jpg"}]
    with patch("app.routes.pages.get_hobbies", new_callable=AsyncMock, return_value=mock_data):
        response = await client.get("/hobbies")
    assert response.status_code == 200
    assert "Hobbies" in response.text


@pytest.mark.asyncio
async def test_travels(client):
    mock_data = [{"name": "Paris, France", "lat": 48.8566, "lng": 2.3522}]
    with patch("app.routes.pages.get_locations", new_callable=AsyncMock, return_value=mock_data):
        response = await client.get("/travels")
    assert response.status_code == 200
    assert "Travels" in response.text


@pytest.mark.asyncio
async def test_timeline(client):
    response = await client.get("/timeline")
    assert response.status_code == 200
    assert "Timeline" in response.text
