import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Home() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    api.get("/restaurants/").then((res) => {
      setRestaurants(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="text-center mt-20">Loading...</div>;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        🍽️ All Restaurants
      </h1>
      {restaurants.length === 0 ? (
        <p className="text-gray-500">No restaurants available yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {restaurants.map((r) => (
            <div
              key={r.id}
              onClick={() => navigate(`/restaurants/${r.id}`)}
              className="bg-white rounded-xl shadow-md p-6 cursor-pointer hover:shadow-lg hover:border-orange-400 border-2 border-transparent transition"
            >
              <h2 className="text-xl font-bold text-gray-800">{r.name}</h2>
              <p className="text-gray-500 mt-1">{r.description}</p>
              <p className="text-gray-400 text-sm mt-2">📍 {r.address}</p>
              <span className="mt-3 inline-block bg-green-100 text-green-600 text-xs px-2 py-1 rounded">
                Open
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}