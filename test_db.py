from database.db import SessionLocal
from database.models import SpeedAlert

db = SessionLocal()

try:
    alert = SpeedAlert(
        vehicle_id=999,
        speed_kmh=123.45,
        threshold_kmh=80,
        video_source="videos/test.mp4"
    )

    db.add(alert)
    db.commit()

    print("✅ Test alert inserted successfully!")

finally:
    db.close()