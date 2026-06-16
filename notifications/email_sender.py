import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


class EmailSender:
    def __init__(self):
        self.sender = os.getenv("EMAIL_SENDER")
        self.password = os.getenv("EMAIL_APP_PASSWORD")
        self.receiver = os.getenv("EMAIL_RECEIVER")

    def send_alert(self, vehicle_id, speed_kmh, threshold_kmh):
        msg = EmailMessage()
        msg["Subject"] = "🚨 Speed Detection Alert"
        msg["From"] = self.sender
        msg["To"] = self.receiver

        msg.set_content(
            f"""
🚨 VEHICLE OVERSPEED DETECTED

Vehicle ID : {vehicle_id}
Speed      : {speed_kmh:.2f} km/h
Threshold  : {threshold_kmh:.2f} km/h

System: AI Speed Detection Module
"""
        )

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.starttls()
                smtp.login(self.sender, self.password)
                smtp.send_message(msg)

            print("✅ Email sent successfully!")

        except Exception as e:
            print("❌ Email failed:", str(e))