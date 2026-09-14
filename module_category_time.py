# ==============================
# 1. IMPORT THƯ VIỆN
# ==============================

import matplotlib.pyplot as plt
import pandas as pd


# ==============================
# 2. HÀM XỬ LÝ CHÍNH (GỌI TỪ FILE TỔNG HỢP)
# ==============================

def process_category_time_module(df):
    df = df.copy()

    # --- 2.1 XỬ LÝ DỮ LIỆU ---
    df["total_sold"] = pd.to_numeric(
        df["total_sold"],
        errors="coerce"
    ).fillna(0)

    df["w_date"] = pd.to_datetime(
        df["w_date"],
        errors="coerce"
    )

    def get_main_category(value):
        if pd.isna(value):
            return "Không xác định"
        value = str(value)
        parts = value.split("|")
        if len(parts) > 1:
            category = parts[1].strip()
            if category != "":
                return category
        return value.strip()

    df["main_category"] = df["item_category_detail"].apply(get_main_category)

    # --- 2.2 BIỂU ĐỒ 1: TOP 10 DANH MỤC ---
    category_sales = (
        df.groupby("main_category")["total_sold"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    chart1 = category_sales.sort_values(ascending=True)

    plt.figure(figsize=(12, 7))
    plt.barh(chart1.index, chart1.values)
    plt.title("Top 10 danh mục có lượng bán cao nhất", fontsize=16, fontweight="bold")
    plt.xlabel("Tổng số lượng bán", fontsize=12)
    plt.ylabel("Danh mục", fontsize=12)
    plt.tight_layout()
    plt.savefig("01_top_10_danh_muc.png", dpi=300, bbox_inches="tight")
    plt.close()

    # --- 2.3 BIỂU ĐỒ 2: TOP 10 SẢN PHẨM ---
    product_sales = (
        df.groupby("title")["total_sold"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    chart2 = product_sales.reset_index()
    chart2.columns = ["title", "total_sold"]

    def shorten_product_name(name):
        name = str(name)
        if "|" in name:
            name = name.split("|")[0]
        name = name.strip()
        if len(name) > 55:
            name = name[:55] + "..."
        return name

    chart2["short_title"] = chart2["title"].apply(shorten_product_name)
    chart2 = chart2.sort_values(by="total_sold", ascending=True)

    plt.figure(figsize=(13, 7))
    plt.barh(chart2["short_title"], chart2["total_sold"])
    plt.title("Top 10 sản phẩm bán chạy nhất", fontsize=16, fontweight="bold")
    plt.xlabel("Tổng số lượng bán", fontsize=12)
    plt.ylabel("Sản phẩm", fontsize=12)
    plt.tight_layout()
    plt.savefig("02_top_10_san_pham.png", dpi=300, bbox_inches="tight")
    plt.close()

    # --- 2.4 BIỂU ĐỒ 3: XU HƯỚNG THEO THỜI GIAN ---
    daily_sales = (
        df.dropna(subset=["w_date"])
        .groupby("w_date")["total_sold"]
        .sum()
        .sort_index()
    )

    plt.figure(figsize=(12, 6))
    plt.plot(daily_sales.index, daily_sales.values, marker="o")
    plt.title("Xu hướng lượng bán theo thời gian", fontsize=16, fontweight="bold")
    plt.xlabel("Ngày", fontsize=12)
    plt.ylabel("Tổng số lượng bán", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("03_xu_huong_luong_ban.png", dpi=300, bbox_inches="tight")
    plt.close()

    # --- 2.5 BIỂU ĐỒ 4: TỶ TRỌNG TOP 10 DANH MỤC ---
    top_10_categories = (
        df.groupby("main_category")["total_sold"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 8))
    plt.pie(
        top_10_categories.values,
        labels=top_10_categories.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Tỷ trọng lượng bán của Top 10 danh mục", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig("04_ty_trong_top_10_danh_muc.png", dpi=300, bbox_inches="tight")
    plt.close()

    # --- 2.6 TRẢ VỀ DỮ LIỆU ĐÃ XỬ LÝ ---
    return df
