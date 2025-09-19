import os
import logging
from flask import Flask
from dotenv import load_dotenv

from paths import BACKEND_DIR, FRONTEND_DIR, DEFAULT_SQLITE_URL, DATABASE_DIR
import sys

# Add backend for imports
sys.path.append(str(BACKEND_DIR))

# Local imports
from database.models import db
from blueprints.user import user_bp
from blueprints.admin import admin_bp
from email_sender import get_email_sender

# -----------------------
# Setup
# -----------------------
load_dotenv()

app = Flask(__name__, template_folder=str(FRONTEND_DIR))

# Database
os.makedirs(DATABASE_DIR, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smart-complaint-box")


def create_database():
    with app.app_context():
        db.create_all()
        logger.info("✅ Database tables created.")


# Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    create_database()
    app.run(debug=True, host="127.0.0.1", port=5000)