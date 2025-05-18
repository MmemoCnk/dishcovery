import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="DISHCOVERY",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* DISHCOVERY title */
    .dishcovery-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #333;
    }
    
    /* Welcome banner */
    .welcome-banner {
        background-color: #e17a54;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    /* Side panel sections */
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
    
    /* Cart icon styling - Fixed at TOP right corner */
    .cart-icon {
        position: absolute;
        top: 20px; /* Move to top */
        right: 30px;
        z-index: 1000;
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
        font-size: 12px;
        font-weight: bold;
    }
    
    /* Menu quantity buttons */
    .quantity-btn {
        display: inline-block;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        border: 1px solid #ccc;
        background-color: white;
        color: #333;
        font-weight: bold;
        text-align: center;
        line-height: 30px;
        cursor: pointer;
        margin: 0 5px;
    }
    
    .quantity-value {
        display: inline-block;
        width: 30px;
        text-align: center;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Helper functions
def add_to_cart(item_id):
    """Add an item to the cart"""
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id] += 1
    else:
        st.session_state.cart[item_id] = 1

def remove_from_cart(item_id):
    """Remove an item from the cart"""
    if item_id in st.session_state.cart:
        if st.session_state.cart[item_id] > 0:
            st.session_state.cart[item_id] -= 1
            if st.session_state.cart[item_id] == 0:
                del st.session_state.cart[item_id]

def get_item_quantity(item_id):
    """Get the quantity of an item in the cart"""
    return st.session_state.cart.get(item_id, 0)

# Sample menu items
menu_items = [
    {
        "id": "1",
        "name": "Tom Yum Kung",
        "price": 150,
        "image": "https://images.unsplash.com/photo-1548943487-a2e4e43b4853",
        "category": "soup"
    },
    {
        "id": "2",
        "name": "Pad Thai",
        "price": 120,
        "image": "https://images.unsplash.com/photo-1559314809-0d155014e29e",
        "category": "main"
    },
    {
        "id": "3",
        "name": "Rice",
        "price": 25,
        "image": "https://images.unsplash.com/photo-1516684732162-798a0062be99",
        "category": "main"
    },
    {
        "id": "4",
        "name": "Fresh water",
        "price": 20,
        "image": "https://images.unsplash.com/photo-1616118132534-731f94e918c8",
        "category": "drinks"
    },
    {
        "id": "5",
        "name": "Stir fried Thai basil",
        "price": 140,
        "image": "https://images.unsplash.com/photo-1625398407796-82650a8c9dd4",
        "category": "main"
    }
]

# Layout the app
col1, col2 = st.columns([1, 3])

with col1:
    # DISHCOVERY title
    st.markdown('<h1 class="dishcovery-title">DISHCOVERY</h1>', unsafe_allow_html=True)
    
    # Member login section
    st.write("Please Input Customer ID")
    
    member_id = st.text_input("Member ID", value="1111")
    phone = st.text_input("Tel number", value="1111")
    
    enter_btn = st.button("Enter")
    
    # Set authenticated in session state
    if enter_btn:
        st.session_state.authenticated = True
    
    # Always show Recommendation section (even before login)
    st.markdown('''
    <div class="section-container">
        <div class="section-header">
            Recommendation
        </div>
        <div class="section-content">
            <div style="display: flex; justify-content: space-between;">
                <span>Omelette (new)</span>
                <span style="color: green;">100</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Fries Pork with Garlic</span>
                <span style="color: green;">99</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Som Tam</span>
                <span style="color: green;">80</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>Satay</span>
                <span style="color: green;">30</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>test1</span>
                <span style="color: green;">30</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span>test2</span>
                <span style="color: green;">30</span>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Block ordering: 1. Recommendation (always shown above), 2. Customer information, 3. Favorite Dishes, 4. Allergic Food
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        # 1. Favorite Dishes section (only after login)
        st.markdown('''
        <div class="section-container">
            <div class="section-header">
                Favorite Dishes
            </div>
            <div class="section-content">
                <div>• Pad Thai</div>
                <div>• Green Curry</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 2. Allergic Food section (only after login)
        st.markdown('''
        <div class="section-container">
            <div class="section-header">
                Allergic Food
            </div>
            <div class="section-content">
                <div>• Peanuts</div>
                <div>• Shellfish</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 3. Customer information at the bottom
        st.write("Customer Information")
        st.text_input("Name :", value="test1", disabled=True)
        st.text_input("Surname :", value="test2", disabled=True)
        current_date = "Sunday, March 2, 2025, 12:00"
        st.write(f"Date & Time : {current_date}")

with col2:
    # Welcome banner
    st.markdown('<div class="welcome-banner">Welcome</div>', unsafe_allow_html=True)
    
    # Main Menu header
    st.markdown('## Main Menu')
    
    # Search bar
    st.text_input("", placeholder="Search")
    
    # Category tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["All", "Main Dishes", "Soup", "Appetizers", "Drinks"])
    
    with tab1:  # Display all items in the All tab
        for item in menu_items:
            cols = st.columns([1, 3, 1])
            
            with cols[0]:
                st.image(item["image"], width=100)
            
            with cols[1]:
                st.write(f"### {item['name']}")
                st.write(f"฿{item['price']}")
            
            # Quantity controls
            with cols[2]:
                quantity = get_item_quantity(item["id"])
                
                # Display current quantity
                st.write(f"Quantity: {quantity}")
                
                # Use image buttons instead of interactive elements
                # Generate unique form ID to enable multiple forms on the same page
                form_id = f"form_{item['id']}"
                
                # Create a form with buttons
                with st.form(key=form_id, clear_on_submit=False):
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: flex-end;">
                        <div class="quantity-btn">-</div>
                        <div class="quantity-value">{quantity}</div>
                        <div class="quantity-btn">+</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # These buttons are hidden but functional
                    cols = st.columns(2)
                    with cols[0]:
                        minus_btn = st.form_submit_button("-", help="Decrease quantity")
                    with cols[1]:
                        plus_btn = st.form_submit_button("+", help="Increase quantity")
                    
                    # Handle button clicks
                    if minus_btn:
                        remove_from_cart(item["id"])
                        st.rerun()
                    
                    if plus_btn:
                        add_to_cart(item["id"])
                        st.rerun()

# Cart icon with proper styling - positioned at the TOP right corner (fixed)
cart_count = sum(st.session_state.cart.values()) if st.session_state.cart else 0

# Cart icon with proper styling and counter
cart_html = f"""
<div class="cart-icon">
    <div style="position: relative;">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        {f'<span class="cart-counter">{cart_count}</span>' if cart_count > 0 else ''}
    </div>
</div>
"""
st.markdown(cart_html, unsafe_allow_html=True)
