import uuid
import pytz
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, send_from_directory, current_app

from database.models import db
from backend.router import get_level1_department, get_level2_department
from backend.storage import save_complaint, get_complaint, get_status_logs, list_complaints
from backend.classifier import classify_complaint_text
from backend.relay import relay_email, tag_subject

logger = logging.getLogger(__name__)
ist = pytz.timezone("Asia/Kolkata")

# Blueprint (no template folder now)
user_bp = Blueprint("user", __name__)

# ---------------- Utility Functions ---------------- #

def calculate_eta_message(urgency):
    eta_hours = {"High": 6, "Medium": 12, "Low": 48}.get(urgency, 72)
    if eta_hours >= 24:
        days = eta_hours // 24
        hours_remainder = eta_hours % 24
        return f"{days} days" if hours_remainder == 0 else f"{days} days and {hours_remainder} hours"
    return f"{eta_hours} hours"

def to_ist(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(ist).isoformat()

# ---------------- Frontend Routes ---------------- #

@user_bp.route("/")
def index():
    return send_from_directory(current_app.static_folder, "index.html")

@user_bp.route("/track")
def track():
    return send_from_directory(current_app.static_folder, "track.html")

# ---------------- API Routes ---------------- #

@user_bp.route("/predict", methods=["POST"])
def predict():
    data = request.json
    complaint_text = data.get("complaint_text")
    if not complaint_text:
        return jsonify({"error": "Complaint text is required"}), 400

    try:
        classification = classify_complaint_text(complaint_text)
        category = classification["category"]
        subcategory = classification["subcategory"]
        urgency = classification["urgency"]

        return jsonify({
            "complaint_text": complaint_text,
            "category": category,
            "subcategory": subcategory,
            "urgency": urgency,
            "eta_message": calculate_eta_message(urgency),
            "assigned_to": get_level1_department(category, subcategory),
            "escalation_email": get_level2_department(category, subcategory),
        }), 200

    except ValueError:
        logger.error("Prediction error: models not loaded")
        return jsonify({"error": "Prediction models not loaded. Please train first."}), 500


@user_bp.route("/submit", methods=["POST"])
def submit():
    data = request.json
    complaint_text = data.get("complaint_text")
    urgency = data.get("urgency")
    category = data.get("category")
    subcategory = data.get("subcategory")
    assigned_to = data.get("assigned_to")

    if not all([complaint_text, urgency, category, subcategory, assigned_to]):
        return jsonify({"error": "Missing required data"}), 400

    complaint_id = str(uuid.uuid4()).split("-")[0].upper()

    try:
        new_complaint = save_complaint(
            complaint_id, complaint_text, category, subcategory, urgency, assigned_to
        )

        from backend.email_templates import build_complaint_email
        from backend.email_sender import get_email_sender
        from backend.router import get_level2_department, get_eta_message

        email_sender = get_email_sender()
        eta_message = get_eta_message(new_complaint.urgency)

        display_email = new_complaint.assigned_to
        to_email = relay_email(display_email)

        subject, body = build_complaint_email({
            "complaint_id": new_complaint.complaint_id,
            "category": new_complaint.category,
            "subcategory": new_complaint.subcategory,
            "urgency": new_complaint.urgency,
            "user_input": complaint_text,
            "assigned_to": display_email,
            "eta_message": eta_message,
        })

        subject = tag_subject(subject)
        email_sender.send_email(subject, body, to_email)

        return jsonify({
            "success": True,
            "complaint_id": new_complaint.complaint_id,
            "message": "Complaint submitted successfully!",
            "submitted_at": to_ist(new_complaint.created_at),
            "status": new_complaint.status,
            "category": new_complaint.category,
            "subcategory": new_complaint.subcategory,
            "urgency": new_complaint.urgency,
            "assigned_to": display_email,
            "eta_message": eta_message,
            "escalation_email": get_level2_department(new_complaint.category, new_complaint.subcategory),
        }), 200

    except Exception as e:
        logger.exception("Complaint submission failed.")
        db.session.rollback()
        return jsonify({"error": "Internal error during submission"}), 500


@user_bp.route("/get_status/<complaint_id>", methods=["GET"])
def get_status(complaint_id):
    complaint = get_complaint(complaint_id)
    if not complaint:
        return jsonify({"error": "Complaint not found"}), 404

    logs = get_status_logs(complaint_id)
    return jsonify({
        "complaint_id": complaint.complaint_id,
        "complaint_text": complaint.user_input,
        "status": complaint.status,
        "category": complaint.category,
        "subcategory": complaint.subcategory,
        "urgency": complaint.urgency,
        "assigned_to": complaint.assigned_to,
        "submitted_at": to_ist(complaint.created_at),
        "eta_message": calculate_eta_message(complaint.urgency),
        "escalation_email": get_level2_department(complaint.category, complaint.subcategory),
        "logs": [
            {"status": log.status, "assigned_to": log.assigned_to, "timestamp": to_ist(log.timestamp)}
            for log in logs
        ],
    }), 200


@user_bp.route("/list_complaints", methods=["GET"])
def list_all_complaints():
    complaints = list_complaints()
    return jsonify([
        {
            "complaint_id": c.complaint_id,
            "user_input": c.user_input,
            "submitted_at": to_ist(c.created_at),
            "status": c.status,
            "category": c.category,
            "subcategory": c.subcategory,
            "urgency": c.urgency or "Unknown",
            "assigned_to": c.assigned_to,
            "eta_message": calculate_eta_message(c.urgency or "Unknown"),
        }
        for c in complaints
    ])