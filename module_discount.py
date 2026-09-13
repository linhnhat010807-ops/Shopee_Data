
"""
PHÂN TÍCH GIÁ VÀ KHUYẾN MÃI - Dữ liệu Shopee
--------------------------------------------
1. So sánh giá gốc (price_ori) và giá thực tế (price_actual)
2. Tính % giảm giá
3. Phân tích mối liên hệ giữa % giảm giá và số lượng bán (total_sold)
4. Trực quan hóa: 1 lưới 4 biểu đồ tổng quan + 1 ma trận tương quan (heatmap)
"""
 
import pandas as pd              # đọc file Excel và xử lý dữ liệu dạng bảng (DataFrame)
import numpy as np                # tính toán số học, đặc biệt là log(1+x) để giảm độ lệch dữ liệu
import matplotlib.pyplot as plt   # vẽ biểu đồ (histogram, scatter, bar...)
import seaborn as sns             # vẽ heatmap đẹp hơn, và set style tổng thể cho biểu đồ
from scipy import stats           # tính hệ số tương quan Pearson & Spearman kèm p-value
 
sns.set_theme(style="whitegrid")  # áp dụng theme nền lưới trắng cho toàn bộ biểu đồ trong file
 
# 0. ĐỌC DỮ LIỆU
FILE_PATH = "shopee_data_clean.xlsx"   # đường dẫn tới file dữ liệu, đổi lại nếu file ở vị trí khác
df = pd.read_excel(FILE_PATH)          # đọc file Excel vào DataFrame df
print("Số dòng, số cột ban đầu:", df.shape)   # in số dòng/cột để kiểm tra đã đọc đúng dữ liệu 
# 2. TÍNH SỐ TIỀN GIẢM & PHẦN TRĂM GIẢM GIÁ
df["discount_amount"] = df["price_ori"] - df["price_actual"]
# ↑ tạo cột mới = số tiền được giảm (giá gốc trừ giá thực tế)
 
df["discount_pct"] = (df["discount_amount"] / df["price_ori"]) * 100
# ↑ tạo cột mới = phần trăm giảm giá = (số tiền giảm / giá gốc) * 100
 
# Gom nhóm mức giảm giá thành các khoảng (bins) để so sánh lượng bán trung bình
bins = [-0.01, 0, 10, 20, 30, 40, 50, 100]
# ↑ các mốc chia khoảng % giảm giá (bắt đầu từ -0.01 để bao trọn giá trị 0%)
labels = ["0%", "0-10%", "10-20%", "20-30%", "30-40%", "40-50%", ">50%"]
# ↑ tên nhãn tương ứng cho từng khoảng ở trên (7 mốc bins -> 7 nhãn... 6 khoảng, khớp với 7 bins)
df["discount_group"] = pd.cut(df["discount_pct"], bins=bins, labels=labels)
# ↑ dùng pd.cut để gán mỗi sản phẩm vào 1 nhóm % giảm giá tương ứng, lưu vào cột discount_group
 
print("\nThống kê % giảm giá:")
print(df["discount_pct"].describe())
# ↑ in thống kê mô tả (mean, std, min, max, các mốc phần trăm...) của cột % giảm giá
 
# 3. SO SÁNH GIÁ GỐC VÀ GIÁ THỰC TẾ (tổng quan)
summary_price = pd.DataFrame({
    "Giá gốc (price_ori)": df["price_ori"].describe(),
    "Giá thực tế (price_actual)": df["price_actual"].describe()
})
# ↑ ghép 2 bảng thống kê mô tả (của price_ori và price_actual) thành 1 DataFrame để so sánh song song
print("\n=== So sánh Giá gốc vs Giá thực tế ===")
print(summary_price)   # in bảng so sánh ra màn hình
 
group_stats = df.groupby("discount_group", observed=True).agg(
    so_luong_sp=("discount_pct", "count"),        # đếm số sản phẩm trong mỗi nhóm
    trung_binh_giam_gia=("discount_pct", "mean"),  # % giảm giá trung bình của mỗi nhóm
    trung_binh_ban=("total_sold", "mean"),         # số lượng bán trung bình của mỗi nhóm
    tong_ban=("total_sold", "sum")                 # tổng số lượng bán của mỗi nhóm
).reset_index()
# ↑ nhóm dữ liệu theo discount_group rồi tính 4 chỉ số thống kê ở trên cho từng nhóm
#   observed=True: chỉ lấy các nhóm thực sự xuất hiện trong dữ liệu (tránh nhóm rỗng)
#   .reset_index(): đưa discount_group từ index thành cột bình thường để dễ vẽ biểu đồ
print("\n=== Số lượng bán trung bình theo nhóm mức giảm giá ===")
print(group_stats)   # in bảng thống kê theo nhóm mức giảm giá
 
# 4. PHÂN TÍCH TƯƠNG QUAN: % GIẢM GIÁ vs SỐ LƯỢNG BÁN
corr_pearson, p_pearson = stats.pearsonr(df["discount_pct"], df["total_sold"])
# ↑ tính hệ số tương quan Pearson (đo mối quan hệ TUYẾN TÍNH) giữa % giảm giá và số lượng bán,
#   trả về hệ số r và p-value (p-value nhỏ nghĩa là mối quan hệ có ý nghĩa thống kê)
 
corr_spearman, p_spearman = stats.spearmanr(df["discount_pct"], df["total_sold"])
# ↑ tính hệ số tương quan Spearman (đo mối quan hệ theo THỨ HẠNG, không cần tuyến tính,
#   phù hợp hơn Pearson vì total_sold bị lệch phân phối rất mạnh)
 
print("\n=== Hệ số tương quan giữa % giảm giá và số lượng bán ===")
print(f"Pearson : r = {corr_pearson:.4f}, p-value = {p_pearson:.4g}")
print(f"Spearman: r = {corr_spearman:.4f}, p-value = {p_spearman:.4g}")
# ↑ in kết quả 2 hệ số tương quan, làm tròn 4 chữ số thập phân
 
if abs(corr_spearman) < 0.1:
    nhan_xet = "gần như không có mối liên hệ tuyến tính rõ ràng"
elif abs(corr_spearman) < 0.3:
    nhan_xet = "có mối liên hệ yếu"
elif abs(corr_spearman) < 0.5:
    nhan_xet = "có mối liên hệ trung bình"
else:
    nhan_xet = "có mối liên hệ khá mạnh"
# ↑ dựa vào độ lớn |Spearman r| để tự động phân loại mức độ tương quan mạnh/yếu
 
chieu = "cùng chiều (giảm giá càng nhiều, bán càng nhiều)" if corr_spearman > 0 else "ngược chiều"
# ↑ xác định chiều tương quan: dương -> cùng chiều, âm -> ngược chiều
 
print(f"=> Nhận xét: % giảm giá và số lượng bán {nhan_xet}, xu hướng {chieu} "
      f"(Spearman r = {corr_spearman:.3f}).")
# ↑ in câu nhận xét tổng hợp bằng tiếng Việt dựa trên 2 biến vừa tính ở trên
 
# 5. TRỰC QUAN HÓA
 
# ---------- HÌNH 1: lưới 2x2 tổng quan (giống layout yêu cầu) ----------
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
# ↑ tạo 1 hình (fig) chứa lưới 2 hàng x 2 cột subplot (axes), kích thước 14x10 inch
#   axes là mảng 2x2, truy cập từng ô bằng axes[hàng, cột]
 
# (1) Phân phối giá gốc vs giá thực tế (thang log để dễ nhìn vì giá lệch mạnh)
ax = axes[0, 0]   # chọn subplot ở hàng 0, cột 0 (góc trên bên trái)
log_price_ori = np.log1p(df["price_ori"])
# ↑ tính log(1 + price_ori): dùng log1p thay vì log thường để tránh lỗi log(0),
#   đồng thời giúp "nén" các giá trị giá quá lớn lại, biểu đồ dễ nhìn hơn
log_price_actual = np.log1p(df["price_actual"])
# ↑ tương tự, tính log(1 + price_actual)
ax.hist(log_price_ori, bins=40, alpha=0.55, label="Giá gốc (price_ori)", color="#e74c3c")
# ↑ vẽ histogram (biểu đồ tần suất) của log giá gốc, 40 cột (bins), độ trong suốt 0.55, màu đỏ
ax.hist(log_price_actual, bins=40, alpha=0.55, label="Giá thực tế (price_actual)", color="#3498db")
# ↑ vẽ chồng thêm histogram của log giá thực tế, màu xanh dương, để so sánh 2 phân phối
ax.set_title("Phân phối giá gốc vs giá thực tế (thang log)")   # tiêu đề subplot
ax.set_xlabel("log(1 + giá)")           # nhãn trục x
ax.set_ylabel("Số lượng sản phẩm")      # nhãn trục y
ax.legend()   # hiện chú thích (label) phân biệt màu đỏ/xanh là giá gốc/giá thực tế
 
# (2) Phân phối % giảm giá
ax = axes[0, 1]   # chọn subplot ở hàng 0, cột 1 (góc trên bên phải)
ax.hist(df["discount_pct"], bins=30, color="#2ecc71", edgecolor="white")
# ↑ vẽ histogram của % giảm giá, 30 cột, màu xanh lá, viền cột màu trắng cho rõ ràng
ax.set_title("Phân phối % giảm giá")
ax.set_xlabel("% giảm giá")
ax.set_ylabel("Số lượng sản phẩm")
ax.axvline(df["discount_pct"].mean(), color="black", linestyle="--", linewidth=1,
           label=f"TB = {df['discount_pct'].mean():.1f}%")
# ↑ vẽ 1 đường thẳng đứng nét đứt tại giá trị trung bình % giảm giá, kèm nhãn ghi rõ số liệu
ax.legend()   # hiện chú thích cho đường trung bình vừa vẽ
 
# (3) % giảm giá vs Lượng bán (trục y dạng log)
ax = axes[1, 0]   # chọn subplot ở hàng 1, cột 0 (góc dưới bên trái)
ax.scatter(df["discount_pct"], df["total_sold"], alpha=0.25, s=10, color="#8e44ad")
# ↑ vẽ scatter plot: mỗi điểm là 1 sản phẩm, trục x = % giảm giá, trục y = số lượng bán
#   alpha=0.25 (độ trong suốt) và s=10 (kích thước điểm nhỏ) để nhìn rõ mật độ điểm khi dữ liệu nhiều
ax.set_yscale("log")   # ↑ chuyển trục y sang thang log vì total_sold lệch phân phối rất mạnh
ax.set_title(f"% giảm giá vs Lượng bán (trục y log)\nSpearman r = {corr_spearman:.2f}")
# ↑ tiêu đề có kèm luôn hệ số tương quan Spearman đã tính ở bước 4, để người xem thấy ngay
ax.set_xlabel("% giảm giá")
ax.set_ylabel("Total sold (log scale)")
 
# (4) Lượng bán TB theo khoảng % giảm giá
ax = axes[1, 1]   # chọn subplot ở hàng 1, cột 1 (góc dưới bên phải)
bars = ax.bar(group_stats["discount_group"].astype(str), group_stats["trung_binh_ban"],
              color="#e67e22", edgecolor="white")
# ↑ vẽ bar chart: trục x là các nhóm % giảm giá, trục y là lượng bán trung bình của mỗi nhóm
#   .astype(str) để đảm bảo nhãn nhóm hiển thị đúng dạng chữ; bars lưu lại để gắn nhãn số liệu bên dưới
ax.set_title("Lượng bán TB theo khoảng % giảm giá")
ax.set_xlabel("Khoảng % giảm giá")
ax.set_ylabel("Total sold trung bình")
# chú thích số liệu trên đầu mỗi cột
for bar, val in zip(bars, group_stats["trung_binh_ban"]):
    # ↑ duyệt qua từng cột (bar) cùng với giá trị (val) tương ứng của nó
    ax.annotate(f"{val:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, val),
                xytext=(0, 3), textcoords="offset points",
                ha="center", va="bottom", fontsize=8)
    # ↑ ghi số liệu (định dạng có dấu phẩy ngăn cách hàng nghìn) ngay phía trên đỉnh mỗi cột:
    #   xy: vị trí đỉnh cột (giữa cột theo trục x, chiều cao val theo trục y)
    #   xytext=(0,3): dịch chữ lên thêm 3 điểm ảnh cho khỏi đè lên cột
    #   ha="center", va="bottom": căn giữa theo chiều ngang, căn đáy chữ theo chiều dọc
 
fig.suptitle("PHÂN TÍCH GIÁ VÀ KHUYẾN MÃI SẢN PHẨM", fontsize=15, fontweight="bold")
# ↑ đặt tiêu đề chung cho cả hình (bao trùm cả 4 subplot), chữ đậm cỡ 15
fig.tight_layout(rect=[0, 0, 1, 0.96])
# ↑ tự động canh chỉnh khoảng cách giữa các subplot cho gọn gàng, không chồng chữ lên nhau
#   rect=[0,0,1,0.96]: chừa 4% phía trên cho tiêu đề chung (suptitle) không bị đè lên biểu đồ
fig.savefig("bieu_do_tong_quan_gia_khuyenmai.png", dpi=150)
# ↑ lưu hình thành file PNG, độ phân giải 150 dpi (đủ nét để xem/in)
plt.close(fig)   # đóng hình lại để giải phóng bộ nhớ, tránh hiển thị chồng lên hình tiếp theo
 
# ---------- HÌNH 2: MA TRẬN TƯƠNG QUAN (Correlation Heatmap) ----------
df["log_total_sold"] = np.log1p(df["total_sold"])
# ↑ tạo thêm cột log(1 + total_sold) để đưa vào ma trận tương quan
#   (giúp thấy rõ tương quan hơn vì total_sold gốc bị lệch phân phối mạnh)
 
corr_cols = ["price_ori", "price_actual", "discount_amount", "discount_pct",
             "total_sold", "log_total_sold", "item_rating", "total_rating"]
# ↑ danh sách các cột số sẽ đưa vào tính ma trận tương quan
 
corr_labels = ["Giá gốc", "Giá thực tế", "Số tiền giảm", "% giảm giá",
               "Lượng bán", "log(Lượng bán)", "Đánh giá SP", "Số lượt đánh giá"]
# ↑ tên tiếng Việt tương ứng 1-1 với corr_cols, dùng để hiển thị cho dễ đọc thay vì tên cột kỹ thuật
 
corr_matrix = df[corr_cols].corr(method="spearman")
# ↑ tính ma trận tương quan Spearman giữa tất cả các cặp cột trong corr_cols
#   dùng Spearman (thay vì Pearson mặc định) vì phù hợp với dữ liệu lệch phân phối như ở đây
 
corr_matrix.index = corr_labels     # đổi tên các dòng của ma trận sang tiếng Việt
corr_matrix.columns = corr_labels   # đổi tên các cột của ma trận sang tiếng Việt
 
plt.figure(figsize=(9, 7))   # tạo 1 hình mới kích thước 9x7 inch cho heatmap
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
 

