import streamlit as st
import streamlit.components.v1 as components

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
.css-18e3th9 {padding-top: 0;}
.css-1d391kg {padding-top: 0;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ใช้เฉพาะ HTML Component แทน path-based component
component_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DISHCOVERY</title>
    <!-- React and ReactDOM -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    
    <style>
        body {
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            background-color: #f3f4f6;
        }
        .card {
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #e2e8f0;
            border-radius: 0.25rem;
            margin-bottom: 0.75rem;
        }
        .button {
            background-color: #1e293b;
            color: white;
            padding: 0.75rem;
            border-radius: 0.25rem;
            font-weight: 500;
            cursor: pointer;
            text-align: center;
            display: block;
            width: 100%;
        }
        .button:hover {
            background-color: #334155;
        }
        .card-header {
            background-color: #e2e8f0;
            padding: 0.5rem;
            border-top-left-radius: 0.5rem;
            border-top-right-radius: 0.5rem;
            text-align: center;
            font-weight: 600;
        }
        .tab {
            padding: 0.5rem 1rem;
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            cursor: pointer;
            text-align: center;
        }
        .tab-active {
            background-color: #f8fafc;
            border-bottom: 2px solid #334155;
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
            width: 4rem;
            height: 4rem;
            background-color: #f3f4f6;
            margin-right: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 0.25rem;
        }
        .counter-button {
            width: 2rem;
            height: 2rem;
            border-radius: 9999px;
            background-color: white;
            border: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .counter-button:hover {
            background-color: #f8fafc;
        }
    </style>
</head>
<body>
    <div id="root"></div>
    
    <script>
        // ประกาศและกำหนดตัวแปรจาก React
        const { createElement: h, useState, useEffect, useContext, createContext } = React;
        const { createRoot } = ReactDOM;

        // สร้าง OrderContext
        const OrderContext = createContext();
        
        // ข้อมูลเมนูอาหารตัวอย่าง
        const menuItemsData = {
            "Main Dishes": [
                { name: "Tom Yum Kung", price: 120 },
                { name: "Pad Thai", price: 100 },
                { name: "Stir fried Thai basil", price: 90 }
            ],
            "Soup": [
                { name: "Chicken Soup", price: 80 },
                { name: "Vegetable Soup", price: 70 }
            ],
            "Appetizers": [],
            "Desserts": [
                { name: "Mango Sticky Rice", price: 90 },
                { name: "Coconut Ice Cream", price: 60 }
            ],
            "Drinks": [
                { name: "Fresh water", price: 20 },
                { name: "Thai Milk Tea", price: 50 }
            ]
        };
        
        // ข้อมูลคำแนะนำตัวอย่าง
        const recommendationsData = [
            { name: "Omelette (new)", quantity: 100 },
            { name: "Fries Pork with Garlic", quantity: 99 },
            { name: "Som Tam", quantity: 80 },
            { name: "Satay", quantity: 30 },
            { name: "test1", quantity: 30 },
            { name: "test2", quantity: 30 }
        ];
        
        // ข้อมูลผู้ใช้ตัวอย่าง
        const usersData = [
            { 
                id: "12345", 
                phone: "0891234567", 
                name: "John", 
                surname: "Doe", 
                favoriteDishes: ["Pad Thai", "Tom Yum"], 
                allergicFood: ["Peanuts"] 
            }
        ];

        // OrderProvider component
        function OrderProvider({ children }) {
            const [cart, setCart] = useState({});
            const [activeTab, setActiveTab] = useState("All");
            const [searchQuery, setSearchQuery] = useState("");
            const [loggedIn, setLoggedIn] = useState(false);
            const [currentUser, setCurrentUser] = useState(null);
            const [checkoutSuccess, setCheckoutSuccess] = useState(false);
            
            // ฟังก์ชันเข้าสู่ระบบ
            const login = (memberId, phone) => {
                const user = usersData.find(u => u.id === memberId && u.phone === phone);
                if (user) {
                    setCurrentUser(user);
                    setLoggedIn(true);
                    return true;
                }
                return false;
            };
            
            // เพิ่มรายการในตะกร้า
            const addToCart = (item, remark = "") => {
                setCart(prev => {
                    const updatedCart = { ...prev };
                    if (updatedCart[item.name]) {
                        updatedCart[item.name].quantity += 1;
                        if (remark) {
                            updatedCart[item.name].remark = remark;
                        }
                    } else {
                        updatedCart[item.name] = {
                            ...item,
                            quantity: 1,
                            remark
                        };
                    }
                    return updatedCart;
                });
            };
            
            // ลบรายการจากตะกร้า
            const removeFromCart = (itemName) => {
                setCart(prev => {
                    const updatedCart = { ...prev };
                    if (updatedCart[itemName] && updatedCart[itemName].quantity > 0) {
                        updatedCart[itemName].quantity -= 1;
                        if (updatedCart[itemName].quantity === 0) {
                            delete updatedCart[itemName];
                        }
                    }
                    return updatedCart;
                });
            };
            
            // ล้างตะกร้า
            const clearCart = () => {
                setCart({});
            };
            
            return h(OrderContext.Provider, {
                value: {
                    cart,
                    activeTab,
                    setActiveTab,
                    searchQuery,
                    setSearchQuery,
                    addToCart,
                    removeFromCart,
                    clearCart,
                    login,
                    loggedIn,
                    currentUser,
                    checkoutSuccess,
                    setCheckoutSuccess
                }
            }, children);
        }

        // Hook สำหรับใช้ OrderContext
        function useOrder() {
            return useContext(OrderContext);
        }

        // CustomerInfo component
        function CustomerInfo() {
            const [memberId, setMemberId] = useState("");
            const [phone, setPhone] = useState("");
            const { login, loggedIn, currentUser } = useOrder();
            const currentDate = new Date().toLocaleString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            const handleLogin = () => {
                if (!login(memberId, phone)) {
                    alert("Invalid credentials. Continuing as guest.");
                }
            };
            
            return h('div', { className: 'card h-full' }, [
                h('div', { className: 'p-4' }, [
                    !loggedIn ? h('div', { className: 'space-y-4' }, [
                        h('h2', { className: 'text-xl font-semibold' }, 'Please Input Customer ID'),
                        h('input', { 
                            className: 'input', 
                            placeholder: 'Member ID',
                            value: memberId,
                            onChange: (e) => setMemberId(e.target.value)
                        }),
                        h('input', { 
                            className: 'input', 
                            placeholder: 'Tel number',
                            value: phone,
                            onChange: (e) => setPhone(e.target.value)
                        }),
                        h('div', { 
                            className: 'button', 
                            onClick: handleLogin 
                        }, 'Enter')
                    ]) : null,
                    
                    h('div', { className: 'space-y-4 pt-4' }, [
                        h('h2', { className: 'text-xl font-semibold' }, 'Customer Information'),
                        h('input', { 
                            className: 'input', 
                            placeholder: 'Name',
                            value: currentUser?.name || "",
                            disabled: true
                        }),
                        h('input', { 
                            className: 'input', 
                            placeholder: 'Surname',
                            value: currentUser?.surname || "",
                            disabled: true
                        }),
                        h('input', { 
                            className: 'input', 
                            placeholder: 'Date & Time',
                            value: currentDate,
                            disabled: true
                        })
                    ])
                ])
            ]);
        }

        // RecommendationPanel component
        function RecommendationPanel() {
            const { loggedIn, currentUser } = useOrder();
            
            return h('div', { className: 'flex flex-col gap-4' }, [
                // Favorite Dishes card
                h('div', { className: 'card mb-2' }, [
                    h('div', { className: 'card-header' }, 'Favorite Dishes'),
                    h('div', { className: 'p-4' }, 
                        loggedIn && currentUser?.favoriteDishes ? 
                            currentUser.favoriteDishes.map((dish, index) => 
                                h('div', { 
                                    key: index, 
                                    className: 'bg-gray-50 p-3 rounded-md my-2' 
                                }, dish)
                            ) :
                            h('div', { className: 'text-gray-500' }, 'No favorite dishes available')
                    )
                ]),
                
                // Recommendations card
                h('div', { className: 'card mb-2' }, [
                    h('div', { className: 'card-header' }, 'Recommendation'),
                    h('div', { className: 'p-4' }, 
                        recommendationsData.map((rec, index) => 
                            h('div', { 
                                key: index, 
                                className: 'bg-gray-50 p-3 rounded-md my-2 flex justify-between' 
                            }, [
                                h('span', {}, rec.name),
                                h('span', {}, rec.quantity)
                            ])
                        )
                    )
                ]),
                
                // Allergic Food card
                h('div', { className: 'card' }, [
                    h('div', { className: 'card-header' }, 'Allergic Food'),
                    h('div', { className: 'p-4' }, 
                        loggedIn && currentUser?.allergicFood ? 
                            currentUser.allergicFood.map((allergen, index) => 
                                h('div', { 
                                    key: index, 
                                    className: 'bg-gray-50 p-3 rounded-md my-2' 
                                }, allergen)
                            ) :
                            h('div', { className: 'text-gray-500' }, 'No allergic food information available')
                    )
                ])
            ]);
        }

        // ShoppingCart component
        function ShoppingCart({ onClose }) {
            const { cart, clearCart, setCheckoutSuccess } = useOrder();
            
            const totalCartPrice = Object.values(cart).reduce(
                (sum, item) => sum + (item.price * item.quantity), 
                0
            );
            
            const handleCheckout = () => {
                setCheckoutSuccess(true);
                setTimeout(() => {
                    clearCart();
                    onClose();
                }, 1000);
            };
            
            return h('div', { className: 'card w-72 shadow-lg' }, [
                h('div', { className: 'flex justify-between items-center p-4' }, [
                    h('h3', { className: 'font-bold text-lg' }, 'Shopping Cart'),
                    h('div', { 
                        className: 'cursor-pointer', 
                        onClick: onClose 
                    }, 'X')
                ]),
                h('hr', {}),
                h('div', { className: 'p-4 space-y-4 max-h-96 overflow-auto' }, [
                    Object.keys(cart).length > 0 ? [
                        ...Object.entries(cart).map(([name, item]) => 
                            h('div', { key: name, className: 'py-1' }, [
                                h('div', { className: 'flex justify-between' }, [
                                    h('span', {}, `${name} x ${item.quantity}`),
                                    h('span', {}, `฿${item.price * item.quantity}`)
                                ]),
                                item.remark && h('div', { 
                                    className: 'text-sm italic text-gray-600' 
                                }, `Remark: ${item.remark}`)
                            ])
                        ),
                        h('hr', { className: 'my-2' }),
                        h('div', { className: 'font-bold flex justify-between' }, [
                            h('span', {}, 'Total:'),
                            h('span', {}, `฿${totalCartPrice}`)
                        ]),
                        h('div', { 
                            className: 'button mt-2', 
                            onClick: handleCheckout 
                        }, 'Checkout')
                    ] : h('div', { 
                        className: 'py-4 text-center text-gray-500' 
                    }, 'Your cart is empty')
                ])
            ]);
        }

        // FoodMenu component
        function FoodMenu() {
            const { 
                addToCart, 
                removeFromCart,
                cart,
                activeTab, 
                setActiveTab,
                searchQuery,
                setSearchQuery
            } = useOrder();
            
            const [selectedItem, setSelectedItem] = useState(null);
            const [remark, setRemark] = useState("");
            
            const handleAddToCart = (item, withRemark = false) => {
                if (withRemark) {
                    setSelectedItem(item);
                    setRemark("");
                } else {
                    addToCart(item);
                }
            };
            
            const handleRemoveFromCart = (itemName) => {
                removeFromCart(itemName);
            };
            
            const handleSubmitRemark = () => {
                if (selectedItem) {
                    addToCart(selectedItem, remark);
                    setSelectedItem(null);
                }
            };
            
            // รายการอาหารทั้งหมด
            const allItems = Object.entries(menuItemsData).reduce((acc, [category, items]) => {
                return [...acc, ...items];
            }, []);
            
            // กรองรายการตามคำค้นหาหรือแท็บที่เลือก
            const displayItems = searchQuery
                ? allItems.filter(item => 
                    item.name.toLowerCase().includes(searchQuery.toLowerCase())
                )
                : activeTab === "All"
                ? allItems
                : menuItemsData[activeTab] || [];
            
            // รายการแท็บทั้งหมด
            const categoryTabs = ["All", ...Object.keys(menuItemsData)];
            
            return h('div', { className: 'h-full flex flex-col' }, [
                // Search Bar
                h('div', { className: 'mb-4 relative' }, [
                    h('input', {
                        className: 'input pl-8',
                        placeholder: 'Search',
                        value: searchQuery,
                        onChange: (e) => setSearchQuery(e.target.value)
                    }),
                    h('span', { 
                        className: 'absolute left-2 top-3 text-gray-500' 
                    }, '🔍')
                ]),
                
                // Category Tabs
                h('div', { className: 'grid grid-cols-6 mb-4' }, 
                    categoryTabs.map((category) => 
                        h('div', {
                            key: category,
                            className: `tab ${activeTab === category ? 'tab-active' : ''}`,
                            onClick: () => setActiveTab(category)
                        }, category)
                    )
                ),
                
                // Food Items
                h('div', { className: 'flex-1 overflow-auto mb-4 pr-2' }, 
                    displayItems.map((item) => {
                        const quantity = cart[item.name]?.quantity || 0;
                        
                        return h('div', { 
                            key: item.name, 
                            className: 'food-item',
                            onClick: () => handleAddToCart(item, true)
                        }, [
                            h('div', { className: 'food-image' }, '🍽️'),
                            h('div', { className: 'flex-1 font-medium' }, item.name),
                            h('div', { className: 'flex items-center' }, [
                                h('button', { 
                                    className: 'counter-button',
                                    onClick: (e) => {
                                        e.stopPropagation();
                                        handleRemoveFromCart(item.name);
                                    },
                                    disabled: quantity === 0
                                }, '-'),
                                h('span', { className: 'mx-3 w-6 text-center' }, quantity),
                                h('button', { 
                                    className: 'counter-button',
                                    onClick: (e) => {
                                        e.stopPropagation();
                                        handleAddToCart(item);
                                    }
                                }, '+')
                            ])
                        ]);
                    })
                ),
                
                // Remark Dialog
                selectedItem && h('div', { 
                    className: 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50' 
                }, [
                    h('div', { className: 'bg-white rounded-md p-6 w-96' }, [
                        h('h3', { className: 'text-lg font-semibold mb-4' }, 
                            `Add Remark for ${selectedItem?.name}`
                        ),
                        h('input', {
                            className: 'input mb-4',
                            placeholder: 'Enter your remark here...',
                            value: remark,
                            onChange: (e) => setRemark(e.target.value)
                        }),
                        h('div', { className: 'flex justify-end space-x-2' }, [
                            h('button', { 
                                className: 'px-4 py-2 border rounded-md',
                                onClick: () => setSelectedItem(null)
                            }, 'Cancel'),
                            h('button', { 
                                className: 'px-4 py-2 bg-gray-800 text-white rounded-md',
                                onClick: handleSubmitRemark
                            }, 'Submit')
                        ])
                    ])
                ])
            ]);
        }

        // App component หลัก
        function App() {
            const { checkoutSuccess, cart } = useOrder();
            const [showCart, setShowCart] = useState(false);
            const [toastVisible, setToastVisible] = useState(false);
            const [toastMessage, setToastMessage] = useState('');
            
            const totalItems = Object.values(cart).reduce(
                (sum, item) => sum + item.quantity, 
                0
            );
            
            useEffect(() => {
                if (checkoutSuccess) {
                    setToastMessage('ส่งเข้าครัวแล้ว - Your order has been sent to the kitchen');
                    setToastVisible(true);
                    setTimeout(() => setToastVisible(false), 3000);
                    
                    // ส่งข้อมูลไปยัง Streamlit Python ผ่าน window.parent.postMessage
                    try {
                        const orderData = {
                            cart,
                            totalItems,
                            totalPrice: Object.values(cart).reduce(
                                (sum, item) => sum + (item.price * item.quantity), 0
                            )
                        };
                        // ส่งข้อมูลแบบ manual
                        window.parent.postMessage({
                            type: "streamlit:setComponentValue",
                            value: orderData
                        }, "*");
                    } catch (err) {
                        console.error("Error sending data to Streamlit:", err);
                    }
                }
            }, [checkoutSuccess, cart, totalItems]);
            
            return h('div', { className: 'min-h-screen bg-gray-100 p-4' }, [
                h('div', { className: 'flex flex-col h-[calc(100vh-2rem)]' }, [
                    // Top section
                    h('div', { className: 'flex justify-between items-center mb-4' }, [
                        h('div', { className: 'w-1/4 pr-4' }, [
                            h('h1', { className: 'text-3xl font-bold text-gray-800' }, 'DISHCOVERY')
                        ]),
                        
                        h('div', { 
                            className: 'flex-grow bg-orange-500 text-white flex items-center p-4 h-16 rounded-md' 
                        }, [
                            h('div', { className: 'text-xl font-bold' }, 'Welcome')
                        ]),
                        
                        h('div', { className: 'relative ml-4' }, [
                            h('button', { 
                                className: 'bg-white rounded-md p-2 h-12 w-12 flex items-center justify-center',
                                onClick: () => setShowCart(!showCart)
                            }, [
                                h('span', {}, '🛒'),
                                totalItems > 0 && h('span', { 
                                    className: 'absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs' 
                                }, totalItems)
                            ]),
                            showCart && h('div', { 
                                className: 'absolute top-full right-0 mt-2 z-50' 
                            }, [
                                h(ShoppingCart, { onClose: () => setShowCart(false) })
                            ])
                        ])
                    ]),
                    
                    // Main content
                    h('div', { className: 'flex gap-4 h-full' }, [
                        // Left Column
                        h('div', { className: 'w-1/4 flex flex-col gap-4' }, [
                            h(CustomerInfo),
                            h(RecommendationPanel)
                        ]),
                        
                        // Right Column
                        h('div', { className: 'w-3/4' }, [
                            // Main Menu Header
                            h('div', { 
                                className: 'bg-gray-200 text-gray-800 flex items-center p-4 h-16 mb-4 rounded-md' 
                            }, [
                                h('div', { className: 'text-2xl font-bold' }, 'Main Menu')
                            ]),
                            
                            // Food Menu
                            h(FoodMenu)
                        ])
                    ])
                ]),
                
                // Toast notification
                toastVisible && h('div', { 
                    className: 'fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-md shadow-lg' 
                }, toastMessage)
            ]);
        }

        // Wrap the App with OrderProvider
        function AppWithProvider() {
            return h(OrderProvider, {}, h(App));
        }

        // Render the app
        const root = createRoot(document.getElementById('root'));
        root.render(h(AppWithProvider));

        // ฟังก์ชันเพื่อรับข้อมูลจาก Streamlit
        window.addEventListener("message", function(event) {
            // รับข้อมูลที่ส่งมาจาก Python
            if (event.data.type === "streamlit:render") {
                console.log("Received render event from Streamlit:", event.data);
            }
        });

        // แจ้ง Streamlit ว่า component พร้อมใช้งาน
        window.parent.postMessage({
            type: "streamlit:componentReady",
            value: {}
        }, "*");
    </script>
</body>
</html>
"""

dishcovery_component = components.html(component_html, height=800, scrolling=True)

# ตัวแปร dishcovery_component จะมีค่าเมื่อมีการส่งข้อมูลกลับมาจาก component
if dishcovery_component:
    st.session_state['order_data'] = dishcovery_component

# แสดงข้อมูลการสั่งอาหาร (จะแสดงเมื่อมีการส่งข้อมูลกลับมาจาก component)
with st.expander("ดูข้อมูลการสั่งอาหาร", expanded=False):
    if 'order_data' in st.session_state:
        order_data = st.session_state['order_data']
        st.write("### สรุปการสั่งซื้อ")
        st.write(f"จำนวนรายการทั้งหมด: {order_data.get('totalItems', 0)}")
        st.write(f"ราคารวม: ฿{order_data.get('totalPrice', 0)}")
        
        if 'cart' in order_data and order_data['cart']:
            st.write("### รายการอาหารที่สั่ง")
            for name, item in order_data['cart'].items():
                st.write(f"**{name}** x {item['quantity']} - ฿{item['price'] * item['quantity']}")
                if 'remark' in item and item['remark']:
                    st.write(f"*หมายเหตุ: {item['remark']}*")
        else:
            st.write("ไม่มีรายการอาหารในตะกร้า")
    else:
        st.write("ยังไม่มีข้อมูลการสั่งอาหาร กรุณาสั่งอาหารและกดชำระเงิน")
