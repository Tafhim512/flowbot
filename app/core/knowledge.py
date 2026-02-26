"""
Knowledge System module — retrieves relevant information from the knowledge base.
"""

import json
import os
from typing import List, Dict, Any


def load_knowledge_files(knowledge_dir: str) -> Dict[str, List[Dict]]:
    """
    Load all knowledge files from a directory.
    """
    knowledge = {}
    
    if not os.path.exists(knowledge_dir):
        return knowledge
    
    for filename in os.listdir(knowledge_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(knowledge_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    knowledge[filename[:-5]] = data  # Remove .json extension
                except json.JSONDecodeError as e:
                    print(f"Error loading knowledge file {filename}: {e}")
    
    return knowledge


def retrieve_knowledge(business_config: Dict, user_message: str) -> List[str]:
    """
    Retrieve relevant knowledge snippets based on the user's message.
    """
    knowledge_snippets = []
    
    # Load knowledge files
    knowledge_dir = business_config.get("knowledge_dir", "")
    knowledge = load_knowledge_files(knowledge_dir)
    
    # Search for matching FAQs
    if "faqs" in knowledge:
        for faq in knowledge["faqs"]:
            if faq.get("question") and faq.get("answer"):
                if any(keyword in user_message.lower() for keyword in faq["question"].lower().split()):
                    knowledge_snippets.append(f"Q: {faq['question']}\nA: {faq['answer']}")
    
    # Search for matching services
    if "services" in knowledge:
        for service in knowledge["services"]:
            if any(keyword in user_message.lower() for keyword in service["name"].lower().split()):
                knowledge_snippets.append(f"Service: {service['name']}")
                if "description" in service:
                    knowledge_snippets.append(f"Description: {service['description']}")
                if "price" in service:
                    knowledge_snippets.append(f"Price: {service['price']}")
    
    # Search for pricing information
    if "pricing" in knowledge:
        for pricing in knowledge["pricing"]:
            item_name = pricing.get("name") or pricing.get("item", "")
            if item_name and any(keyword in user_message.lower() for keyword in item_name.lower().split()):
                knowledge_snippets.append(f"Item: {pricing.get('item', pricing.get('name', 'N/A'))}")
                if "price" in pricing:
                    knowledge_snippets.append(f"Price: {pricing['price']}")
    
    return knowledge_snippets
