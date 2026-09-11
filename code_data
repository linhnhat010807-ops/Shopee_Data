import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
# ==================== CONFIG ====================
FILE_PATH = "/mnt/user-data/uploads/shopee_data_clean.xlsx"
COL_PRICE_ORI = "price_ori"
COL_PRICE_ACTUAL = "price_actual"
COL_SOLD = "total_sold"
# ==================================================
 
 
def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """Đọc dữ liệu và làm sạch: loại bỏ giá trị âm/bằng 0, giá thực tế > giá gốc (dữ liệu lỗi)."""
    df = pd.read_excel(file_path)
 
    before = len(df)
    df = df[(df[COL_PRICE_ORI] > 0) & (df[COL_PRICE_ACTUAL] > 0)].copy()
    df = df[df[COL_PRICE_ACTUAL] <= df[COL_PRICE_ORI]].copy()
    after = len(df)
    print(f"Đã loại {before - after} dòng dữ liệu lỗi (giá <= 0 hoặc giá thực tế > giá gốc).")
    print(f"Số dòng dữ liệu hợp lệ còn lại: {after}\n")
 
    return df
 
 
def calculate_discount(df: pd.DataFrame) -> pd.DataFrame:
    """Tính số tiền giảm và phần trăm giảm giá."""
    df = df.copy()
    df["discount_amount"] = df[COL_PRICE_ORI] - df[COL_PRICE_ACTUAL]
    df["discount_pct"] = (df["discount_amount"] / df[COL_PRICE_ORI]) * 100
    return df
 
 
def summarize_price_comparison(df: pd.DataFrame):
    """So sánh tổng quan giữa giá gốc và giá thực tế."""
    summary = pd.DataFrame({
        "price_ori": df[COL_PRICE_ORI].describe(),
        "price_actual": df[COL_PRICE_ACTUAL].describe(),
    }).round(2)
    print("=== So sánh giá gốc vs giá thực tế ===")
    print(summary)
    print()
 
    no_discount = (df["discount_pct"] == 0).sum()
    has_discount = (df["discount_pct"] > 0).sum()
    print(f"Số sản phẩm KHÔNG giảm giá: {no_discount} ({no_discount/len(df)*100:.1f}%)")
    print(f"Số sản phẩm CÓ giảm giá: {has_discount} ({has_discount/len(df)*100:.1f}%)")
    print(f"Mức giảm giá trung bình (trên các SP có giảm): {df.loc[df['discount_pct']>0, 'discount_pct'].mean():.1f}%")
    print()
    return summary
 
 
def analyze_discount_vs_sold(df: pd.DataFrame, n_bins: int = 10):
    """
    Phân tích mối liên hệ giữa % giảm giá và số lượng bán.
    - Tính hệ số tương quan (Pearson & Spearman)
    - Chia % giảm giá thành các khoảng (bins) và so sánh total_sold trung bình mỗi khoảng
    """
    pearson_corr = df["discount_pct"].corr(df[COL_SOLD], method="pearson")
    spearman_corr = df["discount_pct"].corr(df[COL_SOLD], method="spearman")
 
    print("=== Tương quan giữa % giảm giá và lượng bán ===")
    print(f"Hệ số tương quan Pearson  (tuyến tính): {pearson_corr:.3f}")
    print(f"Hệ số tương quan Spearman (theo hạng):   {spearman_corr:.3f}")
    print("(Giá trị càng gần 1: tương quan dương mạnh | càng gần -1: tương quan âm mạnh | gần 0: không rõ liên hệ)\n")
 
    # Chia thành các khoảng % giảm giá để so sánh trực quan hơn
    bins = [-0.01, 0, 10, 20, 30, 40, 50, 100]
    labels = ["0%", "0-10%", "10-20%", "20-30%", "30-40%", "40-50%", ">50%"]
    df = df.copy()
    df["discount_bin"] = pd.cut(df["discount_pct"], bins=bins, labels=labels)
 
    bin_summary = (
        df.groupby("discount_bin", observed=True)
        .agg(
            avg_total_sold=(COL_SOLD, "mean"),
            median_total_sold=(COL_SOLD, "median"),
            product_count=(COL_SOLD, "count"),
        )
        .round(1)
    )
    print("=== Lượng bán trung bình theo từng khoảng % giảm giá ===")
    print(bin_summary)
    print()
 
    return pearson_corr, spearman_corr, bin_summary, df
 
 
def plot_results(df: pd.DataFrame, bin_summary: pd.DataFrame):
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
 
    # 1. So sánh phân phối giá gốc vs giá thực tế (log scale vì giá lệch nhiều)
    axes[0, 0].hist(np.log1p(df[COL_PRICE_ORI]), bins=50, alpha=0.6, label="Giá gốc", color="#C44E52")
    axes[0, 0].hist(np.log1p(df[COL_PRICE_ACTUAL]), bins=50, alpha=0.6, label="Giá thực tế", color="#4C72B0")
    axes[0, 0].set_title("Phân phối giá gốc vs giá thực tế (thang log)")
    axes[0, 0].set_xlabel("log(1 + giá)")
    axes[0, 0].set_ylabel("Số lượng sản phẩm")
    axes[0, 0].legend()
 
    # 2. Phân phối % giảm giá
    axes[0, 1].hist(df["discount_pct"], bins=40, color="#55A868")
    axes[0, 1].set_title("Phân phối % giảm giá")
    axes[0, 1].set_xlabel("% giảm giá")
    axes[0, 1].set_ylabel("Số lượng sản phẩm")
 
    # 3. Scatter: % giảm giá vs total_sold (log scale trục y vì total_sold lệch mạnh)
    axes[1, 0].scatter(df["discount_pct"], df[COL_SOLD], alpha=0.15, s=10, color="#8172B2")
    axes[1, 0].set_yscale("log")
    axes[1, 0].set_title("% giảm giá vs Lượng bán (trục y dạng log)")
    axes[1, 0].set_xlabel("% giảm giá")
    axes[1, 0].set_ylabel("Total sold (log scale)")
 
    # 4. Bar chart: lượng bán trung bình theo khoảng giảm giá
    axes[1, 1].bar(bin_summary.index.astype(str), bin_summary["avg_total_sold"], color="#DD8452")
    axes[1, 1].set_title("Lượng bán TB theo khoảng % giảm giá")
    axes[1, 1].set_xlabel("Khoảng % giảm giá")
    axes[1, 1].set_ylabel("Total sold trung bình")
    axes[1, 1].tick_params(axis="x", rotation=30)
 
    plt.tight_layout()
    plt.savefig("/mnt/user-data/outputs/price_discount_analysis.png", dpi=150)
    plt.show()
    print("Đã lưu biểu đồ: price_discount_analysis.png")
 
 
def main():
    df = load_and_clean_data(FILE_PATH)
    df = calculate_discount(df)
 
    summarize_price_comparison(df)
    pearson_corr, spearman_corr, bin_summary, df = analyze_discount_vs_sold(df)
    plot_results(df, bin_summary)
 
    # Nhận định nhanh dựa trên hệ số tương quan
    if abs(pearson_corr) < 0.05 and abs(spearman_corr) < 0.05:
        conclusion = "Mức giảm giá gần như KHÔNG có liên hệ rõ ràng với lượng bán."
    elif spearman_corr > 0:
        conclusion = "Giảm giá nhiều hơn có xu hướng đi kèm lượng bán CAO HƠN (liên hệ dương)."
    else:
        conclusion = "Giảm giá nhiều hơn có xu hướng đi kèm lượng bán THẤP HƠN (liên hệ âm) - có thể do yếu tố khác chi phối (ngành hàng, shop, giá trị tuyệt đối...)."
    print(f"\n=> Nhận định: {conclusion}")
 
 
if __name__ == "__main__":
    main()
