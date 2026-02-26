"""
AI Brain module — LLM integration and conversation memory handling.
"""

import yaml
import json
import os
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.models.business import Business
from app.models.conversation import Conversation
from app.services.llm_client import call_llm
from app.utils.prompt_builder import build_system_prompt
from app.core.knowledge import retrieve_knowledge
from app.core.decision import classify_intent


def load_business_config(business: Business) -> Dict[str, Any]:
    """
    Load business configuration from YAML file.
    """
    config_path = business.config_path
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Business config file not found: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_conversation_history(business_id: str, session_id: str, db: Session) -> List[Dict[str, str]]:
    """
    Get the conversation history for a specific session.
    """
    history = db.query(Conversation).filter(
        Conversation.business_id == business_id,
        Conversation.session_id == session_id
    ).order_by(Conversation.created_at).all()
    
    return [
        {"role": conv.role, "content": conv.content}
        for conv in history
    ]


def generate_ai_response(
    business: Business,
    session_id: str,
    user_message: str,
    db: Session
) -> Dict[str, str]:
    """
    Generate an AI response to a user message using LLM integration.
    """
    # Load business config
    business_config = load_business_config(business)

    # Get conversation history
    history = get_conversation_history(business.id, session_id, db)

    # Retrieve relevant knowledge (FAQs, services, pricing)
    knowledge_snippets = retrieve_knowledge(business_config, user_message)

    # Classify user intent
    intent = classify_intent(business_config, user_message, knowledge_snippets)

    # Build system prompt
    system_prompt = build_system_prompt(business_config, knowledge_snippets)

    # Call LLM
    ai_reply = call_llm(system_prompt, history, user_message)

    return {
        "reply": ai_reply,
        "intent": intent
    }
