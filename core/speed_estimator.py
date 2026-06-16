import math
from collections import deque


class SpeedEstimator:

    def __init__(
        self,
        ppm=80,
        fps=30,
        history=10,
        smoothing=5
    ):

        self.ppm = ppm
        self.fps = fps

        # Store centroid history
        self.positions = {}

        # Store speed history
        self.speeds = {}

        self.history = history
        self.smoothing = smoothing

    def update(self, track_id, centroid):

        # ------------------------
        # INIT POSITION HISTORY
        # ------------------------
        if track_id not in self.positions:

            self.positions[track_id] = deque(
                maxlen=self.history
            )

            self.speeds[track_id] = deque(
                maxlen=self.smoothing
            )

        # Add new centroid
        self.positions[track_id].append(centroid)

        # Need at least 2 points
        if len(self.positions[track_id]) < 2:
            return 0

        # ------------------------
        # USE OLDEST + NEWEST
        # ------------------------
        old_x, old_y = self.positions[track_id][0]
        new_x, new_y = self.positions[track_id][-1]

        # Pixel distance
        distance_pixels = math.sqrt(
            (new_x - old_x) ** 2 +
            (new_y - old_y) ** 2
        )

        # Ignore tiny jitter
        if distance_pixels < 2:
            return 0

        # ------------------------
        # PIXELS → METERS
        # ------------------------
        distance_meters = distance_pixels / self.ppm

        # Total frames used
        frames_passed = len(
            self.positions[track_id]
        )

        # Time in seconds
        time_seconds = frames_passed / self.fps

        if time_seconds == 0:
            return 0

        # ------------------------
        # SPEED
        # ------------------------
        speed_mps = distance_meters / time_seconds

        speed_kmh = speed_mps * 3.6

        # ------------------------
        # SPEED SMOOTHING
        # ------------------------
        self.speeds[track_id].append(speed_kmh)

        smooth_speed = sum(
            self.speeds[track_id]
        ) / len(self.speeds[track_id])

        return smooth_speed