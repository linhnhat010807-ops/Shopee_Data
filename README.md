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
- **Top 10 danh mục nhiều sản phẩm nhất:**
  ![Nhiều sản phẩm](Screenshot 2026-09-13 134001.png)
- **Số lượng sản phẩm theo giá:**
  ![Khoảng giá](Screenshot 2026-09-13 134020.png)
- **Phân bố giá bán thực tế của sản phẩm:**
  ![Giá thực tế](Screenshot 2026-09-13 134038.png)
- **Top 10 danh mục có giá trung bình cao:**
  ![Trung bình giá bán cao](Screenshot 2026-09-13 134049.png)
---

### 2. Rating & Lượt bán (`module_rating_sold.py`)
- **Phân phối giá:**
  ![Phân phối giá](01_distributions.png)
- **Top 10 sản phẩm được đánh giá nhiều nhất:**
  ![Đánh giá sản phẩm](02_top_rated_products.png)
- **Top 15 sản phẩm bán chạy nhất:**
  ![Sản phẩm bán chạy](03_top_selling_products.png)
- **Lượt bán và đánh giá:**
  ![Đánh giá sản phẩm](04_rating_vs_sold.png)

---

### 3. Danh mục chính & Thời gian (`module_category_time.py`)
- **Top 10 Danh mục danh mục:**
  ![Top 10 Danh mục](01_top_10_danh_muc.png)
- **Tỷ trọng Top 10 sản phẩm:**
  ![Tỷ trọng Top 10 Danh mục](02_top_10_san_pham.png)
- **Xu hướng lượt bán:**
  ![Xu hướng](03_xu_huong_luong_ban.png)
- **Tỷ trọng:**
  ![Tỷ trọng Top 10 Danh mục](04_ty_trong_top_10_danh_muc.png)
  
---

### 4. Mức giảm giá (%) & Ưu đãi (`module_discount.py`)
- **Ma trận tương quan Giảm giá:**
  ![Ma trận tương quan Mức giảm giá](bieu_do_ma_tran_tuong_quan.png)
- **Biểu đồ tổng quan Mức giảm giá & Ưu đãi:**
  ![Biểu đồ Tổng quan Giá Khuyến mãi](bieu_do_tong_quan_gia_khuyenmai.png)

---

### 5. Tổng hợp & Đánh giá Tiềm năng (`module_potential_analysis.py`)
- **Tổng hợp đánh giá sản phẩm tiềm năng:**
  ![Tổng hợp sản phẩm tiềm năng](06_tong_hop_san_pham_tiem_nang.png)
- **Ma trận tương quan tổng thể:**
  ![Correlation Heatmap](05_correlation_heatmap.png)
