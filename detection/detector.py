from ultralytics import YOLO

class VehicleDetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        results = self.model(frame)[0]

        detections = []

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls in [2, 3, 5, 7]:
                x1, y1, x2, y2 = box.xyxy[0]

                detections.append([
                    x1,
                    y1,
                    x2,
                    y2,
                    conf,
                    cls
                ])

        return detections