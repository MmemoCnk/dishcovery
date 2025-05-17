
import { useOrder } from "../context/OrderContext";
import { recommendations } from "../data/menuItems";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

export default function RecommendationPanel() {
  const { loggedIn, currentUser } = useOrder();
  
  return (
    <div className="flex flex-col gap-4">
      {/* Favorite Dishes */}
      <Card className="mb-2">
        <CardHeader className="pb-2 bg-gray-200">
          <CardTitle className="text-center text-lg text-gray-800">Favorite Dishes</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 pt-3">
          {loggedIn && currentUser?.favoriteDishes ? (
            currentUser.favoriteDishes.map((dish, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded-md">
                {dish}
              </div>
            ))
          ) : (
            <div className="text-gray-500">No favorite dishes available</div>
          )}
        </CardContent>
      </Card>
      
      {/* Recommendations */}
      <Card className="mb-2">
        <CardHeader className="pb-2 bg-gray-200">
          <CardTitle className="text-center text-lg text-gray-800">Recommendation</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 pt-3">
          {recommendations.map((rec, index) => (
            <div key={index} className="bg-gray-50 p-3 rounded-md flex justify-between">
              <span>{rec.name}</span>
              <span>{rec.quantity}</span>
            </div>
          ))}
        </CardContent>
      </Card>
      
      {/* Allergic Food */}
      <Card>
        <CardHeader className="pb-2 bg-gray-200">
          <CardTitle className="text-center text-lg text-gray-800">Allergic Food</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 pt-3">
          {loggedIn && currentUser?.allergicFood ? (
            currentUser.allergicFood.map((allergen, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded-md">
                {allergen}
              </div>
            ))
          ) : (
            <div className="text-gray-500">No allergic food information available</div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
