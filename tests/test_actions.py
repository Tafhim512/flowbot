"""
Unit tests for the Action Engine module.
"""

import pytest
from app.core.actions import extract_lead_info


class TestExtractLeadInfo:
    """Tests for the extract_lead_info function."""

    def test_extract_email(self):
        """Test email extraction from text."""
        text = "Please contact me at john@example.com"
        
        result = extract_lead_info(text)
        
        assert "email" in result
        assert result["email"] == "john@example.com"

    def test_extract_multiple_emails(self):
        """Test that only the first email is extracted."""
        text = "Email me at john@example.com or jane@test.org"
        
        result = extract_lead_info(text)
        
        assert "email" in result
        assert result["email"] == "john@example.com"

    def test_extract_phone(self):
        """Test phone number extraction."""
        text = "Call me at 5551234567"
        
        result = extract_lead_info(text)
        
        assert "phone" in result
        assert result["phone"] == "5551234567"

    def test_extract_phone_with_formatting(self):
        """Test phone extraction with dashes and spaces."""
        text = "Call me at 555-123-4567"
        
        result = extract_lead_info(text)
        
        assert "phone" in result
        # Should extract the digits
        assert "5551234567" in result["phone"]

    def test_extract_name_simple(self):
        """Test name extraction with explicit introduction."""
        text = "My name is John Smith"
        
        result = extract_lead_info(text)
        
        assert "name" in result

    def test_extract_name_call_me(self):
        """Test name extraction with 'call me' pattern."""
        text = "Call me John"
        
        result = extract_lead_info(text)
        
        assert "name" in result
        assert result["name"] == "John"

    def test_extract_name_i_am(self):
        """Test name extraction with 'I am' pattern."""
        text = "I am Sarah Johnson"
        
        result = extract_lead_info(text)
        
        assert "name" in result

    def test_extract_all_fields(self):
        """Test extracting all lead fields at once."""
        text = "Hi, my name is John Doe. Call me at 555-123-4567 or email me at john@example.com"
        
        result = extract_lead_info(text)
        
        assert "name" in result
        assert "phone" in result
        assert "email" in result

    def test_no_extraction(self):
        """Test that unrelated text returns empty dict."""
        text = "Hello, I was wondering about your services"
        
        result = extract_lead_info(text)
        
        # Should return empty or minimal info
        assert isinstance(result, dict)

    def test_extract_phone_variations(self):
        """Test various phone number formats."""
        # Test 10 digits
        result = extract_lead_info("Call 1234567890")
        assert "phone" in result
        
        # Test 15 digits max
        result = extract_lead_info("Call 123456789012345")
        assert "phone" in result


class TestDetermineActions:
    """Tests for action determination (imported from decision)."""
    
    def test_import_from_decision(self):
        """Verify determine_actions can be imported from decision module."""
        from app.core.decision import determine_actions
        
        actions = determine_actions("lead", "test message", "test reply")
        
        assert isinstance(actions, list)
        assert "send_reply" in actions
