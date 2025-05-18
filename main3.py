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

# Initialize session state variables
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False

# Define callback functions BEFORE they are used
def add_item(item_id):
    """Add an item to the cart"""
    if item_id in st.session_state.cart:
        st.session_state.cart[item_id] += 1
    else:
        st.session_state.cart[item_id] = 1

def remove_item(item_id):
    """Remove an item from the cart"""
    if item_id in st.session_state.cart:
        if st.session_state.cart[item_id] > 1:
            st.session_state.cart[item_id] -= 1
        else:
            del st.session_state.cart[item_id]

def toggle_cart():
    """Toggle cart view"""
    st.session_state.show_cart = not st.session_state.show_cart

def login():
    """Handle login"""
    st.session_state.authenticated = True

def checkout():
    """Process checkout"""
    st.session_state.cart = {}
    st.session_state.checkout_success = True

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

# Helper function to get item by ID
def get_item_by_id(item_id):
    for item in menu_items:
        if item["id"] == item_id:
            return item
    return None

# Custom CSS
st.markdown("""
<style>
    /* Container styles */
    .main-container {
        padding: 0 1rem;
    }
    
    /* Cart counter */
    .cart-counter {
        display: inline-block;
        background-color: red;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        text-align: center;
        line-height: 20px;
        margin-left: 5px;
    }
    
    /* Item card */
    .item-card {
        border: 1px solid #eee;
        border-radius: 8px;
        margin-bottom: 1rem;
        padding: 1rem;
    }
    
    /* Hide default header */
    header {
        visibility: hidden;
    }
    
    /* Hide default footer */
    footer {
        visibility: hidden;
    }
    
    /* Hide hamburger menu */
    #MainMenu {
        visibility: hidden;
    }
    
    /* Hide deploy button */
    .stDeployButton {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Layout columns
col1, col2 = st.columns([1, 3])

# Left sidebar
with col1:
    # Title
    st.markdown('<h1>DISHCOVERY</h1>', unsafe_allow_html=True)
    
    # Login section
    st.write("Please Input Customer ID")
    member_id = st.text_input("Member ID", value="1111")
    phone = st.text_input("Tel number", value="1111")
    
    # Login button with callback
    if st.button("Enter", key="login_button", on_click=login):
        st.success("Login successful!")
    
    # Recommendation section - always show
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
    
    # Show additional sections after login
    if st.session_state.authenticated:
        # Favorite Dishes
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
        
        # Allergic Food
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
        
        # Customer Information
        st.write("Customer Information")
        st.text_input("Name :", value="test1", disabled=True)
        st.text_input("Surname :", value="test2", disabled=True)
        current_date = datetime.now().strftime("%A, %B %d, %Y, %H:%M")
        st.write(f"Date & Time : {current_date}")

# Main content column
with col2:
    # Cart icon and button
    cart_items_count = sum(st.session_state.cart.values()) if st.session_state.cart else 0
    cart_col1, cart_col2 = st.columns([5, 1])
    
    with cart_col1:
        st.markdown(
            """
            <div style="background-color: #e17a54; color: white; padding: 1rem; border-radius: 5px; margin-bottom: 1rem;">
                Welcome
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with cart_col2:
        cart_button_label = f"🛒 {'(' + str(cart_items_count) + ')' if cart_items_count > 0 else ''}"
        st.button(cart_button_label, key="cart_button", on_click=toggle_cart)
    
    # Show cart if toggled
    if st.session_state.show_cart:
        with st.expander("Your Cart", expanded=True):
            if st.session_state.cart:
                total_price = 0
                st.write("### Items in your cart:")
                
                for item_id, quantity in st.session_state.cart.items():
                    item = get_item_by_id(item_id)
                    if item:
                        item_total = item["price"] * quantity
                        total_price += item_total
                        
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"{item['name']} - ฿{item['price']} x {quantity}")
                        with col2:
                            st.write(f"฿{item_total}")
                        with col3:
                            st.button("Remove", key=f"remove_{item_id}", on_click=remove_item, args=(item_id,))
                
                st.write(f"### Total: ฿{total_price}")
                
                if st.button("Checkout", key="checkout_button", on_click=checkout):
                    st.success("Order placed successfully!")
            else:
                st.write("Your cart is empty")
    
    # Display success message if checkout was successful
    if 'checkout_success' in st.session_state and st.session_state.checkout_success:
        st.success("Your order has been placed successfully!")
        # Reset the success message after showing
        st.session_state.checkout_success = False
    
    # Main Menu
    st.markdown('## Main Menu')
    
    # Search bar
    st.text_input("", placeholder="Search")
    
    # Category tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["All", "Main Dishes", "Soup", "Appetizers", "Drinks"])
    
    # Display menu items in tabs
    with tab1:
        for item in menu_items:
            col_img, col_info, col_actions = st.columns([1, 3, 1])
            
            with col_img:
                st.image(item["image"], width=100)
            
            with col_info:
                st.subheader(item["name"])
                st.write(f"฿{item['price']}")
            
            with col_actions:
                # Get current quantity in cart
                quantity = st.session_state.cart.get(item["id"], 0)
                
                # Display quantity
                st.write(f"Quantity: {quantity}")
                
                # Add minus and plus buttons
                minus_col, qty_col, plus_col = st.columns([1, 1, 1])
                
                with minus_col:
                    st.button("-", key=f"minus_{item['id']}", on_click=remove_item, args=(item["id"],))
                
                with qty_col:
                    st.write(f"{quantity}")
                
                with plus_col:
                    st.button("+", key=f"plus_{item['id']}", on_click=add_item, args=(item["id"],))
