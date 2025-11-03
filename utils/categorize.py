def categorize_waste(detections):
    """Gom nhóm loại rác và gợi ý hướng xử lý"""
    groups = {
        "Tái chế": ["plastic", "metal", "glass", "paper", "cardboard"],
        "Hữu cơ": ["food", "vegetable", "fruit"],
        "Nguy hại": ["battery", "electronic", "chemical"],
        "Khác": []
    }

    summary = {}
    suggestions = []

    for d in detections:
        cls = d["class"].lower()
        found = False
        for group, items in groups.items():
            if any(k in cls for k in items):
                summary.setdefault(group, []).append(cls)
                found = True
                break
        if not found:
            summary.setdefault("Khác", []).append(cls)

    # Gợi ý xử lý
    if "Tái chế" in summary:
        suggestions.append("♻️ Các vật liệu tái chế nên được rửa sạch và phân loại riêng.")
    if "Hữu cơ" in summary:
        suggestions.append("🌱 Rác hữu cơ có thể ủ làm phân compost.")
    if "Nguy hại" in summary:
        suggestions.append("⚠️ Rác nguy hại nên mang đến điểm thu gom chuyên biệt.")

    return summary, suggestions
