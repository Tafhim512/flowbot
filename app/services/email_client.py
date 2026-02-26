"""
Email Client module — sends emails.
This is a mock implementation that logs emails to console.
For production, use a real email service like SendGrid or SMTP.
"""


def send_email(to: str, subject: str, body: str) -> bool:
    """
    Send an email (mock implementation).
    """
    print(f"=== Email Sent ===")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print("==================")
    
    return True


def send_lead_notification_email(lead_info: dict, business_name: str) -> bool:
    """
    Send a notification email about a new lead.
    """
    subject = f"New Lead for {business_name}"
    
    body = f"""
    A new lead has been captured for {business_name}!
    
    Lead Information:
    """
    for key, value in lead_info.items():
        if value:
            body += f"{key}: {value}\n"
    
    return send_email(
        to=f"admin@{business_name.lower().replace(' ', '')}.com",
        subject=subject,
        body=body
    )
