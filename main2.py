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

# Custom CSS for cart icon and transparent buttons
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

# Cart icon at top right
cart_count = sum(st.session_state.cart.values()) if st.session_state.cart else 0
st.markdown(
    f"""
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
    """,
    unsafe_allow_html=True
)

# Layout the app
col1, col2 = st.columns([1, 3])

with col1:
    # DISHCOVERY title
    st.markdown('<h1>DISHCOVERY</h1>', unsafe_allow_html=True)
    
    # Member login section
    st.write("Please Input Customer ID")
    
    member_id = st.text_input("Member ID", value="1111")
    phone = st.text_input("Tel number", value="1111")
    
    # IMPORTANT: Keep the Enter button functional
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
        # For each menu item
        for i, item in enumerate(menu_items):
            # Get quantity of this item
            quantity = get_item_quantity(item["id"])
            
            # Create 3 columns for layout
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
                # Display quantity first
                st.write(f"Quantity: {quantity}")
                
                # NO NESTED COLUMNS: Just use URL parameters for buttons
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; align-items: center; margin-top: 10px;">
                    <!-- Minus button as transparent box with - sign -->
                    <a href="?minus={item['id']}" style="text-decoration: none;">
                        <div style="width: 40px; height: 40px; border: 1px solid #ddd; border-radius: 8px; 
                                    display: flex; align-items: center; justify-content: center; 
                                    font-weight: bold; font-size: 20px; margin-right: 5px;">-</div>
                    </a>
                    
                    <!-- Display quantity -->
                    <span style="margin: 0 10px; font-weight: bold;">{quantity}</span>
                    
                    <!-- Plus button as transparent box with + sign -->
                    <a href="?plus={item['id']}" style="text-decoration: none;">
                        <div style="width: 40px; height: 40px; border: 1px solid #ddd; border-radius: 8px; 
                                    display: flex; align-items: center; justify-content: center; 
                                    font-weight: bold; font-size: 20px; margin-left: 5px;">+</div>
                    </a>
                </div>
                """, unsafe_allow_html=True)

# Handle URL parameters for button actions
params = st.query_params

if "plus" in params:
    item_id = params["plus"][0]
    add_to_cart(item_id)
    # Clear parameter and refresh
    del st.query_params["plus"]
    st.rerun()

if "minus" in params:
    item_id = params["minus"][0]
    remove_from_cart(item_id)
    # Clear parameter and refresh
    del st.query_params["minus"]
    st.rerun()
