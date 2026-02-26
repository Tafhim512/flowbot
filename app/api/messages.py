"""
API endpoint for handling incoming messages.
This is the main entry point for the AI automation platform.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.business import Business
from app.models.conversation import Conversation
from app.schemas.message import MessageInput, MessageOutput
from app.core.brain import generate_ai_response
from app.core.actions import execute_actions


router = APIRouter()


@router.post("/messages", response_model=MessageOutput)
def handle_message(input: MessageInput, db: Session = Depends(get_db)):
    """
    Receive a message from a user and return an AI response.
    - **business_id**: The unique ID of the business (from businesses table)
    - **session_id**: A unique ID for the conversation thread (groups messages)
    - **text**: The user's message text
    """
    # Get business from database
    business = db.query(Business).filter(Business.id == input.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    # Generate AI response
    ai_response = generate_ai_response(
        business=business,
        session_id=input.session_id,
        user_message=input.text,
        db=db
    )

    # Execute actions (send reply, create lead, etc.)
    actions_taken = execute_actions(
        business=business,
        session_id=input.session_id,
        ai_response=ai_response,
        db=db
    )

    # Save user message to conversations table
    user_conversation = Conversation(
        business_id=input.business_id,
        session_id=input.session_id,
        role="user",
        content=input.text
    )
    db.add(user_conversation)

    # Save AI reply to conversations table
    ai_conversation = Conversation(
        business_id=input.business_id,
        session_id=input.session_id,
        role="assistant",
        content=ai_response["reply"]
    )
    db.add(ai_conversation)

    db.commit()
    db.refresh(user_conversation)
    db.refresh(ai_conversation)

    # Return response
    return {
        "reply": ai_response["reply"],
        "intent": ai_response["intent"],
        "actions_taken": actions_taken,
        "session_id": input.session_id
    }
