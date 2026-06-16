from core.alert_manager import AlertManager

manager = AlertManager(threshold=80)

manager.process_alert(
    vehicle_id=500,
    speed_kmh=102.5,
)