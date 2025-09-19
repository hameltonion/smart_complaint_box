import os
import sys
import logging
from flask import Flask
from dotenv import load_dotenv

from paths import BACKEND_DIR, FRONTEND_DIR, DEFAULT_SQLITE_URL, DATABASE_DIR

# Add backend to path
sys.path.append(str(BACKEND_DIR))

# Local imports
from database.models import db
from blueprints.user import user_bp
from blueprints.admin import admin_bp
from email_sender import get_email_sender

# ML training (optional)
from ml_models import trainall

# -----------------------
# Setup
# -----------------------
load_dotenv()

app = Flask(__name__, template_folder=str(FRONTEND_DIR))

# Database setup
os.makedirs(DATABASE_DIR, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-complaint-box")

# -----------------------
# Database & ML
# -----------------------
def create_database():
    with app.app_context():
        db.create_all()
        logger.info("✅ Database tables created.")

def check_models():
    MODEL_DIR = os.path.join("ml_models", "trained_data")
    REQUIRED_MODELS = ["category_model.pkl", "urgency_model.pkl"]
    return all(os.path.exists(os.path.join(MODEL_DIR, m)) for m in REQUIRED_MODELS)

def train_models_if_missing():
    if not check_models():
        logger.info("Models missing. Training now...")
        trainall.train_all()
        logger.info("✅ ML models trained.")
    else:
        logger.info("All ML models found. Skipping training.")

# -----------------------
# Blueprints
# -----------------------
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    create_database()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)