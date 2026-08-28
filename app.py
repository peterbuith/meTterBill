import streamlit as st

st.set_page_config(page_title="Tính Tiền Nước", page_icon="🚰")
st.title("🚰 Ứng dụng Tính Tiền Nước")

# Nhập dữ liệu chỉ số
col1, col2 = st.columns(2)
with col1:
    chi_so_cu = st.number_input("Chỉ số nước cũ (m³):", min_value=0, value=100, step=1)
with col2:
    chi_so_moi = st.number_input("Chỉ số nước mới (m³):", min_value=0, value=115, step=1)

# Xử lý tính toán khi bấm nút
if st.button("Tính tiền nước"):
    if chi_so_moi < chi_so_cu:
        st.error("Lỗi: Chỉ số mới không được nhỏ hơn chỉ số cũ!")
    else:
        so_khoan = chi_so_moi - chi_so_cu
        
        # Bảng giá nước sinh hoạt tham khảo (giá giả định)
        # Bậc 1: 0 - 10 m³ -> 7.500đ/m³
        # Bậc 2: 11 - 20 m³ -> 8.500đ/m³
        # Bậc 3: Trên 20 m³ -> 10.000đ/m³
        
        tien_bac_1 = min(so_khoan, 10) * 7500
        tien_bac_2 = max(0, min(so_khoan - 10, 10)) * 8500
        tien_bac_3 = max(0, so_khoan - 20) * 10000
        
        tong_tien = tien_bac_1 + tien_bac_2 + tien_bac_3
        vat = tong_tien * 0.05  # Thuế VAT 5%
        tong_thanh_toan = tong_tien + vat

        # Hiển thị kết quả
        st.success(f"Tổng lượng nước tiêu thụ: **{so_khoan} m³**")
        
        st.markdown(f"""
        * **Tiền nước gốc:** {tong_tien:,.0f} VNĐ
        * **Thuế VAT (5%):** {vat:,.0f} VNĐ
        ---
        ### **Tổng thanh toán: {tong_thanh_toan:,.0f} VNĐ**
        """)