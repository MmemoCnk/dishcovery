// src/data/menuItems.ts

// ประกาศ interface สำหรับเมนูอาหาร
export interface MenuItem {
    name: string;
    price: number;
  }
  
  // ประกาศ interface สำหรับข้อมูลคำแนะนำ
  export interface RecommendationItem {
    name: string;
    quantity: number;
  }
  
  // ข้อมูลเมนูอาหาร
  export const menuItems: Record<string, MenuItem[]> = {
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
  
  // ข้อมูลคำแนะนำ
  export const recommendations: RecommendationItem[] = [
    { name: "Omelette (new)", quantity: 100 },
    { name: "Fries Pork with Garlic", quantity: 99 },
    { name: "Som Tam", quantity: 80 },
    { name: "Satay", quantity: 30 },
    { name: "test1", quantity: 30 },
    { name: "test2", quantity: 30 }
  ];
  
  // ข้อมูลผู้ใช้ตัวอย่าง
  export interface User {
    id: string;
    phone: string;
    name: string;
    surname: string;
    favoriteDishes?: string[];
    allergicFood?: string[];
  }
  
  export const users: User[] = [
    { 
      id: "12345", 
      phone: "0891234567", 
      name: "John", 
      surname: "Doe", 
      favoriteDishes: ["Pad Thai", "Tom Yum"], 
      allergicFood: ["Peanuts"] 
    }
  ];