import cv2
import os
from ultralytics import YOLO
from core.speed_estimator import SpeedEstimator
from core.alert_manager import AlertManager

# ----------------------------
# CONFIG
# ----------------------------
VIDEO_PATH = "videos/1.mp4"
OUTPUT_PATH = "output/result.mp4"

# Create output folder if missing
os.makedirs("output", exist_ok=True)

# ----------------------------
# LOAD MODEL
# ----------------------------
model = YOLO("yolov8n.pt")

# ----------------------------
# VIDEO SETUP
# ----------------------------
cap = cv2.VideoCapture(VIDEO_PATH)

fps = cap.get(cv2.CAP_PROP_FPS)

if fps == 0:
    fps = 30

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"[INFO] FPS: {fps}")
print(f"[INFO] Resolution: {width}x{height}")

# Speed estimator
speed_estimator = SpeedEstimator(
    ppm=80,
    fps=fps
)
alert_manager = AlertManager(threshold=80)

# Output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(
    OUTPUT_PATH,
    fourcc,
    fps,
    (width, height)
)

# Vehicle classes in COCO
VEHICLE_CLASSES = [2, 3, 5, 7]

# ----------------------------
# MAIN LOOP
# ----------------------------
while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    # YOLO Tracking
    results = model.track(
        frame,
        persist=True,
        verbose=False
    )[0]

    if results.boxes.id is not None:

        boxes = results.boxes.xyxy.cpu().numpy()
        ids = results.boxes.id.cpu().numpy().astype(int)
        classes = results.boxes.cls.cpu().numpy().astype(int)

        for box, track_id, cls in zip(boxes, ids, classes):

            if cls not in VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box)

            # Centroid
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # Speed
            speed = speed_estimator.update(
                track_id,
                (cx, cy)
            )

            # ------------------------
            # ALERT CHECK
            # ------------------------
            alert_manager.process_alert(
                vehicle_id=track_id,
                speed_kmh=speed,
                video_source=VIDEO_PATH
            )

            # Draw Box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Draw Centroid
            cv2.circle(
                frame,
                (cx, cy),
                4,
                (255, 0, 0),
                -1
            )

            # Label
            cv2.putText(
                frame,
                f"ID {track_id} | {speed:.1f} km/h",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

    # Save frame
    out.write(frame)

    # Display
    cv2.imshow(
        "Vehicle Speed Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------------------
# CLEANUP
# ----------------------------
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"[DONE] Output saved at: {OUTPUT_PATH}")