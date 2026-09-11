# Phân tích hành vi khách hàng - Shopee

Phân tích `item_rating`, `total_rating`, `total_sold` từ dữ liệu sản phẩm Shopee, tìm top sản phẩm được đánh giá nhiều nhất, top sản phẩm bán chạy nhất, và mối quan hệ giữa rating và lượt bán. Kết quả được trực quan hóa thành biểu đồ.

## Cấu trúc thư mục

```
shopee-analysis/
├── analysis.py          # Script phân tích chính
├── requirements.txt     # Thư viện cần cài
├── data/
│   └── shopee_data_clean.xlsx
└── outputs/              # Biểu đồ và bảng kết quả (được tạo khi chạy script)
```

## Cách chạy

```bash
pip install -r requirements.txt
python analysis.py
```

Kết quả (biểu đồ PNG + bảng CSV) sẽ được lưu vào thư mục `outputs/`.

## Nội dung phân tích

1. **Thống kê mô tả** cho `item_rating`, `total_rating`, `total_sold` (`01_distributions.png`, `basic_stats.csv`)
2. **Top 15 sản phẩm được đánh giá nhiều nhất** theo `total_rating` (`02_top_rated_products.png`, `top_rated_products.csv`)
3. **Top 15 sản phẩm bán chạy nhất** theo `total_sold` (`03_top_selling_products.png`, `top_selling_products.csv`)
4. **Mối quan hệ giữa rating và lượt bán**: hệ số tương quan, scatter plot, và heatmap tương quan (`04_rating_vs_sold.png`, `05_correlation_heatmap.png`, `correlation_summary.txt`)

## ⚠️ Lưu ý quan trọng về dữ liệu

Trong bộ dữ liệu này, hai cột **`total_rating` và `total_sold` có giá trị giống hệt nhau ở toàn bộ 19,174 dòng** (tương quan = 1.0000). Điều này nhiều khả năng là lỗi từ bước crawl/clean dữ liệu gốc (một cột bị ghi đè giá trị của cột kia), chứ không phải một insight thực sự — vì vậy `item_rating` là chỉ số tin cậy duy nhất để đánh giá thực sự mối quan hệ "rating cao thì bán chạy hơn không?" trong bộ dữ liệu hiện tại. Nên kiểm tra lại nguồn dữ liệu gốc trước khi dùng `total_rating`/`total_sold` cho các phân tích sâu hơn.
