"""
Project 04: Facial Recognition Security Cam

Hidden Gem: `face-recognition` — the simplest face detection API in Python.

What it does: Uses webcam to detect faces in real-time. If no webcam is available,
runs in demo mode with a synthetic image. Logs all detection events.
"""
import os
import time
from datetime import datetime


def log_detection(count, source="webcam"):
    """Log a face detection event."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Faces detected: {count} (source: {source})"
    print(entry)
    with open("detection_log.txt", "a") as f:
        f.write(entry + "\n")


def run_webcam_detection(duration=30):
    """Run face detection on webcam feed for N seconds."""
    try:
        import cv2
        import face_recognition
    except ImportError:
        print("Required packages not installed.")
        print("Install with: pip install opencv-python face-recognition")
        return False

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("No webcam detected. Running in demo mode.")
        return False

    print(f"Webcam active. Scanning for {duration} seconds...")
    start = time.time()
    frame_count = 0

    while time.time() - start < duration:
        ret, frame = cap.read()
        if not ret:
            break

        # Downscale for speed
        small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb = small[:, :, ::-1]

        locations = face_recognition.face_locations(rgb)
        count = len(locations)

        if count > 0:
            log_detection(count)

        # Draw boxes
        for (top, right, bottom, left) in locations:
            top, right, bottom, left = top * 2, right * 2, bottom * 2, left * 2
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.putText(frame, f"Faces: {count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Security Cam", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Scanned {frame_count} frames in {duration}s")
    return True


def demo_mode():
    """Run without webcam — simulate detection events."""
    print("--- Demo Mode (no webcam) ---")
    print("Simulating face detection events over 10 seconds...\n")

    events = [
        (1, "entry_door"),
        (0, "entry_door"),
        (2, "entry_door"),
        (1, "entry_door"),
        (0, "entry_door"),
    ]

    for count, source in events:
        log_detection(count, source)
        time.sleep(2)

    print("\nDemo complete. Check detection_log.txt for the log.")


def main():
    print("--- Facial Recognition Security Cam ---")
    try:
        success = run_webcam_detection(duration=30)
        if not success:
            demo_mode()
    except Exception as e:
        print(f"Webcam mode failed: {e}")
        demo_mode()


if __name__ == "__main__":
    main()
