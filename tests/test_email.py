from notifications.email_sender import EmailSender

email = EmailSender()

email.send_alert(
    vehicle_id=101,
    speed_kmh=92.5,
    threshold_kmh=80
)