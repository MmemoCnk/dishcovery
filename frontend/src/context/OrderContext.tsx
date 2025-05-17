// src/context/OrderContext.tsx

import React, { createContext, useContext, useState } from 'react';
import { MenuItem, User, users } from '../data/menuItems';

// ประกาศ interface สำหรับรายการในตะกร้า
export interface CartItem extends MenuItem {
  quantity: number;
  remark?: string;
}

// ประกาศ interface สำหรับ OrderContext
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

// สร้าง Context
const OrderContext = createContext<OrderContextType | undefined>(undefined);

// OrderProvider component
export const OrderProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cart, setCart] = useState<Record<string, CartItem>>({});
  const [activeTab, setActiveTab] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [checkoutSuccess, setCheckoutSuccess] = useState(false);
  
  // ฟังก์ชันเข้าสู่ระบบ
  const login = (memberId: string, phone: string): boolean => {
    const user = users.find(u => u.id === memberId && u.phone === phone);
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
export const useOrder = () => {
  const context = useContext(OrderContext);
  if (context === undefined) {
    throw new Error("useOrder must be used within an OrderProvider");
  }
  return context;
};