import pandas as pd
import matplotlib.pyplot as plt


# 1. ĐỌC DỮ LIỆU TỪ FILE EXCEL

df = pd.read_excel("shopee_data_clean.xlsx")

print("Đọc dữ liệu thành công!")

print("\nSố dòng:", len(df))
print("Số cột:", len(df.columns))

print("\nCác cột trong dữ liệu:")
print(df.columns.tolist())


# 2. THỐNG KÊ TỔNG QUAN SẢN PHẨM

print("\n" + "=" * 60)
print("THỐNG KÊ TỔNG QUAN")
print("=" * 60)

# Số lượng sản phẩm
so_luong_san_pham = df["title"].nunique()

print("\nSố lượng sản phẩm:", so_luong_san_pham)

# Số lượng danh mục
so_luong_danh_muc = df["item_category_detail"].nunique()

print("Số lượng danh mục:", so_luong_danh_muc)

# Giá bán
print("\n--- Thống kê giá bán thực tế ---")

print("Giá thấp nhất:",
      df["price_actual"].min())

print("Giá cao nhất:",
      df["price_actual"].max())

print("Giá trung bình:",
      df["price_actual"].mean())

print("Giá trung vị:",
      df["price_actual"].median())


# 3. THỐNG KÊ SỐ LƯỢNG SẢN PHẨM THEO DANH MỤC

category_count = (
    df["item_category_detail"]
    .value_counts()
)

print("\n" + "=" * 60)
print("TOP 10 DANH MỤC CÓ NHIỀU SẢN PHẨM NHẤT")
print("=" * 60)

print(category_count.head(10))


# 4. BIỂU ĐỒ 1
# TOP 10 DANH MỤC CÓ NHIỀU SẢN PHẨM NHẤT

top_category = category_count.head(10)

plt.figure(figsize=(10, 6))

top_category.sort_values().plot(
    kind="barh"
)

plt.title(
    "Top 10 danh mục có nhiều sản phẩm nhất"
)

plt.xlabel("Số lượng sản phẩm")
plt.ylabel("Danh mục")

plt.tight_layout()
plt.show()


# 5. PHÂN CHIA SẢN PHẨM THEO KHOẢNG GIÁ

bins = [
    0,
    50000,
    100000,
    200000,
    500000,
    float("inf")
]

labels = [
    "Dưới 50.000",
    "50.000 - 100.000",
    "100.000 - 200.000",
    "200.000 - 500.000",
    "Trên 500.000"
]

df["price_range"] = pd.cut(
    df["price_actual"],
    bins=bins,
    labels=labels,
    include_lowest=True
)

price_range_count = (
    df["price_range"]
    .value_counts()
    .sort_index()
)

print("\n" + "=" * 60)
print("SỐ LƯỢNG SẢN PHẨM THEO KHOẢNG GIÁ")
print("=" * 60)

print(price_range_count)


# 6. BIỂU ĐỒ 2
# SỐ LƯỢNG SẢN PHẨM THEO KHOẢNG GIÁ

plt.figure(figsize=(10, 6))

price_range_count.plot(
    kind="bar"
)

plt.title(
    "Số lượng sản phẩm theo khoảng giá"
)

plt.xlabel("Khoảng giá")
plt.ylabel("Số lượng sản phẩm")

plt.xticks(rotation=30)

plt.tight_layout()
plt.show()


# 7. BIỂU ĐỒ 3
# PHÂN BỐ GIÁ BÁN THỰC TẾ

plt.figure(figsize=(10, 6))

plt.hist(
    df["price_actual"],
    bins=30
)

plt.title(
    "Phân bố giá bán thực tế của sản phẩm"
)

plt.xlabel("Giá bán thực tế")
plt.ylabel("Số lượng sản phẩm")

plt.tight_layout()
plt.show()


# 8. GIÁ BÁN TRUNG BÌNH THEO DANH MỤC

category_price = (
    df.groupby("item_category_detail")["price_actual"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 DANH MỤC CÓ GIÁ BÁN TRUNG BÌNH CAO NHẤT")
print("=" * 60)

print(category_price)


# 9. BIỂU ĐỒ 4
# GIÁ BÁN TRUNG BÌNH THEO DANH MỤC

plt.figure(figsize=(10, 6))

category_price.sort_values().plot(
    kind="barh"
)

plt.title(
    "Top 10 danh mục có giá bán trung bình cao nhất"
)

plt.xlabel("Giá bán trung bình")
plt.ylabel("Danh mục")

plt.tight_layout()
plt.show()


# 10. KẾT LUẬN TỔNG QUAN

print("\n" + "=" * 60)
print("HOÀN THÀNH PHÂN TÍCH TỔNG QUAN")
print("=" * 60)

print("\nDanh mục có nhiều sản phẩm nhất:")
print(category_count.index[0])

print("\nSố lượng sản phẩm của danh mục này:")
print(category_count.iloc[0])

print("\nKhoảng giá có nhiều sản phẩm nhất:")
print(price_range_count.idxmax())

print("\nSố lượng sản phẩm trong khoảng giá này:")
print(price_range_count.max())