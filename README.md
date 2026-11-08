# FinTrack - Personal Finance Tracker (MERN Stack)

A modern, responsive, and full-featured **Personal Finance Tracking Web Application** built using MongoDB, Express.js, React, Node.js, and Tailwind CSS.

---

## 🚀 Features

- **Authentication & Security**
  - JWT Authentication stored securely in HTTP-only cookies
  - Password encryption with bcryptjs
  - Protected API routes and protected frontend route guards
  - Helmet security headers and rate limiting

- **Interactive Dashboard**
  - KPI Cards: Net Balance, Total Income, Total Expenses, and Savings Rate
  - Income vs Expenses cash flow Area Chart (Recharts)
  - Category Expense Breakdown Donut Chart
  - Recent transactions list with quick action to add new transactions
  - Dynamic timeframe filters (This Month, Last Month, This Year, All Time)

- **Transaction Management**
  - Paginated transactions table
  - Advanced multi-filter system: Type (Income/Expense), Category, Payment Method, Date Range
  - Real-time search and sorting (Newest, Oldest, Highest, Lowest Amount)
  - Add & Edit transaction modals with full validation
  - Safe delete confirmations

- **Budget Planner**
  - Category-based budget limits (Weekly, Monthly, Yearly)
  - Real-time spending calculation & remaining balance tracking
  - Visual status alerts: **On track** (Green), **Warning >80%** (Amber), and **Exceeded** (Red)

- **Financial Analytics**
  - Monthly income vs expense comparative bar charts
  - Multi-month net savings trendline
  - Categorical distribution & share percentage breakdown

- **Savings Goals**
  - Visual target tracking with custom color themes
  - Contribution and withdrawal ledger records
  - Automated status completion when target reached

- **Account Settings**
  - Edit profile name and email
  - Secure password reset
  - Custom category creator and manager

- **🛡️ Dedicated Administrator Command Center (`/admin`)**
  - **System Overview Dashboard:** Platform-wide gross volume inflow/outflow, registered users count, and monthly cash flow telemetry.
  - **User Directory Management:** Search users, toggle active/suspended status, promote/demote administrator roles, or permanently delete accounts with cascade cleanup.
  - **Global Transactions Audit:** Real-time system-wide transaction monitor across all accounts with search, type filters, and delete moderation.
  - **Category Master:** Add and manage system-wide default categories seeded to all users with custom palettes.
  - **System Telemetry & Health:** Real-time Node.js runtime stats, heap memory consumption, MongoDB connection state, and live API ping latency test.
  - **Distinct Admin Theme:** Dark Command Center styling with indigo/violet accents and seamless 1-click switching to the User Portal.

---

## 🛠️ Tech Stack

- **Frontend**: React 19, Vite, Tailwind CSS 4, React Router 7, Recharts, Lucide React, React Hook Form, React Hot Toast, Axios
- **Backend**: Node.js, Express 5, Mongoose 9, JWT, bcryptjs, Helmet, Express-Rate-Limit, Cookie-Parser
- **Database**: MongoDB (Local or MongoDB Atlas)

---

## 📦 Project Structure

```
Project/
├── client/                 # React + Vite Frontend
│   ├── src/
│   │   ├── components/     # Reusable UI & Modals
│   │   ├── context/        # Auth Context
│   │   ├── layouts/        # Dashboard Layout & Sidebar
│   │   ├── pages/          # Dashboard, Transactions, Budgets, Analytics, Goals, Settings
│   │   ├── services/       # Axios API client
│   │   └── utils/          # Currency formatters, date helpers
│   └── package.json
├── server/                 # Express REST API
│   ├── config/             # MongoDB connection
│   ├── controllers/        # Business logic controllers
│   ├── middleware/         # Auth, validation, error handler
│   ├── models/             # Mongoose schemas (User, Transaction, Budget, SavingsGoal, etc.)
│   ├── routes/             # Express API routes
│   ├── utils/              # Seed script
│   ├── tests/              # Jest test suite
│   └── package.json
└── README.md
```

---

## 🏃 Getting Started

### 1. Prerequisites
- Node.js (v18+)
- MongoDB running locally or a MongoDB Atlas URI

### 2. Backend Setup
```bash
cd server
cp .env.example .env
npm install
```

Make sure your `.env` contains:
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/fintrack
JWT_SECRET=your_jwt_secret_key_here
CLIENT_URL=http://localhost:5173
```

#### Seed Demo Data (Optional)
Populate sample categories, transactions, budgets, and savings goals:
```bash
npm run seed
```
> **Available Accounts & Credentials:**
> | Profile | Email | Password | Role / Access |
> |---|---|---|---|
> | **👑 System Administrator** | `admin@fintrack.com` | `Admin@123456` | **Administrator (`/admin`)** |
> | **Chauhan Om S.** | `om40@gmail.com` | `demo123456` | **Administrator (`/admin` + `/`)** |
> | **Rahul Sharma** | `demo@fintrack.com` | `demo123456` | Standard User |
> | **Priya Patel** | `priya@fintrack.com` | `priya123456` | Standard User |

#### Start Backend Server
```bash
npm run dev
# or for production:
npm start
```

### 3. Frontend Setup
```bash
cd client
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Testing

Run backend tests:
```bash
cd server
npm test
```

Build production client:
```bash
cd client
npm run build
```
