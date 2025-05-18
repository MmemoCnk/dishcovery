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

# Very minimal CSS - focused only on the essentials
st.markdown("""
<style>
    /* Cart button styling */
    .cart-button {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background-color: #e17a54;
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
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
    
    /* IMPORTANT: Style for our quantity controls - minimal and focused on functionality */
    .quantity-row {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 10px;
    }
    
    .quantity-btn {
        font-size: 18px;
        font-weight: bold;
    }
    
    .quantity-display {
        font-weight: bold;
        min-width: 30px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'active_category' not in st.session_state:
    st.session_state.active_category = "all"
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Sample data - just for demo
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
    }
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

# Layout the app in two columns
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown('<h1>DISHCOVERY</h1>', unsafe_allow_html=True)
    
    # Simplified left sidebar content
    st.markdown('## Customer Login')
    st.text_input("Member ID")
    st.text_input("Tel number")
    
    if st.button("Enter"):
        st.success("Login successful!")

with col2:
    # Welcome banner
    st.markdown('<div style="background-color: #e17a54; color: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">Welcome</div>', unsafe_allow_html=True)
    
    # Main Menu header
    st.markdown('## Main Menu')
    
    # Search bar
    st.text_input("", placeholder="Search menu...")
    
    # Category tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["All", "Main Dishes", "Appetizers", "Desserts", "Drinks"])
    
    with tab1:
        # Display menu items with SIMPLE, FUNCTIONAL quantity controls
        for item in menu_items:
            with st.container():
                cols = st.columns([1, 3, 1])
                
                with cols[0]:
                    st.image(item["image"], width=100)
                
                with cols[1]:
                    st.write(f"### {item['name']}")
                    st.write(f"฿{item['price']}")
                    st.write(item["description"])
                
                # SOLUTION: Simple, direct quantity controls without complex HTML/CSS
                with cols[2]:
                    quantity = get_item_quantity(item["id"])
                    
                    # Create a row of controls using st.columns for layout
                    st.write(f"**Quantity:** {quantity}")
                    
                    # Create two equal columns for the + and - buttons
                    minus_col, plus_col = st.columns(2)
                    
                    with minus_col:
                        if st.button("-", key=f"minus_{item['id']}"):
                            if quantity > 0:
                                remove_from_cart(item["id"])
                                st.experimental_rerun()
                    
                    with plus_col:
                        if st.button("+", key=f"plus_{item['id']}"):
                            add_to_cart(item["id"])
                            st.experimental_rerun()

# Cart button
cart_count = get_total_items()
cart_html = f"""
<button class="cart-button">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="9" cy="21" r="1"></circle>
        <circle cx="20" cy="21" r="1"></circle>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
    </svg>
    {f'<span class="cart-counter">{cart_count}</span>' if cart_count > 0 else ''}
</button>
"""
st.markdown(cart_html, unsafe_allow_html=True)
