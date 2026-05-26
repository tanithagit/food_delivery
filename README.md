#  Food Delivery SaaS Platform

A full-stack multi-role food delivery SaaS platform built with FastAPI and React. Customers can browse restaurants, place orders, and make payments. Restaurant owners can manage menus and update order status.

---

##  Tech Stack

### Backend
- **FastAPI** — Modern Python web framework
- **PostgreSQL** — Relational database
- **SQLAlchemy** — ORM for database models
- **JWT** — Secure authentication
- **Stripe** — Payment processing
- **FastAPI-Mail** — Email notifications

### Frontend
- **React (Vite)** — Frontend framework
- **Tailwind CSS** — Styling
- **React Router** — Client-side routing
- **Axios** — HTTP client

---

##  System Roles

| Role | Permissions |
|---|---|
|  Customer | Register, browse restaurants, add to cart, place orders, make payments, track orders |
|  Restaurant Owner | Register, create restaurant, manage menu items, view orders, update order status |

---

## 🗄️ Project Structure

food_delivery/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py         # App configuration
│   │   │   ├── security.py       # JWT & password hashing
│   │   │   └── dependencies.py   # Auth dependencies
│   │   ├── models/
│   │   │   ├── user.py           # User model
│   │   │   ├── restaurant.py     # Restaurant model
│   │   │   ├── menu_item.py      # MenuItem model
│   │   │   ├── cart.py           # Cart & CartItem models
│   │   │   ├── order.py          # Order & OrderItem models
│   │   │   └── payment.py        # Payment model
│   │   ├── schemas/
│   │   │   ├── user.py           # User schemas
│   │   │   ├── restaurant.py     # Restaurant schemas
│   │   │   ├── menu_item.py      # MenuItem schemas
│   │   │   ├── cart.py           # Cart schemas
│   │   │   ├── order.py          # Order schemas
│   │   │   └── payment.py        # Payment schemas
│   │   ├── routers/
│   │   │   ├── auth.py           # Auth endpoints
│   │   │   ├── restaurant.py     # Restaurant endpoints
│   │   │   ├── cart.py           # Cart endpoints
│   │   │   └── order.py          # Order endpoints
│   │   ├── services/
│   │   │   ├── auth_service.py       # Auth business logic
│   │   │   ├── restaurant_service.py # Restaurant business logic
│   │   │   ├── cart_service.py       # Cart business logic
│   │   │   ├── order_service.py      # Order business logic
│   │   │   ├── payment_service.py    # Stripe payment logic
│   │   │   └── email_service.py      # Email notification logic
│   │   ├── database.py           # Database connection
│   │   └── main.py               # FastAPI app entry point
│   ├── tests/
│   │   ├── conftest.py           # Test configuration & fixtures
│   │   ├── test_auth.py          # Auth tests
│   │   ├── test_restaurant.py    # Restaurant & role tests
│   │   ├── test_order_flow.py    # Order placement tests
│   │   ├── test_payment.py       # Payment flow tests
│   │   └── test_status.py        # Order status tests
│   ├── .env.example
│   ├── pytest.ini
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js          # Axios configuration
│   │   ├── components/
│   │   │   ├── Navbar.jsx        # Navigation bar
│   │   │   └── ProtectedRoute.jsx # Route protection
│   │   ├── context/
│   │   │   └── AuthContext.jsx   # Auth state management
│   │   ├── pages/
│   │   │   ├── Login.jsx         # Login page
│   │   │   ├── Register.jsx      # Register page
│   │   │   ├── Home.jsx          # Restaurants list
│   │   │   ├── RestaurantDetail.jsx # Restaurant menu
│   │   │   ├── Cart.jsx          # Shopping cart
│   │   │   ├── Payment.jsx       # Payment page
│   │   │   ├── OrderSuccess.jsx  # Order success page
│   │   │   ├── OrderTracking.jsx # Order tracking
│   │   │   └── RestaurantDashboard.jsx # Owner dashboard
│   │   └── App.jsx               # Routes configuration
│   └── package.json
│
└── README.md

---

##  Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL
- Stripe account (free test account at stripe.com)
- Gmail account (for email notifications)

---

### Backend Setup

**Step 1: Clone the repository**
```bash
git clone https://github.com/tanithagit/food_delivery.git
cd food_delivery
```

**Step 2: Create virtual environment**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Create PostgreSQL database**
```sql
CREATE DATABASE food_delivery;
```

**Step 5: Create .env file**
```bash
cp .env.example .env
```

Open `.env` and fill in your values:
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/food_delivery
SECRET_KEY=your-very-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
STRIPE_SECRET_KEY=sk_test_your_stripe_key_here
STRIPE_WEBHOOK_SECRET=whsec_placeholder
APP_NAME=FoodDelivery
DEBUG=True
MAIL_USERNAME=your_gmail@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_FROM=your_gmail@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
```

**Step 6: Run the backend**
```bash
uvicorn app.main:app --reload
```

Backend runs at: `http://127.0.0.1:8000`

API Docs at: `http://127.0.0.1:8000/docs`

---

### Frontend Setup

**Step 1: Install dependencies**
```bash
cd frontend
npm install
```

**Step 2: Run the frontend**
```bash
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

##  Order Flow Explanation

---

##  Order Lifecycle

Restaurant owner updates status in this strict order:

pending → confirmed → preparing → out_for_delivery → delivered

Or can cancel at any point:

pending/confirmed → canceled

Invalid transitions are blocked by the backend.

---

##  Payment Integration

This platform uses **Stripe** for secure payment processing.

### How it works:
1. Customer clicks **Proceed to Payment**
2. Backend validates cart and creates a **Stripe PaymentIntent**
3. Customer completes payment on the payment page
4. Backend verifies payment status with Stripe API
5. Order is created **only after** payment is verified as successful
6. Payment record is saved with Stripe PaymentIntent ID

### Stripe Test Mode:
- Use Stripe test key `sk_test_...` in your `.env` file
- No real money is charged in test mode

---

##  Authentication

- **JWT-based** authentication
- Tokens expire in **30 minutes**
- **Role-based access control** enforced on all endpoints
- Protected routes on both frontend and backend

### Roles:
- `customer` — can browse, cart, order, pay, track
- `restaurant_owner` — can manage restaurant, menu, update orders
- `admin` — (optional) monitor everything

---

##  API Endpoints

### Authentication
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | /auth/register | Public | Register new user |
| POST | /auth/login | Public | Login and get JWT token |

### Restaurants
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | /restaurants/ | Customer | List all active restaurants |
| GET | /restaurants/{id} | Customer | Get restaurant details |
| GET | /restaurants/{id}/menu | Customer | Get menu items |
| POST | /restaurants/ | Owner | Create restaurant |
| GET | /restaurants/owner/me | Owner | Get my restaurant |
| PUT | /restaurants/owner/me | Owner | Update my restaurant |
| POST | /restaurants/owner/menu | Owner | Add menu item |
| PUT | /restaurants/owner/menu/{id} | Owner | Update menu item |
| DELETE | /restaurants/owner/menu/{id} | Owner | Delete menu item |

### Cart
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | /cart/ | Customer | View cart |
| POST | /cart/ | Customer | Add item to cart |
| PUT | /cart/{id} | Customer | Update item quantity |
| DELETE | /cart/{id} | Customer | Remove item from cart |

### Orders
| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | /orders/checkout | Customer | Create Stripe PaymentIntent |
| POST | /orders/confirm | Customer | Confirm order after payment |
| GET | /orders/my-orders | Customer | View my orders |
| GET | /orders/restaurant-orders | Owner | View incoming orders |
| PUT | /orders/{id}/status | Owner | Update order status |

---

##  Running Tests

```bash
cd backend
pytest tests/ -v
```

### Test Coverage:
- ✅ User registration and login
- ✅ Duplicate email prevention
- ✅ Wrong password rejection
- ✅ Role-based access control
- ✅ Customer cannot access owner routes
- ✅ Owner cannot access customer routes
- ✅ Unauthenticated access blocked
- ✅ Cart operations
- ✅ Empty cart checkout prevention
- ✅ Full payment flow
- ✅ Cart cleared after order
- ✅ Order status lifecycle
- ✅ Invalid status transitions blocked

**Result: 27 tests passing ✅**

---

##  Critical Business Rules

- Customers cannot order unavailable menu items
- Cart can only contain items from one restaurant at a time
- Order is created **only after** payment is verified as successful
- Cart is automatically cleared after successful order
- Order status follows strict lifecycle — cannot skip steps
- All API endpoints are role-protected

---

##  Email Notifications

Emails are sent automatically for:
- **Order Confirmation** — when customer places an order
- **Status Updates** — when restaurant owner updates order status

### Setup Gmail:
1. Enable 2-Step Verification in Google Account
2. Go to `myaccount.google.com/apppasswords`
3. Create app password for "FoodDelivery"
4. Add credentials to `.env` file

---

##  Bonus Features Implemented

- ✅ Email notifications (order confirmation + status updates)
- ✅ Single restaurant cart validation
- ✅ Toggle menu item availability
- ✅ Clean role-based dashboard UI

---

##  Author

Built as part of Full-Stack SaaS assignment.

GitHub: https://github.com/tanithagit/food_delivery