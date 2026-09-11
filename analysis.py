"""
Phân tích hành vi khách hàng - Shopee data
============================================
- Phân tích item_rating, total_rating, total_sold
- Top sản phẩm được đánh giá nhiều nhất (total_rating cao)
- Top sản phẩm bán chạy nhất (total_sold cao)
- Mối quan hệ giữa rating và lượt bán (correlation + scatter)
- Trực quan hóa thành biểu đồ, lưu vào thư mục outputs/

Cách chạy:
    python analysis.py
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # để chạy được trên môi trường không có màn hình (CI/GitHub Actions)
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "shopee_data_clean.xlsx")
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")
TOP_N = 15


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    # Chuẩn hoá kiểu dữ liệu số
    for col in ["item_rating", "total_rating", "total_sold", "price_actual", "price_ori"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["item_rating", "total_rating", "total_sold"])
    return df


def basic_stats(df: pd.DataFrame) -> None:
    print("=" * 60)
    print("1. THỐNG KÊ MÔ TẢ")
    print("=" * 60)
    stats = df[["item_rating", "total_rating", "total_sold"]].describe()
    print(stats)
    stats.to_csv(os.path.join(OUT_DIR, "basic_stats.csv"))

    # Phân phối item_rating
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(df["item_rating"], bins=20, ax=axes[0], color="#EE4D2D")
    axes[0].set_title("Phân phối Item Rating")
    axes[0].set_xlabel("item_rating")

    sns.histplot(df["total_rating"].clip(upper=df["total_rating"].quantile(0.95)),
                 bins=30, ax=axes[1], color="#F5A623")
    axes[1].set_title("Phân phối Total Rating (đã cắt outlier ở p95)")
    axes[1].set_xlabel("total_rating")

    sns.histplot(df["total_sold"].clip(upper=df["total_sold"].quantile(0.95)),
                 bins=30, ax=axes[2], color="#2ECC71")
    axes[2].set_title("Phân phối Total Sold (đã cắt outlier ở p95)")
    axes[2].set_xlabel("total_sold")

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "01_distributions.png"), dpi=150)
    plt.close()


def top_rated_products(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 60)
    print(f"2. TOP {TOP_N} SẢN PHẨM ĐƯỢC ĐÁNH GIÁ NHIỀU NHẤT (total_rating)")
    print("=" * 60)
    top = df.sort_values("total_rating", ascending=False).head(TOP_N)
    print(top[["title", "item_rating", "total_rating", "total_sold"]].to_string(index=False))
    top.to_csv(os.path.join(OUT_DIR, "top_rated_products.csv"), index=False)

    fig, ax = plt.subplots(figsize=(10, 8))
    labels = top["title"].str.slice(0, 40) + "..."
    sns.barplot(x=top["total_rating"], y=labels, ax=ax, color="#EE4D2D")
    ax.set_title(f"Top {TOP_N} sản phẩm được đánh giá nhiều nhất")
    ax.set_xlabel("Số lượt đánh giá (total_rating)")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "02_top_rated_products.png"), dpi=150)
    plt.close()
    return top


def top_selling_products(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 60)
    print(f"3. TOP {TOP_N} SẢN PHẨM BÁN CHẠY NHẤT (total_sold)")
    print("=" * 60)
    top = df.sort_values("total_sold", ascending=False).head(TOP_N)
    print(top[["title", "item_rating", "total_rating", "total_sold"]].to_string(index=False))
    top.to_csv(os.path.join(OUT_DIR, "top_selling_products.csv"), index=False)

    fig, ax = plt.subplots(figsize=(10, 8))
    labels = top["title"].str.slice(0, 40) + "..."
    sns.barplot(x=top["total_sold"], y=labels, ax=ax, color="#2ECC71")
    ax.set_title(f"Top {TOP_N} sản phẩm bán chạy nhất")
    ax.set_xlabel("Số lượng đã bán (total_sold)")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "03_top_selling_products.png"), dpi=150)
    plt.close()
    return top


def rating_vs_sold_relationship(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("4. MỐI QUAN HỆ GIỮA RATING VÀ LƯỢT BÁN")
    print("=" * 60)

    corr_rating_sold = df["item_rating"].corr(df["total_sold"])
    corr_totalrating_sold = df["total_rating"].corr(df["total_sold"])
    print(f"Tương quan item_rating  vs total_sold : {corr_rating_sold:.4f}")
    print(f"Tương quan total_rating vs total_sold : {corr_totalrating_sold:.4f}")

    with open(os.path.join(OUT_DIR, "correlation_summary.txt"), "w", encoding="utf-8") as f:
        f.write(f"Tương quan item_rating vs total_sold: {corr_rating_sold:.4f}\n")
        f.write(f"Tương quan total_rating vs total_sold: {corr_totalrating_sold:.4f}\n")

    # Scatter: item_rating vs total_sold (log scale vì total_sold lệch mạnh)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.scatterplot(data=df, x="item_rating", y="total_sold", alpha=0.3, ax=axes[0], color="#EE4D2D")
    axes[0].set_yscale("symlog")
    axes[0].set_title("Item rating vs Total sold (log scale)")

    # Rating trung bình theo nhóm (bin) rating để thấy xu hướng rõ hơn
    df_bin = df.copy()
    df_bin["rating_bin"] = df_bin["item_rating"].round(1)
    grouped = df_bin.groupby("rating_bin")["total_sold"].mean().reset_index()
    sns.barplot(data=grouped, x="rating_bin", y="total_sold", ax=axes[1], color="#F5A623")
    axes[1].set_title("Lượt bán trung bình theo mức rating")
    axes[1].set_xlabel("item_rating (làm tròn 0.1)")
    axes[1].set_ylabel("total_sold trung bình")
    axes[1].tick_params(axis="x", rotation=90)

    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "04_rating_vs_sold.png"), dpi=150)
    plt.close()

    # Heatmap tương quan tổng thể
    fig, ax = plt.subplots(figsize=(6, 5))
    corr_matrix = df[["item_rating", "total_rating", "total_sold"]].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="Oranges", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Ma trận tương quan")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "05_correlation_heatmap.png"), dpi=150)
    plt.close()


def main():
    df = load_data(DATA_PATH)
    print(f"Đã tải {len(df):,} sản phẩm.\n")

    basic_stats(df)
    top_rated_products(df)
    top_selling_products(df)
    rating_vs_sold_relationship(df)

    print("\nHoàn tất. Biểu đồ và bảng kết quả đã được lưu trong thư mục 'outputs/'.")


if __name__ == "__main__":
    main()
