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

# Initialize cart view state
if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False

# Initialize authentication status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Custom CSS for cart icon and other styling
st.markdown("""
<style>
    /* Cart icon at top right corner */
    .cart-icon {
        position: fixed;
        top: 20px;
        right: 30px;
        z-index: 9999;
        cursor: pointer;
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
    
    /* Cart modal */
    .cart-modal {
        position: fixed;
        top: 60px;
        right: 30px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 20px;
        width: 350px;
        max-height: 80vh;
        overflow-y: auto;
        z-index: 9998;
    }
    
    /* Cart action buttons */
    .cart-action-btn {
        width: 100%;
        margin-top: 10px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Quantity buttons */
    .quantity-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
    }
    
    .quantity-btn:hover {
        background-color: #e9ecef;
    }
    
    .quantity-display {
        display: inline-block;
        width: 30px;
        text-align: center;
        font-weight: bold;
    }
    
    /* Main content adjustments */
    .main-content {
        padding-bottom: 20px;
    }
    
    /* Item card styling */
    .item-card {
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s;
    }
    
    .item-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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

def toggle_cart():
    """Toggle cart visibility"""
    st.session_state.show_cart = not st.session_state.show_cart

# Callback functions for buttons
def click_minus(item_id):
    remove_from_cart(item_id)

def click_plus(item_id):
    add_to_cart(item_id)

def toggle_cart_view():
    toggle_cart()

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

# Helper function to get item details by id
def get_item_by_id(item_id):
    for item in menu_items:
        if item["id"] == item_id:
            return item
    return None

# Cart icon at top right with click functionality
cart_count = sum(st.session_state.cart.values()) if st.session_state.cart else 0
cart_icon_html = f"""
<div class="cart-icon" onclick="cartIconClicked()">
    <div style="position: relative;">
        <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        {f'<span class="cart-counter">{cart_count}</span>' if cart_count > 0 else ''}
    </div>
</div>

<script>
function cartIconClicked() {
    // Use Streamlit's component communication to click a hidden button
    document.getElementById('cart_toggle_button').click();
}
</script>
"""

st.markdown(cart_icon_html, unsafe_allow_html=True)

# Hidden button to toggle cart
cart_toggle = st.button("Toggle Cart", key="cart_toggle_button", on_click=toggle_cart_view)
if cart_toggle:
    st.rerun()

# Cart modal - only shown when active
if st.session_state.show_cart:
    cart_modal_html = """
    <div class="cart-modal">
        <h3>Your Cart</h3>
        <div style="margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
    """
    
    total_price = 0
    
    if st.session_state.cart:
        for item_id, quantity in st.session_state.cart.items():
            item = get_item_by_id(item_id)
            if item:
                item_total = item["price"] * quantity
                total_price += item_total
                cart_modal_html += f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div>{item["name"]} x {quantity}</div>
                    <div>฿{item_total}</div>
                </div>
                """
        
        cart_modal_html += f"""
        </div>
        <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 15px;">
            <div>Total:</div>
            <div>฿{total_price}</div>
        </div>
        <div>
            <button onclick="document.getElementById('checkout_button').click();" 
                    style="width: 100%; padding: 8px; background-color: #e17a54; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Checkout
            </button>
        </div>
        """
    else:
        cart_modal_html += """
        </div>
        <div style="text-align: center; margin: 20px 0;">
            Your cart is empty
        </div>
        """
    
    cart_modal_html += """
    </div>
    """
    
    st.markdown(cart_modal_html, unsafe_allow_html=True)

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
            
            # Create item card with proper styling
            st.markdown(f"""
            <div class="item-card">
                <div style="display: flex; align-items: center;">
                    <div style="flex: 1;">
                        <img src="{item['image']}" width="100">
                    </div>
                    <div style="flex: 3; padding: 0 15px;">
                        <h3 style="margin: 0;">{item['name']}</h3>
                        <p style="margin: 5px 0;">฿{item['price']}</p>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div>Quantity: {quantity}</div>
                        <div style="display: flex; align-items: center; justify-content: flex-end; margin-top: 10px;">
                            <button id="minus_{item['id']}" class="quantity-btn">-</button>
                            <span class="quantity-display">{quantity}</span>
                            <button id="plus_{item['id']}" class="quantity-btn">+</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                document.getElementById("minus_{item['id']}").addEventListener("click", function() {{
                    document.getElementById("btn_minus_{item['id']}").click();
                }});
                document.getElementById("plus_{item['id']}").addEventListener("click", function() {{
                    document.getElementById("btn_plus_{item['id']}").click();
                }});
            </script>
            """, unsafe_allow_html=True)
            
            # Hidden buttons to be activated by JavaScript
            col_buttons = st.columns([1, 1])
            with col_buttons[0]:
                st.button("-", key=f"btn_minus_{item['id']}", on_click=click_minus, args=(item['id'],), help="Remove item", use_container_width=True)
            with col_buttons[1]:
                st.button("+", key=f"btn_plus_{item['id']}", on_click=click_plus, args=(item['id'],), help="Add item", use_container_width=True)
            
            # Use empty to hide the buttons
            st.markdown('<style>div.row-widget.stButton {display: none;}</style>', unsafe_allow_html=True)

    # Hidden checkout button that will be triggered from the cart modal
    checkout_button = st.button("Checkout", key="checkout_button")
    if checkout_button:
        st.success("Order placed successfully!")
        # Clear cart after checkout
        st.session_state.cart = {}
        st.session_state.show_cart = False
        st.rerun()
