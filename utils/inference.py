# utils/inference.py
from ultralytics import YOLO
from PIL import Image
import numpy as np
import os

# Load model một lần khi module được import
MODEL_PATH = os.path.join("models", "best.pt")
print(f"[INFO] Loading YOLO model from: {MODEL_PATH}")
model = YOLO(MODEL_PATH)
print("[INFO] Model loaded.")

# Bảng gợi ý xử lý (bạn có thể mở rộng)
RECYCLING_GUIDE = {
    "plastic": "♻️ Tái chế hoặc thu gom nhựa đúng nơi quy định",
    "bottle": "♻️ Vật liệu nhựa - rửa sạch trước khi tái chế",
    "paper": "📄 Có thể tái chế, tránh để ướt",
    "cardboard": "📦 Hình như là bìa carton - tái chế được",
    "metal": "🔩 Thu gom bán phế liệu hoặc tái chế",
    "can": "🔩 Lon kim loại - tái chế",
    "glass": "🧴 Có thể tái chế, cần rửa sạch",
    "organic": "🌿 Dùng làm phân compost hữu cơ",
    "food": "🌿 Rác hữu cơ - ủ compost",
    "battery": "⚠️ Rác nguy hại - mang đến điểm thu gom chuyên biệt",
    "electronic": "⚠️ Thiết bị điện tử - thu gom tại điểm thu hồi",
    # mặc định
    "other": "🚮 Không xác định: bỏ đúng thùng rác hoặc kiểm tra thêm"
}

def _get_guide(label: str) -> str:
    lbl = label.lower()
    # tìm key khớp một phần
    for k in RECYCLING_GUIDE.keys():
        if k in lbl:
            return RECYCLING_GUIDE[k]
    return RECYCLING_GUIDE["other"]

def analyze_image(pil_image: Image.Image, conf_threshold: float = 0.25):
    """
    Input:
      - pil_image: PIL.Image opened from user upload
      - conf_threshold: ngưỡng confidence để giữ detect
    Returns:
      - result_pil: PIL.Image có bounding boxes (dùng để hiển thị)
      - detections: list of dicts {label, confidence, guide}
    Ghi chú: đồng thời in log ra console.
    """
    # chạy dự đoán (ultralytics YOLO)
    # bạn có thể thêm imgsz=640, device="cpu"/"0" nếu cần
    results = model.predict(source=pil_image, conf=conf_threshold, verbose=False)
    result = results[0]

    detections = []
    boxes = getattr(result, "boxes", None)

    if boxes is not None and len(boxes) > 0:
        # boxes.cls, boxes.conf là tensors
        classes = boxes.cls.cpu().numpy().astype(int)
        confs = boxes.conf.cpu().numpy()
        names = model.names  # dict id->name
        for cls_id, conf in zip(classes, confs):
            label = names.get(int(cls_id), str(cls_id))
            guide = _get_guide(label)
            detections.append({
                "label": label,
                "confidence": float(conf),
                "guide": guide
            })
            # print log backend
            print(f"[DETECT] {label} - {conf*100:.1f}% -> {guide}")
    else:
        print("[DETECT] Không phát hiện được đối tượng nào.")

    # result.plot() trả numpy array (H x W x 3). Có thể là BGR/RGB tùy phiên bản.
    result_img = result.plot()  # numpy array
    # ensure convert to PIL Image and RGB
    try:
        import cv2
        # nếu màu bị sai (nhiều khả năng result.plot trả BGR), chuyển qua RGB
        if result_img.ndim == 3 and result_img.shape[2] == 3:
            result_img_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        else:
            result_img_rgb = result_img
        result_pil = Image.fromarray(result_img_rgb)
    except Exception:
        # fallback: assume array[..., ::-1] nếu cần, else just fromarray
        try:
            if result_img.ndim == 3 and result_img.shape[2] == 3:
                result_pil = Image.fromarray(result_img[..., ::-1])  # BGR->RGB attempt
            else:
                result_pil = Image.fromarray(result_img)
        except Exception as e:
            # cuối cùng, trả ảnh input nếu không chuyển được
            print(f"[WARN] Không convert được result_img sang PIL: {e}")
            result_pil = pil_image

    return result_pil, detections
