import streamlit as st
import streamlit.components.v1 as components
import os

# กำหนดการตั้งค่าของหน้า
st.set_page_config(
    page_title="DISHCOVERY",
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ซ่อน branding ของ Streamlit
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-18e3th9 {padding-top: 0;}
.css-1d391kg {padding-top: 0;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# หาไดเรกทอรีของไฟล์นี้
current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, "frontend", "build")

# ตรวจสอบว่ามีโฟลเดอร์ build หรือไม่
if os.path.isdir(build_dir):
    # ถ้ามีโฟลเดอร์ build ให้ใช้ built React component
    dishcovery = components.declare_component("dishcovery", path=build_dir)
    component_value = dishcovery()
else:
    # ถ้าไม่มีโฟลเดอร์ build ให้แสดงข้อความแจ้งเตือน
    st.error("React component not built. Please check the frontend/build directory.")
    component_value = None

# ตัวแปร component_value จะมีค่าเมื่อมีการส่งข้อมูลกลับมาจาก React component
if component_value:
    st.session_state['order_data'] = component_value

# แสดงข้อมูลการสั่งอาหาร (จะแสดงเมื่อมีการส่งข้อมูลกลับมาจาก component)
with st.expander("ดูข้อมูลการสั่งอาหาร", expanded=False):
    if 'order_data' in st.session_state:
        order_data = st.session_state['order_data']
        st.write("### สรุปการสั่งซื้อ")
        st.write(f"จำนวนรายการทั้งหมด: {order_data.get('totalItems', 0)}")
        st.write(f"ราคารวม: ฿{order_data.get('totalPrice', 0)}")
        
        if 'cart' in order_data and order_data['cart']:
            st.write("### รายการอาหารที่สั่ง")
            for name, item in order_data['cart'].items():
                st.write(f"**{name}** x {item['quantity']} - ฿{item['price'] * item['quantity']}")
                if 'remark' in item and item['remark']:
                    st.write(f"*หมายเหตุ: {item['remark']}*")
        else:
            st.write("ไม่มีรายการอาหารในตะกร้า")
    else:
        st.write("ยังไม่มีข้อมูลการสั่งอาหาร กรุณาสั่งอาหารและกดชำระเงิน")