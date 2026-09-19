"""
Nhánh: nhanh-loc-du-lieu
Nhiệm vụ: Viết code Python lọc dữ liệu từ file Excel
    - Lọc theo tên sản phẩm (từ khóa tìm kiếm trong title)
    - Lọc theo khoảng giá tiền (price_actual)
    - Chỉ lấy sản phẩm có đánh giá >= 3 sao (item_rating)

"""

from __future__ import annotations

import os
import pandas as pd

# Đường dẫn mặc định đến file dữ liệu (đặt file Excel trong thư mục data/,
# nằm CÙNG CẤP với file loc_du_lieu.py này). Dùng __file__ để tính đường dẫn
# tuyệt đối, nhờ vậy chạy đúng dù bạn đứng ở thư mục nào để gõ lệnh python.
try:
    THU_MUC_GOC = os.path.dirname(os.path.abspath(__file__))
except NameError:  # phòng trường hợp chạy trong môi trường không có __file__
    THU_MUC_GOC = os.getcwd()

DUONG_DAN_FILE_MAC_DINH = os.path.join(THU_MUC_GOC, "data", "shopee_data_clean.xlsx")

# Các cột bắt buộc phải có trong file Excel để hàm hoạt động đúng
CAC_COT_BAT_BUOC = ["title", "item_rating", "price_actual"]


def doc_du_lieu(duong_dan_file: str = DUONG_DAN_FILE_MAC_DINH) -> pd.DataFrame:
    """
    Đọc dữ liệu thô từ file Excel và chuẩn hóa kiểu dữ liệu cơ bản.

    - Ép các cột số (rating, giá, lượt đánh giá, lượt bán) về kiểu numeric,
      giá trị lỗi/không hợp lệ sẽ thành NaN thay vì làm crash chương trình.
    - Loại bỏ các dòng thiếu tên sản phẩm, rating hoặc giá (không đủ dữ liệu để lọc).
    """
    if not os.path.exists(duong_dan_file):
        raise FileNotFoundError(
            f"Không tìm thấy file dữ liệu tại '{duong_dan_file}'. "
            "Hãy kiểm tra lại đường dẫn hoặc đặt file Excel vào thư mục data/."
        )

    df = pd.read_excel(duong_dan_file)

    cot_thieu = [c for c in CAC_COT_BAT_BUOC if c not in df.columns]
    if cot_thieu:
        raise ValueError(f"File Excel thiếu (các) cột bắt buộc: {cot_thieu}")

    # Ép kiểu số cho các cột liên quan đến lọc/tính toán
    for cot in ["item_rating", "price_actual", "price_ori", "total_rating", "total_sold"]:
        if cot in df.columns:
            df[cot] = pd.to_numeric(df[cot], errors="coerce")

    # Loại bỏ dòng thiếu thông tin bắt buộc để lọc
    df = df.dropna(subset=CAC_COT_BAT_BUOC)
    return df.reset_index(drop=True)


def lay_du_lieu(
    duong_dan_file: str = DUONG_DAN_FILE_MAC_DINH,
    tu_khoa: str = "",
    gia_tu: float | None = None,
    gia_den: float | None = None,
    sao_toi_thieu: float = 3.0,
) -> pd.DataFrame:
    """
    Hàm bắt buộc của nhánh nhanh-loc-du-lieu.

    Đọc dữ liệu từ file Excel rồi lọc theo 3 điều kiện:
      1) tu_khoa      : từ khóa xuất hiện trong tên sản phẩm (title),
                        không phân biệt hoa/thường. Để trống ("") nếu không lọc.
      2) gia_tu/gia_den: khoảng giá tiền theo price_actual (giá thực tế đang bán).
                        Để None nếu không giới hạn cận đó.
      3) sao_toi_thieu : chỉ lấy sản phẩm có item_rating >= sao_toi_thieu
                        (mặc định 3 sao theo yêu cầu đề bài).

    Trả về DataFrame đã lọc, index được reset lại từ 0.
    Hàm này là điểm vào chung để các thành viên khác trong nhóm gọi lấy dữ liệu
    (ví dụ: tao_bo_loc_sidebar(df) của Trọng Phúc truyền tu_khoa/gia_tu/gia_den
    lấy từ ô tìm kiếm và thanh slider trên giao diện).
    """
    df = doc_du_lieu(duong_dan_file)

    # 1) Chỉ lấy sản phẩm >= X sao (mặc định 3 sao)
    df = df[df["item_rating"] >= sao_toi_thieu]

    # 2) Lọc theo tên sản phẩm
    if tu_khoa and tu_khoa.strip():
        df = df[df["title"].str.contains(tu_khoa.strip(), case=False, na=False, regex=False)]

    # 3) Lọc theo khoảng giá tiền
    if gia_tu is not None:
        df = df[df["price_actual"] >= gia_tu]
    if gia_den is not None:
        df = df[df["price_actual"] <= gia_den]

    return df.reset_index(drop=True)


if __name__ == "__main__":
    # Demo / kiểm thử nhanh khi chạy trực tiếp: python loc_du_lieu.py
    print("=== Kiểm thử hàm lay_du_lieu() ===\n")

    df_goc = doc_du_lieu()
    print(f"Tổng số sản phẩm trong file gốc: {len(df_goc):,}")

    df_3sao = lay_du_lieu()
    print(f"Sau khi chỉ lấy sản phẩm >= 3 sao: {len(df_3sao):,}")

    df_loc = lay_du_lieu(tu_khoa="bag", gia_tu=5, gia_den=50, sao_toi_thieu=3)
    print(f"\nLọc từ khóa='bag', giá 5-50, >=3 sao: {len(df_loc):,} sản phẩm")
    print(df_loc[["title", "item_rating", "price_actual"]].head(10).to_string(index=False))
