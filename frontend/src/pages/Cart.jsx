import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Cart() {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [checkoutLoading, setCheckoutLoading] = useState(false);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const fetchCart = async () => {
    const res = await api.get("/cart/");
    setCart(res.data);
    setLoading(false);
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const removeItem = async (cartItemId) => {
    await api.delete(`/cart/${cartItemId}`);
    fetchCart();
  };

  const updateQuantity = async (cartItemId, quantity) => {
    if (quantity < 1) return;
    await api.put(`/cart/${cartItemId}`, { quantity });
    fetchCart();
  };

  const handleCheckout = async () => {
    setCheckoutLoading(true);
    try {
      const res = await api.post("/orders/checkout");
      navigate("/payment", {
        state: {
          clientSecret: res.data.client_secret,
          paymentIntentId: res.data.payment_intent_id,
          amount: res.data.amount,
        },
      });
    } catch (err) {
      setMessage(err.response?.data?.detail || "Checkout failed");
    } finally {
      setCheckoutLoading(false);
    }
  };

  if (loading) return <div className="text-center mt-20">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">🛒 Your Cart</h1>
      {message && (
        <div className="bg-red-100 text-red-600 p-3 rounded mb-4">{message}</div>
      )}
      {cart.items.length === 0 ? (
        <p className="text-gray-500">Your cart is empty.</p>
      ) : (
        <>
          <div className="space-y-4">
            {cart.items.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-xl shadow p-4 flex justify-between items-center"
              >
                <div>
                  <h3 className="font-bold text-gray-800">{item.item_name}</h3>
                  <p className="text-orange-500">${item.item_price.toFixed(2)}</p>
                </div>
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    className="bg-gray-200 px-2 py-1 rounded"
                  >
                    -
                  </button>
                  <span>{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    className="bg-gray-200 px-2 py-1 rounded"
                  >
                    +
                  </button>
                  <button
                    onClick={() => removeItem(item.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 bg-white rounded-xl shadow p-4">
            <div className="flex justify-between text-xl font-bold">
              <span>Total</span>
              <span className="text-orange-500">${cart.total.toFixed(2)}</span>
            </div>
            <button
              onClick={handleCheckout}
              disabled={checkoutLoading}
              className="w-full mt-4 bg-orange-500 text-white py-3 rounded-xl font-semibold hover:bg-orange-600 disabled:opacity-50"
            >
              {checkoutLoading ? "Processing..." : "Proceed to Payment"}
            </button>
          </div>
        </>
      )}
    </div>
  );
}