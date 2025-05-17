import streamlit as st
import base64
from PIL import Image
import requests
from io import BytesIO

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
section.main > div:has(~ footer ) {
    padding-top: 0rem;
    padding-bottom: 0rem;
}
.stApp {
    background-color: #f3f4f6;
}
button {
    background-color: transparent;
    border: none;
    outline: none;
}
button:hover {
    background-color: rgba(0,0,0,0.1);
}
.menu-item {
    display: flex;
    align-items: center;
    padding: 10px;
    margin-bottom: 5px;
    background-color: white;
    border-radius: 5px;
}
.menu-image {
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 5px;
    margin-right: 15px;
}
.menu-name {
    flex-grow: 1;
    font-size: 18px;
    font-weight: 500;
}
.menu-counter {
    display: flex;
    align-items: center;
}
.counter-button {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 1px solid #e2e8f0;
    background-color: white;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}
.counter-value {
    width: 30px;
    text-align: center;
    font-size: 16px;
    margin: 0 5px;
}
.card {
    background-color: white;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
.card-header {
    background-color: #e2e8f0;
    margin: -16px -16px 16px -16px;
    padding: 10px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 600;
    font-size: 18px;
    text-align: center;
}
.recommendation-item {
    display: flex;
    justify-content: space-between;
    padding: 8px;
    background-color: #f8fafc;
    border-radius: 4px;
    margin-bottom: 5px;
}
.input-with-icon {
    position: relative;
    margin-bottom: 15px;
}
.input-with-icon input {
    padding-left: 30px;
    width: 100%;
    padding-top: 8px;
    padding-bottom: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
}
.input-icon {
    position: absolute;
    top: 50%;
    left: 10px;
    transform: translateY(-50%);
    color: #aaa;
}
.search-container {
    position: relative;
    margin-bottom: 15px;
}
.search-container input {
    width: 100%;
    padding: 10px 10px 10px 40px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}
.search-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
}
.category-tab {
    padding: 8px 16px;
    background-color: white;
    border: 1px solid #e2e8f0;
    cursor: pointer;
    text-align: center;
    border-radius: 4px;
}
.category-tab.active {
    background-color: #f8fafc;
    border-bottom: 2px solid #4a5568;
}
.top-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}
.welcome-banner {
    background-color: #e67e22; /* Orange */
    color: white;
    padding: 15px;
    border-radius: 5px;
    text-align: center;
    flex-grow: 1;
    margin: 0 20px;
    font-size: 24px;
    font-weight: bold;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# รูปภาพเมนูอาหาร - ใช้ URL สำหรับรูปภาพตัวอย่าง
food_images = {
    "Tom Yum Kung": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Tom_yam_kung_maenam.jpg/220px-Tom_yam_kung_maenam.jpg",
    "Pad Thai": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Mee_Pad_Thai.jpg/250px-Mee_Pad_Thai.jpg",
    "Rice": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/White_rice_cooked.jpg/235px-White_rice_cooked.jpg",
    "Fresh water": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Evian_bottle.JPG/220px-Evian_bottle.JPG",
    "Stir fried Thai basil": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Phat_kaphrao.jpg/250px-Phat_kaphrao.jpg"
}

# ข้อมูลเมนูอาหาร
menu_items = {
    "Main Dishes": [
        {"name": "Tom Yum Kung", "price": 120},
        {"name": "Pad Thai", "price": 100},
        {"name": "Stir fried Thai basil", "price": 90}
    ],
    "Soup": [
        {"name": "Chicken Soup", "price": 80},
        {"name": "Vegetable Soup", "price": 70}
    ],
    "Appetizers": [],
    "Desserts": [
        {"name": "Mango Sticky Rice", "price": 90},
        {"name": "Coconut Ice Cream", "price": 60}
    ],
    "Drinks": [
        {"name": "Fresh water", "price": 20},
        {"name": "Thai Milk Tea", "price": 50}
    ]
}

# เพิ่ม "Rice" ใน Main Dishes
rice_exists = False
for item in menu_items["Main Dishes"]:
    if item["name"] == "Rice":
        rice_exists = True
        break
        
if not rice_exists:
    menu_items["Main Dishes"].append({"name": "Rice", "price": 30})

# ข้อมูลคำแนะนำ
recommendations = [
    {"name": "Omelette (new)", "quantity": 100},
    {"name": "Fries Pork with Garlic", "quantity": 99},
    {"name": "Som Tam", "quantity": 80},
    {"name": "Satay", "quantity": 30},
    {"name": "test1", "quantity": 30},
    {"name": "test2", "quantity": 30}
]

# ข้อมูลผู้ใช้ตัวอย่าง
user_data = {
    "id": "12345",
    "phone": "0891234567",
    "name": "John",
    "surname": "Doe",
    "favorite_dishes": ["Pad Thai", "Tom Yum"],
    "allergic_food": ["Peanuts"]
}

# ตั้งค่าค่าเริ่มต้นใน session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "All"
if 'checkout_success' not in st.session_state:
    st.session_state.checkout_success = False

# ฟังก์ชั่นสำหรับโหลดรูปภาพจาก URL
def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return Image.new('RGB', (100, 100), color = 'grey')

# ฟังก์ชั่นสำหรับสร้างปุ่ม +/-
def create_counter(item_key):
    quantity = st.session_state.cart.get(item_key, {}).get("quantity", 0)
    html = f"""
    <div class="menu-counter">
        <button class="counter-button" onclick="decrementCounter('{item_key}')">-</button>
        <div class="counter-value">{quantity}</div>
        <button class="counter-button" onclick="incrementCounter('{item_key}')">+</button>
    </div>
    """
    return html

# หัวข้อหลัก
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.markdown("<h1 style='font-size: 32px; font-weight: bold;'>DISHCOVERY</h1>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='welcome-banner'>Welcome</div>", unsafe_allow_html=True)
with col3:
    cart_count = sum(item["quantity"] for item in st.session_state.cart.values()) if st.session_state.cart else 0
    st.markdown(f"<div style='text-align: right; font-size: 28px;'>🛒</div>", unsafe_allow_html=True)

# แบ่งหน้าจอเป็น 2 คอลัมน์
left_col, right_col = st.columns([1, 3])

# คอลัมน์ซ้าย - ข้อมูลลูกค้าและคำแนะนำ
with left_col:
    # ข้อมูลลูกค้า
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if not st.session_state.logged_in:
            st.markdown("<h3>Please Input Customer ID</h3>", unsafe_allow_html=True)
            
            st.markdown("<div class='input-with-icon'>", unsafe_allow_html=True)
            st.markdown("<span class='input-icon'>👤</span>", unsafe_allow_html=True)
            member_id = st.text_input("Member ID", key="member_id", label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='input-with-icon'>", unsafe_allow_html=True)
            st.markdown("<span class='input-icon'>📱</span>", unsafe_allow_html=True)
            phone = st.text_input("Tel number", key="phone", label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("Enter", key="login_button"):
                if member_id == user_data["id"] and phone == user_data["phone"]:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user_data
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
        else:
            st.markdown("<h3>Customer Information</h3>", unsafe_allow_html=True)
            
            st.markdown("<div class='input-with-icon'>", unsafe_allow_html=True)
            st.markdown("<span class='input-icon'>👤</span>", unsafe_allow_html=True)
            st.text_input("Name", value=st.session_state.current_user["name"], disabled=True, label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='input-with-icon'>", unsafe_allow_html=True)
            st.markdown("<span class='input-icon'>👤</span>", unsafe_allow_html=True)
            st.text_input("Surname", value=st.session_state.current_user["surname"], disabled=True, label_visibility="collapsed")
            st.markdown("</div>", unsafe_allow_html=True)
            
            import datetime
            current_date = datetime.datetime.now().strftime("Sunday, March 2, 2025, 12:00")
            st.markdown(f"<div>Date & Time : {current_date}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Favorite Dishes
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>Favorite Dishes</div>", unsafe_allow_html=True)
        if st.session_state.logged_in and "favorite_dishes" in st.session_state.current_user:
            for dish in st.session_state.current_user["favorite_dishes"]:
                st.markdown(f"<div style='background-color: #f8fafc; padding: 10px; border-radius: 5px; margin-top: 5px;'>{dish}</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div style="color: #a0aec0;">No favorite dishes available</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Recommendations
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>Recommendation</div>", unsafe_allow_html=True)
        for rec in recommendations:
            st.markdown(f"<div class='recommendation-item'><span>{'⚡ ' if rec['name'] == 'Omelette (new)' else ''}{rec['name']}</span><span>{rec['quantity']}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Allergic Food
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-header'>Allergic Food</div>", unsafe_allow_html=True)
        if st.session_state.logged_in and "allergic_food" in st.session_state.current_user:
            for allergen in st.session_state.current_user["allergic_food"]:
                st.markdown(f"<div style='background-color: #f8fafc; padding: 10px; border-radius: 5px; margin-top: 5px;'>{allergen}</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div style="color: #a0aec0;"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# คอลัมน์ขวา - เมนูอาหาร
with right_col:
    st.markdown("<div style='background-color: #e2e8f0; padding: 15px; border-radius: 5px; margin-bottom: 15px;'><h2 style='margin: 0;'>Main Menu</h2></div>", unsafe_allow_html=True)
    
    # Search Bar
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    st.markdown("<span class='search-icon'>🔍</span>", unsafe_allow_html=True)
    search_query = st.text_input("Search", key="search", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Category Tabs
    categories = ["All"] + list(menu_items.keys())
    cols = st.columns(len(categories))
    selected_tab = st.session_state.active_tab
    
    for i, category in enumerate(categories):
        with cols[i]:
            tab_class = "category-tab active" if selected_tab == category else "category-tab"
            if st.button(f"⚡ {category}", key=f"tab_{category}", use_container_width=True):
                st.session_state.active_tab = category
                selected_tab = category
    
    # Display items based on search or category
    all_items = []
    for category, items in menu_items.items():
        all_items.extend(items)
    
    if search_query:
        display_items = [item for item in all_items if search_query.lower() in item["name"].lower()]
    elif selected_tab == "All":
        display_items = all_items
    else:
        display_items = menu_items.get(selected_tab, [])
    
    # JavaScript for interactive buttons
    st.markdown("""
    <script>
    function incrementCounter(itemName) {
        // Send event to Streamlit
        window.parent.postMessage({
            type: "streamlit:componentEvent",
            action: "increment",
            itemName: itemName
        }, "*");
    }
    
    function decrementCounter(itemName) {
        // Send event to Streamlit
        window.parent.postMessage({
            type: "streamlit:componentEvent",
            action: "decrement",
            itemName: itemName
        }, "*");
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Food Items with Add/Remove buttons
    for item in display_items:
        item_key = item["name"]
        quantity = st.session_state.cart.get(item_key, {}).get("quantity", 0)
        
        cols = st.columns([1, 5, 1])
        
        with cols[0]:
            # Display food image
            if item["name"] in food_images:
                img_url = food_images[item["name"]]
                st.image(img_url, width=80)
            else:
                st.markdown("<div style='width: 80px; height: 80px; background-color: #f3f4f6; display: flex; align-items: center; justify-content: center; border-radius: 5px;'>🍽️</div>", unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"<div style='font-size: 18px; font-weight: 500; padding-top: 20px;'>{item['name']}</div>", unsafe_allow_html=True)
        
        with cols[2]:
            # Counter buttons
            st.markdown("""
            <div style="display: flex; align-items: center; justify-content: center; padding-top: 20px;">
                <button onClick="() => {}" style="width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd; background-color: white;">-</button>
                <span style="margin: 0 10px; width: 20px; text-align: center;">0</span>
                <button onClick="() => {}" style="width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid #ddd; background-color: white;">+</button>
            </div>
            """, unsafe_allow_html=True)
            
            minus, count, plus = st.columns([1, 1, 1])
            
            with minus:
                if st.button("-", key=f"minus_{item_key}", help=f"Reduce {item_key} quantity"):
                    if item_key in st.session_state.cart and st.session_state.cart[item_key]["quantity"] > 0:
                        st.session_state.cart[item_key]["quantity"] -= 1
                        if st.session_state.cart[item_key]["quantity"] == 0:
                            del st.session_state.cart[item_key]
                        st.experimental_rerun()
            
            with count:
                st.text(f"{quantity}")
            
            with plus:
                if st.button("+", key=f"plus_{item_key}", help=f"Add {item_key} to cart"):
                    if item_key in st.session_state.cart:
                        st.session_state.cart[item_key]["quantity"] += 1
                    else:
                        st.session_state.cart[item_key] = {
                            "name": item["name"],
                            "price": item["price"],
                            "quantity": 1,
                            "remark": ""
                        }
                    st.experimental_rerun()

# ตะกร้า
if len(st.session_state.cart) > 0:
    total_items = sum(item["quantity"] for item in st.session_state.cart.values())
    total_price = sum(item["price"] * item["quantity"] for item in st.session_state.cart.values())
    
    st.sidebar.markdown("# Shopping Cart")
    
    for name, item in st.session_state.cart.items():
        st.sidebar.markdown(f"**{name}** x {item['quantity']} - ฿{item['price'] * item['quantity']}")
        if "remark" in item and item["remark"]:
            st.sidebar.markdown(f"*Remark: {item['remark']}*")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### Total: ฿{total_price}")
    
    if st.sidebar.button("Checkout"):
        st.session_state.checkout_success = True
        st.sidebar.success("ส่งเข้าครัวแล้ว - Your order has been sent to the kitchen")
        st.session_state.cart = {}
        st.experimental_rerun()
