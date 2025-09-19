import logging
import os
import pytz
from flask import Blueprint, request, render_template, jsonify
from datetime import datetime

from backend.storage import list_complaints, update_complaint, get_complaint
from backend.router import get_level1_department
from database.models import db
from paths import FRONTEND_DIR
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

admin_bp = Blueprint("admin_bp", __name__, template_folder=str(FRONTEND_DIR))
logger = logging.getLogger("smart-complaint-box")
ist = pytz.timezone("Asia/Kolkata")

# Load admin keys from .env
ADMIN_KEY = os.getenv("ADMIN_KEY", "default_admin_key")
MODIFY_KEY = os.getenv("MODIFY_KEY", "default_modify_key")


def to_ist(dt):
    if not dt:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.utc)
    return dt.astimezone(ist)


@admin_bp.route("/admin")
def admin_page():
    all_complaints = list_complaints()
    for c in all_complaints:
        c.created_at = to_ist(c.created_at)
        c.updated_at = to_ist(c.updated_at)
    return render_template("admin.html", complaints=all_complaints)


@admin_bp.route("/verify_key", methods=["POST"])
def verify_key():
    data = request.json
    key = data.get("key")

    if key == ADMIN_KEY:
        return jsonify({"success": True, "permission_level": "read-only"}), 200
    elif key == MODIFY_KEY:
        return jsonify({"success": True, "permission_level": "read-write"}), 200
    return jsonify({"success": False, "error": "Invalid key"}), 401


@admin_bp.route("/update_complaint", methods=["POST"])
def update_complaint_details():
    """Update complaint details (status, category, subcategory, urgency, assigned_to)."""
    data = request.json
    complaint_id = data.get("complaint_id")
    modify_key = data.get("modify_key")

    if modify_key != MODIFY_KEY:
        return jsonify({"error": "Invalid modification key"}), 401

    updates = {
        key: data[key]
        for key in ["status", "category", "subcategory", "urgency", "assigned_to"]
        if key in data
    }

    if "category" in updates or "subcategory" in updates:
        complaint = get_complaint(complaint_id)
        if complaint:
            new_assigned_to = get_level1_department(
                updates.get("category", complaint.category),
                updates.get("subcategory", complaint.subcategory),
            )
            updates["assigned_to"] = new_assigned_to

    if not complaint_id or not updates:
        return jsonify({"error": "Complaint ID and at least one field to update are required"}), 400

    try:
        updated_complaint = update_complaint(complaint_id, updates)
        if updated_complaint:
            return jsonify(
                {
                    "success": True,
                    "message": f"Complaint {complaint_id} updated successfully",
                    "updated": {
                        "status": updated_complaint.status,
                        "category": updated_complaint.category,
                        "subcategory": updated_complaint.subcategory,
                        "urgency": updated_complaint.urgency,
                        "assigned_to": updated_complaint.assigned_to,
                        "updated_at": to_ist(updated_complaint.updated_at).strftime("%d-%m-%Y %H:%M"),
                    },
                }
            ), 200
        else:
            return jsonify({"error": "Complaint not found"}), 404
    except Exception as e:
        db.session.rollback()
        logger.exception("Complaint update error: %s", e)
        return jsonify({"error": "Failed to update complaint"}), 500


@admin_bp.route("/delete_complaint", methods=["POST"])
def delete_complaint():
    """Delete a complaint by ID (for admin use only)."""
    data = request.json
    complaint_id = data.get("complaint_id")
    modify_key = data.get("modify_key")

    if modify_key != MODIFY_KEY:
        return jsonify({"error": "Invalid modification key"}), 401

    try:
        complaint = get_complaint(complaint_id)
        if not complaint:
            return jsonify({"error": "Complaint not found"}), 404

        db.session.delete(complaint)
        db.session.commit()
        return jsonify({"success": True, "message": f"Complaint {complaint_id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.exception("Complaint delete error: %s", e)
        return jsonify({"error": "Failed to delete complaint"}), 500