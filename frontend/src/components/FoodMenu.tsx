
import { useState } from "react";
import { useOrder } from "../context/OrderContext";
import { menuItems, MenuItem } from "../data/menuItems";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "./ui/dialog";
import { Plus, Minus } from "lucide-react";
import { Tabs, TabsList, TabsTrigger } from "./ui/tabs";

export default function FoodMenu() {
  const { 
    addToCart, 
    removeFromCart,
    cart,
    activeTab, 
    setActiveTab,
    searchQuery,
    setSearchQuery
  } = useOrder();
  
  const [selectedItem, setSelectedItem] = useState<MenuItem | null>(null);
  const [remark, setRemark] = useState("");
  
  const handleAddToCart = (item: MenuItem, withRemark: boolean = false) => {
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
  
  // Filter items based on search query or active tab
  const displayItems: MenuItem[] = searchQuery
    ? Object.values(menuItems).flat().filter(item => 
        item.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : activeTab === "All"
    ? Object.values(menuItems).flat()
    : menuItems[activeTab] || [];
  
  // Get all category tabs
  const categoryTabs = ["All", ...Object.keys(menuItems)];

  return (
    <div className="h-full flex flex-col">
      {/* Search Bar */}
      <div className="mb-4 relative">
        <Input
          placeholder="Search"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-8"
        />
        <span className="absolute left-2 top-2.5 text-gray-500">🔍</span>
      </div>
      
      {/* Category Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="mb-4">
        <TabsList className="w-full grid grid-cols-6 h-10">
          {categoryTabs.map((category) => (
            <TabsTrigger
              key={category}
              value={category}
              className="text-sm"
            >
              {category}
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>
      
      {/* Food Items */}
      <div className="flex-1 overflow-auto mb-4 pr-2">
        {displayItems.map((item) => {
          const quantity = cart[item.name]?.quantity || 0;
          
          return (
            <div 
              key={item.name} 
              className="flex items-center mb-4 bg-white p-3 rounded-md cursor-pointer"
              onClick={() => handleAddToCart(item, true)}
            >
              <div className="w-16 h-16 bg-gray-100 mr-3 flex items-center justify-center rounded-md overflow-hidden">
                🍽️
              </div>
              
              <div className="flex-1 font-medium">{item.name}</div>
              
              <div className="flex items-center">
                <Button 
                  variant="outline" 
                  size="icon"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleRemoveFromCart(item.name);
                  }}
                  disabled={quantity === 0}
                  className="rounded-full h-8 w-8"
                >
                  <Minus size={16} />
                </Button>
                <span className="mx-3 w-6 text-center">{quantity}</span>
                <Button 
                  variant="outline" 
                  size="icon"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleAddToCart(item);
                  }}
                  className="rounded-full h-8 w-8"
                >
                  <Plus size={16} />
                </Button>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Remark Dialog */}
      <Dialog open={selectedItem !== null} onOpenChange={(open) => !open && setSelectedItem(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Remark for {selectedItem?.name}</DialogTitle>
          </DialogHeader>
          <div className="py-4">
            <Input
              placeholder="Enter your remark here..."
              value={remark}
              onChange={(e) => setRemark(e.target.value)}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setSelectedItem(null)}>
              Cancel
            </Button>
            <Button onClick={handleSubmitRemark}>Submit</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
