Đề tài tập trung phân tích xu hướng mua sắm, phân khúc giá, hành vi khách hàng và nhà bán hàng, đồng thời trực quan hóa dữ liệu bằng biểu đồ và xây dựng giao diện tương tác với Streamlit.
# 📊 BÁO CÁO PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU SHOPEE

Dự án phân tích dữ liệu bán hàng Shopee: xử lý dữ liệu, phân tích phân khúc giá, lượt bán, danh mục, mức giảm giá và đánh giá sản phẩm tiềm năng.

---

## 📁 Dữ liệu & Script Tiền Xử Lý
- **File dữ liệu gốc/đã làm sạch:** `shopee_data_clean.xlsx`
- **Script làm sạch dữ liệu:** `data_clean.py`
- **Script chỉnh sửa dữ liệu:** `edit_data`
- **Script hiển thị dữ liệu dạng bảng:** `hien_thi_bang.py`

---

## 🛠️ Các Module Phân Tích & Biểu Đồ Trực Quan

### 1. Phân khoảng giá & Tổng quan (`module_price_range.py`)
- **Phân phối phân khoảng giá:**
  ![Phân phối giá](01_distributions.png)
- **Top 10 sản phẩm theo giá:**
  ![Top 10 Sản phẩm](02_top_10_san_pham.png)

---

### 2. Rating & Lượt bán (`module_rating_sold.py`)
- **Top sản phẩm bán chạy nhất:**
  ![Top Selling Products](03_top_selling_products.png)
- **Top sản phẩm có lượt đánh giá cao nhất:**
  ![Top Rated Products](02_top_rated_products.png)
- **Mối quan hệ giữa Rating và Lượt bán:**
  ![Rating vs Sold](04_rating_vs_sold.png)
- **Xu hướng lượng bán:**
  ![Xu hướng lượng bán](03_xu_huong_luong_ban.png)

---

### 3. Danh mục chính & Thời gian (`module_category_time.py`)
- **Top 10 Danh mục sản phẩm:**
  ![Top 10 Danh mục](01_top_10_danh_muc.png)
- **Tỷ trọng Top 10 Danh mục:**
  ![Tỷ trọng Top 10 Danh mục](04_ty_trong_top_10_danh_muc.png)

---

### 4. Mức giảm giá (%) & Ưu đãi (`module_discount.py`)
- **Biểu đồ tổng quan Mức giảm giá & Ưu đãi:**
  ![Biểu đồ Tổng quan Giá Khuyến mãi](bieu_do_tong_quan_gia_khuyenmai.png)
- **Ma trận tương quan Giảm giá:**
  ![Ma trận tương quan Mức giảm giá](bieu_do_ma_tran_tuong_quan.png)

---

### 5. Tổng hợp & Đánh giá Tiềm năng (`module_potential_analysis.py`)
- **Tổng hợp đánh giá sản phẩm tiềm năng:**
  ![Tổng hợp sản phẩm tiềm năng](06_tong_hop_san_pham_tiem_na.png)
- **Ma trận tương quan tổng thể:**
  ![Correlation Heatmap](05_correlation_heatmap.png)

---

## 📸 Hình ảnh Giao diện & Screenshot Kết quả
![Screenshot 1](Screenshot%202026-09-13%20134001.png)
![Screenshot 2](Screenshot%202026-09-13%20134020.png)
![Screenshot 3](Screenshot%202026-09-13%20134038.png)
![Screenshot 4](Screenshot%202026-09-13%20134049.png)
