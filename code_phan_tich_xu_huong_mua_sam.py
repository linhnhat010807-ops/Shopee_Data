import pandas as pd

# Đọc dữ liệu
df = pd.read_excel("shopee_data_clean (1).xlsx")

# Tính tổng số lượng bán theo danh mục
category_sales = df.groupby("item_category_detail")["total_sold"].sum()

# Sắp xếp từ cao xuống thấp
category_sales = category_sales.sort_values(ascending=False)

# Lấy 10 danh mục bán chạy nhất
top_categories = category_sales.head(10)

print("\nTOP 10 DANH MỤC CÓ LƯỢNG BÁN CAO NHẤT:")
print(top_categories)
# Tách danh mục chính từ item_category_detail
df["main_category"] = df["item_category_detail"].str.split("|").str[1].str.strip()

# Tính tổng số lượng bán theo danh mục chính
main_category_sales = (
    df.groupby("main_category")["total_sold"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTỔNG LƯỢNG BÁN THEO DANH MỤC CHÍNH:")
print(main_category_sales)
import matplotlib.pyplot as plt

# Lấy Top 10 danh mục
top_10 = main_category_sales.head(10)

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))
top_10.plot(kind="bar")

plt.title("Top 10 danh mục có lượng bán cao nhất")
plt.xlabel("Danh mục sản phẩm")
plt.ylabel("Tổng số lượng bán")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
# TOP 10 SẢN PHẨM BÁN CHẠY NHẤT
product_sales = (
    df.groupby("title")["total_sold"]
    .sum()
    .sort_values(ascending=False)
)

top_products = product_sales.head(10)

print("\nTOP 10 SẢN PHẨM BÁN CHẠY NHẤT:")
print(top_products)
plt.show()
# PHÂN TÍCH XU HƯỚNG MUA SẮM THEO THỜI GIAN

# Chuyển cột ngày sang dạng ngày tháng
df["w_date"] = pd.to_datetime(df["w_date"], errors="coerce")

# Tính tổng lượng bán theo ngày
daily_sales = (
    df.groupby("w_date")["total_sold"]
    .sum()
    .sort_index()
)

print("\nLƯỢNG BÁN THEO THỜI GIAN:")
print(daily_sales)

# Vẽ biểu đồ xu hướng
plt.figure(figsize=(12, 6))

daily_sales.plot(kind="line")

plt.title("Xu hướng lượng bán theo thời gian")
plt.xlabel("Thời gian")
plt.ylabel("Tổng số lượng bán")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# TỶ TRỌNG LƯỢNG BÁN CỦA TOP 10 DANH MỤC

total_sales = main_category_sales.sum()

top_10_percent = (
    main_category_sales.head(10) / total_sales * 100
)

print("\nTỶ TRỌNG TOP 10 DANH MỤC:")
print(top_10_percent.round(2))
