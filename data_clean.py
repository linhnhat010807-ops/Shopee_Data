import pandas as pd
import re

# ==============================
# 1. Đọc dữ liệu
# ==============================

file_input = "20240121_shopee_sample_data.xlsx"
df = pd.read_excel(file_input)


# ==============================
# 2. Chọn các cột cần giữ
# ==============================

columns_keep = [
    "price_ori",
    "item_category_detail",
    "specification",
    "title",
    "w_date",
    "link_ori",
    "item_rating",
    "seller_name",
    "idElastic",
    "price_actual",
    "total_rating",
    "total_sold"
]

df = df[columns_keep]


# ==============================
# 3. Hàm quy đổi k, M, B
# ==============================

def convert_unit(value):
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return value

    value = str(value).strip().replace(",", "")

    match = re.fullmatch(
        r"([-+]?\d*\.?\d+)\s*([kKmMbB])?",
        value
    )

    if not match:
        return None

    number = float(match.group(1))
    unit = match.group(2)

    if unit:
        unit = unit.lower()

        if unit == "k":
            number *= 1000

        elif unit == "m":
            number *= 1000000

        elif unit == "b":
            number *= 1000000000

    return number


# ==============================
# 4. Quy đổi các cột số
# ==============================

columns_convert = [
    "price_ori",
    "price_actual",
    "item_rating",
    "total_rating",
    "total_sold"
]

for col in columns_convert:
    df[col] = df[col].apply(convert_unit)


# ==============================
# 5. Xóa dòng trống
# ==============================

# Xóa dòng hoàn toàn trống
df = df.dropna(how="all")


# ==============================
# 6. Xóa dòng thiếu dữ liệu quan trọng
# ==============================

required_columns = [
    "title",
    "price_actual",
    "item_rating",
    "total_rating",
    "total_sold"
]

df = df.dropna(
    subset=required_columns
)


# ==============================
# 7. Xóa dữ liệu lỗi
# ==============================

# Chuyển các cột số sang dạng số
for col in columns_convert:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# Xóa dòng bị lỗi ở các cột số
df = df.dropna(
    subset=columns_convert
)


# ==============================
# 8. Loại bỏ giá trị âm bất thường
# ==============================

df = df[
    (df["price_actual"] >= 0) &
    (df["price_ori"] >= 0) &
    (df["item_rating"] >= 0) &
    (df["total_rating"] >= 0) &
    (df["total_sold"] >= 0)
]


# ==============================
# 9. Xóa dòng trùng
# ==============================

df = df.drop_duplicates()


# ==============================
# 10. Reset số dòng
# ==============================

df = df.reset_index(drop=True)


# ==============================
# 11. Xuất file Excel
# ==============================

file_output = "shopee_data_clean.xlsx"

df.to_excel(
    file_output,
    index=False
)


# ==============================
# 12. Thông báo kết quả
# ==============================

print("Đã làm sạch dữ liệu!")
print("--------------------------------")
print("Số dòng còn lại:", len(df))
print("Số cột:", len(df.columns))
print("Tên file:", file_output)