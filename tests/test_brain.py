"""
Unit tests for the AI Brain module.
"""

import pytest
from unittest.mock import Mock, patch
from app.core.brain import get_conversation_history, load_business_config


class TestLoadBusinessConfig:
    """Tests for loading business configuration."""

    def test_load_demo_clinic_config(self):
        """Test loading the demo clinic configuration."""
        # Create a mock business object
        mock_business = Mock()
        mock_business.config_path = "business_configs/demo_clinic.yaml"
        
        # Should load successfully
        config = load_business_config(mock_business)
        
        assert config is not None
        assert "business" in config
        assert config["business"]["name"] == "City Health Clinic"

    def test_load_demo_restaurant_config(self):
        """Test loading the demo restaurant configuration."""
        mock_business = Mock()
        mock_business.config_path = "business_configs/demo_restaurant.yaml"
        
        config = load_business_config(mock_business)
        
        assert config is not None
        assert "business" in config
        assert config["business"]["name"] == "The Gourmet Kitchen"

    def test_load_template_config(self):
        """Test loading the template configuration."""
        mock_business = Mock()
        mock_business.config_path = "business_configs/_template.yaml"
        
        config = load_business_config(mock_business)
        
        assert config is not None
        assert "business" in config

    def test_load_nonexistent_config(self):
        """Test error handling for non-existent config file."""
        mock_business = Mock()
        mock_business.config_path = "nonexistent/path.yaml"
        
        with pytest.raises(FileNotFoundError):
            load_business_config(mock_business)


class TestGetConversationHistory:
    """Tests for conversation history retrieval."""

    def test_history_structure(self):
        """Test that conversation history returns proper structure."""
        # This test verifies the function signature and structure
        # In real tests, we would mock the database
        
        # Verify function exists and is callable
        assert callable(get_conversation_history)
        
        # Function should accept the expected parameters
        import inspect
        sig = inspect.signature(get_conversation_history)
        params = list(sig.parameters.keys())
        
        assert "business_id" in params
        assert "session_id" in params
        assert "db" in params


class TestGenerateAIResponse:
    """Tests for AI response generation."""

    def test_response_structure(self):
        """Test that generate_ai_response returns expected structure."""
        from app.core.brain import generate_ai_response
        
        # Verify function exists
        assert callable(generate_ai_response)
        
        # Check function signature
        import inspect
        sig = inspect.signature(generate_ai_response)
        params = list(sig.parameters.keys())
        
        assert "business" in params
        assert "session_id" in params
        assert "user_message" in params
        assert "db" in params
