import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/axios";

export default function RestaurantDetail() {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [menu, setMenu] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    Promise.all([
      api.get(`/restaurants/${id}`),
      api.get(`/restaurants/${id}/menu`),
    ]).then(([rRes, mRes]) => {
      setRestaurant(rRes.data);
      setMenu(mRes.data);
      setLoading(false);
    });
  }, [id]);

  const addToCart = async (menuItemId) => {
    try {
      await api.post("/cart/", { menu_item_id: menuItemId, quantity: 1 });
      setMessage("Item added to cart ✅");
      setTimeout(() => setMessage(""), 2000);
    } catch (err) {
      setMessage(err.response?.data?.detail || "Error adding to cart");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  if (loading) return <div className="text-center mt-20">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800">{restaurant.name}</h1>
      <p className="text-gray-500 mt-1">{restaurant.description}</p>
      <p className="text-gray-400 text-sm">📍 {restaurant.address}</p>

      {message && (
        <div className="mt-4 bg-green-100 text-green-700 p-3 rounded">
          {message}
        </div>
      )}

      <h2 className="text-2xl font-bold mt-8 mb-4">Menu</h2>
      {menu.length === 0 ? (
        <p className="text-gray-500">No menu items yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {menu.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-xl shadow p-4 flex justify-between items-center"
            >
              <div>
                <h3 className="font-bold text-gray-800">{item.name}</h3>
                <p className="text-gray-500 text-sm">{item.description}</p>
                <p className="text-orange-500 font-semibold mt-1">
                  ${item.price.toFixed(2)}
                </p>
                {!item.is_available && (
                  <span className="text-red-500 text-xs">Not available</span>
                )}
              </div>
              <button
                onClick={() => addToCart(item.id)}
                disabled={!item.is_available}
                className="bg-orange-500 text-white px-3 py-2 rounded hover:bg-orange-600 disabled:opacity-40"
              >
                Add
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}