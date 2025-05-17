# app.py - ไฟล์หลักของ Streamlit App

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

# ในการพัฒนา (Development mode) - ใช้ React dev server
# dishcovery = components.declare_component("dishcovery", url="http://localhost:3000")

# ในการ production - ใช้ built React component
# หาไดเรกทอรีของไฟล์นี้
current_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(current_dir, "frontend", "build")

# ประกาศ Custom Component
dishcovery = components.declare_component("dishcovery", path=build_dir)

# เรียกใช้ Component
component_value = dishcovery(
    theme="light",  # ส่ง props ไปยัง React component
)

# แสดงข้อมูลที่ได้รับกลับมาจาก React component (ถ้ามี)
if component_value:
    # แยกส่วนด้านล่างออกมาเพื่อการจัดการและบันทึกข้อมูล
    with st.expander("Order Details", expanded=False):
        st.write("### Cart Summary")
        st.write(f"Total Items: {component_value.get('totalItems', 0)}")
        st.write(f"Total Price: ฿{component_value.get('totalPrice', 0)}")
        
        if "cart" in component_value and component_value["cart"]:
            st.write("### Order Items")
            for name, item in component_value["cart"].items():
                st.write(f"**{name}** x {item['quantity']} - ฿{item['price'] * item['quantity']}")
                if item.get('remark'):
                    st.write(f"*Remark: {item['remark']}*")
        else:
            st.write("No items in cart")