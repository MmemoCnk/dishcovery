import streamlit as st

# กำหนดการตั้งค่าของหน้า
st.set_page_config(
    page_title="DISHCOVERY", 
    page_icon="🍜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ซ่อน branding ของ Streamlit และใช้ CSS เพื่อจัด layout ให้เหมือนภาพตัวอย่าง
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ลบ padding และ margin ที่ไม่จำเป็น */
    .block-container {
        padding-top: 0;
        padding-bottom: 0;
        padding-left: 0;
        padding-right: 0;
    }
    
    .appview-container {
        background-color: #F8F9FA;
    }
    
    /* ส่วนหัวของแอพ */
    .top-header {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: white;
    }
    
    .app-title {
        font-size: 2rem;
        font-weight: bold;
        flex: 1;
        color: #2D3748;
    }
    
    .welcome-banner {
        background-color: #E17C39;
        color: white;
        padding: 1rem;
        margin: 0 1rem;
        border-radius: 0.3rem;
        font-size: 1.5rem;
        font-weight: bold;
        flex: 3;
        text-align: center;
    }
    
    .cart-icon {
        font-size: 1.8rem;
        flex: 1;
        text-align: right;
    }
    
    /* ส่วนเนื้อหาหลัก */
    .main-content {
        display: flex;
        padding: 0 1rem;
    }
    
    .left-panel {
        width: 25%;
        margin-right: 1rem;
    }
    
    .right-panel {
        width: 75%;
    }
    
    /* การ์ด */
    .card {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .card-header {
        background-color: #E5E7EB;
        margin: -1rem -1rem 1rem -1rem;
        padding: 0.7rem;
        border-top-left-radius: 0.5rem;
        border-top-right-radius: 0.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        text-align: center;
    }
    
    /* ส่วนเมนู */
    .main-menu-header {
        background-color: #E5E7EB;
        padding: 1rem;
        border-radius: 0.5rem;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    /* ส่วน input */
    .input-container {
        margin-bottom: 0.8rem;
    }
    
    .input-field {
        width: 100%;
        padding: 0.7rem;
        border: 1px solid #E2E8F0;
        border-radius: 0.3rem;
    }
    
    .button {
        background-color: #2D3748;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.3rem;
        cursor: pointer;
    }
    
    /* ส่วนแสดงรายการอาหาร */
    .tab-container {
        display: flex;
        gap: 0.3rem;
        margin-bottom: 1rem;
    }
    
    .tab {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        cursor: pointer;
        text-align: center;
        flex: 1;
    }
    
    .tab.active {
        background-color: #F0F4F8;
        border-bottom: 2px solid #4A5568;
    }
    
    .food-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        background-color: white;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .food-image {
        width: 80px;
        height: 80px;
        object-fit: cover;
        border-radius: 0.3rem;
        margin-right: 1rem;
    }
    
    .food-name {
        flex: 1;
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    .counter {
        display: flex;
        align-items: center;
    }
    
    .counter-button {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 1px solid #E2E8F0;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    
    .counter-value {
        margin: 0 0.5rem;
        width: 30px;
        text-align: center;
    }
    
    /* รายการแนะนำ */
    .recommendation-item {
        display: flex;
        justify-content: space-between;
        background-color: #F8FAFC;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-bottom: 0.3rem;
    }

    /* ปรับแต่ง Streamlit Elements */
    button[kind="primary"] {
        background-color: #2D3748;
        color: white;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0 !important;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
</style>

<div class="top-header">
    <div class="app-title">DISHCOVERY</div>
    <div class="welcome-banner">Welcome</div>
    <div class="cart-icon">🛒</div>
</div>

<div class="main-content">
    <div class="left-panel">
        <div class="card">
            <h3>Please Input Customer ID</h3>
            <div class="input-container">
                <input type="text" class="input-field" placeholder="Member ID">
            </div>
            <div class="input-container">
                <input type="text" class="input-field" placeholder="Tel number">
            </div>
            <button class="button">Enter</button>
            
            <h3 style="margin-top: 1.5rem;">Customer Information</h3>
            <div class="input-container">
                <input type="text" class="input-field" placeholder="Name" disabled>
            </div>
            <div class="input-container">
                <input type="text" class="input-field" placeholder="Surname" disabled>
            </div>
            <div>Date & Time: Sunday, March 2, 2025, 12:00</div>
        </div>
        
        <div class="card">
            <div class="card-header">Favorite Dishes</div>
            <div style="color: #A0AEC0;">No favorite dishes available</div>
        </div>
        
        <div class="card">
            <div class="card-header">Recommendation</div>
            <div class="recommendation-item">
                <span>⚡ Omelette (new)</span>
                <span>100</span>
            </div>
            <div class="recommendation-item">
                <span>Fries Pork with Garlic</span>
                <span>99</span>
            </div>
            <div class="recommendation-item">
                <span>Som Tam</span>
                <span>80</span>
            </div>
            <div class="recommendation-item">
                <span>Satay</span>
                <span>30</span>
            </div>
            <div class="recommendation-item">
                <span>test1</span>
                <span>30</span>
            </div>
            <div class="recommendation-item">
                <span>test2</span>
                <span>30</span>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">Allergic Food</div>
        </div>
    </div>
    
    <div class="right-panel">
        <div class="main-menu-header">Main Menu</div>
        
        <div style="position: relative; margin-bottom: 1rem;">
            <input type="text" placeholder="🔍 Search" class="input-field" style="padding-left: 2rem;">
        </div>
        
        <div class="tab-container">
            <div class="tab active">⚡ All</div>
            <div class="tab">⚡ Main Dishes</div>
            <div class="tab">⚡ Soup</div>
            <div class="tab">⚡ Appetizers</div>
            <div class="tab">⚡ Desserts</div>
            <div class="tab">⚡ Drinks</div>
        </div>
        
        <div class="food-item">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Tom_yam_kung_maenam.jpg/220px-Tom_yam_kung_maenam.jpg" class="food-image">
            <div class="food-name">Tom Yum Kung</div>
            <div class="counter">
                <div class="counter-button">-</div>
                <div class="counter-value">0</div>
                <div class="counter-button">+</div>
            </div>
        </div>
        
        <div class="food-item">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Mee_Pad_Thai.jpg/250px-Mee_Pad_Thai.jpg" class="food-image">
            <div class="food-name">Pad Thai</div>
            <div class="counter">
                <div class="counter-button">-</div>
                <div class="counter-value">0</div>
                <div class="counter-button">+</div>
            </div>
        </div>
        
        <div class="food-item">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/White_rice_cooked.jpg/235px-White_rice_cooked.jpg" class="food-image">
            <div class="food-name">Rice</div>
            <div class="counter">
                <div class="counter-button">-</div>
                <div class="counter-value">0</div>
                <div class="counter-button">+</div>
            </div>
        </div>
        
        <div class="food-item">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Evian_bottle.JPG/220px-Evian_bottle.JPG" class="food-image">
            <div class="food-name">Fresh water</div>
            <div class="counter">
                <div class="counter-button">-</div>
                <div class="counter-value">0</div>
                <div class="counter-button">+</div>
            </div>
        </div>
        
        <div class="food-item">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Phat_kaphrao.jpg/250px-Phat_kaphrao.jpg" class="food-image">
            <div class="food-name">Stir fried Thai basil</div>
            <div class="counter">
                <div class="counter-button">-</div>
                <div class="counter-value">0</div>
                <div class="counter-button">+</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ข้อมูลเมนูอาหาร (ไม่แสดงผลในหน้าเว็บ แต่เอาไว้ใช้ในโค้ดเบื้องหลัง)
menu_items = {
    "Main Dishes": [
        {"name": "Tom Yum Kung", "price": 120, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Tom_yam_kung_maenam.jpg/220px-Tom_yam_kung_maenam.jpg"},
        {"name": "Pad Thai", "price": 100, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Mee_Pad_Thai.jpg/250px-Mee_Pad_Thai.jpg"},
        {"name": "Stir fried Thai basil", "price": 90, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Phat_kaphrao.jpg/250px-Phat_kaphrao.jpg"},
        {"name": "Rice", "price": 30, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/White_rice_cooked.jpg/235px-White_rice_cooked.jpg"}
    ],
    "Soup": [
        {"name": "Chicken Soup", "price": 80, "image": ""},
        {"name": "Vegetable Soup", "price": 70, "image": ""}
    ],
    "Appetizers": [],
    "Desserts": [
        {"name": "Mango Sticky Rice", "price": 90, "image": ""},
        {"name": "Coconut Ice Cream", "price": 60, "image": ""}
    ],
    "Drinks": [
        {"name": "Fresh water", "price": 20, "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Evian_bottle.JPG/220px-Evian_bottle.JPG"},
        {"name": "Thai Milk Tea", "price": 50, "image": ""}
    ]
}

# สร้าง session_state เพื่อเก็บข้อมูลตะกร้า
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# สร้าง placeholder สำหรับ JavaScript (จำเป็นต้องใช้ JavaScript เพื่อให้ UI ทำงานได้ตามที่ต้องการ)
st.markdown("""
<script>
// รอให้หน้าเว็บโหลดเสร็จก่อน
document.addEventListener('DOMContentLoaded', function() {
    // เพิ่ม event listener ให้กับปุ่ม tab
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // ลบ class active จากทุก tab
            tabs.forEach(t => t.classList.remove('active'));
            // เพิ่ม class active ให้กับ tab ที่คลิก
            this.classList.add('active');
        });
    });
    
    // เพิ่ม event listener ให้กับปุ่ม + และ -
    const increaseButtons = document.querySelectorAll('.counter-button:nth-child(3)');
    const decreaseButtons = document.querySelectorAll('.counter-button:nth-child(1)');
    
    increaseButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            const valueElement = this.previousElementSibling;
            let value = parseInt(valueElement.textContent);
            valueElement.textContent = value + 1;
        });
    });
    
    decreaseButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            const valueElement = this.nextElementSibling;
            let value = parseInt(valueElement.textContent);
            if (value > 0) {
                valueElement.textContent = value - 1;
            }
        });
    });
});
</script>
""", unsafe_allow_html=True)

# นี่เป็นส่วนที่จำเป็นสำหรับ Streamlit เพื่อแสดงผลแอพบน server
# แต่ไม่มีส่วนของ UI เพราะเราสร้าง UI ด้วย HTML/CSS แทน
# จึงซ่อนไว้ด้านล่างและไม่แสดงผล

# คำเตือน: โค้ดนี้ใช้ pure HTML/CSS เพื่อให้มี layout ที่ต้องการ
# แต่ฟังก์ชันการทำงาน (เช่น การเพิ่ม/ลดรายการในตะกร้า) จะไม่ทำงาน
# เพราะ JavaScript ไม่สามารถสื่อสารกับ Streamlit ได้โดยตรง
# หากต้องการให้ฟังก์ชันการทำงานครบถ้วน ต้องใช้ Streamlit widgets แทน HTML
