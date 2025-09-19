# smart_complaint_box/paths.py
from pathlib import Path

# Base directory (root of the project)
BASE_DIR = Path(__file__).resolve().parent

# Common subdirectories
BACKEND_DIR = BASE_DIR / "backend"
CONFIG_DIR = BASE_DIR / "config"
DATABASE_DIR = BASE_DIR / "database"
DOCS_DIR = BASE_DIR / "docs"
FRONTEND_DIR = BASE_DIR / "frontend"
ML_MODELS_DIR = BASE_DIR / "ml_models"
TRAINED_DATA_DIR = ML_MODELS_DIR / "trained_data"
SUBCATEGORY_MODELS_DIR = TRAINED_DATA_DIR / "subcategory_models"
DATASET_PATH = ML_MODELS_DIR / "dataset" / "complaints.csv"

# Config files
ROUTING_CONFIG_PATH = CONFIG_DIR / "routing.json"
ESCALATION_CONFIG_PATH = CONFIG_DIR / "escalation.json"

# Database
DB_FILE = DATABASE_DIR / "smart_complaint_box.db"
DEFAULT_SQLITE_URL = f"sqlite:///{DB_FILE}"