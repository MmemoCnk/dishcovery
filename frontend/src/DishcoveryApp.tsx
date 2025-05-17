import React from "react";
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
  ComponentProps
} from "streamlit-component-lib";

// ประกาศ Interface สำหรับรายการเมนูอาหาร
interface MenuItem {
  name: string;
  price: number;
}

// ประกาศ Interface สำหรับรายการในตะกร้า (เพิ่ม quantity และ remark จาก MenuItem)
interface CartItem extends MenuItem {
  quantity: number;
  remark?: string;
}

// ประกาศ Interface สำหรับ User
interface User {
  id: string;
  phone: string;
  name: string;
  surname: string;
  favoriteDishes?: string[];
  allergicFood?: string[];
}

// ประกาศ Interface สำหรับ OrderContext
interface OrderContextType {
  cart: Record<string, CartItem>;
  activeTab: string;
  setActiveTab: (tab: string) => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  addToCart: (item: MenuItem, remark?: string) => void;
  removeFromCart: (itemName: string) => void;
  clearCart: () => void;
  login: (memberId: string, phone: string) => boolean;
  loggedIn: boolean;
  currentUser: User | null;
  checkoutSuccess: boolean;
  setCheckoutSuccess: (success: boolean) => void;
}

// ข้อมูลเมนูอาหารตัวอย่าง
const menuItemsData: Record<string, MenuItem[]> = {
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
const usersData: User[] = [
  { 
    id: "12345", 
    phone: "0891234567", 
    name: "John", 
    surname: "Doe", 
    favoriteDishes: ["Pad Thai", "Tom Yum"], 
    allergicFood: ["Peanuts"] 
  }
];

// สร้าง OrderContext
const OrderContext = React.createContext<OrderContextType | undefined>(undefined);

// OrderProvider component
const OrderProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cart, setCart] = React.useState<Record<string, CartItem>>({});
  const [activeTab, setActiveTab] = React.useState("All");
  const [searchQuery, setSearchQuery] = React.useState("");
  const [loggedIn, setLoggedIn] = React.useState(false);
  const [currentUser, setCurrentUser] = React.useState<User | null>(null);
  const [checkoutSuccess, setCheckoutSuccess] = React.useState(false);
  
  // ฟังก์ชันเข้าสู่ระบบ
  const login = (memberId: string, phone: string): boolean => {
    const user = usersData.find(u => u.id === memberId && u.phone === phone);
    if (user) {
      setCurrentUser(user);
      setLoggedIn(true);
      return true;
    }
    return false;
  };
  
  // เพิ่มรายการในตะกร้า
  const addToCart = (item: MenuItem, remark = "") => {
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
  const removeFromCart = (itemName: string) => {
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
  
  // ส่งค่าทั้งหมดไปยัง Provider
  return (
    <OrderContext.Provider
      value={{
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
      }}
    >
      {children}
    </OrderContext.Provider>
  );
};

// Custom hook เพื่อใช้ OrderContext
const useOrder = () => {
  const context = React.useContext(OrderContext);
  if (context === undefined) {
    throw new Error("useOrder must be used within an OrderProvider");
  }
  return context;
};

// CustomerInfo component
const CustomerInfo: React.FC = () => {
  const [memberId, setMemberId] = React.useState("");
  const [phone, setPhone] = React.useState("");
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
  
  return (
    <div className="card h-full">
      <div className="card-header">
        <div className="text-3xl font-bold text-center">&nbsp;</div>
      </div>
      <div className="p-4 space-y-4">
        {!loggedIn && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Please Input Customer ID</h2>
            <input
              className="input"
              placeholder="Member ID"
              value={memberId}
              onChange={(e) => setMemberId(e.target.value)}
            />
            <input
              className="input"
              placeholder="Tel number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
            <button 
              className="button"
              onClick={handleLogin}
            >
              Enter
            </button>
          </div>
        )}

        <div className="space-y-4 pt-4">
          <h2 className="text-xl font-semibold">Customer Information</h2>
          <input 
            className="input"
            placeholder="Name" 
            value={currentUser?.name || ""} 
            disabled
          />
          <input 
            className="input"
            placeholder="Surname" 
            value={currentUser?.surname || ""} 
            disabled
          />
          <input 
            className="input"
            placeholder="Date & Time" 
            value={currentDate} 
            disabled
          />
        </div>
      </div>
    </div>
  );
};

// RecommendationPanel component
const RecommendationPanel: React.FC = () => {
  const { loggedIn, currentUser } = useOrder();
  
  return (
    <div className="flex flex-col gap-4">
      {/* Favorite Dishes */}
      <div className="card mb-2">
        <div className="card-header">Favorite Dishes</div>
        <div className="p-4">
          {loggedIn && currentUser?.favoriteDishes ? (
            currentUser.favoriteDishes.map((dish, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded-md my-2">
                {dish}
              </div>
            ))
          ) : (
            <div className="text-gray-500">No favorite dishes available</div>
          )}
        </div>
      </div>
      
      {/* Recommendations */}
      <div className="card mb-2">
        <div className="card-header">Recommendation</div>
        <div className="p-4">
          {recommendationsData.map((rec, index) => (
            <div key={index} className="bg-gray-50 p-3 rounded-md my-2 flex justify-between">
              <span>{rec.name}</span>
              <span>{rec.quantity}</span>
            </div>
          ))}
        </div>
      </div>
      
      {/* Allergic Food */}
      <div className="card">
        <div className="card-header">Allergic Food</div>
        <div className="p-4">
          {loggedIn && currentUser?.allergicFood ? (
            currentUser.allergicFood.map((allergen, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded-md my-2">
                {allergen}
              </div>
            ))
          ) : (
            <div className="text-gray-500">No allergic food information available</div>
          )}
        </div>
      </div>
    </div>
  );
};

// ShoppingCart component
interface ShoppingCartProps {
  onClose: () => void;
}

const ShoppingCart: React.FC<ShoppingCartProps> = ({ onClose }) => {
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
  
  return (
    <div className="card w-72 shadow-lg">
      <div className="flex justify-between items-center p-4">
        <h3 className="font-bold text-lg">Shopping Cart</h3>
        <div 
          className="cursor-pointer" 
          onClick={onClose}
        >
          X
        </div>
      </div>
      <hr />
      <div className="p-4 space-y-4 max-h-96 overflow-auto">
        {Object.keys(cart).length > 0 ? (
          <>
            {Object.entries(cart).map(([name, item]) => (
              <div key={name} className="py-1">
                <div className="flex justify-between">
                  <span>{name} x {item.quantity}</span>
                  <span>฿{item.price * item.quantity}</span>
                </div>
                {item.remark && <div className="text-sm italic text-gray-600">Remark: {item.remark}</div>}
              </div>
            ))}
            <hr className="my-2" />
            <div className="font-bold flex justify-between">
              <span>Total:</span>
              <span>฿{totalCartPrice}</span>
            </div>
            <button 
              className="button mt-2"
              onClick={handleCheckout}
            >
              Checkout
            </button>
          </>
        ) : (
          <div className="py-4 text-center text-gray-500">Your cart is empty</div>
        )}
      </div>
    </div>
  );
};

// FoodMenu component
const FoodMenu: React.FC = () => {
  const { 
    addToCart, 
    removeFromCart,
    cart,
    activeTab, 
    setActiveTab,
    searchQuery,
    setSearchQuery
  } = useOrder();
  
  const [selectedItem, setSelectedItem] = React.useState<MenuItem | null>(null);
  const [remark, setRemark] = React.useState("");
  
  const handleAddToCart = (item: MenuItem, withRemark = false) => {
    if (withRemark) {
      setSelectedItem(item);
      setRemark("");
    } else {
      addToCart(item);
    }
  };
  
  const handleRemoveFromCart = (itemName: string) => {
    removeFromCart(itemName);
  };
  
  const handleSubmitRemark = () => {
    if (selectedItem) {
      addToCart(selectedItem, remark);
      setSelectedItem(null);
    }
  };
  
  // รายการอาหารทั้งหมด
  const allItems = Object.entries(menuItemsData).reduce((acc, [_, items]) => {
    return [...acc, ...items];
  }, [] as MenuItem[]);
  
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
  
  return (
    <div className="h-full flex flex-col">
      {/* Search Bar */}
      <div className="mb-4 relative">
        <input
          className="input pl-8"
          placeholder="Search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <span className="absolute left-2 top-3 text-gray-500">
          🔍
        </span>
      </div>
      
      {/* Category Tabs */}
      <div className="grid grid-cols-6 mb-4">
        {categoryTabs.map((category) => (
          <div
            key={category}
            className={`tab ${activeTab === category ? 'tab-active' : ''}`}
            onClick={() => setActiveTab(category)}
          >
            {category}
          </div>
        ))}
      </div>
      
      {/* Food Items */}
      <div className="flex-1 overflow-auto mb-4 pr-2">
        {displayItems.map((item) => {
          const quantity = cart[item.name]?.quantity || 0;
          
          return (
            <div 
              key={item.name} 
              className="food-item"
              onClick={() => handleAddToCart(item, true)}
            >
              <div className="food-image">🍽️</div>
              <div className="flex-1 font-medium">{item.name}</div>
              <div className="flex items-center">
                <button 
                  className="counter-button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleRemoveFromCart(item.name);
                  }}
                  disabled={quantity === 0}
                >
                  -
                </button>
                <span className="mx-3 w-6 text-center">{quantity}</span>
                <button 
                  className="counter-button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleAddToCart(item);
                  }}
                >
                  +
                </button>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Remark Dialog */}
      {selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-md p-6 w-96">
            <h3 className="text-lg font-semibold mb-4">
              Add Remark for {selectedItem?.name}
            </h3>
            <input
              className="input mb-4"
              placeholder="Enter your remark here..."
              value={remark}
              onChange={(e) => setRemark(e.target.value)}
            />
            <div className="flex justify-end space-x-2">
              <button 
                className="px-4 py-2 border rounded-md"
                onClick={() => setSelectedItem(null)}
              >
                Cancel
              </button>
              <button 
                className="px-4 py-2 bg-gray-800 text-white rounded-md"
                onClick={handleSubmitRemark}
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Main App Component ที่จะใช้กับ Streamlit
interface DishcoveryAppProps extends ComponentProps {
  // Props ที่จะรับมาจาก Python
  theme?: string;
}

class DishcoveryApp extends StreamlitComponentBase<DishcoveryAppProps> {
  public render = (): React.ReactNode => {
    // App component
    const App: React.FC = () => {
      const { checkoutSuccess, cart } = useOrder();
      const [showCart, setShowCart] = React.useState(false);
      const [toastVisible, setToastVisible] = React.useState(false);
      const [toastMessage, setToastMessage] = React.useState("");
      
      const totalItems = Object.values(cart).reduce(
        (sum, item) => sum + item.quantity, 
        0
      );
      
      React.useEffect(() => {
        if (checkoutSuccess) {
          setToastMessage("ส่งเข้าครัวแล้ว - Your order has been sent to the kitchen");
          setToastVisible(true);
          setTimeout(() => setToastVisible(false), 3000);
        }
      }, [checkoutSuccess]);
      
      // รายงานข้อมูลกลับไปที่ Streamlit เมื่อมีการเปลี่ยนแปลงใน cart
      React.useEffect(() => {
        Streamlit.setComponentValue({
          cart: cart,
          totalItems: totalItems,
          totalPrice: Object.values(cart).reduce(
            (sum, item) => sum + (item.price * item.quantity), 
            0
          )
        });
      }, [cart, totalItems]);
      
      return (
        <div className="min-h-screen bg-gray-100 p-4">
          <div className="flex flex-col h-[calc(100vh-2rem)]">
            {/* Top section */}
            <div className="flex justify-between items-center mb-4">
              <div className="w-1/4 pr-4">
                <h1 className="text-3xl font-bold text-gray-800">DISHCOVERY</h1>
              </div>
              
              <div className="flex-grow bg-orange-500 text-white flex items-center p-4 h-16 rounded-md">
                <div className="text-xl font-bold">Welcome</div>
              </div>
              
              <div className="relative ml-4">
                <button
                  className="bg-white rounded-md p-2 h-12 w-12 flex items-center justify-center"
                  onClick={() => setShowCart(!showCart)}
                >
                  🛒
                  {totalItems > 0 && (
                    <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
                      {totalItems}
                    </span>
                  )}
                </button>
                {showCart && (
                  <div className="absolute top-full right-0 mt-2 z-50">
                    <ShoppingCart onClose={() => setShowCart(false)} />
                  </div>
                )}
              </div>
            </div>
            
            {/* Main content */}
            <div className="flex gap-4 h-full">
              {/* Left Column */}
              <div className="w-1/4 flex flex-col gap-4">
                <CustomerInfo />
                <RecommendationPanel />
              </div>
              
              {/* Right Column */}
              <div className="w-3/4">
                {/* Main Menu Header */}
                <div className="bg-gray-200 text-gray-800 flex items-center p-4 h-16 mb-4 rounded-md">
                  <div className="text-2xl font-bold">Main Menu</div>
                </div>
                
                {/* Food Menu */}
                <FoodMenu />
              </div>
            </div>
          </div>
          
          {/* Toast notification */}
          {toastVisible && (
            <div className="fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-md shadow-lg">
              {toastMessage}
            </div>
          )}
        </div>
      );
    };

    // Wrap the App with OrderProvider
    return (
      <OrderProvider>
        <App />
      </OrderProvider>
    );
  }
}

// เชื่อมต่อ Component กับ Streamlit
export default withStreamlitConnection(DishcoveryApp);