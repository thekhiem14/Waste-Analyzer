from ultralytics import YOLO
from PIL import Image
import os

# Load model YOLO
model = YOLO("models/best.pt")

def analyze_image(image_path):
    """Phân tích ảnh và trả về danh sách loại rác"""
    results = model(image_path)
    names = model.names

    # Lấy kết quả class name
    detections = []
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        detections.append({
            "class": names[cls_id],
            "confidence": round(conf, 2)
        })

    return detections, results[0].plot()  # plot() trả ảnh có bounding box
