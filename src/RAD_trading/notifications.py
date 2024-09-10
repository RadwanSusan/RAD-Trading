# src\RAD_trading\notifications.py
import yagmail
class EmailNotifier:
    def __init__(self, sender_email, sender_password):
        self.yag = yagmail.SMTP(sender_email, sender_password)
    def send_notification(self, subject, body, recipient):
        self.yag.send(
            to=recipient,
            subject=subject,
            contents=body,
        )
email_notifier = EmailNotifier("your_email@example.com", "your_email_password")
