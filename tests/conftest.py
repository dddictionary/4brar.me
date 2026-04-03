import os
from unittest.mock import AsyncMock, patch

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

os.environ.setdefault("MYSQL_HOST", "127.0.0.1")
os.environ.setdefault("MYSQL_USER", "testuser")
os.environ.setdefault("MYSQL_PASSWORD", "testpass")
os.environ.setdefault("MYSQL_DATABASE", "testdb")
os.environ.setdefault("URL", "localhost:5000")

from app.main import app  # noqa: E402


@pytest_asyncio.fixture
async def client():
    mock_pool = AsyncMock()
    with patch("app.database.pool", mock_pool), patch("app.database.get_pool", return_value=mock_pool):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest_asyncio.fixture
def mock_pool():
    return AsyncMock()
