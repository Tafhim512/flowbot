"""
Unit tests for the Knowledge System module.
"""

import pytest
import json
import os
from app.core.knowledge import retrieve_knowledge, load_knowledge_files


class TestRetrieveKnowledge:
    """Tests for the retrieve_knowledge function."""

    def test_retrieve_faq_knowledge(self):
        """Test FAQ retrieval based on user message."""
        business_config = {"knowledge_dir": "knowledge_base/demo_clinic"}
        
        # Search for hours-related content
        snippets = retrieve_knowledge(business_config, "What are your office hours?")
        
        # Should find relevant FAQ
        assert len(snippets) > 0
        assert any("hours" in snippet.lower() for snippet in snippets)

    def test_retrieve_service_knowledge(self):
        """Test service retrieval based on user message."""
        business_config = {"knowledge_dir": "knowledge_base/demo_clinic"}
        
        # Search for service-related content
        snippets = retrieve_knowledge(business_config, "What services do you offer?")
        
        # Should find relevant services
        assert len(snippets) > 0

    def test_retrieve_pricing_knowledge(self):
        """Test pricing retrieval based on user message."""
        business_config = {"knowledge_dir": "knowledge_base/demo_clinic"}
        
        # Search for pricing-related content
        snippets = retrieve_knowledge(business_config, "How much does a checkup cost?")
        
        # Should find relevant pricing
        assert len(snippets) > 0

    def test_retrieve_no_match(self):
        """Test that unrelated queries return empty or minimal results."""
        business_config = {"knowledge_dir": "knowledge_base/demo_clinic"}
        
        # Search for unrelated content
        snippets = retrieve_knowledge(business_config, "xyz123 nonsense query")
        
        # May return empty or minimal results
        assert isinstance(snippets, list)

    def test_retrieve_with_empty_config(self):
        """Test handling of empty configuration."""
        business_config = {}
        
        # Should not crash
        snippets = retrieve_knowledge(business_config, "Hello")
        assert isinstance(snippets, list)

    def test_retrieve_restaurant_knowledge(self):
        """Test restaurant knowledge retrieval."""
        business_config = {"knowledge_dir": "knowledge_base/demo_restaurant"}
        
        # Search for restaurant content
        snippets = retrieve_knowledge(business_config, "Do you take reservations?")
        
        assert len(snippets) > 0


class TestLoadKnowledgeFiles:
    """Tests for the load_knowledge_files function."""

    def test_load_clinic_knowledge(self):
        """Test loading clinic knowledge files."""
        knowledge = load_knowledge_files("knowledge_base/demo_clinic")
        
        # Should have loaded files
        assert isinstance(knowledge, dict)

    def test_load_restaurant_knowledge(self):
        """Test loading restaurant knowledge files."""
        knowledge = load_knowledge_files("knowledge_base/demo_restaurant")
        
        # Should have loaded files
        assert isinstance(knowledge, dict)

    def test_load_nonexistent_directory(self):
        """Test handling of non-existent directory."""
        knowledge = load_knowledge_files("nonexistent_directory")
        
        # Should return empty dict
        assert knowledge == {}

    def test_knowledge_file_structure(self):
        """Test that loaded knowledge has expected structure."""
        knowledge = load_knowledge_files("knowledge_base/demo_clinic")
        
        # If files exist, check structure
        if "faqs" in knowledge:
            assert isinstance(knowledge["faqs"], list)
