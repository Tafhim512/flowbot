"""
Action Engine module — executes planned actions based on AI response.
"""

import json
import re
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.models.business import Business
from app.models.lead import Lead
from app.models.action_log import ActionLog
from app.services.email_client import send_email
from app.core.decision import determine_actions


def extract_lead_info(text: str) -> Dict[str, Any]:
    """
    Extract lead information (name, phone, email) from text using simple regex patterns.
    """
    lead_info = {}
    
    # Extract email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        lead_info["email"] = emails[0]
    
    # Extract phone numbers (simple pattern)
    phone_pattern = r'\b\d{10,15}\b'
    phones = re.findall(phone_pattern, text.replace("-", "").replace(" ", ""))
    if phones:
        lead_info["phone"] = phones[0]
    
    # Extract names (simple approach - may need improvement)
    # This is a very basic name extraction - consider using NER (Named Entity Recognition) for better results
    if not lead_info.get("name"):
        # Look for "name" keyword followed by something that looks like a name
        name_match = re.search(r'(?:name|call me|i am|i\'m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text.lower())
        if name_match:
            lead_info["name"] = name_match.group(1).title()
    
    return lead_info


def create_lead(business: Business, lead_data: Dict[str, Any], db: Session) -> str:
    """
    Create a new lead in the database.
    """
    db_lead = Lead(
        business_id=business.id,
        **lead_data
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # Log the action
    log_action(
        business_id=business.id,
        action_type="create_lead",
        payload={"lead_id": str(db_lead.id)},
        db=db
    )
    
    return str(db_lead.id)


def schedule_booking(business: Business, booking_data: Dict[str, Any], db: Session) -> str:
    """
    Schedule a booking (mock implementation).
    """
    booking_id = "booking-" + business.slug + "-" + str(len(db.query(Lead).filter(Lead.business_id == business.id).all()) + 1)
    
    # Log the action
    log_action(
        business_id=business.id,
        action_type="schedule_booking",
        payload={"booking_id": booking_id, **booking_data},
        db=db
    )
    
    return booking_id


def log_action(business_id: str, action_type: str, payload: Dict[str, Any], db: Session):
    """
    Log an action in the actions_log table.
    """
    action_log = ActionLog(
        business_id=business_id,
        action_type=action_type,
        payload=payload
    )
    db.add(action_log)
    db.commit()
    db.refresh(action_log)


def execute_actions(business: Business, session_id: str, ai_response: Dict[str, str], db: Session) -> List[str]:
    """
    Execute the planned actions based on the AI response.
    """
    actions_taken = []
    
    # Determine which actions to take
    intent = ai_response["intent"]
    user_message = ai_response.get("user_message", "")
    ai_reply = ai_response["reply"]
    
    actions = determine_actions(intent, user_message, ai_reply)
    
    for action in actions:
        if action == "send_reply":
            actions_taken.append("send_reply")
            # In a real implementation, this would send a reply via WhatsApp or email
            pass
        
        elif action == "create_lead":
            # Extract lead info from conversation
            # For now, we'll just create a placeholder lead
            lead_info = extract_lead_info(user_message)
            if not lead_info:
                lead_info = {"source": "unknown"}
            lead_id = create_lead(business, lead_info, db)
            actions_taken.append(f"create_lead:{lead_id}")
        
        elif action == "send_email":
            # Mock email sending
            send_email(
                to="admin@" + business.slug + ".com",
                subject="Support Request",
                body=f"User message: {user_message}"
            )
            actions_taken.append("send_email")
        
        elif action == "schedule_booking":
            booking_id = schedule_booking(business, {"session_id": session_id}, db)
            actions_taken.append(f"schedule_booking:{booking_id}")
    
    return actions_taken
