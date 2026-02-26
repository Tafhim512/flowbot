"""
Unit tests for the Prompt Builder utility.
"""

import pytest
from app.utils.prompt_builder import build_system_prompt


class TestBuildSystemPrompt:
    """Tests for the build_system_prompt function."""

    def test_basic_prompt_generation(self):
        """Test basic prompt generation with minimal config."""
        business_config = {
            "business": {"name": "Test Business"},
            "role": "assistant",
            "personality": {"tone": "friendly", "language": "English"}
        }
        
        prompt = build_system_prompt(business_config, [])
        
        assert "Test Business" in prompt
        assert "assistant" in prompt
        assert "friendly" in prompt

    def test_prompt_includes_knowledge(self):
        """Test that knowledge snippets are included in prompt."""
        business_config = {
            "business": {"name": "Test Business"},
            "role": "assistant",
            "personality": {"tone": "professional", "language": "English"}
        }
        
        knowledge_snippets = [
            "Q: What are your hours?\nA: We're open 9-5",
            "Service: Consultation - $100"
        ]
        
        prompt = build_system_prompt(business_config, knowledge_snippets)
        
        assert "hours" in prompt
        assert "Consultation" in prompt

    def test_prompt_includes_rules(self):
        """Test that business rules are included."""
        business_config = {
            "business": {"name": "Test Business"},
            "role": "assistant",
            "personality": {"tone": "professional", "language": "English"},
            "rules": [
                "Be polite",
                "Confirm details before proceeding"
            ]
        }
        
        prompt = build_system_prompt(business_config, [])
        
        assert "Be polite" in prompt
        assert "Confirm details" in prompt

    def test_prompt_includes_services(self):
        """Test that services are included in prompt."""
        business_config = {
            "business": {"name": "Test Business"},
            "role": "assistant",
            "personality": {"tone": "professional", "language": "English"},
            "services": [
                "Consulting",
                "Training",
                "Support"
            ]
        }
        
        prompt = build_system_prompt(business_config, [])
        
        assert "Consulting" in prompt
        assert "Training" in prompt
        assert "Support" in prompt

    def test_prompt_with_empty_knowledge(self):
        """Test prompt generation with empty knowledge."""
        business_config = {
            "business": {"name": "Test Business"},
            "role": "assistant",
            "personality": {"tone": "friendly", "language": "English"}
        }
        
        prompt = build_system_prompt(business_config, [])
        
        assert "Test Business" in prompt
        assert "No specific knowledge available" in prompt

    def test_prompt_clinic_example(self):
        """Test prompt with clinic configuration."""
        business_config = {
            "business": {"name": "City Health Clinic"},
            "role": "medical_receptionist",
            "personality": {
                "tone": "professional",
                "language": "English",
                "greeting": "Hello! Welcome to City Health Clinic."
            }
        }
        
        prompt = build_system_prompt(business_config, [])
        
        assert "City Health Clinic" in prompt
        assert "medical_receptionist" in prompt
        assert "professional" in prompt

    def test_prompt_restaurant_example(self):
        """Test prompt with restaurant configuration."""
        business_config = {
            "business": {"name": "The Gourmet Kitchen"},
            "role": "restaurant_host",
            "personality": {
                "tone": "friendly",
                "language": "English",
                "greeting": "Welcome to The Gourmet Kitchen!"
            }
        }
        
        prompt = build_system_prompt(business_config, [])
        
        assert "The Gourmet Kitchen" in prompt
        assert "restaurant_host" in prompt
        assert "friendly" in prompt
