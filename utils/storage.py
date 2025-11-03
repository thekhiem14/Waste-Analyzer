import pandas as pd
import os
from datetime import datetime

HISTORY_FILE = "data/history.csv"

def save_history(image_name, detections):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "image": image_name,
        "detections": ", ".join([d["class"] for d in detections])
    }])
    if os.path.exists(HISTORY_FILE):
        df.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(HISTORY_FILE, index=False)

def load_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    else:
        return pd.DataFrame(columns=["timestamp", "image", "detections"])
