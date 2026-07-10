def send_mock_email(email_to: str, subject: str, message: str):
    """
    Mock email sender that prints to console.
    In a real application, replace this with SendGrid, SES, SMTP, etc.
    """
    print("-" * 50)
    print(f"MOCK EMAIL SENT TO: {email_to}")
    print(f"SUBJECT: {subject}")
    print(f"MESSAGE:\n{message}")
    print("-" * 50)
