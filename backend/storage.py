from database.models import db, Complaint, StatusLog
from datetime import datetime
import pytz

utc = pytz.utc
ist = pytz.timezone("Asia/Kolkata")


def now_utc():
    return datetime.now(utc)


def save_complaint(complaint_id, user_input, category, subcategory, urgency, assigned_to):
    current_time_utc = now_utc()

    new_complaint = Complaint(
        complaint_id=complaint_id,
        user_input=user_input,
        category=category,
        subcategory=subcategory,
        urgency=urgency,
        status="Pending",
        assigned_to=assigned_to,
        created_at=current_time_utc,
        updated_at=current_time_utc,
    )
    db.session.add(new_complaint)

    new_log = StatusLog(
        complaint_id=complaint_id,
        status="Pending",
        assigned_to=assigned_to,
        timestamp=current_time_utc,
    )
    db.session.add(new_log)

    db.session.commit()
    return new_complaint


def get_complaint(complaint_id):
    return Complaint.query.filter_by(complaint_id=complaint_id.upper()).first()


def list_complaints():
    return Complaint.query.all()


def update_status(complaint_id, new_status, assigned_to=None):
    complaint = get_complaint(complaint_id)
    if not complaint:
        return None

    complaint.status = new_status
    if assigned_to:
        complaint.assigned_to = assigned_to

    current_time_utc = now_utc()
    complaint.updated_at = current_time_utc

    new_log = StatusLog(
        complaint_id=complaint_id,
        status=new_status,
        assigned_to=assigned_to or complaint.assigned_to,
        timestamp=current_time_utc,
    )
    db.session.add(new_log)
    db.session.commit()
    return complaint


def get_status_logs(complaint_id):
    return (
        StatusLog.query.filter_by(complaint_id=complaint_id.upper())
        .order_by(StatusLog.timestamp)
        .all()
    )


def update_complaint(complaint_id, data):
    complaint = get_complaint(complaint_id)
    if not complaint:
        return None

    original_status = complaint.status
    if "status" in data:
        complaint.status = data["status"]
    if "category" in data:
        complaint.category = data["category"]
    if "subcategory" in data:
        complaint.subcategory = data["subcategory"]
    if "urgency" in data:
        complaint.urgency = data["urgency"]
    if "assigned_to" in data:
        complaint.assigned_to = data["assigned_to"]

    current_time_utc = now_utc()
    complaint.updated_at = current_time_utc

    if "status" in data and data["status"] != original_status:
        new_log = StatusLog(
            complaint_id=complaint_id,
            status=data["status"],
            assigned_to=complaint.assigned_to,
            timestamp=current_time_utc,
        )
        db.session.add(new_log)

    db.session.commit()
    return complaint