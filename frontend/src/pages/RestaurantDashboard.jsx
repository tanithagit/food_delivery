import { useEffect, useState } from "react";
import api from "../api/axios";

const STATUS_OPTIONS = [
  "confirmed",
  "preparing",
  "out_for_delivery",
  "delivered",
  "canceled",
];

const STATUS_COLORS = {
  pending: "bg-yellow-100 text-yellow-700",
  confirmed: "bg-blue-100 text-blue-700",
  preparing: "bg-purple-100 text-purple-700",
  out_for_delivery: "bg-orange-100 text-orange-700",
  delivered: "bg-green-100 text-green-700",
  canceled: "bg-red-100 text-red-700",
};

export default function RestaurantDashboard() {
  const [restaurant, setRestaurant] = useState(null);
  const [menu, setMenu] = useState([]);
  const [orders, setOrders] = useState([]);
  const [newItem, setNewItem] = useState({
    name: "",
    description: "",
    price: "",
    is_available: true,
  });
  const [restaurantForm, setRestaurantForm] = useState({
    name: "",
    description: "",
    address: "",
  });
  const [message, setMessage] = useState("");
  const [activeTab, setActiveTab] = useState("orders");

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const rRes = await api.get("/restaurants/owner/me");
      setRestaurant(rRes.data);
      const mRes = await api.get(`/restaurants/${rRes.data.id}/menu`);
      setMenu(mRes.data);
      const oRes = await api.get("/orders/restaurant-orders");
      setOrders(oRes.data);
    } catch {
      setRestaurant(null);
    }
  };

  const createRestaurant = async (e) => {
    e.preventDefault();
    try {
      await api.post("/restaurants/", restaurantForm);
      setMessage("Restaurant created ✅");
      fetchDashboard();
    } catch (err) {
      setMessage(err.response?.data?.detail || "Error");
    }
  };

  const addMenuItem = async (e) => {
    e.preventDefault();
    try {
      await api.post("/restaurants/owner/menu", {
        ...newItem,
        price: parseFloat(newItem.price),
      });
      setNewItem({ name: "", description: "", price: "", is_available: true });
      setMessage("Menu item added ✅");
      const mRes = await api.get(`/restaurants/${restaurant.id}/menu`);
      setMenu(mRes.data);
    } catch (err) {
      setMessage(err.response?.data?.detail || "Error");
    }
  };

  const toggleAvailability = async (item) => {
    await api.put(`/restaurants/owner/menu/${item.id}`, {
      is_available: !item.is_available,
    });
    const mRes = await api.get(`/restaurants/${restaurant.id}/menu`);
    setMenu(mRes.data);
  };
  const updateOrderStatus = async (orderId, newStatus) => {
  try {
    console.log("Updating order", orderId, "to status", newStatus);
    const res = await api.put(`/orders/${orderId}/status`, { status: newStatus });
    console.log("Update response:", res.data);
    setMessage(`Order #${orderId} updated to ${newStatus} ✅`);
    const oRes = await api.get("/orders/restaurant-orders");
    setOrders(oRes.data);
  } catch (err) {
    console.error("Error:", err.response?.data);
    setMessage(err.response?.data?.detail || "Error updating status");
  }
};


  if (!restaurant) {
    return (
      <div className="max-w-xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Create Your Restaurant</h1>
        {message && (
          <div className="bg-green-100 text-green-700 p-3 rounded mb-4">
            {message}
          </div>
        )}
        <form onSubmit={createRestaurant} className="space-y-4 bg-white p-6 rounded-xl shadow">
          <input
            placeholder="Restaurant Name"
            value={restaurantForm.name}
            onChange={(e) => setRestaurantForm({ ...restaurantForm, name: e.target.value })}
            className="w-full border rounded px-3 py-2"
            required
          />
          <input
            placeholder="Description"
            value={restaurantForm.description}
            onChange={(e) => setRestaurantForm({ ...restaurantForm, description: e.target.value })}
            className="w-full border rounded px-3 py-2"
          />
          <input
            placeholder="Address"
            value={restaurantForm.address}
            onChange={(e) => setRestaurantForm({ ...restaurantForm, address: e.target.value })}
            className="w-full border rounded px-3 py-2"
          />
          <button
            type="submit"
            className="w-full bg-orange-500 text-white py-2 rounded font-semibold hover:bg-orange-600"
          >
            Create Restaurant
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        🍽️ {restaurant.name}
      </h1>
      <p className="text-gray-500 mb-6">{restaurant.address}</p>

      {message && (
        <div className="bg-green-100 text-green-700 p-3 rounded mb-4">
          {message}
        </div>
      )}

      <div className="flex gap-4 mb-6">
        {["orders", "menu", "add-item"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded font-semibold ${
              activeTab === tab
                ? "bg-orange-500 text-white"
                : "bg-gray-100 text-gray-700"
            }`}
          >
            {tab === "orders" ? "📦 Orders" : tab === "menu" ? "🍔 Menu" : "➕ Add Item"}
          </button>
        ))}
      </div>

      {activeTab === "orders" && (
        <div className="space-y-4">
          {orders.length === 0 ? (
            <p className="text-gray-500">No orders yet.</p>
          ) : (
            orders.map((order) => (
              <div key={order.id} className="bg-white rounded-xl shadow p-6">
                <div className="flex justify-between items-center mb-3">
                  <h2 className="font-bold text-gray-800">Order #{order.id}</h2>
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${STATUS_COLORS[order.status]}`}>
                    {order.status.replace(/_/g, " ").toUpperCase()}
                  </span>
                </div>
                <div className="space-y-1 mb-3">
                  {order.items.map((item) => (
                    <div key={item.id} className="flex justify-between text-sm text-gray-600">
                      <span>{item.item_name} x{item.quantity}</span>
                      <span>${(item.price * item.quantity).toFixed(2)}</span>
                    </div>
                  ))}
                </div>
                <div className="flex justify-between items-center border-t pt-3">
                  <span className="font-bold text-orange-500">
                    Total: ${order.total_amount.toFixed(2)}
                  </span>
                  <select
  defaultValue={order.status}
  onChange={(e) => {
    const newStatus = e.target.value;
    if (newStatus !== order.status) {
      updateOrderStatus(order.id, newStatus);
    }
  }}
  className="border rounded px-2 py-1 text-sm"
>
  <option value="pending">pending</option>
  <option value="confirmed">confirmed</option>
  <option value="preparing">preparing</option>
  <option value="out_for_delivery">out_for_delivery</option>
  <option value="delivered">delivered</option>
  <option value="canceled">canceled</option>
</select>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === "menu" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {menu.map((item) => (
            <div key={item.id} className="bg-white rounded-xl shadow p-4 flex justify-between items-center">
              <div>
                <h3 className="font-bold text-gray-800">{item.name}</h3>
                <p className="text-gray-500 text-sm">{item.description}</p>
                <p className="text-orange-500 font-semibold">${item.price.toFixed(2)}</p>
              </div>
              <button
                onClick={() => toggleAvailability(item)}
                className={`px-3 py-1 rounded text-sm font-semibold ${
                  item.is_available
                    ? "bg-green-100 text-green-700"
                    : "bg-red-100 text-red-700"
                }`}
              >
                {item.is_available ? "Available" : "Unavailable"}
              </button>
            </div>
          ))}
        </div>
      )}

      {activeTab === "add-item" && (
        <form onSubmit={addMenuItem} className="bg-white rounded-xl shadow p-6 space-y-4 max-w-md">
          <input
            placeholder="Item Name"
            value={newItem.name}
            onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
            className="w-full border rounded px-3 py-2"
            required
          />
          <input
            placeholder="Description"
            value={newItem.description}
            onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
            className="w-full border rounded px-3 py-2"
          />
          <input
            placeholder="Price"
            type="number"
            step="0.01"
            value={newItem.price}
            onChange={(e) => setNewItem({ ...newItem, price: e.target.value })}
            className="w-full border rounded px-3 py-2"
            required
          />
          <button
            type="submit"
            className="w-full bg-orange-500 text-white py-2 rounded font-semibold hover:bg-orange-600"
          >
            Add Menu Item
          </button>
        </form>
      )}
    </div>
  );
}