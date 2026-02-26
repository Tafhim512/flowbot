"""
Unit tests for the Decision Engine module.
"""

import pytest
from app.core.decision import classify_intent, determine_actions


class TestClassifyIntent:
    """Tests for the classify_intent function."""

    def test_classify_question_intent(self):
        """Test that question intents are correctly classified."""
        business_config = {"faqs": []}
        
        # Test various question patterns
        assert classify_intent(business_config, "What are your hours?", []) == "question"
        assert classify_intent(business_config, "How much does it cost?", []) == "question"
        assert classify_intent(business_config, "When are you open?", []) == "question"
        assert classify_intent(business_config, "Where are you located?", []) == "question"

    def test_classify_lead_intent(self):
        """Test that lead intents are correctly classified."""
        business_config = {"faqs": []}
        
        # Test various lead patterns
        assert classify_intent(business_config, "I'm interested in your services", []) == "lead"
        assert classify_intent(business_config, "Please call me at 555-1234", []) == "lead"
        assert classify_intent(business_config, "Email me at test@example.com", []) == "lead"
        assert classify_intent(business_config, "I want to sign up", []) == "lead"

    def test_classify_booking_intent(self):
        """Test that booking intents are correctly classified."""
        business_config = {"faqs": []}
        
        # Test various booking patterns
        assert classify_intent(business_config, "I want to book an appointment", []) == "booking"
        assert classify_intent(business_config, "Can I schedule a time?", []) == "booking"
        assert classify_intent(business_config, "I'd like to reserve a table", []) == "booking"
        assert classify_intent(business_config, "What dates are available?", []) == "booking"

    def test_classify_support_intent(self):
        """Test that support intents are correctly classified."""
        business_config = {"faqs": []}
        
        # Test various support patterns
        assert classify_intent(business_config, "I need help", []) == "support"
        assert classify_intent(business_config, "There's a problem with my order", []) == "support"
        assert classify_intent(business_config, "It's not working", []) == "support"
        assert classify_intent(business_config, "I have a complaint", []) == "support"

    def test_classify_action_request_intent(self):
        """Test that action request intents are correctly classified."""
        business_config = {"faqs": []}
        
        # Test various action patterns
        assert classify_intent(business_config, "Please send me the document", []) == "action_request"
        assert classify_intent(business_config, "I want to download the file", []) == "action_request"
        assert classify_intent(business_config, "Cancel my subscription", []) == "action_request"
        assert classify_intent(business_config, "Update my information", []) == "action_request"

    def test_classify_default_intent(self):
        """Test that unrecognized messages default to question intent."""
        business_config = {"faqs": []}
        
        # Test ambiguous messages
        assert classify_intent(business_config, "Hello there", []) == "question"
        assert classify_intent(business_config, "Thanks", []) == "question"

    def test_classify_faq_based_intent(self):
        """Test that FAQ-based classification works."""
        business_config = {
            "faqs": [
                {"question": "Do you offer refunds?", "answer": "Yes, we do."}
            ]
        }
        
        # FAQ content should help classify intent
        assert classify_intent(business_config, "Do you offer refunds?", []) == "question"


class TestDetermineActions:
    """Tests for the determine_actions function."""

    def test_question_intent_actions(self):
        """Test actions for question intent."""
        actions = determine_actions("question", "What are your hours?", "We are open 9-5")
        
        assert "send_reply" in actions
        assert len(actions) == 1

    def test_lead_intent_actions(self):
        """Test actions for lead intent."""
        actions = determine_actions(
            "lead", 
            "I'm interested, call me at 555-1234",
            "We'll call you soon"
        )
        
        assert "send_reply" in actions
        assert "create_lead" in actions

    def test_booking_intent_actions(self):
        """Test actions for booking intent."""
        actions = determine_actions(
            "booking",
            "I want to book an appointment",
            "Let's schedule that for you"
        )
        
        assert "send_reply" in actions
        assert "schedule_booking" in actions

    def test_support_intent_actions(self):
        """Test actions for support intent."""
        actions = determine_actions(
            "support",
            "I have a problem",
            "How can we help?"
        )
        
        assert "send_reply" in actions
        assert "send_email" in actions

    def test_action_request_intent_actions(self):
        """Test actions for action request intent."""
        actions = determine_actions(
            "action_request",
            "Send me the document",
            "Sending document now"
        )
        
        assert "send_reply" in actions
