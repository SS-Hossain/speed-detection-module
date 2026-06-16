# 🚗 AI Vehicle Speed Detection System

An AI-powered vehicle speed detection system built using **YOLOv8**, **OpenCV**, **PostgreSQL**, and **Python**.

The system detects vehicles from a video source, tracks them across frames, estimates their speed, generates overspeed alerts, sends email notifications, and stores alerts in a PostgreSQL database.

---

## ✨ Features

* Vehicle Detection using YOLOv8
* Multi-object Vehicle Tracking
* Speed Estimation with Smoothing
* Overspeed Alert Generation
* Email Notifications
* PostgreSQL Alert Storage
* Alert Deduplication
* Video Processing Pipeline
* Modular Project Structure
* Ready for Future RTSP Integration

---

## 🏗️ Project Architecture

```text
Video Input
     │
     ▼
YOLOv8 Detection
     │
     ▼
Vehicle Tracking
     │
     ▼
Speed Estimation
     │
     ▼
Overspeed Detection
     │
     ├─────────────► Email Alert
     │
     ▼
PostgreSQL Database
```

---

## 📂 Project Structure

```text
speed_detection_module/
│
├── videos/
│   └── 1.mp4
│
├── output/
│   └── result.mp4
│
├── core/
│   ├── speed_estimator.py
│   └── alert_manager.py
│
├── detection/
│   └── detector.py
│
├── tracking/
│
├── database/
│   ├── db.py
│   └── models.py
│
├── notifications/
│   └── email_sender.py
│
├── tests/
│   ├── test_db.py
│   ├── test_email.py
│   └── test_alert.py
│
├── .env
├── requirements.txt
├── main.py
└── README.md
```

---

## 🛠️ Technology Stack

| Component             | Technology    |
| --------------------- | ------------- |
| Language              | Python        |
| Computer Vision       | OpenCV        |
| Detection             | YOLOv8        |
| Deep Learning         | PyTorch       |
| Tracking              | YOLO Tracking |
| Database              | PostgreSQL    |
| ORM                   | SQLAlchemy    |
| Email Service         | SMTP (Gmail)  |
| Environment Variables | python-dotenv |

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/SS-Hossain/speed-detection-module.git

cd speed_detection_module
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🐘 PostgreSQL Setup

Create database:

```sql
CREATE DATABASE speed_detection;
```

Connect:

```sql
\c speed_detection
```

Create table:

```sql
CREATE TABLE speed_alerts (
    id SERIAL PRIMARY KEY,
    vehicle_id INTEGER UNIQUE NOT NULL,
    speed_kmh FLOAT NOT NULL,
    threshold_kmh FLOAT NOT NULL,
    alert_time TIMESTAMP NOT NULL,
    video_source VARCHAR(255)
);
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=speed_detection
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver_email@gmail.com
```

---

## 📧 Gmail Configuration

Enable:

* Google 2-Step Verification
* App Password

Generate an App Password and use it inside:

```env
EMAIL_PASSWORD=your_app_password
```

---

## ▶️ Running the Application

Place a video inside:

```text
videos/
```

Update path if required:

```python
VIDEO_PATH = "videos/1.mp4"
```

Run:

```bash
python main.py
```

---

## 📊 Database Alerts

Each overspeed vehicle is stored inside PostgreSQL.

Example:

| vehicle_id | speed_kmh |
| ---------- | --------- |
| 3          | 83.63     |
| 6          | 88.30     |
| 9          | 82.29     |

Vehicle IDs are unique and existing records are automatically updated.

---

## 📧 Email Alerts

Whenever a vehicle exceeds the configured threshold:

```python
threshold = 80
```

An email notification is automatically sent.

Example:

```text
🚨 VEHICLE OVERSPEED DETECTED

Vehicle ID : 3
Speed      : 83.63 km/h
Threshold  : 80.00 km/h
```

---

## 🧠 Speed Estimation

Current implementation:

* Centroid-based tracking
* Historical position buffering
* Moving average smoothing
* Pixel-to-meter calibration
* Speed output in km/h

---

## 🚀 Future Enhancements

* RTSP Live Camera Support
* Homography-Based Calibration
* Bird's Eye View Transformation
* Multi-Camera Support
* Vehicle Snapshot Evidence
* Web Dashboard
* Analytics & Reporting
* Docker Deployment
* REST API Integration

---

## 📸 Example Output

```text
ID 3 | 83.6 km/h
ID 6 | 88.3 km/h
ID 9 | 82.2 km/h
```

Bounding boxes, tracking IDs, centroids, and speeds are rendered directly onto the output video.

---

## 📝 Current Status

### Completed

* [x] Vehicle Detection
* [x] Vehicle Tracking
* [x] Speed Estimation V2
* [x] Alert Generation
* [x] PostgreSQL Integration
* [x] Email Notifications
* [x] Alert Manager
* [x] Alert Deduplication

### Planned

* [ ] Homography Calibration
* [ ] RTSP Streaming
* [ ] Dashboard
* [ ] Snapshot Evidence
* [ ] Multi-Camera Support

---

## 👨‍💻 Author

Developed as an end-to-end AI Vehicle Speed Detection System using Computer Vision and Deep Learning.

Built with Python, YOLOv8, OpenCV, PostgreSQL, and SQLAlchemy.
