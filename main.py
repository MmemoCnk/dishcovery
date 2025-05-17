import streamlit as st
import pandas as pd
from PIL import Image
import base64
import json
import os
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="DISHCOVERY",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container styles */
    .main {
        padding: 0 !important;
    }
    
    /* Header styles */
    .dishcovery-header {
        background-color: white;
        padding: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e0e0e0;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .dishcovery-title {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
    }
    
    .welcome-banner {
        background-color: #e17a54;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    /* Menu content */
    .menu-content {
        padding: 1rem;
    }
    
    /* Category tabs */
    .category-tab {
        background-color: #f3f4f6;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin-right: 0.5rem;
        cursor: pointer;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    .category-tab.active {
        background-color: #e17a54;
        color: white;
    }
    
    /* Menu card */
    .menu-card {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: white;
        display: flex;
        align-items: center;
        transition: box-shadow 0.3s;
    }
    
    .menu-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .food-img {
        width: 80px;
        height: 80px;
        object-fit: cover;
        border-radius: 8px;
        margin-right: 1rem;
    }
    
    /* Quantity buttons */
    .quantity-btn {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 1px solid #e0e0e0;
        background-color: white;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 1.2rem;
    }
    
    .quantity-btn.add {
        color: #e17a54;
        border-color: #e17a54;
    }
    
    /* Toast notification */
    .toast {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #4caf50;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        z-index: 1000;
        display: none;
    }
    
    /* Customer info section */
    .customer-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Member login section */
    .member-login {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        color: #6c757d;
        font-size: 0.8rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 2rem;
    }
    
    /* Item name styling */
    .item-name {
        font-weight: bold;
        margin-bottom: 0.25rem;
    }
    
    /* Cart button counter */
    .cart-counter {
        position: absolute;
        top: -8px;
        right: -8px;
        background-color: #e74c3c;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
    }
    
    /* Custom button */
    .custom-button {
        background-color: #e17a54;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        cursor: pointer;
    }
    
    .custom-button:hover {
        background-color: #d1694a;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #555;
        margin: 1rem 0;
        padding: 0.5rem;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    
    /* Side panel sections */
    .side-panel-section {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Dialog styles */
    .stAlert > div {
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'active_category' not in st.session_state:
    st.session_state.active_category = "all"
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'show_food_dialog' not in st.session_state:
    st.session_state.show_food_dialog = False
if 'selected_food' not in st.session_state:
    st.session_state.selected_food = None
if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False
if 'order_sent' not in st.session_state:
    st.session_state.order_sent = False
if 'show_toast' not in st.session_state:
    st.session_state.show_toast = False
if 'toast_message' not in st.session_state:
    st.session_state.toast_message = ""

# Sample data
categories = [
    {"id": "all", "name": "All"},
    {"id": "main", "name": "Main Dishes"},
    {"id": "appetizers", "name": "Appetizers"},
    {"id": "desserts", "name": "Desserts"},
    {"id": "drinks", "name": "Drinks"}
]

menu_items = [
    {
        "id": "1",
        "name": "Pad Thai",
        "price": 120,
        "image": "https://images.unsplash.com/photo-1559314809-0d155014e29e",
        "categoryId": "main",
        "description": "Traditional Thai stir-fried rice noodles with egg, tofu, bean sprouts, and ground peanuts."
    },
    {
        "id": "2",
        "name": "Tom Yum Soup",
        "price": 150,
        "image": "https://images.unsplash.com/photo-1548943487-a2e4e43b4853",
        "categoryId": "appetizers",
        "description": "Hot and sour Thai soup with lemongrass, lime, and your choice of shrimp or chicken."
    },
    {
        "id": "3",
        "name": "Green Curry",
        "price": 180,
        "image": "https://images.unsplash.com/photo-1604579278540-db35e0495aea",
        "categoryId": "main",
        "description": "Rich and creamy Thai green curry with eggplant, bamboo shoots, and basil."
    },
    {
        "id": "4",
        "name": "Mango Sticky Rice",
        "price": 90,
        "image": "https://images.unsplash.com/photo-1621304813372-016faff0efdd",
        "categoryId": "desserts",
        "description": "Sweet sticky rice soaked in coconut milk, served with fresh mango."
    },
    {
        "id": "5",
        "name": "Thai Iced Tea",
        "price": 60,
        "image": "https://images.unsplash.com/photo-1563461661026-49631dd5d68e",
        "categoryId": "drinks",
        "description": "Sweet Thai tea with milk, served over ice."
    },
    {
        "id": "6",
        "name": "Stir Fried Thai Basil",
        "price": 140,
        "image": "https://images.unsplash.com/photo-1625398407796-82650a8c9dd4",
        "categoryId": "main",
        "description": "Stir-fried meat with Thai basil, chili, and garlic."
    },
    {
        "id": "7",
        "name": "Fresh Water",
        "price": 20,
        "image": "https://images.unsplash.com/photo-1616118132534-731f94e918c8",
        "categoryId": "drinks",
        "description": "Refreshing bottled water."
    },
    {
        "id": "8",
        "name": "Rice",
        "price": 25,
        "image": "https://images.unsplash.com/photo-1516684732162-798a0062be99",
        "categoryId": "main",
        "description": "Steamed jasmine rice, a perfect side for Thai dishes."
    }
]

# Sample user data
user_database = {
    "1111": {
        "phone": "1111",
        "firstName": "test1",
        "lastName": "test2",
        "allergies": ["Peanuts", "Shellfish"],
        "favorites": ["Pad Thai", "Green Curry"]
    }
}

# Recommended dishes with scores
recommendations = [
    {"name": "Omelette (new)", "score": 100},
    {"name": "Fries Pork with Garlic", "score": 99},
    {"name": "Som Tam", "score": 80},
    {"name": "Satay", "score": 30},
    {"name": "test1", "score": 30},
    {"name": "test2", "score": 30}
]

# Helper functions
def get_item_quantity(item_id):
    """Get the quantity of an item in the cart"""
    for item in st.session_state.cart:
        if item["id"] == item_id:
            return item["quantity"]
    return 0

def add_to_cart(item, remark=None):
    """Add an item to the cart"""
    # Check if item already exists in cart
    for i, cart_item in enumerate(st.session_state.cart):
        if cart_item["id"] == item["id"]:
            # Update quantity
            st.session_state.cart[i]["quantity"] += 1
            if remark:
                st.session_state.cart[i]["remark"] = remark
            return
    
    # Add new item to cart
    cart_item = {
        "id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "image": item["image"],
        "quantity": 1,
        "remark": remark
    }
    st.session_state.cart.append(cart_item)

def update_cart_quantity(item_id, quantity):
    """Update the quantity of an item in the cart"""
    for i, item in enumerate(st.session_state.cart):
        if item["id"] == item_id:
            if quantity <= 0:
                # Remove item from cart
                st.session_state.cart.pop(i)
            else:
                # Update quantity
                st.session_state.cart[i]["quantity"] = quantity
            return

def remove_from_cart(item_id):
    """Remove an item from the cart"""
    for i, item in enumerate(st.session_state.cart):
        if item["id"] == item_id:
            st.session_state.cart.pop(i)
            return

def get_total_items():
    """Get the total number of items in the cart"""
    return sum(item["quantity"] for item in st.session_state.cart)

def get_total_price():
    """Get the total price of items in the cart"""
    return sum(item["price"] * item["quantity"] for item in st.session_state.cart)

def filter_menu_items():
    """Filter menu items based on active category and search query"""
    filtered = menu_items
    
    # Filter by category
    if st.session_state.active_category != "all":
        filtered = [item for item in filtered if item["categoryId"] == st.session_state.active_category]
    
    # Filter by search query
    if st.session_state.search_query:
        query = st.session_state.search_query.lower()
        filtered = [item for item in filtered if query in item["name"].lower()]
    
    return filtered

def authenticate_user(member_id, phone):
    """Authenticate user with member ID and phone number"""
    if member_id in user_database and user_database[member_id]["phone"] == phone:
        st.session_state.is_authenticated = True
        st.session_state.user_data = user_database[member_id]
        return True
    return False

def show_toast(message, duration=3):
    """Show a toast message"""
    st.session_state.show_toast = True
    st.session_state.toast_message = message
    # The toast will be hidden after a timeout in the JavaScript

def checkout():
    """Process checkout"""
    st.session_state.order_sent = True
    show_toast("Order sent to kitchen!")
    # Clear cart after a delay (simulated)
    # In a real app, you'd send this to a backend

# Layout the app
col1, col2 = st.columns([1, 3])

with col1:
    # DISHCOVERY title
    st.markdown('<h1 class="dishcovery-title">DISHCOVERY</h1>', unsafe_allow_html=True)
    
    # Member login section
    st.markdown('<div class="side-panel-section">', unsafe_allow_html=True)
    st.write("Please Input Customer ID")
    
    member_id = st.text_input("Member ID", key="member_id_input")
    phone = st.text_input("Tel number", key="phone_input")
    
    if st.button("Enter"):
        if authenticate_user(member_id, phone):
            st.success(f"Welcome, {st.session_state.user_data['firstName']} {st.session_state.user_data['lastName']}")
        else:
            st.error("Invalid credentials")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Customer information (shown only when authenticated)
    if st.session_state.is_authenticated and st.session_state.user_data:
        st.markdown('<div class="side-panel-section">', unsafe_allow_html=True)
        st.write("Customer Information")
        st.text_input("Name:", value=st.session_state.user_data["firstName"], disabled=True)
        st.text_input("Surname:", value=st.session_state.user_data["lastName"], disabled=True)
        current_date = datetime.now().strftime("%A, %B %d, %Y, %H:%M")
        st.write(f"Date & Time: {current_date}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Custom CSS for the orange sections
        st.markdown("""
        <style>
        .orange-section {
            background-color: #e17a54;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .orange-header {
            background-color: rgba(255, 255, 255, 0.3);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        .white-box {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Favorite Dishes section
        st.markdown('<div class="orange-section">', unsafe_allow_html=True)
        st.markdown('<div class="orange-header">Favorite Dishes</div>', unsafe_allow_html=True)
        st.markdown('<div class="white-box">', unsafe_allow_html=True)
        
        # Content inside white box
        if "favorites" in st.session_state.user_data:
            for fav in st.session_state.user_data["favorites"]:
                st.write(f"• {fav}")
        else:
            st.write("No favorites found.")
            
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Recommendation section - direct HTML approach
        st.markdown('''
        <div style="background-color: #e17a54; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
            <div style="background-color: rgba(255, 255, 255, 0.3); color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; text-align: center; font-size: 24px; font-weight: bold;">
                Recommendation
            </div>
            <div style="background-color: white; border-radius: 10px; padding: 15px;">
                <div style="display: flex; justify-content: space-between; padding: 5px 0;">
                    <span>Omelette (new)</span>
                    <span style="color: green;">100</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 5px 0;">
                    <span>Fries Pork with Garlic</span>
                    <span style="color: green;">99</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 5px 0;">
                    <span>Som Tam</span>
                    <span style="color: green;">80</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 5px 0;">
                    <span>Satay</span>
                    <span style="color: green;">30</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 5px 0;">
                    <span>test1</span>
                    <span style="color: green;">30</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 5px 0;">
                    <span>test2</span>
                    <span style="color: green;">30</span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Allergic Food section
        st.markdown('<div class="orange-section">', unsafe_allow_html=True)
        st.markdown('<div class="orange-header">Allergic Food</div>', unsafe_allow_html=True)
        st.markdown('<div class="white-box">', unsafe_allow_html=True)
        
        # Content inside white box
        if "allergies" in st.session_state.user_data:
            for allergy in st.session_state.user_data["allergies"]:
                st.write(f"• {allergy}")
        else:
            st.write("No allergies found.")
            
        st.markdown('</div></div>', unsafe_allow_html=True)

with col2:
    # Welcome banner
    welcome_text = f"Welcome, {st.session_state.user_data['firstName'] if st.session_state.is_authenticated else 'Guest'}"
    st.markdown(f'<div class="welcome-banner">{welcome_text}</div>', unsafe_allow_html=True)
    
    # Main Menu header
    st.markdown('<h2>Main Menu</h2>', unsafe_allow_html=True)
    
    # Search bar
    search_query = st.text_input("", placeholder="Search menu...", value=st.session_state.search_query)
    if search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
        st.experimental_rerun()
    
    # Category tabs
    st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
    cols = st.columns(len(categories))
    for i, category in enumerate(categories):
        with cols[i]:
            if st.button(category["name"], key=f"category_{category['id']}"):
                st.session_state.active_category = category["id"]
                st.experimental_rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter menu items
    filtered_items = filter_menu_items()
    
    # Display menu items
    for item in filtered_items:
        menu_card = st.container()
        with menu_card:
            cols = st.columns([1, 3, 1])
            
            with cols[0]:
                st.image(item["image"], width=100)
            
            with cols[1]:
                st.write(f"### {item['name']}")
                st.write(f"฿{item['price']}")
            
            with cols[2]:
                quantity = get_item_quantity(item["id"])
                
                # Display quantity controls in a horizontal layout
                st.write(f"Quantity: {quantity}")
                
                minus_btn = st.button("-", key=f"minus_{item['id']}")
                if minus_btn:
                    if quantity > 0:
                        update_cart_quantity(item["id"], quantity - 1)
                        st.experimental_rerun()
                
                plus_btn = st.button("+", key=f"plus_{item['id']}")
                if plus_btn:
                    # When clicking +, add directly to cart
                    add_to_cart(item)
                    st.experimental_rerun()
                
                # Clicking the item area should open dialog
                view_btn = st.button("View Details", key=f"view_{item['id']}")
                if view_btn:
                    st.session_state.show_food_dialog = True
                    st.session_state.selected_food = item
                    st.experimental_rerun()

    # Food dialog
    if st.session_state.show_food_dialog and st.session_state.selected_food:
        with st.form(key="food_dialog", clear_on_submit=True):
            item = st.session_state.selected_food
            st.image(item["image"], width=150)
            st.write(f"### {item['name']}")
            st.write(f"฿{item['price']}")
            st.write(item["description"])
            
            remark = st.text_area("Special instructions", placeholder="E.g., less spicy, no onions, etc.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Add to Cart"):
                    add_to_cart(item, remark)
                    st.session_state.show_food_dialog = False
                    st.experimental_rerun()
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.show_food_dialog = False
                    st.experimental_rerun()

# Shopping cart button (fixed position)
cart_count = get_total_items()
cart_button_html = f"""
<div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
    <button onclick="document.getElementById('cart-dialog').style.display='block'" class="custom-button" style="position: relative;">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        {f'<span class="cart-counter">{cart_count}</span>' if cart_count > 0 else ''}
    </button>
</div>
"""
st.markdown(cart_button_html, unsafe_allow_html=True)

# Shopping cart dialog
cart_dialog_html = f"""
<div id="cart-dialog" style="display: none; position: fixed; top: 0; right: 0; width: 100%; max-width: 400px; height: 100%; background: white; box-shadow: -2px 0 5px rgba(0,0,0,0.1); z-index: 1001; overflow-y: auto; padding: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e0e0e0; padding-bottom: 1rem; margin-bottom: 1rem;">
        <h2>Shopping Cart</h2>
        <button onclick="document.getElementById('cart-dialog').style.display='none'" style="background: none; border: none; cursor: pointer;">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
    </div>
"""

if len(st.session_state.cart) == 0:
    cart_dialog_html += """
    <div style="text-align: center; padding: 2rem;">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 1rem; color: #ccc;">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        <p style="color: #666;">Your cart is empty</p>
    </div>
    """
else:
    for item in st.session_state.cart:
        cart_dialog_html += f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0;">
            <div style="display: flex; align-items: center;">
                <img src="{item['image']}" alt="{item['name']}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px; margin-right: 0.5rem;">
                <div>
                    <div style="font-weight: bold;">{item['name']}</div>
                    <div style="font-size: 0.8rem; color: #666;">฿{item['price']} × {item['quantity']} = ฿{item['price'] * item['quantity']}</div>
                    {f'<div style="font-size: 0.8rem; color: #666; font-style: italic;">{item["remark"]}</div>' if item.get('remark') else ''}
                </div>
            </div>
            <button onclick="updateCartItem('{item['id']}', 'remove')" style="background: none; border: none; color: #e74c3c; cursor: pointer;">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 6h18"></path>
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                </svg>
            </button>
        </div>
        """

# Add total and checkout button
if len(st.session_state.cart) > 0:
    total_price = get_total_price()
    checkout_button_disabled = "disabled" if st.session_state.order_sent else ""
    checkout_button_text = "Order sent to kitchen!" if st.session_state.order_sent else "Checkout"
    
    cart_dialog_html += f"""
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e0e0e0;">
        <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 1.2rem; margin-bottom: 1rem;">
            <span>Total</span>
            <span>฿{total_price}</span>
        </div>
        <button onclick="checkoutCart()" {checkout_button_disabled} style="width: 100%; padding: 0.75rem; background-color: #e17a54; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
            {checkout_button_text}
        </button>
    </div>
    """

cart_dialog_html += """
</div>
"""

# Add JavaScript for cart functionality
js_code = """
<script>
    function updateCartItem(itemId, action) {
        // Send message to Streamlit
        const data = {
            itemId: itemId,
            action: action
        };
        window.parent.postMessage({type: "cart_action", data: JSON.stringify(data)}, "*");
    }
    
    function checkoutCart() {
        // Send message to Streamlit
        window.parent.postMessage({type: "checkout"}, "*");
    }
    
    // Listen for messages from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'cart_updated') {
            // Refresh page to update cart
            window.location.reload();
        }
        if (event.data.type === 'order_sent') {
            // Show order sent message
            document.getElementById('checkout-button').innerText = "Order sent to kitchen!";
            document.getElementById('checkout-button').disabled = true;
            
            // Show toast
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerText = "Order sent to kitchen!";
            toast.style.display = 'block';
            document.body.appendChild(toast);
            
            // Hide toast after 3 seconds
            setTimeout(() => {
                toast.style.display = 'none';
                // Close cart dialog
                document.getElementById('cart-dialog').style.display = 'none';
                // Refresh page to update cart
                window.location.reload();
            }, 3000);
        }
    });
</script>
"""

# Append JavaScript to the page
st.markdown(cart_dialog_html + js_code, unsafe_allow_html=True)

# Handle shopping cart actions from JavaScript
if 'cart_action' in st.query_params:
    action_data = json.loads(st.query_params['cart_action'][0])
    item_id = action_data['itemId']
    action = action_data['action']
    
    if action == 'remove':
        remove_from_cart(item_id)
        st.experimental_rerun()

# Handle checkout from JavaScript
if 'checkout' in st.query_params:
    checkout()
    st.experimental_rerun()

# Toast notification
if st.session_state.show_toast:
    toast_html = f"""
    <div id="toast" class="toast" style="display: block;">{st.session_state.toast_message}</div>
    <script>
        setTimeout(function() {{
            document.getElementById('toast').style.display = 'none';
        }}, 3000);
    </script>
    """
    st.markdown(toast_html, unsafe_allow_html=True)
    st.session_state.show_toast = False

# Footer
st.markdown('<div class="footer">© 2024 DISHCOVERY. All rights reserved.</div>', unsafe_allow_html=True)

# Add streamlit component handlers
def handle_streamlit_events():
    # This function would handle streamlit events in a production app
    # For this demo, we're using JavaScript and query params
    pass

# Add form handlers for direct submission
if 'submit_checkout' in st.session_state and st.session_state.submit_checkout:
    checkout()
    st.session_state.submit_checkout = False
    st.experimental_rerun()

if 'add_item_directly' in st.session_state and st.session_state.add_item_directly:
    item_id = st.session_state.add_item_directly
    item = next((item for item in menu_items if item["id"] == item_id), None)
    if item:
        add_to_cart(item)
    st.session_state.add_item_directly = None
    st.experimental_rerun()

if 'remove_item_directly' in st.session_state and st.session_state.remove_item_directly:
    remove_from_cart(st.session_state.remove_item_directly)
    st.session_state.remove_item_directly = None
    st.experimental_rerun()

# Add additional JS for handling clicks and making the app more interactive
additional_js = """
<script>
// Function to open food dialog when clicking on food item
function openFoodDialog(foodId) {
    window.parent.postMessage({type: "open_food_dialog", foodId: foodId}, "*");
}

// Make entire menu card clickable
document.addEventListener('DOMContentLoaded', function() {
    const menuCards = document.querySelectorAll('.menu-card');
    menuCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Prevent triggering when clicking buttons
            if (!e.target.closest('button')) {
                const foodId = card.getAttribute('data-food-id');
                openFoodDialog(foodId);
            }
        });
    });
});
</script>
"""

st.markdown(additional_js, unsafe_allow_html=True)

# This is the end of the app. In production, you'd want to:
# 1. Connect to a database for menu items, user authentication, and orders
# 2. Implement proper API endpoints for cart management
# 3. Add proper error handling and validation
# 4. Implement order tracking and history
# 5. Improve the UI with proper responsive design
