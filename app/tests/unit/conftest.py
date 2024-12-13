# import pytest
# from httpx import AsyncClient, ASGITransport
# from unittest.mock import AsyncMock
# from sqlalchemy.ext.asyncio import AsyncSession


# from main import app
# from core.database import get_db


# # Mock database session
# @pytest.fixture(scope="function")
# async def mocked_db_session():
#     """Fixture to mock the database session."""
#     db_session = AsyncMock(spec=AsyncSession)
#     # db_session.execute.return_value = None
#     yield db_session


# @pytest.fixture(scope="function")
# async def test_app(mocked_db_session):
#     test_app = app
#     test_app.dependency_overrides[get_db] = mocked_db_session
#     yield test_app


# @pytest.fixture(scope="function")
# async def async_client(test_app):
#     """Fixture to use AsyncClient with the FastAPI app."""
#     # NOTE: Pass `app=app` properly into the AsyncClient
#     async with AsyncClient(
#         transport=ASGITransport(app=test_app), base_url="http://testserver"
#     ) as client:
#         yield client
