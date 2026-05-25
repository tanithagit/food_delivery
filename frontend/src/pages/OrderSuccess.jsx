import { useLocation, useNavigate } from "react-router-dom";

export default function OrderSuccess() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const order = state?.order;

  return (
    <div className="min-h-screen bg-orange-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md text-center">
        <div className="text-6xl mb-4">🎉</div>
        <h2 className="text-2xl font-bold text-green-600 mb-2">
          Order Placed Successfully!
        </h2>
        <p className="text-gray-600 mb-4">
          Order #{order?.id} has been placed. Total: $
          {order?.total_amount?.toFixed(2)}
        </p>
        <div className="bg-gray-50 rounded p-4 text-left mb-6">
          <p className="font-semibold text-gray-700 mb-2">Order Items:</p>
          {order?.items?.map((item) => (
            <div key={item.id} className="flex justify-between text-sm text-gray-600">
              <span>{item.item_name} x{item.quantity}</span>
              <span>${(item.price * item.quantity).toFixed(2)}</span>
            </div>
          ))}
        </div>
        <button
          onClick={() => navigate("/my-orders")}
          className="w-full bg-orange-500 text-white py-2 rounded font-semibold hover:bg-orange-600"
        >
          Track My Orders
        </button>
      </div>
    </div>
  );
}