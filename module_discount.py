"""
PHÂN TÍCH GIÁ VÀ KHUYẾN MÃI - Dữ liệu Shopee
--------------------------------------------
1. So sánh giá gốc (price_ori) và giá thực tế (price_actual)
2. Tính % giảm giá
3. Phân tích mối liên hệ giữa % giảm giá và số lượng bán (total_sold)
4. Trực quan hóa: 1 lưới 4 biểu đồ tổng quan + 1 ma trận tương quan (heatmap)
"""
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
 
sns.set_theme(style="whitegrid")
 
FILE_PATH = "shopee_data_clean.xlsx"   
 
# HÀM 1: ĐỌC DỮ LIỆU
def load_data(file_path):
    """Đọc file Excel và trả về DataFrame."""
    df = pd.read_excel(file_path)
    print("Số dòng, số cột ban đầu:", df.shape)
    return df
 
# HÀM 2: TÍNH SỐ TIỀN GIẢM & PHẦN TRĂM GIẢM GIÁ
def calculate_discount(df):
    """Tính discount_amount, discount_pct và gom nhóm discount_group."""
    df["discount_amount"] = df["price_ori"] - df["price_actual"]
    df["discount_pct"] = (df["discount_amount"] / df["price_ori"]) * 100
 
    bins = [-0.01, 0, 10, 20, 30, 40, 50, 100]
    labels = ["0%", "0-10%", "10-20%", "20-30%", "30-40%", "40-50%", ">50%"]
    df["discount_group"] = pd.cut(df["discount_pct"], bins=bins, labels=labels)
 
    print("\nThống kê % giảm giá:")
    print(df["discount_pct"].describe())
    return df
 
# HÀM 3: SO SÁNH GIÁ GỐC VÀ GIÁ THỰC TẾ
def summarize_price_comparison(df):
    """In bảng thống kê mô tả so sánh giá gốc vs giá thực tế,
    và bảng lượng bán trung bình theo nhóm mức giảm giá."""
    summary_price = pd.DataFrame({
        "Giá gốc (price_ori)": df["price_ori"].describe(),
        "Giá thực tế (price_actual)": df["price_actual"].describe()
    })
    print("\n=== So sánh Giá gốc vs Giá thực tế ===")
    print(summary_price)
 
    group_stats = df.groupby("discount_group", observed=True).agg(
        so_luong_sp=("discount_pct", "count"),
        trung_binh_giam_gia=("discount_pct", "mean"),
        trung_binh_ban=("total_sold", "mean"),
        tong_ban=("total_sold", "sum")
    ).reset_index()
 
    print("\n=== Số lượng bán trung bình theo nhóm mức giảm giá ===")
    print(group_stats)
    return group_stats
 
# HÀM 4: PHÂN TÍCH TƯƠNG QUAN % GIẢM GIÁ vs SỐ LƯỢNG BÁN
def analyze_discount_vs_sold(df):
    """Tính hệ số tương quan Pearson & Spearman giữa discount_pct và total_sold,
    đưa ra nhận xét bằng lời, trả về hệ số Spearman để dùng lại khi vẽ biểu đồ."""
    corr_pearson, p_pearson = stats.pearsonr(df["discount_pct"], df["total_sold"])
    corr_spearman, p_spearman = stats.spearmanr(df["discount_pct"], df["total_sold"])
 
    print("\n=== Hệ số tương quan giữa % giảm giá và số lượng bán ===")
    print(f"Pearson : r = {corr_pearson:.4f}, p-value = {p_pearson:.4g}")
    print(f"Spearman: r = {corr_spearman:.4f}, p-value = {p_spearman:.4g}")
 
    if abs(corr_spearman) < 0.1:
        nhan_xet = "gần như không có mối liên hệ tuyến tính rõ ràng"
    elif abs(corr_spearman) < 0.3:
        nhan_xet = "có mối liên hệ yếu"
    elif abs(corr_spearman) < 0.5:
        nhan_xet = "có mối liên hệ trung bình"
    else:
        nhan_xet = "có mối liên hệ khá mạnh"
 
    chieu = "cùng chiều (giảm giá càng nhiều, bán càng nhiều)" if corr_spearman > 0 else "ngược chiều"
    print(f"=> Nhận xét: % giảm giá và số lượng bán {nhan_xet}, xu hướng {chieu} "
          f"(Spearman r = {corr_spearman:.3f}).")
 
    return corr_spearman
 
# HÀM 5: VẼ 4 BIỂU ĐỒ TỔNG QUAN (LƯỚI 2x2)
def plot_overview(df, group_stats, corr_spearman,
                   output_file="bieu_do_tong_quan_gia_khuyenmai.png"):
    """Vẽ lưới 2x2: phân phối giá, phân phối % giảm giá, scatter, bar chart."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
 
    # (1) Phân phối giá gốc vs giá thực tế (thang log để dễ nhìn vì giá lệch mạnh)
    ax = axes[0, 0]
    log_price_ori = np.log1p(df["price_ori"])
    log_price_actual = np.log1p(df["price_actual"])
    ax.hist(log_price_ori, bins=40, alpha=0.55, label="Giá gốc (price_ori)", color="#e74c3c")
    ax.hist(log_price_actual, bins=40, alpha=0.55, label="Giá thực tế (price_actual)", color="#3498db")
    ax.set_title("Phân phối giá gốc vs giá thực tế (thang log)")
    ax.set_xlabel("Mức giá (Đã điều chỉnh)")
    ax.set_ylabel("Số lượng sản phẩm")
    ax.legend()
 
    # (2) Phân phối % giảm giá
    ax = axes[0, 1]
    ax.hist(df["discount_pct"], bins=30, color="#2ecc71", edgecolor="white")
    ax.set_title("Phân phối % giảm giá")
    ax.set_xlabel("% giảm giá")
    ax.set_ylabel("Số lượng sản phẩm")
    ax.axvline(df["discount_pct"].mean(), color="black", linestyle="--", linewidth=1,
               label=f"TB = {df['discount_pct'].mean():.1f}%")
    ax.legend()
 
    # (3) % giảm giá vs Lượng bán (trục y dạng log)
    ax = axes[1, 0]
    ax.scatter(df["discount_pct"], df["total_sold"], alpha=0.25, s=10, color="#8e44ad")
    ax.set_yscale("log")
    ax.set_title(f"% giảm giá vs Lượng bán (trục y log)\nr = {corr_spearman:.2f}")
    ax.set_xlabel("% giảm giá")
    ax.set_ylabel("Total sold (log scale)")
 
    # (4) Lượng bán TB theo khoảng % giảm giá
    ax = axes[1, 1]
    bars = ax.bar(group_stats["discount_group"].astype(str), group_stats["trung_binh_ban"],
                  color="#e67e22", edgecolor="white")
    ax.set_title("Lượng bán TB theo khoảng % giảm giá")
    ax.set_xlabel("Khoảng % giảm giá")
    ax.set_ylabel("Total sold trung bình")
    for bar, val in zip(bars, group_stats["trung_binh_ban"]):
        ax.annotate(f"{val:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, val),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8)
 
    fig.suptitle("PHÂN TÍCH GIÁ VÀ KHUYẾN MÃI SẢN PHẨM", fontsize=15, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(output_file, dpi=150)
    plt.close(fig)
    return output_file
 
# HÀM 6: VẼ MA TRẬN TƯƠNG QUAN (HEATMAP)
def plot_correlation_matrix(df, output_file="bieu_do_ma_tran_tuong_quan.png"):
    """Tính và vẽ ma trận tương quan Spearman giữa các biến chính."""
    df["log_total_sold"] = np.log1p(df["total_sold"])
 
    corr_cols = ["price_ori", "price_actual", "discount_amount", "discount_pct",
                 "total_sold", "log_total_sold", "item_rating", "total_rating"]
    corr_labels = ["Giá gốc", "Giá thực tế", "Số tiền giảm", "% giảm giá",
                   "Lượng bán", "log(Lượng bán)", "Đánh giá SP", "Số lượt đánh giá"]
 
    corr_matrix = df[corr_cols].corr(method="spearman")
    corr_matrix.index = corr_labels
    corr_matrix.columns = corr_labels
 
    plt.figure(figsize=(9, 7))
    sns.heatmap(
        corr_matrix,
        annot=True, fmt=".2f",
        cmap="coolwarm", vmin=-1, vmax=1,
        linewidths=0.5, square=True,
        cbar_kws={"label": "Hệ số tương quan"}
    )
    plt.title("Ma trận tương quan giữa các biến giá, khuyến mãi và lượng bán")
    plt.xticks(rotation=40, ha="right")
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()
    return output_file

# HÀM MAIN: GỌI TUẦN TỰ CÁC HÀM Ở TRÊN
def main():
    df = load_data(FILE_PATH)
    df = calculate_discount(df)
    group_stats = summarize_price_comparison(df)
    corr_spearman = analyze_discount_vs_sold(df)
 
    file1 = plot_overview(df, group_stats, corr_spearman)
    file2 = plot_correlation_matrix(df)
 
    print("\nĐã lưu 2 file biểu đồ:")
    print(f" 1. {file1}  (4 biểu đồ: phân phối giá, % giảm giá, scatter, bar TB)")
    print(f" 2. {file2}  (ma trận tương quan)")
if __name__ == "__main__":
    main()
 



