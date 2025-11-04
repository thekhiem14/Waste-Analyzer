# Thêm mapping ở đầu file app.py
label_map = {
    '铝箔': 'Aluminum Foil',
    '瓶盖': 'Bottle Cap',
    '瓶子': 'Bottle',
    '碎玻璃': 'Broken Glass',
    '罐头': 'Can',
    '纸箱': 'Cardboard',
    '香烟': 'Cigarette',
    '杯子': 'Cup',
    '盖子': 'Lid',
    '其他垃圾': 'Other Trash',
    '其他塑料': 'Other Plastic',
    '纸张': 'Paper',
    '塑料袋包装纸': 'Plastic Bag / Wrapper',
    '塑性容器': 'Plastic Container',
    'Pop标签': 'Pop Label',
    '吸管': 'Straw',
    '泡沫塑料片': 'Foam Sheet',
    '无标号垃圾': 'Unlabeled Trash'
}
# mapping từ index (0..17) sang tên tiếng Anh
class_map = {
    0: 'Aluminum foil',
    1: 'Bottle cap',
    2: 'Bottle',
    3: 'Broken glass',
    4: 'Can',
    5: 'Cardboard',
    6: 'Cigarette',
    7: 'Cup',
    8: 'Lid',
    9: 'Other waste',
    10: 'Other plastic',
    11: 'Paper',
    12: 'Plastic bag/wrapping',
    13: 'Plastic container',
    14: 'Pop label',
    15: 'Straw',
    16: 'Foam sheet',
    17: 'Unlabeled waste'
}


# app.py
import streamlit as st
from PIL import Image
import os
from utils.inference import analyze_image
from utils.storage import save_history, load_history  # nếu bạn đã có storage.py
from utils.categorize import categorize_waste  # nếu bạn có chức năng gom nhóm

# Cấu hình trang
st.set_page_config(page_title="Waste Analyzer", page_icon="♻️", layout="wide")

st.title("♻️ Waste Analyzer - Phân loại rác thải thông minh")
st.write("Upload ảnh -> Hệ thống sẽ phát hiện loại rác, in log backend, lưu lịch sử và gợi ý xử lý.")

# Tạo folder lưu uploads nếu chưa có
UPLOAD_DIR = os.path.join("data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Uploader
uploaded = st.file_uploader("Chọn ảnh (jpg, png)", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)

if uploaded is not None:
    # Save file to disk
    save_path = os.path.join(UPLOAD_DIR, uploaded.name)
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())

    # Hiển thị ảnh gốc
    image = Image.open(save_path).convert("RGB")
    with col1:
        st.subheader("Ảnh gốc")
        st.image(image, use_container_width=True)

    # Gọi inference
    with st.spinner("Đang phân tích..."):
        result_img, detections = analyze_image(image, conf_threshold=0.25)

    # Hiển thị kết quả và log
    with col2:
        st.subheader("Kết quả phát hiện")
        if len(detections) > 0:
            for d in detections:
                eng_label = label_map.get(d['label'], d['label'])  # chuyển sang tiếng Anh
                st.markdown(f"**{eng_label}** — `{d['confidence']*100:.1f}%`")
                st.info(d["guide"])
        else:
            st.warning("Không phát hiện được đối tượng nào.")

        # Lưu lịch sử nếu có storage.save_history
        try:
            save_history(uploaded.name, detections)
        except Exception as e:
            # nếu storage chưa được setup, in ra log
            print(f"[WARN] save_history failed: {e}")

    # Hiển thị ảnh có bounding box (dưới cả hai cột)
    st.subheader("Ảnh sau khi phân tích")
    st.image(result_img, use_container_width=True)

else:
    st.info("⬆️ Hãy tải lên 1 ảnh để bắt đầu phân tích.")
    # Hiển thị lịch sử ngắn (nếu muốn)
    try:
        hist_df = load_history()
        if not hist_df.empty:
            st.subheader("Lịch sử gần đây")
            st.dataframe(hist_df.tail(10))
    except Exception as e:
        # Nếu storage chưa tồn tại, bỏ qua
        print(f"[INFO] load_history skipped: {e}")
