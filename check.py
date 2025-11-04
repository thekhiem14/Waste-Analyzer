from ultralytics import YOLO

# Load model
model = YOLO("models/best.pt")

# Xem thông tin tổng quan
model.info()

# Hoặc xem kiến trúc mạng
print(model.model)
