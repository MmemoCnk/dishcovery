"use strict";

// Streamlit component setup
class StreamlitComponentAPI {
  constructor() {
    this._handlers = {};
    this._frameMsgHandler = this._frameMsgHandler.bind(this);
    window.addEventListener("message", this._frameMsgHandler);
  }

  _frameMsgHandler(event) {
    if (event.data.type === "streamlit:render") {
      this._onRenderMessage(event.data);
    }
  }

  _onRenderMessage(renderData) {
    const args = renderData.args;
    this._renderComponent(args);
  }

  _renderComponent(args) {
    const appRoot = document.getElementById("root");
    ReactApp.init(appRoot, this, args);
  }

  setComponentValue(value) {
    window.parent.postMessage({
      type: "streamlit:setComponentValue",
      value: value,
    }, "*");
  }

  setFrameHeight(height) {
    window.parent.postMessage({
      type: "streamlit:setFrameHeight",
      height: height,
    }, "*");
  }
}

// Initialize Streamlit connection
const Streamlit = new StreamlitComponentAPI();

// Our React-like app
const ReactApp = {
  init(rootElement, streamlit, args) {
    this.rootElement = rootElement;
    this.streamlit = streamlit;
    this.args = args;
    this.render();
    this.setupResizeObserver();
  },

  setupResizeObserver() {
    const resizeObserver = new ResizeObserver(entries => {
      const rect = entries[0].contentRect;
      this.streamlit.setFrameHeight(rect.height);
    });
    resizeObserver.observe(this.rootElement);
  },

  render() {
    // Menu data
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

    // Recommendations data
    const recommendationsData = [
      { name: "Omelette (new)", quantity: 100 },
      { name: "Fries Pork with Garlic", quantity: 99 },
      { name: "Som Tam", quantity: 80 },
      { name: "Satay", quantity: 30 },
      { name: "test1", quantity: 30 },
      { name: "test2", quantity: 30 }
    ];

    // User data
    const userData = {
      id: "12345",
      phone: "0891234567",
      name: "John",
      surname: "Doe",
      favoriteDishes: ["Pad Thai", "Tom Yum"],
      allergicFood: ["Peanuts"]
    };

    // Get all menu items
    const allMenuItems = Object.values(menuItemsData).flat();

    // Create app UI
    this.rootElement.innerHTML = `
      <div class="min-h-screen bg-gray-100 p-4">
        <div class="flex flex-col h-[calc(100vh-2rem)]">
          <!-- Top section -->
          <div class="flex justify-between items-center mb-4">
            <div class="w-1/4 pr-4">
              <h1 class="text-3xl font-bold text-gray-800">DISHCOVERY</h1>
            </div>
            
            <div class="flex-grow bg-orange-500 text-white flex items-center p-4 h-16 rounded-md">
              <div class="text-xl font-bold">Welcome</div>
            </div>
            
            <div class="relative ml-4">
              <button id="cart-button" class="bg-white rounded-md p-2 h-12 w-12 flex items-center justify-center">
                🛒
                <span id="cart-badge" class="hidden absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">0</span>
              </button>
              <div id="shopping-cart" class="hidden absolute top-full right-0 mt-2 z-50">
                <!-- Shopping cart content will be added here -->
              </div>
            </div>
          </div>
          
          <!-- Main content -->
          <div class="flex gap-4 h-full">
            <!-- Left Column -->
            <div class="w-1/4 flex flex-col gap-4">
              <!-- Customer Info -->
              <div class="card h-full">
                <div class="p-4">
                  <div id="login-form" class="space-y-4">
                    <h2 class="text-xl font-semibold">Please Input Customer ID</h2>
                    <input id="member-id" class="input" placeholder="Member ID" value="">
                    <input id="phone" class="input" placeholder="Tel number" value="">
                    <button id="login-button" class="button">Enter</button>
                  </div>
                  
                  <div id="customer-info" class="hidden space-y-4 pt-4">
                    <h2 class="text-xl font-semibold">Customer Information</h2>
                    <input id="name" class="input" placeholder="Name" value="" disabled>
                    <input id="surname" class="input" placeholder="Surname" value="" disabled>
                    <input id="date-time" class="input" placeholder="Date & Time" value="" disabled>
                  </div>
                </div>
              </div>
              
              <!-- Recommendation Panel -->
              <div class="flex flex-col gap-4">
                <!-- Favorite Dishes -->
                <div class="card mb-2">
                  <div class="card-header">Favorite Dishes</div>
                  <div id="favorite-dishes" class="p-4">
                    <div class="text-gray-500">No favorite dishes available</div>
                  </div>
                </div>
                
                <!-- Recommendations -->
                <div class="card mb-2">
                  <div class="card-header">Recommendation</div>
                  <div id="recommendations" class="p-4">
                    ${recommendationsData.map(rec => `
                      <div class="bg-gray-50 p-3 rounded-md my-2 flex justify-between">
                        <span>${rec.name}</span>
                        <span>${rec.quantity}</span>
                      </div>
                    `).join('')}
                  </div>
                </div>
                
                <!-- Allergic Food -->
                <div class="card">
                  <div class="card-header">Allergic Food</div>
                  <div id="allergic-food" class="p-4">
                    <div class="text-gray-500">No allergic food information available</div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Right Column -->
            <div class="w-3/4">
              <!-- Main Menu Header -->
              <div class="bg-gray-200 text-gray-800 flex items-center p-4 h-16 mb-4 rounded-md">
                <div class="text-2xl font-bold">Main Menu</div>
              </div>
              
              <!-- Food Menu -->
              <div class="h-full flex flex-col">
                <!-- Search Bar -->
                <div class="mb-4 relative">
                  <input id="search-input" class="input pl-8" placeholder="Search">
                  <span class="absolute left-2 top-3 text-gray-500">🔍</span>
                </div>
                
                <!-- Category Tabs -->
                <div id="category-tabs" class="grid grid-cols-6 mb-4">
                  <div class="tab tab-active" data-tab="All">All</div>
                  ${Object.keys(menuItemsData).map(category => `
                    <div class="tab" data-tab="${category}">${category}</div>
                  `).join('')}
                </div>
                
                <!-- Food Items -->
                <div id="food-items" class="flex-1 overflow-auto mb-4 pr-2">
                  ${allMenuItems.map(item => `
                    <div class="food-item" data-name="${item.name}" data-price="${item.price}">
                      <div class="food-image">🍽️</div>
                      <div class="flex-1 font-medium">${item.name}</div>
                      <div class="flex items-center">
                        <button class="counter-button minus-button" data-name="${item.name}">-</button>
                        <span class="mx-3 w-6 text-center item-quantity" data-name="${item.name}">0</span>
                        <button class="counter-button plus-button" data-name="${item.name}" data-price="${item.price}">+</button>
                      </div>
                    </div>
                  `).join('')}
                </div>
                
                <!-- Remark Dialog -->
                <div id="remark-dialog" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                  <div class="bg-white rounded-md p-6 w-96">
                    <h3 id="remark-title" class="text-lg font-semibold mb-4">Add Remark</h3>
                    <input id="remark-input" class="input mb-4" placeholder="Enter your remark here...">
                    <div class="flex justify-end space-x-2">
                      <button id="remark-cancel" class="px-4 py-2 border rounded-md">Cancel</button>
                      <button id="remark-submit" class="px-4 py-2 bg-gray-800 text-white rounded-md">Submit</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Toast notification -->
        <div id="toast" class="hidden fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-md shadow-lg"></div>
      </div>
    `;

    // Initialize app state
    this.state = {
      activeTab: "All",
      searchQuery: "",
      cart: {},
      loggedIn: false,
      currentUser: null,
      selectedItem: null,
      remark: ""
    };

    // Add event listeners
    this.addEventListeners();
  },

  addEventListeners() {
    // Login button
    const loginButton = document.getElementById("login-button");
    loginButton.addEventListener("click", () => {
      const memberId = document.getElementById("member-id").value;
      const phone = document.getElementById("phone").value;
      this.login(memberId, phone);
    });

    // Category tabs
    const tabs = document.querySelectorAll("#category-tabs .tab");
    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        tabs.forEach(t => t.classList.remove("tab-active"));
        tab.classList.add("tab-active");
        this.filterItems(tab.dataset.tab, this.state.searchQuery);
      });
    });

    // Search input
    const searchInput = document.getElementById("search-input");
    searchInput.addEventListener("input", (e) => {
      this.state.searchQuery = e.target.value;
      this.filterItems(this.state.activeTab, this.state.searchQuery);
    });

    // Plus buttons
    const plusButtons = document.querySelectorAll(".plus-button");
    plusButtons.forEach(button => {
      button.addEventListener("click", (e) => {
        e.stopPropagation();
        const name = button.dataset.name;
        const price = parseFloat(button.dataset.price);
        this.addToCart({ name, price });
      });
    });

    // Minus buttons
    const minusButtons = document.querySelectorAll(".minus-button");
    minusButtons.forEach(button => {
      button.addEventListener("click", (e) => {
        e.stopPropagation();
        const name = button.dataset.name;
        this.removeFromCart(name);
      });
    });

    // Food items (for remark)
    const foodItems = document.querySelectorAll(".food-item");
    foodItems.forEach(item => {
      item.addEventListener("click", () => {
        const name = item.dataset.name;
        const price = parseFloat(item.dataset.price);
        this.showRemarkDialog({ name, price });
      });
    });

    // Remark dialog
    const remarkDialog = document.getElementById("remark-dialog");
    const remarkCancel = document.getElementById("remark-cancel");
    const remarkSubmit = document.getElementById("remark-submit");

    remarkCancel.addEventListener("click", () => {
      this.hideRemarkDialog();
    });

    remarkSubmit.addEventListener("click", () => {
      const remark = document.getElementById("remark-input").value;
      this.addToCart(this.state.selectedItem, remark);
      this.hideRemarkDialog();
    });

    // Shopping cart
    const cartButton = document.getElementById("cart-button");
    cartButton.addEventListener("click", () => {
      const shoppingCart = document.getElementById("shopping-cart");
      shoppingCart.classList.toggle("hidden");
      this.updateShoppingCart();
    });
  },

  login(memberId, phone) {
    // Simulating login verification
    if (memberId === "12345" && phone === "0891234567") {
      this.state.loggedIn = true;
      this.state.currentUser = {
        id: "12345",
        phone: "0891234567",
        name: "John",
        surname: "Doe",
        favoriteDishes: ["Pad Thai", "Tom Yum"],
        allergicFood: ["Peanuts"]
      };
      
      // Update UI
      document.getElementById("login-form").classList.add("hidden");
      document.getElementById("customer-info").classList.remove("hidden");
      
      document.getElementById("name").value = this.state.currentUser.name;
      document.getElementById("surname").value = this.state.currentUser.surname;
      document.getElementById("date-time").value = new Date().toLocaleString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
      
      // Update favorite dishes and allergic food
      this.updateUserPreferences();
    } else {
      alert("Invalid credentials. Continuing as guest.");
    }
  },

  updateUserPreferences() {
    if (this.state.loggedIn && this.state.currentUser) {
      // Update favorite dishes
      const favoriteDishesEl = document.getElementById("favorite-dishes");
      if (this.state.currentUser.favoriteDishes && this.state.currentUser.favoriteDishes.length > 0) {
        favoriteDishesEl.innerHTML = this.state.currentUser.favoriteDishes.map(dish => `
          <div class="bg-gray-50 p-3 rounded-md my-2">${dish}</div>
        `).join('');
      }
      
      // Update allergic food
      const allergicFoodEl = document.getElementById("allergic-food");
      if (this.state.currentUser.allergicFood && this.state.currentUser.allergicFood.length > 0) {
        allergicFoodEl.innerHTML = this.state.currentUser.allergicFood.map(allergen => `
          <div class="bg-gray-50 p-3 rounded-md my-2">${allergen}</div>
        `).join('');
      }
    }
  },

  filterItems(category, searchQuery) {
    this.state.activeTab = category;
    
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
    
    // Get all menu items
    const allMenuItems = Object.values(menuItemsData).flat();
    
    // Filter items based on category and search query
    let displayItems;
    if (searchQuery) {
      displayItems = allMenuItems.filter(item => 
        item.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    } else {
      displayItems = category === "All" ? allMenuItems : (menuItemsData[category] || []);
    }
    
    // Update food items in UI
    const foodItemsEl = document.getElementById("food-items");
    foodItemsEl.innerHTML = displayItems.map(item => `
      <div class="food-item" data-name="${item.name}" data-price="${item.price}">
        <div class="food-image">🍽️</div>
        <div class="flex-1 font-medium">${item.name}</div>
        <div class="flex items-center">
          <button class="counter-button minus-button" data-name="${item.name}">-</button>
          <span class="mx-3 w-6 text-center item-quantity" data-name="${item.name}">${this.state.cart[item.name]?.quantity || 0}</span>
          <button class="counter-button plus-button" data-name="${item.name}" data-price="${item.price}">+</button>
        </div>
      </div>
    `).join('');
    
    // Re-add event listeners
    this.addFoodItemEventListeners();
  },

  addFoodItemEventListeners() {
    // Plus buttons
    const plusButtons = document.querySelectorAll(".plus-button");
    plusButtons.forEach(button => {
      button.addEventListener("click", (e) => {
        e.stopPropagation();
        const name = button.dataset.name;
        const price = parseFloat(button.dataset.price);
        this.addToCart({ name, price });
      });
    });

    // Minus buttons
    const minusButtons = document.querySelectorAll(".minus-button");
    minusButtons.forEach(button => {
      button.addEventListener("click", (e) => {
        e.stopPropagation();
        const name = button.dataset.name;
        this.removeFromCart(name);
      });
    });

    // Food items (for remark)
    const foodItems = document.querySelectorAll(".food-item");
    foodItems.forEach(item => {
      item.addEventListener("click", () => {
        const name = item.dataset.name;
        const price = parseFloat(item.dataset.price);
        this.showRemarkDialog({ name, price });
      });
    });
  },

  addToCart(item, remark = "") {
    if (!this.state.cart[item.name]) {
      this.state.cart[item.name] = {
        ...item,
        quantity: 1,
        remark
      };
    } else {
      this.state.cart[item.name].quantity += 1;
      if (remark) {
        this.state.cart[item.name].remark = remark;
      }
    }
    
    // Update UI
    this.updateCartUI();
  },

  removeFromCart(itemName) {
    if (this.state.cart[itemName] && this.state.cart[itemName].quantity > 0) {
      this.state.cart[itemName].quantity -= 1;
      if (this.state.cart[itemName].quantity === 0) {
        delete this.state.cart[itemName];
      }
    }
    
    // Update UI
    this.updateCartUI();
  },

  updateCartUI() {
    // Update quantity displays
    Object.keys(this.state.cart).forEach(itemName => {
      const quantityEl = document.querySelector(`.item-quantity[data-name="${itemName}"]`);
      if (quantityEl) {
        quantityEl.textContent = this.state.cart[itemName].quantity;
      }
    });
    
    // Update cart badge
    const cartBadge = document.getElementById("cart-badge");
    const totalItems = Object.values(this.state.cart).reduce(
      (sum, item) => sum + item.quantity, 
      0
    );
    
    if (totalItems > 0) {
      cartBadge.textContent = totalItems;
      cartBadge.classList.remove("hidden");
    } else {
      cartBadge.classList.add("hidden");
    }
    
    // Update shopping cart if visible
    const shoppingCart = document.getElementById("shopping-cart");
    if (!shoppingCart.classList.contains("hidden")) {
      this.updateShoppingCart();
    }
  },

  updateShoppingCart() {
    const shoppingCart = document.getElementById("shopping-cart");
    const totalItems = Object.values(this.state.cart).reduce(
      (sum, item) => sum + item.quantity, 
      0
    );
    
    const totalCartPrice = Object.values(this.state.cart).reduce(
      (sum, item) => sum + (item.price * item.quantity), 
      0
    );
    
    if (totalItems > 0) {
      const cartItems = Object.entries(this.state.cart).map(([name, item]) => `
        <div class="py-1">
          <div class="flex justify-between">
            <span>${name} x ${item.quantity}</span>
            <span>฿${item.price * item.quantity}</span>
          </div>
          ${item.remark ? `<div class="text-sm italic text-gray-600">Remark: ${item.remark}</div>` : ''}
        </div>
      `).join('');
      
      shoppingCart.innerHTML = `
        <div class="card w-72 shadow-lg">
          <div class="flex justify-between items-center p-4">
            <h3 class="font-bold text-lg">Shopping Cart</h3>
            <div id="close-cart" class="cursor-pointer">X</div>
          </div>
          <hr>
          <div class="p-4 space-y-4 max-h-96 overflow-auto">
            ${cartItems}
            <hr class="my-2">
            <div class="font-bold flex justify-between">
              <span>Total:</span>
              <span>฿${totalCartPrice}</span>
            </div>
            <button id="checkout-button" class="button mt-2">Checkout</button>
          </div>
        </div>
      `;
      
      // Add event listeners
      document.getElementById("close-cart").addEventListener("click", () => {
        shoppingCart.classList.add("hidden");
      });
      
      document.getElementById("checkout-button").addEventListener("click", () => {
        this.checkout();
      });
    } else {
      shoppingCart.innerHTML = `
        <div class="card w-72 shadow-lg">
          <div class="flex justify-between items-center p-4">
            <h3 class="font-bold text-lg">Shopping Cart</h3>
            <div id="close-cart" class="cursor-pointer">X</div>
          </div>
          <hr>
          <div class="p-4 space-y-4">
            <div class="py-4 text-center text-gray-500">Your cart is empty</div>
          </div>
        </div>
      `;
      
      // Add event listener
      document.getElementById("close-cart").addEventListener("click", () => {
        shoppingCart.classList.add("hidden");
      });
    }
  },

  showRemarkDialog(item) {
    this.state.selectedItem = item;
    this.state.remark = "";
    
    const remarkDialog = document.getElementById("remark-dialog");
    const remarkTitle = document.getElementById("remark-title");
    const remarkInput = document.getElementById("remark-input");
    
    remarkTitle.textContent = `Add Remark for ${item.name}`;
    remarkInput.value = "";
    
    remarkDialog.classList.remove("hidden");
  },

  hideRemarkDialog() {
    const remarkDialog = document.getElementById("remark-dialog");
    remarkDialog.classList.add("hidden");
    this.state.selectedItem = null;
    this.state.remark = "";
  },

  checkout() {
    // Close shopping cart
    const shoppingCart = document.getElementById("shopping-cart");
    shoppingCart.classList.add("hidden");
    
    // Show toast notification
    this.showToast("ส่งเข้าครัวแล้ว - Your order has been sent to the kitchen");
    
    // Send data to Streamlit
    const totalItems = Object.values(this.state.cart).reduce(
      (sum, item) => sum + item.quantity, 
      0
    );
    
    const totalPrice = Object.values(this.state.cart).reduce(
      (sum, item) => sum + (item.price * item.quantity), 
      0
    );
    
    this.streamlit.setComponentValue({
      cart: this.state.cart,
      totalItems,
      totalPrice
    });
    
    // Clear cart after a short delay
    setTimeout(() => {
      this.state.cart = {};
      this.updateCartUI();
    }, 1000);
  },

  showToast(message) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.classList.remove("hidden");
    
    setTimeout(() => {
      toast.classList.add("hidden");
    }, 3000);
  }
};

// Tell Streamlit we're ready to start receiving data
window.parent.postMessage({
  type: "streamlit:componentReady",
  value: {}
}, "*");