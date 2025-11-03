import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("relay")

# Load once at import time
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
DEMO_EMAIL = os.getenv("DEMO_EMAIL", "your_email@gmail.com")

def relay_email(original_email: str) -> str:
    """
    Returns the target email for sending.
    If DEMO_MODE is enabled, routes every email to DEMO_EMAIL.
    Otherwise, returns the department email as-is.
    """
    if DEMO_MODE:
        logger.info(f"[RELAY] Redirecting '{original_email}' → '{DEMO_EMAIL}' (demo mode)")
        return DEMO_EMAIL
    return original_email


def tag_subject(subject: str) -> str:
    """
    Prefixes the subject with [DEMO] if in demo mode.
    Helps identify demo messages in your inbox easily.
    """
    if DEMO_MODE:
        return f"[DEMO] {subject}"
    return subject