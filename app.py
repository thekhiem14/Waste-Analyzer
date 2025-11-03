import streamlit as st
from utils.inference import analyze_image
from utils.categorize import categorize_waste
from utils.storage import save_history, load_history
from PIL import Image
import os

st.set_page_config(page_title="Waste Analyzer", layout="wide")

st.title("♻️ Waste Analyzer - Phân tích và phân loại rác thông minh")

tab1, tab2 = st.tabs(["🔍 Phân tích ảnh", "📜 Lịch sử"])

with tab1:
    uploaded = st.file_uploader("Tải ảnh rác cần phân tích", type=["jpg", "png", "jpeg"])
    if uploaded:
        img_path = os.path.join("data/uploads", uploaded.name)
        os.makedirs("data/uploads", exist_ok=True)
        with open(img_path, "wb") as f:
            f.write(uploaded.getbuffer())

        st.image(uploaded, caption="Ảnh đầu vào", use_column_width=True)
        with st.spinner("Đang phân tích..."):
            detections, result_img = analyze_image(img_path)

        st.image(result_img, caption="Kết quả phát hiện", use_column_width=True)

        summary, suggestions = categorize_waste(detections)
        st.subheader("🧩 Phân nhóm rác:")
        st.json(summary)

        st.subheader("💡 Gợi ý xử lý:")
        for s in suggestions:
            st.info(s)

        save_history(uploaded.name, detections)

with tab2:
    st.subheader("📜 Lịch sử phân tích")
    history = load_history()
    st.dataframe(history)
