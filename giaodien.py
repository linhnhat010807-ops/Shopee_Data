import streamlit as st
import pandas as pd

# 1. CẤU HÌNH TRANG

st.set_page_config(
    page_title="Shopee Analytics",
    page_icon="🛒",
    layout="wide"
)

# 2. CSS GIAO DIỆN

st.markdown("""
<style>

    /* Nền chính */
    .stApp {
        background-color: #f7f8fa;
    }

    /* Tiêu đề */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #ee4d2d;
        margin-bottom: 0;
    }

    .sub-title {
        color: #666666;
        font-size: 17px;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    /* Card thống kê */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #eeeeee;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }

    .stat-title {
        color: #777777;
        font-size: 15px;
    }

    .stat-value {
        color: #ee4d2d;
        font-size: 30px;
        font-weight: 700;
    }

    /* Tiêu đề section */
    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #333333;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
    }

</style>
""", unsafe_allow_html=True)

# 3. HÀM TẠO BỘ LỌC
def tao_bo_loc_sidebar(df):

    st.sidebar.markdown(
        "## 🔎 Bộ lọc sản phẩm"
    )

    st.sidebar.markdown(
        "Tìm kiếm và lọc sản phẩm Shopee"
    )

    st.sidebar.divider()

    # Tìm kiếm sản phẩmư

    tu_khoa = st.sidebar.text_input(
        "Tên sản phẩm",
        placeholder="Nhập tên sản phẩm..."
    )

    # Khoảng giá

    gia_min = int(df["price_actual"].min())
    gia_max = int(df["price_actual"].max())

    khoang_gia = st.sidebar.slider(
        "💰 Khoảng giá",
        min_value=gia_min,
        max_value=gia_max,
        value=(gia_min, gia_max),
        step=1000,
        format="%d"
    )

    # Rating

    rating_min = st.sidebar.slider(
        "⭐ Số sao tối thiểu",
        min_value=0.0,
        max_value=5.0,
        value=3.0,
        step=0.5
    )

    # Lọc dữ liệu

    df_loc = df.copy()

    if tu_khoa:

        df_loc = df_loc[
            df_loc["title"]
            .astype(str)
            .str.contains(
                tu_khoa,
                case=False,
                na=False
            )
        ]

    df_loc = df_loc[
        (df_loc["price_actual"] >= khoang_gia[0]) &
        (df_loc["price_actual"] <= khoang_gia[1])
    ]

    df_loc = df_loc[
        df_loc["item_rating"] >= rating_min
    ]

    return df_loc

# 4. MAIN

def main():

    # Đọc dữ liệu
    df = pd.read_excel(
        "shopee_data_clean.xlsx"
    )

    # Chuyển dữ liệu sang số

    df["price_actual"] = pd.to_numeric(
        df["price_actual"],
        errors="coerce"
    )

    df["item_rating"] = pd.to_numeric(
        df["item_rating"],
        errors="coerce"
    )

    df["total_sold"] = pd.to_numeric(
        df["total_sold"],
        errors="coerce"
    ).fillna(0)

    df["total_rating"] = pd.to_numeric(
        df["total_rating"],
        errors="coerce"
    ).fillna(0)

    df = df.dropna(
        subset=[
            "title",
            "price_actual",
            "item_rating"
        ]
    )

    # HEADER
    st.markdown(
        '<p class="main-title">🛒 Shopee Analytics</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-title">'
        'Phân tích và tìm kiếm sản phẩm trên Shopee'
        '</p>',
        unsafe_allow_html=True
    )

    # BỘ LỌC

    df_loc = tao_bo_loc_sidebar(df)

    # CARDS THỐNG KÊ
    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">
                    📦 Tổng sản phẩm
                </div>
                <div class="stat-value">
                    {len(df):,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">
                    🔍 Kết quả lọc
                </div>
                <div class="stat-value">
                    {len(df_loc):,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">
                    ⭐ Rating trung bình
                </div>
                <div class="stat-value">
                    {df_loc["item_rating"].mean():.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">
                    🛍️ Tổng lượt bán
                </div>
                <div class="stat-value">
                    {df_loc["total_sold"].sum():,.0f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    # KẾT QUẢ
    st.markdown(
        '<div class="section-title">'
        '🛍️ Kết quả sản phẩm'
        '</div>',
        unsafe_allow_html=True
    )
    # Chọn các cột cần hiển thị
    cot_hien_thi = [
        "title",
        "price_actual",
        "item_rating",
        "total_rating",
        "total_sold"
    ]
    bang = df_loc[cot_hien_thi].copy()
    bang.columns = [
        "Tên sản phẩm",
        "Giá bán",
        "Đánh giá",
        "Số lượt đánh giá",
        "Đã bán"
    ]
    # Định dạng giá
    bang["Giá bán"] = bang["Giá bán"].apply(
        lambda x: f"{x:,.0f} ₫"
    )
    # Hiển thị bảng
    st.dataframe(
        bang,
        use_container_width=True,
        height=500,
        hide_index=True
    )
# 5. CHẠY CHƯƠNG TRÌNH
if __name__ == "__main__":
    main()