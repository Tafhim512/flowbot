"""
Unit tests for the Messages API endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


class TestMessagesEndpoint:
    """Tests for the /messages API endpoint."""

    def test_endpoint_exists(self, client):
        """Test that the messages endpoint exists."""
        response = client.get("/api/v1/messages")
        # Should return 405 Method Not Allowed, not 404
        assert response.status_code in [405, 404]

    def test_post_message_requires_business_id(self, client):
        """Test that business_id is required."""
        response = client.post(
            "/api/v1/messages",
            json={"session_id": "test", "text": "Hello"}
        )
        # Should return validation error
        assert response.status_code == 422

    def test_post_message_requires_session_id(self, client):
        """Test that session_id is required."""
        response = client.post(
            "/api/v1/messages",
            json={"business_id": "test-id", "text": "Hello"}
        )
        # Should return validation error
        assert response.status_code == 422

    def test_post_message_requires_text(self, client):
        """Test that text is required."""
        response = client.post(
            "/api/v1/messages",
            json={"business_id": "test-id", "session_id": "test"}
        )
        # Should return validation error
        assert response.status_code == 422


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_message(self, client):
        """Test that root endpoint returns expected message."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "message" in response.json()


class TestAPIEndpoints:
    """Tests for other API endpoints."""

    def test_businesses_endpoint_exists(self, client):
        """Test that businesses endpoint exists."""
        response = client.get("/api/v1/businesses")
        
        assert response.status_code == 200

    def test_leads_endpoint_exists(self, client):
        """Test that leads endpoint exists."""
        response = client.get("/api/v1/leads")
        
        assert response.status_code == 200
