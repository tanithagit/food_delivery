import { useEffect, useState } from "react";
import api from "../api/axios";

const STATUS_COLORS = {
  pending: "bg-yellow-100 text-yellow-700",
  confirmed: "bg-blue-100 text-blue-700",
  preparing: "bg-purple-100 text-purple-700",
  out_for_delivery: "bg-orange-100 text-orange-700",
  delivered: "bg-green-100 text-green-700",
  canceled: "bg-red-100 text-red-700",
};

export default function OrderTracking() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/orders/my-orders").then((res) => {
      setOrders(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="text-center mt-20">Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">📦 My Orders</h1>
      {orders.length === 0 ? (
        <p className="text-gray-500">No orders yet.</p>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => (
            <div key={order.id} className="bg-white rounded-xl shadow p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-bold text-gray-800">
                  Order #{order.id}
                </h2>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    STATUS_COLORS[order.status]
                  }`}
                >
                  {order.status.replace(/_/g, " ").toUpperCase()}
                </span>
              </div>
              <div className="space-y-1 mb-4">
                {order.items.map((item) => (
                  <div
                    key={item.id}
                    className="flex justify-between text-sm text-gray-600"
                  >
                    <span>{item.item_name} x{item.quantity}</span>
                    <span>${(item.price * item.quantity).toFixed(2)}</span>
                  </div>
                ))}
              </div>
              <div className="flex justify-between font-bold text-gray-800 border-t pt-3">
                <span>Total</span>
                <span className="text-orange-500">
                  ${order.total_amount.toFixed(2)}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}