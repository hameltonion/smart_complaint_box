import os
import logging
import joblib
import subprocess
from pathlib import Path
from paths import TRAINED_DATA_DIR, SUBCATEGORY_MODELS_DIR, ML_MODELS_DIR

logger = logging.getLogger("classifier")

# Global model placeholders
cat_model = None
urg_model = None
subcategory_models = {}


def train_models():
    """
    Automatically runs trainall.py if trained models are missing.
    Adds project root to PYTHONPATH so 'paths' can be imported correctly.
    """
    train_script = ML_MODELS_DIR / "trainall.py"

    if not train_script.exists():
        logger.error("❌ Training script not found at %s", train_script)
        return False

    logger.warning("⚠️ Models missing. Running trainall.py automatically...")

    try:
        # ✅ Ensure Python can import 'paths' by adding project root to PYTHONPATH
        project_root = Path(__file__).resolve().parents[1]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root)

        subprocess.run(
            ["python", str(train_script)],
            check=True,
            cwd=ML_MODELS_DIR,  # run from ml_models folder
            env=env
        )

        logger.info("✅ Model retraining completed successfully.")
        return True

    except subprocess.CalledProcessError as e:
        logger.error("❌ Model training failed: %s", e)
        return False


def load_models():
    """
    Loads trained models. If missing, triggers auto-training.
    """
    global cat_model, urg_model, subcategory_models

    try:
        # Ensure directories exist
        if not TRAINED_DATA_DIR.exists():
            logger.warning("Trained data directory missing: %s", TRAINED_DATA_DIR)
            TRAINED_DATA_DIR.mkdir(parents=True, exist_ok=True)

        cat_path = TRAINED_DATA_DIR / "category_model.pkl"
        urg_path = TRAINED_DATA_DIR / "urgency_model.pkl"

        # ✅ Auto-train if models are missing
        if not (cat_path.exists() and urg_path.exists()):
            trained = train_models()
            if not trained:
                raise FileNotFoundError("Required model files not found and auto-train failed.")

        # Load category and urgency models
        cat_model = joblib.load(cat_path)
        urg_model = joblib.load(urg_path)

        # Load subcategory models
        subcategory_models.clear()
        if SUBCATEGORY_MODELS_DIR.exists():
            for filename in os.listdir(SUBCATEGORY_MODELS_DIR):
                if filename.endswith(".pkl"):
                    category = filename.split("_", 1)[-1].replace(".pkl", "")
                    model_path = SUBCATEGORY_MODELS_DIR / filename
                    subcategory_models[category.lower()] = joblib.load(model_path)

        logger.info("✅ Models loaded successfully. Subcategories: %s", list(subcategory_models.keys()))

    except FileNotFoundError as e:
        logger.error("❌ Model loading error: %s", e)
        raise
    except Exception as e:
        logger.exception("❌ Unexpected error while loading models: %s", e)
        raise


def classify_complaint_text(text: str):
    """
    Runs classification using loaded models.
    Automatically reloads if models are missing.
    """
    global cat_model, urg_model, subcategory_models

    if cat_model is None or urg_model is None:
        logger.warning("⚠️ Models not loaded in memory. Reloading...")
        load_models()

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


# ✅ Load models on import (auto-trains if missing)
load_models()