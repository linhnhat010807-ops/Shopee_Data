import pandas as pd
import matplotlib.pyplot as plt


def phan_tich_tong_quan(df):
    """
    Hàm thực hiện các phép tính và tạo dữ liệu
    phục vụ cho việc phân tích tổng quan.
    """

    # 1. Tổng quan dữ liệu
    total_products = df["title"].nunique()
    total_categories = df["item_category_detail"].nunique()

    price_min = df["price_actual"].min()
    price_max = df["price_actual"].max()
    price_mean = df["price_actual"].mean()
    price_median = df["price_actual"].median()

    # 2. Số lượng sản phẩm theo danh mục
    category_count = df["item_category_detail"].value_counts()

    # 3. Phân chia sản phẩm theo khoảng giá
    bins = [0, 50000, 100000, 200000, 500000, float("inf")]
    labels = ["<50K", "50K-100K", "100K-200K", "200K-500K", ">500K"]

    df["price_range"] = pd.cut(
        df["price_actual"],
        bins=bins,
        labels=labels
    )

    price_count = df["price_range"].value_counts().sort_index()

    # 4. Giá trung bình theo danh mục
    category_price = (
        df.groupby("item_category_detail")["price_actual"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    # Trả kết quả để bên ngoài sử dụng
    return (
        total_products,
        total_categories,
        price_min,
        price_max,
        price_mean,
        price_median,
        category_count,
        price_count,
        category_price
    )


if __name__ == "__main__":

    # Đọc file Excel
    df = pd.read_excel("shopee_data_clean.xlsx")

    # Gọi hàm phân tích
    result = phan_tich_tong_quan(df)

    (
        total_products,
        total_categories,
        price_min,
        price_max,
        price_mean,
        price_median,
        category_count,
        price_count,
        category_price
    ) = result

    # 1. IN TỔNG QUAN

    print("===== TỔNG QUAN DỮ LIỆU =====")
    print("Số lượng sản phẩm:", total_products)
    print("Số lượng danh mục:", total_categories)

    print("\nGiá sản phẩm:")
    print("Giá thấp nhất:", price_min)
    print("Giá cao nhất:", price_max)
    print("Giá trung bình:", price_mean)
    print("Giá trung vị:", price_median)

    # 2. IN TOP DANH MỤC

    print("\n===== TOP DANH MỤC =====")
    print(category_count.head(10))

    # 3. BIỂU ĐỒ TOP 10 DANH MỤC

    plt.figure(figsize=(10, 6))
    category_count.head(10).sort_values().plot(kind="barh")
    plt.title("Top 10 danh mục có nhiều sản phẩm nhất")
    plt.xlabel("Số lượng sản phẩm")
    plt.ylabel("Danh mục")
    plt.tight_layout()
    plt.show()

    # 4. BIỂU ĐỒ KHOẢNG GIÁ

    print("\n===== PHÂN BỐ THEO KHOẢNG GIÁ =====")
    print(price_count)

    plt.figure(figsize=(8, 5))
    price_count.plot(kind="bar")
    plt.title("Số lượng sản phẩm theo khoảng giá")
    plt.xlabel("Khoảng giá")
    plt.ylabel("Số lượng sản phẩm")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # 5. BIỂU ĐỒ PHÂN BỐ GIÁ

    plt.figure(figsize=(8, 5))
    plt.hist(df["price_actual"], bins=30)
    plt.title("Phân bố giá sản phẩm")
    plt.xlabel("Giá bán thực tế")
    plt.ylabel("Số lượng sản phẩm")
    plt.tight_layout()
    plt.show()

    # 6. GIÁ TRUNG BÌNH THEO DANH MỤC

    print("\n===== TOP DANH MỤC CÓ GIÁ TRUNG BÌNH CAO =====")
    print(category_price)

    plt.figure(figsize=(10, 6))
    category_price.sort_values().plot(kind="barh")
    plt.title("Top 10 danh mục có giá bán trung bình cao nhất")
    plt.xlabel("Giá bán trung bình")
    plt.ylabel("Danh mục")
    plt.tight_layout()
    plt.show()