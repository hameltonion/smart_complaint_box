import os
import logging
import joblib

# Import centralized paths
from paths import TRAINED_DATA_DIR, SUBCATEGORY_MODELS_DIR

logger = logging.getLogger("classifier")

# Models
cat_model = None
urg_model = None
subcategory_models = {}

try:
    if not TRAINED_DATA_DIR.exists():
        raise FileNotFoundError(f"Models directory not found: {TRAINED_DATA_DIR}")

    cat_model = joblib.load(TRAINED_DATA_DIR / "category_model.pkl")
    urg_model = joblib.load(TRAINED_DATA_DIR / "urgency_model.pkl")

    if SUBCATEGORY_MODELS_DIR.exists():
        for filename in os.listdir(SUBCATEGORY_MODELS_DIR):
            if filename.endswith(".pkl"):
                category = filename.split("_", 1)[-1].replace(".pkl", "")
                model_path = SUBCATEGORY_MODELS_DIR / filename
                subcategory_models[category.lower()] = joblib.load(model_path)

    logger.info("✅ Models loaded successfully. Subcategories: %s", list(subcategory_models.keys()))

except FileNotFoundError as e:
    logger.error("Model loading error: %s", e)
    raise
except Exception as e:
    logger.exception("Unexpected error while loading models: %s", e)
    raise


def classify_complaint_text(text: str):
    """Run classification using loaded models."""
    if cat_model is None or urg_model is None:
        raise ValueError("Models are not loaded. Please train first.")

    category = cat_model.predict([text])[0]
    urgency = urg_model.predict([text])[0]

    subcategory = None
    subcat_model = subcategory_models.get(category.lower())
    if subcat_model:
        subcategory = subcat_model.predict([text])[0]

    return {
        "category": category,
        "subcategory": subcategory,
        "urgency": urgency
    }