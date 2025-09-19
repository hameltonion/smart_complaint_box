from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Complaint(db.Model):
    __tablename__ = 'complaints'
    
    complaint_id = db.Column(db.String(50), primary_key=True)
    user_input = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50), nullable=False)
    urgency = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    assigned_to = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Complaint {self.complaint_id} {self.category}/{self.subcategory} {self.status}>"

class Department(db.Model):
    __tablename__ = 'departments'
    
    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50), nullable=False)
    level1_email = db.Column(db.String(100))
    level2_email = db.Column(db.String(100))
    level3_email = db.Column(db.String(100))

    __table_args__ = (
        db.UniqueConstraint("category", "subcategory", name="uq_category_subcategory"),
    )

    def __repr__(self):
        return f"<Department {self.category}/{self.subcategory}>"

class StatusLog(db.Model):
    __tablename__ = 'status_log'
    
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    complaint_id = db.Column(db.String(50), db.ForeignKey('complaints.complaint_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    assigned_to = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    complaint = db.relationship(
        'Complaint', 
        backref=db.backref('status_logs', lazy=True, cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<StatusLog {self.complaint_id} {self.status} at {self.timestamp}>"