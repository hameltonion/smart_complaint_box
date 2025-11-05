import os
import sys
import logging
from flask import Flask
from dotenv import load_dotenv

# Internal imports
from paths import BACKEND_DIR, DEFAULT_SQLITE_URL, DATABASE_DIR

# Add backend folder to Python path
sys.path.append(str(BACKEND_DIR))

# Local backend modules
from database.models import db
from blueprints.user import user_bp
from blueprints.admin import admin_bp
from email_sender import get_email_sender
from ml_models import trainall

# ------------------------------------------------
# Load environment variables
# ------------------------------------------------
load_dotenv()

# ------------------------------------------------
# Flask App Setup
# ------------------------------------------------
# Serve frontend directly from /static
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
    static_url_path=""  # static files served directly at root (e.g., /style.css)
)

# ------------------------------------------------
# Database Configuration
# ------------------------------------------------
os.makedirs(DATABASE_DIR, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ------------------------------------------------
# Logging Configuration
# ------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-complaint-box")

# ------------------------------------------------
# Helper Functions
# ------------------------------------------------
def create_database():
    with app.app_context():
        db.create_all()
        logger.info("✅ Database tables created successfully.")

def check_models():
    MODEL_DIR = os.path.join("ml_models", "trained_data")
    REQUIRED_MODELS = ["category_model.pkl", "urgency_model.pkl"]
    return all(os.path.exists(os.path.join(MODEL_DIR, m)) for m in REQUIRED_MODELS)

def train_models_if_missing():
    if not check_models():
        logger.info("⚙️  Models missing — training now...")
        trainall.train_all()
        logger.info("✅ ML models trained successfully.")
    else:
        logger.info("✅ ML models found. Skipping training.")

# ------------------------------------------------
# Blueprints Registration
# ------------------------------------------------
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

# ------------------------------------------------
# Error Handlers
# ------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    # Optional: serve index.html for unknown paths (useful for SPA-like routing)
    index_path = os.path.join(app.static_folder, "index.html")
    if os.path.exists(index_path):
        return app.send_static_file("index.html")
    return "404: Page not found", 404

# ------------------------------------------------
# App Entry Point
# ------------------------------------------------
if __name__ == "__main__":
    create_database()
    train_models_if_missing()
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"🚀 Starting Smart Complaint Box on http://127.0.0.1:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)