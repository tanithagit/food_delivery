import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Payment() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!state) {
    navigate("/cart");
    return null;
  }

  const { clientSecret, paymentIntentId, amount } = state;

  const handleTestPayment = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.post("/orders/confirm", {
        payment_intent_id: paymentIntentId,
      });
      navigate("/order-success", { state: { order: res.data } });
    } catch (err) {
      setError(err.response?.data?.detail || "Payment confirmation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-orange-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          💳 Complete Payment
        </h2>
        <p className="text-gray-500 mb-6">
          Amount to pay:{" "}
          <span className="text-orange-500 font-bold">${amount?.toFixed(2)}</span>
        </p>

        <div className="bg-yellow-50 border border-yellow-300 p-4 rounded mb-6">
          <p className="text-yellow-800 font-semibold">🧪 Test Mode</p>
          <p className="text-yellow-700 text-sm mt-1">
            This is using Stripe test mode. Click the button below to simulate
            a successful payment.
          </p>
        </div>

        {error && (
          <div className="bg-red-100 text-red-600 p-3 rounded mb-4">{error}</div>
        )}

        <button
          onClick={handleTestPayment}
          disabled={loading}
          className="w-full bg-orange-500 text-white py-3 rounded-xl font-semibold hover:bg-orange-600 disabled:opacity-50"
        >
          {loading ? "Processing..." : "Pay Now (Test Mode)"}
        </button>
      </div>
    </div>
  );
}