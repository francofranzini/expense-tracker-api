# Expense Tracker API

A REST API for personal and business expense tracking, built with FastAPI and PostgreSQL. Features JWT authentication, categorized spending, and KPI summaries.

🔗 **Live API:** [expense-tracker-api-production-9d6b.up.railway.app/docs](https://expense-tracker-api-production-9d6b.up.railway.app/docs)

---

## Features

- User registration and authentication with JWT
- Create, read, update, and delete expenses
- Fixed expense categories with validation
- Filter expenses by category and date range
- Paginated expense listing with total count and `has_more` flag
- KPI summaries: total spending, count, and average
- Spending breakdown by category
- Passwords stored with bcrypt hashing
- Auto-generated Swagger documentation
- Docker support for local development

---

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose) + bcrypt (passlib)
- **Testing:** pytest + TestClient
- **Containerization:** Docker + Docker Compose
- **Deployment:** Railway

---

## Getting Started

### Option 1 — Docker (recommended)

```bash
# Clone the repository
git clone https://github.com/francofranzini/expense-tracker-api.git
cd expense-tracker-api

# Create a .env file
echo "SECRET_PASSKEY=your_secret_key" > .env

# Start the API and database
docker compose up --build
```

API will be available at `http://localhost:8000/docs`

### Option 2 — Manual setup

#### Prerequisites

- Python 3.10+
- PostgreSQL

```bash
# Clone the repository
git clone https://github.com/francofranzini/expense-tracker-api.git
cd expense-tracker-api

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Environment Variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/expense_tracker
SECRET_PASSKEY=your_secret_key
```

#### Run the API

```bash
uvicorn app.main:app --reload
```

API will be available at `http://127.0.0.1:8000/docs`

---

## Running Tests

```bash
# Requires a test database — add to your .env:
# TEST_DATABASE_URL=postgresql://postgres:your_password@localhost:5432/expense_tracker_test

pytest -v
```

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/create` | Register a new user |
| POST | `/users/login` | Login and receive JWT token |

### Expenses
| Method | Endpoint         | Description                              | Auth |
|--------|------------------|------------------------------------------|------|
| GET    | `/expenses/`     | List expenses (paginated, with filters)  | ✅   |
| POST   | `/expenses/`     | Create a new expense                     | ✅   |
| GET    | `/expenses/{id}` | Get expense by ID                        | ✅   |
| PUT    | `/expenses/{id}` | Update an expense (partial)              | ✅   |
| DELETE | `/expenses/{id}` | Delete an expense                        | ✅   |

#### GET /expenses — Query Parameters

| Parameter   | Type   | Default | Description                        |
|-------------|--------|---------|------------------------------------|
| `skip`      | int    | 0       | Number of records to skip          |
| `limit`     | int    | 20      | Max records to return (max: 100)   |
| `category`  | string | —       | Filter by category                 |
| `date_from` | date   | —       | Filter expenses from this date     |
| `date_to`   | date   | —       | Filter expenses up to this date    |

**Response:**
```json
{
  "items": [...],
  "total": 42,
  "skip": 0,
  "limit": 20,
  "has_more": true
}
```

### Analytics
| Method | Endpoint                        | Description                    | Auth |
|--------|---------------------------------|--------------------------------|------|
| GET    | `/expenses/summary`             | Total, count, and average      | ✅   |
| GET    | `/expenses/summary/by-category` | Spending breakdown by category | ✅   |

### Expense Categories

`food` · `transport` · `operations` · `utilities` · `entertainment` · `other`

---

## Project Structure

```
expense-tracker-api/
├── app/
│   ├── main.py          # App entry point
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # JWT authentication
│   └── routers/
│       ├── expenses.py  # Expense endpoints
│       └── users.py     # User endpoints
├── tests/
│   ├── conftest.py      # Fixtures and test DB setup
│   ├── test_expenses.py # Expense endpoint tests
│   └── test_users.py    # User endpoint tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Procfile
└── .env
```

---

## Author

Franco Franzini · [github.com/francofranzini](https://github.com/francofranzini)
