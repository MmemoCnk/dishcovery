import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="DISHCOVERY",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Initialize authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Initialize cart view state
if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False

# Custom CSS for cart icon and styling
st.markdown("""
<style>
    /* Cart icon at top right corner */
    .cart-icon {
        position: fixed;
        top: 20px;
        right: 30px;
        z-index: 9999;
    }
    
    /* Cart counter badge */
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
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Hide default buttons that we'll replace with custom ones */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="element-container"]:has(button) {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions for cart management
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

# Store default item data
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

# Helper function to get item details by id
def get_item_by_id(item_id):
    for item in menu_items:
        if item["id"] == item_id:
            return item
    return None

# Callback function for cart button click
def toggle_cart():
    st.session_state.show_cart = not st.session_state.show_cart

# Cart icon at top right
cart_count = sum(st.session_state.cart.values()) if st.session_state.cart else 0
cart_icon_html = f"""
<div class="cart-icon" onclick="document.getElementById('cart_button').click()">
    <div style="position: relative; cursor: pointer;">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        {f'<span class="cart-counter">{cart_count}</span>' if cart_count > 0 else ''}
    </div>
</div>
"""
st.markdown(cart_icon_html, unsafe_allow_html=True)

# Hide the cart button that will be triggered by the cart icon
cart_button = st.button("Cart", key="cart_button", on_click=toggle_cart)
st.markdown('<style>#cart_button{display: none;}</style>', unsafe_allow_html=True)

# Cart view - show only when active
if st.session_state.show_cart:
    cart_items = st.session_state.cart
    if cart_items:
        with st.sidebar:
            st.header("Your Cart")
            total = 0
            for item_id, quantity in cart_items.items():
                item = get_item_by_id(item_id)
                if item:
                    st.write(f"{item['name']} x {quantity} = ฿{item['price'] * quantity}")
                    total += item['price'] * quantity
            
            st.write(f"**Total: ฿{total}**")
            if st.button("Checkout"):
                st.success("Order placed successfully!")
                st.session_state.cart = {}
                st.session_state.show_cart = False
                st.rerun()
    else:
        with st.sidebar:
            st.header("Your Cart")
            st.write("Your cart is empty")

# Layout the app
col1, col2 = st.columns([1, 3])

with col1:
    # DISHCOVERY title
    st.markdown('<h1>DISHCOVERY</h1>', unsafe_allow_html=True)
    
    # Member login section
    st.write("Please Input Customer ID")
    
    member_id = st.text_input("Member ID", value="1111")
    phone = st.text_input("Tel number", value="1111")
    
    # Enter button
    enter_button = st.button("Enter", key="login_button")
    if enter_button:
        st.session_state.authenticated = True
        st.success("Login successful!")
    
    # Always show Recommendation
    st.markdown(
        """
        <div style="background-color: #e17a54; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
            <div style="background-color: rgba(255, 255, 255, 0.3); color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; text-align: center; font-size: 24px; font-weight: bold;">
                Recommendation
            </div>
            <div style="background-color: white; border-radius: 10px; padding: 15px;">
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
        """,
        unsafe_allow_html=True
    )
    
    # Show these sections only after login
    if st.session_state.authenticated:
        # 1. Favorite Dishes section
        st.markdown(
            """
            <div style="background-color: #e17a54; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <div style="background-color: rgba(255, 255, 255, 0.3); color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; text-align: center; font-size: 24px; font-weight: bold;">
                    Favorite Dishes
                </div>
                <div style="background-color: white; border-radius: 10px; padding: 15px;">
                    <div>• Pad Thai</div>
                    <div>• Green Curry</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 2. Allergic Food section
        st.markdown(
            """
            <div style="background-color: #e17a54; border-radius: 10px; padding: 15px; margin-bottom: 20px;">
                <div style="background-color: rgba(255, 255, 255, 0.3); color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; text-align: center; font-size: 24px; font-weight: bold;">
                    Allergic Food
                </div>
                <div style="background-color: white; border-radius: 10px; padding: 15px;">
                    <div>• Peanuts</div>
                    <div>• Shellfish</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 3. Customer information
        st.write("Customer Information")
        st.text_input("Name :", value="test1", disabled=True)
        st.text_input("Surname :", value="test2", disabled=True)
        current_date = "Sunday, March 2, 2025, 12:00"
        st.write(f"Date & Time : {current_date}")

with col2:
    # Welcome banner
    st.markdown(
        """
        <div style="background-color: #e17a54; color: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
            Welcome
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Main Menu header
    st.markdown('## Main Menu')
    
    # Search bar
    st.text_input("", placeholder="Search")
    
    # Category tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["All", "Main Dishes", "Soup", "Appetizers", "Drinks"])
    
    with tab1:  # Display all items in the All tab
        for i, item in enumerate(menu_items):
            # Get current quantity of this item
            quantity = get_item_quantity(item["id"])
            
            # Create columns for item display
            col_img, col_info, col_actions = st.columns([1, 3, 1])
            
            # Column 1: Image
            with col_img:
                st.image(item["image"], width=100)
            
            # Column 2: Name and price
            with col_info:
                st.subheader(item["name"])
                st.write(f"฿{item['price']}")
            
            # Column 3: Quantity and buttons
            with col_actions:
                # Display quantity
                st.write(f"Quantity: {quantity}")
                
                # Create buttons that will be hidden and replaced with custom HTML buttons
                minus_btn = st.button("-", key=f"minus_{item['id']}")
                plus_btn = st.button("+", key=f"plus_{item['id']}")
                
                # Custom + and - buttons with direct session state manipulation
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: flex-end; gap: 10px;">
                    <button onclick="
                        if ({quantity} > 0) {{
                            fetch('/_stcore/stream?WS_TOKEN=' + new URLSearchParams(window.location.search).get('WS_TOKEN'), {{
                                method: 'POST',
                                headers: {{'Content-Type': 'application/json'}},
                                body: JSON.stringify({{
                                    'type': 'streamlit:setComponentValue',
                                    'payload': {{
                                        'componentId': 'minus_{item['id']}',
                                        'value': true,
                                        'disabled': false,
                                        'dataType': 'bool'
                                    }}
                                }})
                            }});
                        }}"
                        style="width: 30px; height: 30px; border: 1px solid #ddd; border-radius: 4px; 
                              display: flex; align-items: center; justify-content: center; 
                              font-weight: bold; font-size: 16px; cursor: pointer;">-</button>
                    <span style="font-weight: bold; width: 20px; text-align: center;">{quantity}</span>
                    <button onclick="
                        fetch('/_stcore/stream?WS_TOKEN=' + new URLSearchParams(window.location.search).get('WS_TOKEN'), {{
                            method: 'POST',
                            headers: {{'Content-Type': 'application/json'}},
                            body: JSON.stringify({{
                                'type': 'streamlit:setComponentValue',
                                'payload': {{
                                    'componentId': 'plus_{item['id']}',
                                    'value': true,
                                    'disabled': false,
                                    'dataType': 'bool'
                                }}
                            }})
                        }});"
                        style="width: 30px; height: 30px; border: 1px solid #ddd; border-radius: 4px; 
                              display: flex; align-items: center; justify-content: center; 
                              font-weight: bold; font-size: 16px; cursor: pointer;">+</button>
                </div>
                """, unsafe_allow_html=True)
                
                # Process button clicks
                if minus_btn:
                    remove_from_cart(item["id"])
                    st.rerun()
                if plus_btn:
                    add_to_cart(item["id"])
                    st.rerun()
