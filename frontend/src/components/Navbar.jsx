import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-orange-500 text-white px-6 py-4 flex justify-between items-center shadow-md">
      <Link to="/" className="text-2xl font-bold">
        🍔 FoodDelivery
      </Link>
      <div className="flex items-center gap-4">
        {user ? (
          <>
            <span className="text-sm">
              Hello, {user.full_name} ({user.role})
            </span>
            {user.role === "customer" && (
              <>
                <Link to="/restaurants" className="hover:underline">
                  Restaurants
                </Link>
                <Link to="/cart" className="hover:underline">
                  🛒 Cart
                </Link>
                <Link to="/my-orders" className="hover:underline">
                  My Orders
                </Link>
              </>
            )}
            {user.role === "restaurant_owner" && (
              <Link to="/dashboard" className="hover:underline">
                Dashboard
              </Link>
            )}
            <button
              onClick={handleLogout}
              className="bg-white text-orange-500 px-3 py-1 rounded font-semibold hover:bg-orange-100"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:underline">
              Login
            </Link>
            <Link to="/register" className="hover:underline">
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}