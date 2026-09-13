# ==============================
# 1. IMPORT THƯ VIỆN
# ==============================

import pandas as pd
import matplotlib.pyplot as plt


# ==============================
# 2. ĐỌC FILE DỮ LIỆU
# ==============================

file_path = "shopee_data_clean (1).xlsx"

df = pd.read_excel(file_path)

print("==========================================")
print("ĐỌC DỮ LIỆU THÀNH CÔNG")
print("==========================================")

print("Số dòng:", len(df))
print("Số cột:", len(df.columns))

print("\nCác cột trong dữ liệu:")
print(df.columns.tolist())


# ==============================
# 3. KIỂM TRA CÁC CỘT CẦN THIẾT
# ==============================

required_columns = [
    "title",
    "total_sold",
    "item_category_detail",
    "w_date"
]

for column in required_columns:
    if column not in df.columns:
        print(f"\nLỖI: Không tìm thấy cột '{column}'")
        raise SystemExit


# ==============================
# 4. XỬ LÝ DỮ LIỆU
# ==============================

# Chuyển total_sold sang dạng số
df["total_sold"] = pd.to_numeric(
    df["total_sold"],
    errors="coerce"
).fillna(0)


# Chuyển ngày sang dạng datetime
df["w_date"] = pd.to_datetime(
    df["w_date"],
    errors="coerce"
)


# ==============================
# 5. TẠO DANH MỤC CHÍNH
# ==============================

def get_main_category(value):

    if pd.isna(value):
        return "Không xác định"

    value = str(value)

    # Dữ liệu có dạng:
    # Shopee > Health & Beauty > ...
    parts = value.split("|")

    if len(parts) > 1:
        category = parts[1].strip()

        if category != "":
            return category

    return value.strip()


df["main_category"] = df[
    "item_category_detail"
].apply(get_main_category)


print("\n==========================================")
print("XỬ LÝ DỮ LIỆU HOÀN TẤT")
print("==========================================")

print("\n5 dòng dữ liệu đầu tiên:")
print(
    df[
        [
            "title",
            "main_category",
            "total_sold",
            "w_date"
        ]
    ].head()
)


# ============================================================
# BIỂU ĐỒ 1
# TOP 10 DANH MỤC CÓ LƯỢNG BÁN CAO NHẤT
# ============================================================

category_sales = (
    df.groupby("main_category")["total_sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n==========================================")
print("TOP 10 DANH MỤC BÁN CHẠY NHẤT")
print("==========================================")

print(category_sales)


# Đảo thứ tự để danh mục cao nhất nằm trên cùng
chart1 = category_sales.sort_values(ascending=True)

plt.figure(figsize=(12, 7))

plt.barh(
    chart1.index,
    chart1.values
)

plt.title(
    "Top 10 danh mục có lượng bán cao nhất",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Tổng số lượng bán",
    fontsize=12
)

plt.ylabel(
    "Danh mục",
    fontsize=12
)

plt.tight_layout()

plt.savefig(
    "01_top_10_danh_muc.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# BIỂU ĐỒ 2
# TOP 10 SẢN PHẨM BÁN CHẠY NHẤT
# ============================================================

product_sales = (
    df.groupby("title")["total_sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


print("\n==========================================")
print("TOP 10 SẢN PHẨM BÁN CHẠY NHẤT")
print("==========================================")

for i, (name, sales) in enumerate(
    product_sales.items(),
    start=1
):
    print(i, "-", name)
    print("    Số lượng bán:", sales)


# Chuyển sang DataFrame
chart2 = product_sales.reset_index()

chart2.columns = [
    "title",
    "total_sold"
]


# ------------------------------
# RÚT GỌN TÊN SẢN PHẨM
# ------------------------------

def shorten_product_name(name):

    name = str(name)

    # Bỏ phần "| Shopee Malaysia"
    if "|" in name:
        name = name.split("|")[0]

    name = name.strip()

    # Giới hạn tên còn 55 ký tự
    if len(name) > 55:
        name = name[:55] + "..."

    return name


chart2["short_title"] = chart2[
    "title"
].apply(shorten_product_name)


# Sắp xếp từ thấp -> cao
# để sản phẩm bán nhiều nhất nằm trên cùng
chart2 = chart2.sort_values(
    by="total_sold",
    ascending=True
)


# ------------------------------
# VẼ BIỂU ĐỒ
# ------------------------------

plt.figure(figsize=(13, 7))

plt.barh(
    chart2["short_title"],
    chart2["total_sold"]
)

plt.title(
    "Top 10 sản phẩm bán chạy nhất",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Tổng số lượng bán",
    fontsize=12
)

plt.ylabel(
    "Sản phẩm",
    fontsize=12
)

plt.tight_layout()

plt.savefig(
    "02_top_10_san_pham.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# BIỂU ĐỒ 3
# XU HƯỚNG LƯỢNG BÁN THEO THỜI GIAN
# ============================================================

daily_sales = (
    df.dropna(subset=["w_date"])
    .groupby("w_date")["total_sold"]
    .sum()
    .sort_index()
)


print("\n==========================================")
print("XU HƯỚNG LƯỢNG BÁN THEO THỜI GIAN")
print("==========================================")

print(daily_sales)


# ------------------------------
# VẼ BIỂU ĐỒ
# ------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    daily_sales.index,
    daily_sales.values,
    marker="o"
)

plt.title(
    "Xu hướng lượng bán theo thời gian",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Ngày",
    fontsize=12
)

plt.ylabel(
    "Tổng số lượng bán",
    fontsize=12
)

plt.xticks(
    rotation=45
)

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "03_xu_huong_luong_ban.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# BIỂU ĐỒ 4
# TỶ TRỌNG LƯỢNG BÁN CỦA TOP 10 DANH MỤC
# ============================================================

top_10_categories = (
    df.groupby("main_category")["total_sold"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


total_top_10 = top_10_categories.sum()

total_all = df["total_sold"].sum()

percentage_top_10 = (
    total_top_10 / total_all * 100
)


print("\n==========================================")
print("TỶ TRỌNG TOP 10 DANH MỤC")
print("==========================================")

print(top_10_categories)

print(
    f"\nTop 10 danh mục chiếm "
    f"{percentage_top_10:.2f}% tổng lượng bán."
)


# ------------------------------
# VẼ BIỂU ĐỒ TRÒN
# ------------------------------

plt.figure(figsize=(10, 8))

plt.pie(
    top_10_categories.values,
    labels=top_10_categories.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Tỷ trọng lượng bán của Top 10 danh mục",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "04_ty_trong_top_10_danh_muc.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 6. TỔNG KẾT
# ============================================================

print("\n==========================================")
print("HOÀN TẤT PHÂN TÍCH")
print("==========================================")

print("\nĐã tạo 4 biểu đồ:")

print("1. 01_top_10_danh_muc.png")
print("2. 02_top_10_san_pham.png")
print("3. 03_xu_huong_luong_ban.png")
print("4. 04_ty_trong_top_10_danh_muc.png")

print("\nCác file biểu đồ đã được lưu thành công.")