from core.alert_manager import AlertManager

manager = AlertManager(threshold=80)

print(
    manager.process_alert(
        vehicle_id=1,
        speed_kmh=95.6,
    )
)

# Duplicate should NOT be inserted
print(
    manager.process_alert(
        vehicle_id=1,
        speed_kmh=110,
    )
)

# Different vehicle -> should insert
print(
    manager.process_alert(
        vehicle_id=2,
        speed_kmh=90,
    )
)

# Below threshold -> ignored
print(
    manager.process_alert(
        vehicle_id=3,
        speed_kmh=60,
    )
)