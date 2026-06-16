from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class SpeedAlert(Base):
    __tablename__ = "speed_alerts"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, nullable=False)
    speed_kmh = Column(Float, nullable=False)
    threshold_kmh = Column(Float, nullable=False)
    alert_time = Column(DateTime, default=datetime.utcnow)
    video_source = Column(String(255))