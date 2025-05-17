
import { useState } from "react";
import { useOrder } from "../context/OrderContext";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

export default function CustomerInfo() {
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

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="text-3xl font-bold text-center">&nbsp;</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {!loggedIn && (
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Please Input Customer ID</h2>
            <Input
              placeholder="Member ID"
              value={memberId}
              onChange={(e) => setMemberId(e.target.value)}
            />
            <Input
              placeholder="Tel number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
            <Button onClick={handleLogin} className="w-full">
              Enter
            </Button>
          </div>
        )}

        <div className="space-y-4 pt-4">
          <h2 className="text-xl font-semibold">Customer Information</h2>
          <Input 
            placeholder="Name" 
            value={currentUser?.name || ""} 
            disabled
          />
          <Input 
            placeholder="Surname" 
            value={currentUser?.surname || ""} 
            disabled
          />
          <Input 
            placeholder="Date & Time" 
            value={currentDate} 
            disabled
          />
        </div>
      </CardContent>
    </Card>
  );
}
