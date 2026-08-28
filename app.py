import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ghi Số Nước Thực Địa", page_icon="🚰")
st.title("🚰 Ghi Số Nước Thực Địa")

# 1. Dán đường link CSV đã xuất bản ở Bước 1 vào đây
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQukQgdPNUFzTAGnKS6CgTae4YCngPmHSZ2dfhXgeaQC_XtKPJqAltzzTrvNJ5RThXjjyZBcppFXCsk/pub?output=csv"

@st.cache_data(ttl=60)  # Lưu tạm dữ liệu trong 60 giây để tải cho nhanh
def load_data():
    try:
        # Đọc dữ liệu từ Google Sheets CSV
        df = pd.read_csv(SHEET_CSV_URL)
        return df
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu từ Google Sheets: {e}")
        return None

df = load_data()

if df is not None:
    # 2. Chọn Khách hàng (Hiển thị Mã KH và Tên KH)
    df['Ten_Hien_Thi'] = df['Mã KH'].astype(str) + " - " + df['Tên KH'].astype(str)
    
    selected_user = st.selectbox(
        "🔎 Tìm kiếm/Chọn Khách hàng:",
        options=df['Ten_Hien_Thi']
    )
    
    # Lấy thông tin khách hàng được chọn
    user_info = df[df['Ten_Hien_Thi'] == selected_user].iloc[0]
    
    # 3. Hiển thị thông tin & Chỉ số cũ tự động
    st.info(f"**Địa chỉ:** {user_info.get('Địa Chỉ', 'N/A')}")
    
    # Lấy chỉ số cũ từ file (mặc định là 0 nếu trống)
    chi_so_cu = float(user_info['Chỉ số Cũ']) if pd.notnull(user_info.get('Chỉ số Cũ')) else 0.0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Chỉ số Cũ (Tự động từ Sheet)", value=f"{chi_so_cu:,.0f} m³")
    with col2:
        chi_so_moi = st.number_input(
            "Chỉ số Mới (Nhập thực địa):",
            min_value=float(chi_so_cu),
            value=float(chi_so_cu),
            step=1.0
        )
    
    # 4. Tính toán kết quả
    so_khoan = chi_so_moi - chi_so_cu
    don_gia = 6400  # Đơn giá 6.400đ/m3 theo dữ liệu thực tế
    tong_tien = so_khoan * don_gia

    st.markdown("---")
    st.subheader("📊 Kết quả tính toán")
    
    col_k1, col_k2 = st.columns(2)
    col_k1.metric("Lượng nước tiêu thụ", f"{so_khoan:,.0f} m³")
    col_k2.metric("Tổng tiền thanh toán", f"{tong_tien:,.0f} VNĐ")

    # 5. Nút bấm ghi nhận/xác nhận
    if st.button("✅ Xác nhận ghi số"):
        st.success(f"Đã ghi nhận thành công cho **{user_info['Tên KH']}**: tiêu thụ {so_khoan:,.0f} m³, tiền: {tong_tien:,.0f} VNĐ")
