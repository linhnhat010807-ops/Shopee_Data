Đề tài tập trung phân tích xu hướng mua sắm, phân khúc giá, hành vi khách hàng và nhà bán hàng, đồng thời trực quan hóa dữ liệu bằng biểu đồ và xây dựng giao diện tương tác với Streamlit.
# 📊 BÁO CÁO PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU SHOPEE

Dự án phân tích dữ liệu bán hàng Shopee: xử lý dữ liệu, phân tích danh mục, phân khúc giá, khuyến mãi, đánh giá sản phẩm và tiềm năng phát triển.

---

## 📁 1. Dữ liệu & Code Xử lý
- **Script làm sạch dữ liệu:** `data_clean.py`
- **File dữ liệu đã sạch:** `shopee_data_clean.xlsx`

## 🛠️ 2. Các Module Phân Tích & Biểu Đồ Trực Quan

### Module 1: Phân tích Danh mục & Thời gian (`module_category_time.py`)
- **Top 10 Danh mục:**
  ![Top 10 Danh mục](01_top_10_danh_muc.png)
- **Tỷ trọng Top 10 Danh mục:**
  ![Tỷ trọng Top 10 Danh mục](04_ty_trong_top_10_danh_muc.png)

---

### Module 2: Phân tích Phân khúc Giá (`module_price_range.py`)
- **Phân phối Phân khúc giá:**
  ![Distributions](01_distributions.png)
- **Top 10 Sản phẩm theo giá:**
  ![Top 10 Sản phẩm](02_top_10_san_pham.png)

---

### Module 3: Phân tích Giá & Khuyến mãi (`module_discount.py`)
- **Tổng quan Giá & Khuyến mãi:**
  ![Biểu đồ Tổng quan Giá Khuyến mãi](bieu_do_tong_quan_gia_khuyenmai.png)
- **Ma trận tương quan Khuyến mãi:**
  ![Ma trận tương quan Khuyến mãi](bieu_do_ma_tran_tuong_quan.png)

---

### Module 4: Phân tích Đánh giá & Lượng bán (`module_rating_sold.py`)
- **Sản phẩm bán chạy nhất:**
  ![Top Selling Products](03_top_selling_products.png)
- **Sản phẩm đánh giá cao nhất:**
  ![Top Rated Products](02_top_rated_products.png)
- **Mối quan hệ Đánh giá vs Lượng bán:**
  ![Rating vs Sold](04_rating_vs_sold.png)
- **Xu hướng Lượng bán:**
  ![Xu hướng Lượng bán](03_xu_huong_luong_ban.png)

---

### Module 5: Phân tích Tiềm năng Sản phẩm (`module_potemial_analysis.py`)
- **Tổng hợp Sản phẩm Tiềm năng:**
  ![Tổng hợp sản phẩm tiềm năng](06_tong_hop_san_pham_tiem_na.png)
- **Ma trận Tương quan Tổng thể:**
  ![Correlation Heatmap](05_correlation_heatmap.png)

---

## 📸 3. Hình ảnh Giao diện & Kết quả Thực thi
![Giao diện 1](Screenshot%202026-09-13%20134001.png)
![Giao diện 2](Screenshot%202026-09-13%20134020.png)
![Giao diện 3](Screenshot%202026-09-13%20134038.png)
![Giao diện 4](Screenshot%202026-09-13%20134049.png)
