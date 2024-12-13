import unittest
import asyncio
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.database import Base
from main import app
from api.v1.utils.password import hash_password


from core.database import get_db


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestPonenumberAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.base_url = "/api/v1"
        # self.mock_db = AsyncMock()

        # Create an in-memory SQLite database
        self.engine = create_async_engine(DATABASE_URL, echo=False)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession
        )

        # Override get_db dependency
        async def override_get_db():
            async with self.SessionLocal() as session:
                yield session

        app.dependency_overrides[get_db] = override_get_db

        # Initialize the database schema
        asyncio.run(self.setup_database())

    async def setup_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @patch("api.v1.utils.password.hash_password", side_effect=hash_password)
    async def test_create_phonenumber_success(self, mock_hash_password):
        """Test the /phonenumbers endpoint for successful registration."""

        payload = {
            "email": "testuser@example.com",
            "password": "securepassword",
        }

        # with patch(
        #     "api.v1.utils.password.hash_password",
        #     return_value="mock_hash_password",
        # ):

        response = self.client.post(f"{self.base_url}/auth/register", json=payload)

        # response
        token_response = self.client.post(f"{self.base_url}/auth/token", json=payload)

        headers = {"Authorization": f"Bearer {token_response.json()["access_token"]}"}
        req_data = {"number": "+9779841234567"}

        response = self.client.post(
            f"{self.base_url}/phonenumbers", headers=headers, json=req_data
        )
        # raise Exception(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("number", response.json())
        self.assertIn("phonenumber_id", response.json())

    @patch("api.v1.utils.password.hash_password", side_effect=hash_password)
    async def test_retrieve_phonenumber_success(self, mock_hash_password):
        """Test the /phonenumbers endpoint for successful registration."""

        payload = {
            "email": "testuser@example.com",
            "password": "securepassword",
        }

        # register
        self.client.post(f"{self.base_url}/auth/register", json=payload)

        # get token
        token_response = self.client.post(f"{self.base_url}/auth/token", json=payload)

        headers = {"Authorization": f"Bearer {token_response.json()["access_token"]}"}

        # post number
        req_data = {"number": "+9779841234567"}
        response = self.client.post(
            f"{self.base_url}/phonenumbers", headers=headers, json=req_data
        )

        response = self.client.get(f"{self.base_url}/phonenumbers", headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json()["data"], list)
        self.assertIn("pagination", response.json().keys())

    async def teardown_database(self):
        # Drop all tables to flush the database
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    def tearDown(self):
        app.dependency_overrides = {}
        # self.mock_db.reset_mock()
        self.teardown_database()


if __name__ == "__main__":
    unittest.main()
