import streamlit as st


def hien_thi_bang_san_pham(df_da_loc):
    df_hien_thi = df_da_loc.copy()

    if "link_ori" in df_hien_thi.columns:
        df_hien_thi["link_ori"] = (
            df_hien_thi["link_ori"]
            .fillna("")
            .astype(str)
        )

        st.dataframe(
            df_hien_thi,
            column_config={
                "link_ori": st.column_config.LinkColumn(
                    "Link Shopee",
                    display_text="Xem sản phẩm"
                )
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.dataframe(
            df_hien_thi,
            hide_index=True,
            use_container_width=True
        )