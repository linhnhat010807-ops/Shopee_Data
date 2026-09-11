"""
Chuyển tên cột sang tiếng Anh để đồng bộ với các task khác + xoá cột mô tả (mo_ta) cho nhẹ file.

Input : data/Shopee_Cleaned_Data_hp.xlsx  (tiếng Việt, có cột mo_ta)
Output: data/shopee_data_clean.xlsx        (tiếng Anh, đã bỏ mô tả)

Cách chạy:
    python translate_data.py
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
INPUT_PATH = os.path.join(BASE_DIR, "data", "Shopee_Cleaned_Data_hp.xlsx")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "shopee_data_clean.xlsx")

# Ánh xạ tên cột tiếng Việt -> tiếng Anh (đồng bộ với quy ước đặt tên đang dùng
# cho các task khác: title, item_category_detail, price_ori, price_actual,
# item_rating, total_rating, total_sold, seller_name, w_date, idElastic, specification)
COLUMN_MAP = {
    "ma_san_pham": "idElastic",
    "ten_san_pham": "title",
    "danh_muc": "item_category_detail",
    "thong_so": "specification",
    "gia_goc": "price_ori",
    "gia_ban": "price_actual",
    "luot_ban": "total_sold",
    "diem_danh_gia": "item_rating",
    "so_luot_danh_gia": "total_rating",
    "so_luot_yeu_thich": "total_favorite",
    "ngay_thu_thap": "w_date",
    "nguoi_ban": "seller_name",
    # "mo_ta" cố ý không map -> sẽ bị xoá bên dưới
}

DROP_COLUMNS = ["mo_ta"]


def main():
    df = pd.read_excel(INPUT_PATH)

    missing_in_map = [c for c in df.columns if c not in COLUMN_MAP and c not in DROP_COLUMNS]
    if missing_in_map:
        print(f"⚠️  Cột chưa có trong bảng ánh xạ (giữ nguyên tên): {missing_in_map}")

    df = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns])
    df = df.rename(columns=COLUMN_MAP)

    df.to_excel(OUTPUT_PATH, index=False)

    print(f"Đã lưu: {OUTPUT_PATH}")
    print(f"Số dòng: {len(df):,} | Số cột: {df.shape[1]} (đã bỏ cột 'mo_ta')")
    print(f"Cột: {df.columns.tolist()}")


if __name__ == "__main__":
    main()
