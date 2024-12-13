import unittest
import asyncio
from unittest.mock import  patch
from fastapi.testclient import TestClient
from fastapi import status

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core.database import Base
from main import app
from api.v1.utils.password import hash_password


from core.database import get_db


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class TestAuthAPI(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.base_url = "/api/v1/auth"
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
    async def test_register_user_success(self, mock_hash_password):
        """Test the /register endpoint for successful registration."""

        # Simulate no existing user in the database
        # self.mock_db.execute.return_value.scalar_one_or_none.return_value = None
        # app.dependency_overrides[get_db] = lambda: self.mock_db

        payload = {
            "email": "testuser@example.com",
            "password": "securepassword",
        }

        with patch(
            "api.v1.utils.password.hash_password",
            return_value="mock_hash_password",
        ):
            response = self.client.post(f"{self.base_url}/register", json=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("User registered successfully", response.json().get("message"))

    async def test_register_user_existing_email(self):
        """Test the /register endpoint when the email is already registered."""
        # existing_user = User(email="testuser@example.com", password="hashed_password")
        # self.mock_db.execute.return_value.scalar_one_or_none.return_value = (
        #     existing_user
        # )
        # app.dependency_overrides[get_db] = lambda: self.mock_db

        payload = {
            "email": "testuser@example.com",
            "password": "securepassword",
        }

        with patch(
            "api.v1.utils.password.hash_password",
            return_value="mock_hash_password",
        ):
            # register same user twice
            self.client.post(f"{self.base_url}/register", json=payload)
            response = self.client.post(f"{self.base_url}/register", json=payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email already registered!", response.json().get("detail"))

    async def test_create_token_success(self):
        """Test the /token endpoint for successful login."""
        payload = {
            "email": "testuser@example.com",
            "password": "securepassword",
        }

        with patch(
            "api.v1.utils.password.hash_password",
            return_value="mock_hash_password",
        ):
            # register same user twice
            self.client.post(f"{self.base_url}/register", json=payload)

        response = self.client.post(f"{self.base_url}/register", json=payload)

        with patch(
            "api.v1.utils.jwt.generate_tokens",
            return_value={
                "access_token": "fake_access",
                "refresh_token": "fake_refresh",
                "auth_type": "bearer",
            },
        ):
            response = self.client.post(f"{self.base_url}/token", json=payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.json())
        self.assertIn("refresh_token", response.json())

    async def test_create_token_invalid_credentials(self):
        """Test the /token endpoint with invalid credentials."""
        # self.mock_db.execute.return_value.scalar_one_or_none.return_value = None
        # app.dependency_overrides[get_db] = lambda: self.mock_db

        payload = {
            "email": "testuser@example.com",
            "password": "wrongpassword",
        }

        response = self.client.post(f"{self.base_url}/token", json=payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid credentials.", response.json().get("detail"))

    async def test_refresh_access_token_success(self):
        """Test the /refresh endpoint for successful token refresh."""
        payload = {"email": "testuser@example.com", "password": "password"}
        # register user
        self.client.post(f"{self.base_url}/register", json=payload)

        # create tokens
        token_response = self.client.post(f"{self.base_url}/token", json=payload)
        

        # mock_data = {"access_token": "mock_access_token", "auth_type": "bearer"}
        # with patch(
        #     "api.v1.utils.jwt.verify_token",
        #     return_value={"sub": ""},
        # ), patch("api.v1.utils.jwt.generate_tokens", return_value=mock_data):

        refresh_req_data = {"refresh_token": token_response.json().get("refresh_token")}
    
        # get access token from refresh
        response = self.client.post(f"{self.base_url}/refresh", json=refresh_req_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.json())

    async def test_refresh_access_token_invalid_token(self):
        """Test the /refresh endpoint with an invalid refresh token."""
        payload = {"refresh_token": "invalid_refresh_token"}

        with patch("api.v1.utils.jwt.verify_token", return_value=None):
            response = self.client.post(f"{self.base_url}/refresh", json=payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(
            "Invalid or expired token", response.json().get("detail")
        )

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
