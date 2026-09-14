
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
# 0. ĐỌC DỮ LIỆU
FILE_PATH = "shopee_data_clean.xlsx"   
df = pd.read_excel(FILE_PATH)          
print("Số dòng, số cột ban đầu:", df.shape)   
# 2. TÍNH SỐ TIỀN GIẢM & PHẦN TRĂM GIẢM GIÁ
df["discount_amount"] = df["price_ori"] - df["price_actual"]
df["discount_pct"] = (df["discount_amount"] / df["price_ori"]) * 100
bins = [-0.01, 0, 10, 20, 30, 40, 50, 100]

labels = ["0%", "0-10%", "10-20%", "20-30%", "30-40%", "40-50%", ">50%"]
df["discount_group"] = pd.cut(df["discount_pct"], bins=bins, labels=labels)
 
print("\nThống kê % giảm giá:")
print(df["discount_pct"].describe())
 
# 3. SO SÁNH GIÁ GỐC VÀ GIÁ THỰC TẾ (tổng quan)
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
print(group_stats)   # in bảng thống kê theo nhóm mức giảm giá
 
# 4. PHÂN TÍCH TƯƠNG QUAN: % GIẢM GIÁ vs SỐ LƯỢNG BÁN
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
# 5. TRỰC QUAN HÓA
 
# HÌNH 1: 
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# (1) Phân phối giá gốc vs giá thực tế (thang log để dễ nhìn vì giá lệch mạnh)
ax = axes[0, 0]   # chọn subplot ở hàng 0, cột 0 (góc trên bên trái)
log_price_ori = np.log1p(df["price_ori"])

log_price_actual = np.log1p(df["price_actual"])
ax.hist(log_price_ori, bins=40, alpha=0.55, label="Giá gốc (price_ori)", color="#e74c3c")
ax.hist(log_price_actual, bins=40, alpha=0.55, label="Giá thực tế (price_actual)", color="#3498db")
ax.set_title("Phân phối giá gốc vs giá thực tế (thang log)")   # tiêu đề subplot
ax.set_xlabel("log(1 + giá)")           
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
ax.legend()   # hiện chú thích cho đường trung bình vừa vẽ
 
# (3) % giảm giá vs Lượng bán (trục y dạng log)
ax = axes[1, 0]   
ax.scatter(df["discount_pct"], df["total_sold"], alpha=0.25, s=10, color="#8e44ad")

ax.set_yscale("log")   
ax.set_title(f"% giảm giá vs Lượng bán (trục y log)\nSpearman r = {corr_spearman:.2f}")

ax.set_xlabel("% giảm giá")
ax.set_ylabel("Total sold (log scale)")
 
# (4) Lượng bán TB theo khoảng % giảm giá
ax = axes[1, 1]   # chọn subplot ở hàng 1, cột 1 (góc dưới bên phải)
bars = ax.bar(group_stats["discount_group"].astype(str), group_stats["trung_binh_ban"],
              color="#e67e22", edgecolor="white")

ax.set_title("Lượng bán TB theo khoảng % giảm giá")
ax.set_xlabel("Khoảng % giảm giá")
ax.set_ylabel("Total sold trung bình")

for bar, val in zip(bars, group_stats["trung_binh_ban"]):
    # ↑ duyệt qua từng cột (bar) cùng với giá trị (val) tương ứng của nó
    ax.annotate(f"{val:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, val),
                xytext=(0, 3), textcoords="offset points",
                ha="center", va="bottom", fontsize=8)
   
fig.suptitle("PHÂN TÍCH GIÁ VÀ KHUYẾN MÃI SẢN PHẨM", fontsize=15, fontweight="bold")

fig.tight_layout(rect=[0, 0, 1, 0.96])

fig.savefig("bieu_do_tong_quan_gia_khuyenmai.png", dpi=150)

plt.close(fig)   # đóng hình lại để giải phóng bộ nhớ, tránh hiển thị chồng lên hình tiếp theo
 
#  HÌNH 2: 
df["log_total_sold"] = np.log1p(df["total_sold"])
 
corr_cols = ["price_ori", "price_actual", "discount_amount", "discount_pct",
             "total_sold", "log_total_sold", "item_rating", "total_rating"]

corr_labels = ["Giá gốc", "Giá thực tế", "Số tiền giảm", "% giảm giá",
               "Lượng bán", "log(Lượng bán)", "Đánh giá SP", "Số lượt đánh giá"]

corr_matrix = df[corr_cols].corr(method="spearman")

corr_matrix.index = corr_labels     # đổi tên các dòng của ma trận sang tiếng Việt
corr_matrix.columns = corr_labels   # đổi tên các cột của ma trận sang tiếng Việt
 
plt.figure(figsize=(9, 7))   
sns.heatmap(
    corr_matrix,
    annot=True, fmt=".2f",       # annot=True: ghi số hệ số tương quan lên từng ô; fmt=".2f": làm tròn 2 chữ số
    cmap="coolwarm", vmin=-1, vmax=1,   # bảng màu coolwarm (xanh = âm, đỏ = dương), cố định thang từ -1 đến 1
    linewidths=0.5, square=True,        # kẻ viền mảnh giữa các ô; square=True để mỗi ô là hình vuông
    cbar_kws={"label": "Hệ số tương quan Spearman"}   # nhãn cho thanh màu (colorbar) bên phải
)
plt.title("Ma trận tương quan (Spearman) giữa các biến giá, khuyến mãi và lượng bán")
plt.xticks(rotation=40, ha="right")
# ↑ xoay nhãn trục x 40 độ, căn phải, để tên biến dài không bị chồng chéo lên nhau
plt.tight_layout()   # tự động canh chỉnh lề cho gọn, tránh chữ bị cắt
plt.savefig("bieu_do_ma_tran_tuong_quan.png", dpi=150)   # lưu heatmap thành file PNG
plt.close()   # đóng hình để giải phóng bộ nhớ
 
print("\nĐã lưu 2 file biểu đồ:")
print(" 1. bieu_do_tong_quan_gia_khuyenmai.png  (4 biểu đồ: phân phối giá, % giảm giá, scatter, bar TB)")
print(" 2. bieu_do_ma_tran_tuong_quan.png        (ma trận tương quan)")
 

