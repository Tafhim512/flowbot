"""
LLM Client module — wrapper for LLM API calls.
"""

import os
from typing import List, Dict, Any

from app.config import settings
from openai import OpenAI


def call_llm(system_prompt: str, history: List[Dict[str, str]], user_message: str) -> str:
    """
    Call the LLM API to generate a response.
    """
    # Initialize OpenAI client
    client = OpenAI(
        api_key=settings.OPENAI_API_KEY
    )

    # Prepare messages
    messages = [
        {"role": "system", "content": system_prompt}
    ]

    # Add conversation history
    for turn in history[-10:]:  # Only keep last 10 turns to avoid context window issues
        messages.append({"role": turn["role"], "content": turn["content"]})

    # Add current user message
    messages.append({"role": "user", "content": user_message})

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Fallback response if API call fails
        print(f"LLM API call failed: {e}")
        return "I'm sorry, but I'm having trouble processing your request right now. Please try again later."
