import json
import logging
from paths import ROUTING_CONFIG_PATH

logger = logging.getLogger("router")

ETA_MAPPING = {
    "High": "within 4 hours",
    "Medium": "within 1 business day",
    "Low": "within 3 business days",
    "default": "within 7 business days"
}

def load_routing_config():
    if ROUTING_CONFIG_PATH.exists():
        try:
            with open(ROUTING_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error("Failed to load routing config: %s", e)
    return {}

ROUTING = load_routing_config()

def get_level1_department(category: str, subcategory: str) -> str:
    """Return real department email (never relayed)."""
    return ROUTING.get(category, {}).get(subcategory, {}).get(
        "level1",
        ROUTING.get(category, {}).get("default", {}).get("level1", "general.inquiries@example.com")
    )

def get_level2_department(category: str, subcategory: str) -> str:
    """Return real escalation email (never relayed)."""
    return ROUTING.get(category, {}).get(subcategory, {}).get(
        "level2",
        ROUTING.get(category, {}).get("default", {}).get("level2", "general.escalation@example.com")
    )

def get_eta_message(urgency: str) -> str:
    return ETA_MAPPING.get(urgency, ETA_MAPPING["default"])