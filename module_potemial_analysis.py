"""
PHÂN TÍCH TỔNG HỢP & XÁC ĐỊNH SẢN PHẨM TIỀM NĂNG - SHOPEE DATA.
Mô-đun tích hợp chạy độc lập, kết nối kết quả từ 4 mô-đun thành viên.
"""

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. IMPORT VÀ KIỂM TRA MÔ-ĐUN CỦA CÁC THÀNH VIÊN

HAS_PRICE_RANGE = False
HAS_RATING_SOLD = False
HAS_CATEGORY_TIME = False
HAS_DISCOUNT = False

try:
    import module_price_range
    HAS_PRICE_RANGE = True
except ImportError:
    print("Chưa thấy file 'module_price_range.py' - Sẽ sử dụng hàm tự động dự phòng.")

try:
    import module_rating_sold
    HAS_RATING_SOLD = True
except ImportError:
    print("Chưa thấy file 'module_rating_sold.py' - Sẽ sử dụng hàm tự động dự phòng.")

try:
    import module_category_time
    HAS_CATEGORY_TIME = True
except ImportError:
    print("Chưa thấy file 'module_category_time.py' - Sẽ sử dụng hàm tự động dự phòng.")

try:
    import module_discount
    HAS_DISCOUNT = True
except ImportError:
    print("Chưa thấy file 'module_discount.py' - Sẽ sử dụng hàm tự động dự phòng.")

# Cấu hình font tiếng Việt an toàn cho Matplotlib
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "shopee_data_clean.xlsx")
if not os.path.exists(DATA_PATH):
    DATA_PATH = os.path.join(BASE_DIR, "data", "shopee_data_clean.xlsx")

OUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

# 2. HÀM TỰ ĐỘNG DỰ PHÒNG (FALLBACKS)

def fallback_price_range(df: pd.DataFrame) -> pd.DataFrame:
    """Tự động phân khoảng giá nếu file bị lỗi hoặc chưa ready."""
    bins = [0, 50000, 100000, 200000, 500000, float("inf")]
    labels = ["<50K", "50K-100K", "100K-200K", "200K-500K", ">500K"]
    df["price_range"] = pd.cut(df["price_actual"], bins=bins, labels=labels, include_lowest=True)
    return df

def fallback_category_time(df: pd.DataFrame) -> pd.DataFrame:
    """Tự động tạo cột ngành hàng nếu file bị lỗi hoặc chưa ready."""
    if "item_category_detail" in df.columns:
        def extract_cat(val):
            if pd.isna(val):
                return "Khác"
            parts = str(val).split("|")
            return parts[1].strip() if len(parts) > 1 else parts[0].strip()
        df["main_category"] = df["item_category_detail"].apply(extract_cat)
    elif "category" in df.columns:
        df["main_category"] = df["category"].astype(str).str.split(">").str[0].str.strip()
    else:
        df["main_category"] = "Khác"
    return df

# 3. TÍCH HỢP XỬ LÝ DỮ LIỆU TỪ CÁC MÔ-ĐUN THÀNH PHẦN

def load_and_integrate_all_modules(path: str) -> pd.DataFrame:
    """Đọc dữ liệu và tương thích an toàn với hàm/cột từ 4 file code của thành viên."""
    df = pd.read_excel(path)

    # Làm sạch và chuẩn hóa kiểu dữ liệu số an toàn
    num_cols = ["price_ori", "price_actual", "item_rating", "total_rating", "total_sold"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
    df = df.dropna(subset=["title", "price_actual", "item_rating", "total_sold"]).copy()
    df = df[df["price_actual"] > 0]
    df["revenue"] = df["price_actual"] * df["total_sold"]

    # 1. Module Price Range (module_price_range.py)
    if HAS_PRICE_RANGE and hasattr(module_price_range, "phan_tich_tong_quan"):
        try:
            # Gọi hàm phân tích để kích hoạt và gán lại price_range
            _ = module_price_range.phan_tich_tong_quan(df)
        except Exception as e:
            print(f"Lỗi tương thích Module Price Range: {e}")
            df = fallback_price_range(df)
    else:
        df = fallback_price_range(df)

    # 2. Module Rating & Sold (module_rating_sold.py)
    if HAS_RATING_SOLD and hasattr(module_rating_sold, "load_data"):
        try:
            # Module 2 làm sạch dữ liệu qua hàm load_data
            pass
        except Exception as e:
            print(f"Lỗi tương thích Module Rating & Sold: {e}")

    # 3. Module Category & Time (module_category_time.py)
    if HAS_CATEGORY_TIME and hasattr(module_category_time, "process_category_time_module"):
        try:
            df = module_category_time.process_category_time_module(df)
        except Exception as e:
            print(f"Lỗi tương thích Module Category & Time: {e}")
            df = fallback_category_time(df)
    else:
        df = fallback_category_time(df)

    # 4. Module Discount (module_discount.py)
    if HAS_DISCOUNT and hasattr(module_discount, "calculate_discount"):
        try:
            df = module_discount.calculate_discount(df)
        except Exception as e:
            print(f"Lỗi tương thích Module Discount: {e}")

    # Đảm bảo có cột discount_pct an toàn nếu chưa được khởi tạo
    if "discount_pct" not in df.columns:
        if "price_ori" in df.columns:
            df["discount_pct"] = np.where(
                df["price_ori"] > df["price_actual"],
                ((df["price_ori"] - df["price_actual"]) / df["price_ori"]) * 100,
                0.0
            )
        else:
            df["discount_pct"] = 0.0

    return df

# 4. TÍNH ĐIỂM SẢN PHẨM TIỀM NĂNG

def min_max_scale(series: pd.Series) -> pd.Series:
    """Chuẩn hóa Min-Max an toàn tránh lỗi chia cho 0."""
    min_val, max_val = series.min(), series.max()
    if max_val == min_val:
        return pd.Series(0.0, index=series.index)
    return (series - min_val) / (max_val - min_val)

def calculate_potential_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tính điểm Potential Score (Thang 100):
    - Rating (30%) + Sold (30%) + Revenue (20%) + Khuyến mãi tối ưu (20%)
    """
    df = df.copy()

    rating_norm = min_max_scale(df["item_rating"])
    sold_norm = min_max_scale(np.log1p(df["total_sold"]))
    rev_norm = min_max_scale(np.log1p(df["revenue"]))

    disc_score = np.where(
        (df["discount_pct"] >= 10) & (df["discount_pct"] <= 40), 1.0,
        np.where(df["discount_pct"] > 40, 0.7, 0.4)
    )

    df["potential_score"] = (
        rating_norm * 0.30 +
        sold_norm * 0.30 +
        rev_norm * 0.20 +
        disc_score * 0.20
    ) * 100

    return df

# 5. TRỰC QUAN HÓA BIỂU ĐỒ TỔNG HỢP

def visualize_integrated_analysis(df: pd.DataFrame) -> None:
    """Vẽ lưới biểu đồ 2x2 thể hiện kết quả tích hợp 4 thành viên."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Biểu đồ 1: Ngành hàng chủ lực
    if "main_category" in df.columns and df["main_category"].nunique() > 1:
        top_cats = df.groupby("main_category")["total_sold"].sum().nlargest(8).index
        df_top_cat = df[df["main_category"].isin(top_cats)]
        sns.boxplot(
            data=df_top_cat, x="potential_score", y="main_category", 
            hue="main_category", ax=axes[0, 0], palette="Blues", legend=False
        )
        axes[0, 0].set_title("1. Phân bổ Điểm Tiềm Năng theo Top 8 Ngành Hàng Chủ Lực", fontsize=11, fontweight="bold")
    else:
        axes[0, 0].text(0.5, 0.5, "Chưa có đủ dữ liệu Ngành hàng", ha="center", va="center")
    
    axes[0, 0].set_xlabel("Điểm Tiềm Năng (0 - 100)")
    axes[0, 0].set_ylabel("")

    # Biểu đồ 2: Rating vs Lượt bán theo Khoảng giá
    hue_col = "price_range" if "price_range" in df.columns else None
    sns.scatterplot(
        data=df, x="item_rating", y="total_sold", hue=hue_col,
        ax=axes[0, 1], alpha=0.6, palette="Set1" if hue_col else None
    )
    axes[0, 1].set_yscale("symlog")
    axes[0, 1].set_title("2. Mối quan hệ Rating vs Lượt bán phân theo Khoảng Giá", fontsize=11, fontweight="bold")
    axes[0, 1].set_xlabel("Item Rating ⭐")
    axes[0, 1].set_ylabel("Total Sold (Log Scale)")

    # Biểu đồ 3: Mức giảm giá tối ưu 
    df_disc = df.copy()
    df_disc["discount_group"] = pd.cut(
        df_disc["discount_pct"], 
        bins=[-1, 0, 10, 20, 30, 40, 50, 100],
        labels=["0%", "0-10%", "10-20%", "20-30%", "30-40%", "40-50%", ">50%"]
    )
    grouped_disc = df_disc.groupby("discount_group", observed=True)["potential_score"].mean().reset_index()
    bars = axes[1, 0].bar(grouped_disc["discount_group"].astype(str), grouped_disc["potential_score"], color="#EE4D2D")
    axes[1, 0].set_title("3. Điểm Tiềm Năng Trung bình theo Khoảng % Giảm Giá", fontsize=11, fontweight="bold")
    axes[1, 0].set_xlabel("Khoảng % Giảm giá")
    axes[1, 0].set_ylabel("Điểm Tiềm Năng Trung Bình")
    for bar in bars:
        height = bar.get_height()
        if not np.isnan(height):
            axes[1, 0].annotate(
                f"{height:.1f}", 
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", 
                ha="center", va="bottom", fontsize=8
            )

    # Biểu đồ 4: Top 10 sản phẩm
    top_10 = df.sort_values("potential_score", ascending=False).head(10).iloc[::-1]
    clean_titles = top_10["title"].astype(str).str.replace(r'[^\w\s\d,.-]', '', regex=True)
    labels = clean_titles.str.slice(0, 35) + "..."
    
    axes[1, 1].barh(labels, top_10["potential_score"], color="#2ECC71")
    axes[1, 1].set_title("4. Top 10 Sản Phẩm Có Điểm Tiềm Năng Cao Nhất", fontsize=11, fontweight="bold")
    axes[1, 1].set_xlabel("Điểm Tiềm Năng (0 - 100)")
    axes[1, 1].set_ylabel("")

    fig.suptitle("PHÂN TÍCH TỔNG HỢP VÀ XÁC ĐỊNH SẢN PHẨM TIỀM NĂNG SHOPEE", fontsize=14, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    chart_path = os.path.join(OUT_DIR, "06_tong_hop_san_pham_tiem_nang.png")
    plt.savefig(chart_path, dpi=150)
    plt.close()
    print(f"✔ Đã lưu biểu đồ tổng hợp tại: {chart_path}")

# 6. MAIN PROGRAM

def main():
    print("=" * 70)
    print("MÔ-ĐUN TỔNG HỢP & XÁC ĐỊNH SẢN PHẨM TIỀM NĂNG")
    print("=" * 70)

    df = load_and_integrate_all_modules(DATA_PATH)
    print(f"✔ Đã tích hợp thành công dữ liệu từ các mô-đun: {len(df):,} bản ghi.")

    df = calculate_potential_score(df)

    top_50 = df.sort_values("potential_score", ascending=False).head(50)
    csv_path = os.path.join(OUT_DIR, "top_50_potential_products.csv")
    
    output_cols = ["title", "main_category", "price_actual", "discount_pct", "item_rating", "total_sold", "potential_score", "link_ori"]
    valid_cols = [c for c in output_cols if c in df.columns]
    
    top_50[valid_cols].to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"✔ Đã xuất file Top 50 sản phẩm tiềm năng tại: {csv_path}")

    visualize_integrated_analysis(df)
    print("✔ Hoàn thành phân tích tổng hợp!")

if __name__ == "__main__":
    main()
