import re
from typing import Dict, Any, List

def extract_entities_and_intent(text: str) -> Dict[str, Any]:
    """
    Parses unstructured text to extract system-critical entities and classify user intent.
     Runs locally with zero dependencies or external model latency.
    """
    if not text or not text.strip():
        return {"error": "Provided text is empty.", "entities": {}, "intent": "UNKNOWN"}

    # Entity Extraction Patterns 
    patterns = {
        "emails": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "urls": r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)',
        "dates": r'\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}(?:st|nd|rd|th)?,? \d{4})\b',
        "monetary_amounts": r'\b(?:[\$\€\£\₹\¥]\s?\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s?(?:USD|EUR|GBP|INR|bytes|MB|GB))\b',
        "ip_addresses": r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    }

    entities: Dict[str, List[str]] = {}
    for entity_name, pattern in patterns.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        # Drop duplicates(still preserving structure)
        entities[entity_name] = list(dict.fromkeys(matches))

    # Named Entity Recognition approximation 
    # Looks for sequences of capitalized words, ignoring the very start of lines
    proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    # Filter out common false positives 
    entities["proper_nouns"] = list(dict.fromkeys([name for name in proper_nouns if name.lower() not in [
        'the', 'a', 'an', 'hello', 'please', 'hey', 'if', 'when', 'my', 'our', 'your', 'this', 'you', 'i'
    ]]))

    # intent Classification Engine
    intent_keywords = {
        "FILE_READ": ["read", "get", "open", "fetch", "load", "view", "cat", "content", "workspace/"],
        "FILE_WRITE": ["write", "save", "dump", "output", "create file", "log to", "store in file", "append"],
        "WEB_RESEARCH": ["search", "google", "lookup", "find out", "news", "tavily", "web", "current status"],
        "MEMORY_STORE": ["remember", "save memory", "store context", "long-term", "keep in mind", "note down"],
        "ANALYZE_EMOTION": ["feeling", "emotion", "sentiment", "tone", "happy", "angry", "thrilled", "sad"]
    }

    intent_scores = {intent: 0 for intent in intent_keywords}
    tokens = re.findall(r'\b\w+\b', text.lower())

    for token in tokens:
        for intent, keywords in intent_keywords.items():
            if token in keywords:
                intent_scores[intent] += 1

    # identify top intent candidate, fallback to GENERAL_QUERY if scores are tied at zero
    max_score = max(intent_scores.values())
    if max_score > 0:
        detected_intent = max(intent_scores, key=intent_scores.get)
    else:
        detected_intent = "GENERAL_QUERY"

    return {
        "text_length": len(text),
        "intent": detected_intent,
        "intent_confidence_score": max_score,
        "entities": entities
    }