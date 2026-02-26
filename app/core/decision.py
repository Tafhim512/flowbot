"""
Decision Engine module — classifies user intent and determines next actions.
"""

from typing import Dict, List


def classify_intent(
    business_config: Dict,
    user_message: str,
    knowledge_snippets: List[str]
) -> str:
    """
    Classify the user's intent using a simple keyword-based approach.
    For production, this could be replaced with a more sophisticated classifier.
    """
    user_message = user_message.lower()

    # Intent categories with keywords
    intent_keywords = {
        "question": [
            "what", "how", "why", "when", "where", "who", "?"] + \
            [faq["question"].lower() for faq in business_config.get("faqs", [])],
        "lead": [
            "interested", "sign up", "contact", "call me", "email me",
            "name", "phone", "email", "address", "quote"],
        "booking": [
            "book", "schedule", "appointment", "reserve", "time", "date"],
        "support": [
            "help", "problem", "issue", "trouble", "complaint",
            "not working", "broken", "error"],
        "action_request": [
            "send", "download", "start", "stop", "cancel", "update"]
    }

    # Find matching intent
    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword.lower() in user_message:
                return intent

    # Default intent if no match
    return "question"


def determine_actions(
    intent: str,
    user_message: str,
    ai_reply: str
) -> List[str]:
    """
    Determine the next actions based on the intent.
    """
    actions = ["send_reply"]

    if intent == "lead":
        actions.append("create_lead")

    if intent == "booking":
        actions.append("schedule_booking")

    if intent == "support":
        actions.append("send_email")

    return actions
