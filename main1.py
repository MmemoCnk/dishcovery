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

# Custom CSS - preserving your original styling but making buttons functional
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
    
    /* Quantity controls - IMPROVED to match your screenshot */
    .quantity-controls {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 5px;
    }
    
    .minus-btn {
        border: 1px solid #ccc;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: white;
        color: #555;
        font-size: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    
    .plus-btn {
        border: 1px solid #ccc;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: white;
        color: #555;
        font-size: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }
    
    .quantity-value {
        width: 30px;
        text-align: center;
        font-weight: bold;
    }
    
    /* Cart button */
    .cart-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background-color: transparent;
        border: none;
    }
    
    /* Cart counter */
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
        font-weight: bold;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Hide default Streamlit button style */
    .item-controls button {
        display: none;
    }
    
    /* Custom side panel sections */
    .side-panel-section {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Restaurant sections */
    .section-container {
        background-color: #e17a54;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .section-header {
        background-color: rgba(255, 255, 255, 0.3);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    
    .section-content {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
    }
    
    .section-item {
        display: flex;
        align-items: center;
        margin-bottom: 5px;
    }
    
    .section-item-bullet {
        margin-right: 10px;
    }
    
    .section-item-score {
        display: flex;
        justify-content: space-between;
        padding: 5px 0;
    }
    
    .section-item-score-value {
        color: green;
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

# Sample data
categories = [
    {"id": "all", "name": "All"},
    {"id": "main", "name": "Main Dishes"},
    {"id": "soup", "name": "Soup"},
    {"id": "appetizers", "name": "Appetizers"},
    {"id": "desserts", "name": "Desserts"},
    {"id": "drinks", "name": "Drinks"}
]

menu_items = [
    {
        "id": "1",
        "name": "Tom Yum Kung",
        "price": 150,
        "image": "https://images.unsplash.com/photo-1548943487-a2e4e43b4853",
        "categoryId": "soup",
        "description": "Hot and sour Thai soup with shrimp, lemongrass, lime, and chili."
    },
    {
        "id": "2",
        "name": "Pad Thai",
        "price": 120,
        "image": "https://images.unsplash.com/photo-1559314809-0d155014e29e",
        "categoryId": "main",
        "description": "Traditional Thai stir-fried rice noodles with egg, tofu, bean sprouts, and ground peanuts."
    },
    {
        "id": "3",
        "name": "Rice",
        "price": 25,
        "image": "https://images.unsplash.com/photo-1516684732162-798a0062be99",
        "categoryId": "main",
        "description": "Steamed jasmine rice, a perfect side for Thai dishes."
    },
    {
        "id": "4",
        "name": "Fresh water",
        "price": 20,
        "image": "https://images.unsplash.com/photo-1616118132534-731f94e918c8",
        "categoryId": "drinks",
        "description": "Refreshing bottled water."
    },
    {
        "id": "5",
        "name": "Stir fried Thai basil",
        "price": 140,
        "image": "https://images.unsplash.com/photo-1625398407796-82650a8c9dd4",
        "categoryId": "main",
        "description": "Stir-fried meat with Thai basil, chili, and garlic."
    }
]

# Sample user data
user_data = {
    "firstName": "Test",
    "lastName": "User",
    "phone": "1111",
    "allergies": ["Peanuts", "Shellfish"],
    "favorites": ["Pad Thai", "Green Curry"]
}

# Recommended dishes
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

def add_to_cart(item_id):
    """Add an item to the cart"""
    # Find the item
    item = next((item for item in menu_items if item["id"] == item_id), None)
    if not item:
        return
    
    # Check if item already exists in cart
    for i, cart_item in enumerate(st.session_state.cart):
        if cart_item["id"] == item_id:
            # Update quantity
            st.session_state.cart[i]["quantity"] += 1
            return
    
    # Add new item to cart
    cart_item = {
        "id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "image": item["image"],
        "quantity": 1
    }
    st.session_state.cart.append(cart_item)

def remove_from_cart(item_id):
    """Remove one unit of an item from the cart"""
    for i, cart_item in enumerate(st.session_state.cart):
        if cart_item["id"] == item_id:
            if cart_item["quantity"] > 1:
                # Decrease quantity
                st.session_state.cart[i]["quantity"] -= 1
            else:
                # Remove item from cart
                st.session_state.cart.pop(i)
            return

def get_total_items():
    """Get the total number of items in the cart"""
    return sum(item["quantity"] for item in st.session_state.cart)

def handle_plus_click(item_id):
    add_to_cart(item_id)
    st.experimental_rerun()

def handle_minus_click(item_id):
    quantity = get_item_quantity(item_id)
    if quantity > 0:
        remove_from_cart(item_id)
        st.experimental_rerun()

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
        # Simulate authentication
        st.session_state.is_authenticated = True
        st.session_state.user_data = user_data
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Customer information
    st.markdown('<div class="side-panel-section">', unsafe_allow_html=True)
    st.write("Customer Information")
    st.text_input("Name :", value="", disabled=True)
    st.text_input("Surname :", value="", disabled=True)
    current_date = "Sunday, March 2, 2025, 12:00"
    st.write(f"Date & Time : {current_date}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Favorite Dishes section
    st.markdown('''
    <div class="section-container">
        <div class="section-header">
            Favorite Dishes
        </div>
        <div class="section-content">
            <div class="section-item">
                <span class="section-item-bullet">•</span> Pad Thai
            </div>
            <div class="section-item">
                <span class="section-item-bullet">•</span> Green Curry
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Recommendation section
    st.markdown('''
    <div class="section-container">
        <div class="section-header">
            Recommendation
        </div>
        <div class="section-content">
            <div class="section-item-score">
                <span>Omelette (new)</span>
                <span class="section-item-score-value">100</span>
            </div>
            <div class="section-item-score">
                <span>Fries Pork with Garlic</span>
                <span class="section-item-score-value">99</span>
            </div>
            <div class="section-item-score">
                <span>Som Tam</span>
                <span class="section-item-score-value">80</span>
            </div>
            <div class="section-item-score">
                <span>Satay</span>
                <span class="section-item-score-value">30</span>
            </div>
            <div class="section-item-score">
                <span>test1</span>
                <span class="section-item-score-value">30</span>
            </div>
            <div class="section-item-score">
                <span>test2</span>
                <span class="section-item-score-value">30</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Allergic Food section
    st.markdown('''
    <div class="section-container">
        <div class="section-header">
            Allergic Food
        </div>
        <div class="section-content">
            <div class="section-item">
                <span class="section-item-bullet">•</span> Peanuts
            </div>
            <div class="section-item">
                <span class="section-item-bullet">•</span> Shellfish
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    # Welcome banner
    welcome_text = "Welcome"
    st.markdown(f'<div class="welcome-banner">{welcome_text}</div>', unsafe_allow_html=True)
    
    # Main Menu header
    st.markdown('<h2>Main Menu</h2>', unsafe_allow_html=True)
    
    # Search bar
    st.text_input("", placeholder="Search")
    
    # Category tabs
    tab_cols = st.columns(len(categories))
    for i, category in enumerate(categories):
        with tab_cols[i]:
            if st.button(category["name"], key=f"category_{category['id']}"):
                st.session_state.active_category = category["id"]
                st.experimental_rerun()
    
    # Display menu items with quantity controls that match your screenshot
    for item in menu_items:
        with st.container():
            cols = st.columns([1, 3, 1])
            
            with cols[0]:
                st.image(item["image"], width=100)
            
            with cols[1]:
                st.write(f"# {item['name']}")
                st.write(f"฿{item['price']}")
            
            # THE FIXED PART - Custom controls that look identical to your screenshot
            with cols[2]:
                quantity = get_item_quantity(item["id"])
                
                # Create two hidden buttons to handle the click actions
                with st.container():
                    # These buttons won't be visible but will handle the functionality
                    minus_btn = st.button("-", key=f"minus_{item['id']}")
                    plus_btn = st.button("+", key=f"plus_{item['id']}")
                    
                    if minus_btn:
                        handle_minus_click(item["id"])
                    
                    if plus_btn:
                        handle_plus_click(item["id"])
                
                # Custom HTML to show the quantity controls exactly like your screenshot
                st.markdown(f"""
                <div style="text-align: right; margin-top: 10px;">
                    <div style="margin-bottom: 5px;">Quantity: {quantity}</div>
                    <div style="display: flex; justify-content: flex-end; align-items: center;">
                        <button class="minus-btn" onclick="document.querySelector('button[key=minus_{item['id']}]').click();">-</button>
                        <span style="margin: 0 10px;">{quantity}</span>
                        <button class="plus-btn" onclick="document.querySelector('button[key=plus_{item['id']}]').click();">+</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Shopping cart button (fixed position)
cart_count = get_total_items()
cart_button_html = f"""
<div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
    <button class="cart-button">
        <img src="https://static.thenounproject.com/png/985-200.png" width="40" height="40">
        {f'<span class="cart-counter">{cart_count}</span>' if cart_count > 0 else ''}
    </button>
</div>
"""
st.markdown(cart_button_html, unsafe_allow_html=True)

# Additional JavaScript for better interactivity
st.markdown("""
<script>
    // This makes the custom buttons work better
    document.addEventListener('DOMContentLoaded', function() {
        // Find all plus and minus buttons
        const plusButtons = document.querySelectorAll('.plus-btn');
        const minusButtons = document.querySelectorAll('.minus-btn');
        
        // Add click events
        plusButtons.forEach(button => {
            button.addEventListener('click', function() {
                // The onclick attribute already handles the click
                console.log('Plus clicked');
            });
        });
        
        minusButtons.forEach(button => {
            button.addEventListener('click', function() {
                // The onclick attribute already handles the click
                console.log('Minus clicked');
            });
        });
    });
</script>
""", unsafe_allow_html=True)
