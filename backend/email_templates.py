# backend/email_templates.py
from datetime import datetime
import pytz

ist = pytz.timezone("Asia/Kolkata")

def build_complaint_email(complaint):
    """
    Builds a subject and plain-text email body for complaint notifications.
    Automatically timestamps in IST.
    """
    subject = f"[Smart Complaint Box] Complaint #{complaint['complaint_id']} – {complaint['category']} | {complaint['subcategory']}"
    submitted_at = datetime.now(ist).strftime("%d-%m-%Y %I:%M %p")

    body = f"""
Dear {complaint['assigned_to'].split('@')[0].replace('.', ' ').title()},  

A new complaint has been registered in the Smart Complaint Box System.  

📄 **Complaint Details:**  
• Complaint ID: {complaint['complaint_id']}  
• Category: {complaint['category']}  
• Subcategory: {complaint['subcategory']}  
• Urgency: {complaint['urgency']}  
• Assigned Department: {complaint['assigned_to']}  
• ETA for Resolution: {complaint['eta_message']}  
• Submitted At: {submitted_at}  

🗣️ **User Complaint Text:**  
"{complaint['user_input']}"  

Please take necessary action and update the system once resolved.  

Thank you,  
**Smart Complaint Box System**
    """.strip()

    return subject, body