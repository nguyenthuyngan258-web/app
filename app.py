import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Thiết lập giao diện tối (Dark Mode)
st.set_page_config(page_title="Credit Vision Pro", layout="wide")

st.markdown("""
    <style>
    .stApp {background: #0e1117; color: #ffffff;}
    .css-1r6slp0 {background: #1e1e1e;}
    .metric-card {background: #262730; padding: 20px; border-radius: 15px; border: 1px solid #444;}
    </style>
""", unsafe_allow_html=True)

st.title("🌌 Credit Vision Pro: Credit Simulator")

# Bố cục 3 cột cho Input
col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    so_tien = st.slider("Số tiền vay (tỷ VNĐ)", 0.1, 10.0, 1.0)
    thu_nhap = st.number_input("Thu nhập hàng tháng (triệu)", 10, 500, 50)
with col_input2:
    thoi_han = st.select_slider("Kỳ hạn (tháng)", options=[12, 24, 36, 60, 120, 240, 360])
    lai_suat = st.number_input("Lãi suất (%/năm)", 5.0, 20.0, 9.5)
with col_input3:
    tsdb = st.number_input("Giá trị TSĐB (tỷ)", 0.5, 20.0, 2.0)
    cic = st.radio("Điểm CIC", ["Tốt", "Trung bình", "Xấu"], horizontal=True)

# Tính toán logic
tra_gop = (so_tien * 1000 * (lai_suat/100/12)) # Công thức đơn giản hóa để demo
dti = (tra_gop / thu_nhap) * 100

st.divider()

# Bố cục "WOW": Biểu đồ + Kết quả
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("📊 Phân tích kịch bản")
    # Biểu đồ mô phỏng dòng tiền
    df = {'Kịch bản': ['Lãi suất hiện tại', 'Lãi suất +3% (Rủi ro)'], 
          'Số tiền trả': [tra_gop, tra_gop * 1.2]}
    fig = px.bar(df, x='Kịch bản', y='Số tiền trả', color='Kịch bản', 
                 color_discrete_sequence=['#00c853', '#ff5252'])
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("💡 Chỉ số sức khỏe hồ sơ")
    # Sử dụng thẻ Metric tùy biến
    m1, m2 = st.columns(2)
    m1.metric("DTI Ratio", f"{dti:.1f}%", delta="-5%" if dti < 40 else "Cao", delta_color="inverse")
    m2.metric("Điểm tín dụng", "A+" if cic == "Tốt" else "C")
    
    # Lời khuyên cá nhân hóa
    if dti > 50:
        st.warning("⚠️ Cảnh báo: Tỷ lệ nợ quá cao. Hãy cân nhắc kéo dài kỳ hạn vay.")
    else:
        st.success("✅ Hồ sơ trong vùng an toàn tài chính.")

# Tính năng sáng tạo: "Export PDF Report" (Giả lập)
if st.button("📥 Xuất báo cáo thẩm định chuyên sâu (PDF)"):
    st.balloons()
    st.info("Báo cáo đang được tạo dưới nền... Đã gửi về email của bạn!")
