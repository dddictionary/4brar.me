from unittest.mock import AsyncMock, patch

import pytest


MOCK_WORK = [{"title": "Shopify", "role": "Intern", "startdate": "Sep 2025", "enddate": "Present", "description": "Did stuff"}]
MOCK_EDU = [{"title": "CUNY", "startdate": "Aug 2022", "enddate": "Dec 2025", "description": "CS degree"}]
MOCK_HOBBIES = [{"title": "Soccer", "description": "Fun", "source": "https://example.com/img.jpg"}]
MOCK_LOCATIONS = [{"name": "Paris, France", "lat": 48.8566, "lng": 2.3522}]


def _patch_all():
    """Patch all DB fetchers for the single-page index route."""
    return [
        patch("app.routes.pages.get_work_experiences", new_callable=AsyncMock, return_value=MOCK_WORK),
        patch("app.routes.pages.get_education", new_callable=AsyncMock, return_value=MOCK_EDU),
        patch("app.routes.pages.get_hobbies", new_callable=AsyncMock, return_value=MOCK_HOBBIES),
        patch("app.routes.pages.get_locations", new_callable=AsyncMock, return_value=MOCK_LOCATIONS),
    ]


@pytest.mark.asyncio
async def test_index(client):
    with _patch_all()[0], _patch_all()[1], _patch_all()[2], _patch_all()[3]:
        response = await client.get("/")
    assert response.status_code == 200
    assert "Abrar Habib" in response.text


@pytest.mark.asyncio
async def test_index_has_sections(client):
    """The single page should contain all sections."""
    with _patch_all()[0], _patch_all()[1], _patch_all()[2], _patch_all()[3]:
        response = await client.get("/")
    html = response.text
    assert 'id="about"' in html
    assert 'id="experience"' in html
    assert 'id="education"' in html
    assert 'id="hobbies"' in html
    assert 'id="travels"' in html
    assert 'id="guestbook"' in html


@pytest.mark.asyncio
async def test_index_renders_data(client):
    """The single page should render seeded data."""
    with _patch_all()[0], _patch_all()[1], _patch_all()[2], _patch_all()[3]:
        response = await client.get("/")
    html = response.text
    assert "Shopify" in html
    assert "CUNY" in html
    assert "Soccer" in html
    assert "Paris, France" in html


# ── Old routes redirect to anchors ──

@pytest.mark.asyncio
async def test_aboutme_redirects(client):
    response = await client.get("/aboutme", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/#about"


@pytest.mark.asyncio
async def test_work_redirects(client):
    response = await client.get("/work", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/#experience"


@pytest.mark.asyncio
async def test_education_redirects(client):
    response = await client.get("/education", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/#education"


@pytest.mark.asyncio
async def test_hobbies_redirects(client):
    response = await client.get("/hobbies", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/#hobbies"


@pytest.mark.asyncio
async def test_travels_redirects(client):
    response = await client.get("/travels", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/#travels"


@pytest.mark.asyncio
async def test_timeline_redirects(client):
    response = await client.get("/timeline", follow_redirects=False)
    assert response.status_code == 301
    assert response.headers["location"] == "/#guestbook"
