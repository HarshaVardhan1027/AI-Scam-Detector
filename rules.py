import re

def rule_based_score(text):
    score = 0
    reasons = []
    text_lower = text.lower()

    # Urgency patterns
    if any(word in text_lower for word in ["urgent", "immediately", "now", "asap"]):
        score += 20
        reasons.append("Urgency language detected")

    # Sensitive info
    if any(word in text_lower for word in ["otp", "password", "pin"]):
        score += 30
        reasons.append("Request for sensitive information")

    # Suspicious links
    urls = re.findall(r'(https?://\S+)', text)
    if urls:
        score += 20
        reasons.append("Contains external link")

        # extra check
        if any(domain not in url for url in urls for domain in ["google.com", "amazon.in", "bank"]):
            score += 10
            reasons.append("Link may be suspicious")

    # Money-related traps
    if any(word in text_lower for word in ["win", "prize", "reward", "lottery"]):
        score += 20
        reasons.append("Too-good-to-be-true offer detected")

    # Fear tactics
    if any(word in text_lower for word in ["blocked", "suspended", "expired"]):
        score += 15
        reasons.append("Threat/fear language detected")

    return min(score, 100), reasons
