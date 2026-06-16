from datetime import datetime

from database.db import SessionLocal
from database.models import SpeedAlert
from notifications.email_sender import EmailSender


class AlertManager:

    def __init__(self, threshold=80):

        self.threshold = threshold

        # Prevent duplicate alerts
        self.alerted_vehicle_ids = set()

        # Email sender
        self.email_sender = EmailSender()

    def process_alert(
        self,
        vehicle_id,
        speed_kmh,
        video_source="videos/1.mp4"
    ):

        # Ignore below threshold
        if speed_kmh <= self.threshold:
            return False

        # Ignore duplicate alerts in same run
        if vehicle_id in self.alerted_vehicle_ids:
            return False

        db = SessionLocal()

        try:

            # ------------------------
            # CHECK EXISTING ALERT
            # ------------------------
            existing_alert = (
                db.query(SpeedAlert)
                .filter(
                    SpeedAlert.vehicle_id == int(vehicle_id)
                )
                .first()
            )

            # ------------------------
            # UPDATE EXISTING
            # ------------------------
            if existing_alert:

                existing_alert.speed_kmh = round(
                    float(speed_kmh), 2
                )

                existing_alert.threshold_kmh = float(
                    self.threshold
                )

                existing_alert.alert_time = datetime.now()

                existing_alert.video_source = (
                    video_source
                )

            # ------------------------
            # INSERT NEW
            # ------------------------
            else:

                alert = SpeedAlert(
                    vehicle_id=int(vehicle_id),
                    speed_kmh=round(
                        float(speed_kmh), 2
                    ),
                    threshold_kmh=float(
                        self.threshold
                    ),
                    alert_time=datetime.now(),
                    video_source=video_source
                )

                db.add(alert)

            # IMPORTANT
            db.commit()

            # ------------------------
            # SEND EMAIL
            # ------------------------
            self.email_sender.send_alert(
                vehicle_id=vehicle_id,
                speed_kmh=speed_kmh,
                threshold_kmh=self.threshold
            )

            # Prevent duplicate emails
            self.alerted_vehicle_ids.add(
                vehicle_id
            )

            print(
                f"[ALERT] Vehicle {vehicle_id} "
                f"Speed: {speed_kmh:.2f} km/h"
            )

            return True

        except Exception as e:

            print("❌ Alert processing failed")
            print(e)

            db.rollback()

            return False

        finally:
            db.close()