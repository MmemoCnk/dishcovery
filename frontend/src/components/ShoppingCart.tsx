
import { Card, CardContent, CardHeader } from "./ui/card";
import { Separator } from "./ui/separator";
import { Button } from "./ui/button";
import { X } from "lucide-react";
import { useOrder } from "../context/OrderContext";

interface ShoppingCartProps {
  onClose: () => void;
}

export default function ShoppingCart({ onClose }: ShoppingCartProps) {
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
    <Card className="w-72 shadow-lg">
      <CardHeader className="pb-2 flex flex-row items-center justify-between">
        <h3 className="font-bold text-lg">Shopping Cart</h3>
        <Button variant="ghost" size="icon" onClick={onClose}>
          <X size={18} />
        </Button>
      </CardHeader>
      <Separator />
      <CardContent className="space-y-4 max-h-96 overflow-auto py-4">
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
            <Separator className="my-2" />
            <div className="font-bold flex justify-between">
              <span>Total:</span>
              <span>฿{totalCartPrice}</span>
            </div>
            <Button onClick={handleCheckout} className="w-full mt-2">
              Checkout
            </Button>
          </>
        ) : (
          <div className="py-4 text-center text-gray-500">Your cart is empty</div>
        )}
      </CardContent>
    </Card>
  );
}
