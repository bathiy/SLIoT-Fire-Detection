import cv2
import time
import json
from datetime import datetime
from firebase_config import db, storage

# Load configuration
with open("config.json") as f:
    config = json.load(f)

rtsp_url = config["rtsp_url"]
uid = config["uid"]

# Connect to RTSP
cap = cv2.VideoCapture(rtsp_url)
if not cap.isOpened():
    print("❌ Cannot open RTSP stream")
    exit()

print("🎥 RTSP stream opened")

frame_count = 0
last_saved_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Stream Ended")
        break

    current_time = time.time()

    # Save frame every 1s
    if current_time - last_saved_time >= 1:
        filename = f"frame_{int(current_time)}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Saved: {filename}")
        frame_count += 1
        last_saved_time = current_time

        # Simulated fire detection
        fire_detected = True  # Replace with actual model later

        if fire_detected and frame_count % 10 == 0:
            print("🔥 Fire Detected!")

            # Upload to Firebase Storage
            path_on_cloud = f"fire_images/{uid}/{filename}"
            storage.child(path_on_cloud).put(filename)
            url = storage.child(path_on_cloud).get_url(None)

            # Push alert to DB
            alert = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "image_url": url,
                "status": "Fire Detected"
            }
            db.child("users").child(uid).child("fire_alerts").push(alert)
            print("✅ Alert sent to Firebase")

    # Optional: quit on keypress
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
