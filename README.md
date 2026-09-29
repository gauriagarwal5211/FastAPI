# FastAPI Application-Based Practical Assessment

A FastAPI-based practical assessment containing two REST API applications using FastAPI, SQLModel, and SQLite.

## Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite
- Pydantic
- Uvicorn

## Project Structure

```text
FastAPI_Assessment/
│
├── task1/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── task2/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── screenshots/
│   ├── [Task 1 screenshots]
│   └── task2/
│       └── [Task 2 screenshots]
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Task 1 — Campus Lost & Found API

A REST API for managing lost and found items on a college campus.

## Task 1 Features

- Create lost/found item reports
- View all reported items
- View a specific item by ID
- Update item details and status
- Delete item reports
- Filter items by status
- Filter items by category
- Input validation
- Error handling for missing items
- SQLite database using SQLModel

## Task 1 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/items` | Create a new item |
| GET | `/items` | Get all items |
| GET | `/items/{item_id}` | Get an item by ID |
| PUT | `/items/{item_id}` | Update an item |
| DELETE | `/items/{item_id}` | Delete an item |
| GET | `/items/status/{status}` | Filter items by status |
| GET | `/items/category/{category}` | Filter items by category |

## Task 1 Validation

- Title cannot be empty.
- Description must contain meaningful text.
- Status accepts `Lost`, `Found`, or `Returned`.
- Required fields are validated.
- Appropriate HTTP errors are returned when an item does not exist.

---

# Task 2 — Campus Event Seat Reservation API

A REST API for managing college events and student seat reservations.

## Task 2 Features

- Create and manage campus events
- View all events
- View a specific event
- Update event information
- Delete events
- Create student reservations
- View reservations for an event
- Cancel reservations
- Check event seat availability
- Prevent reservations when an event is full
- Prevent reservations when an event is closed
- Validate event capacity
- Validate student information and email
- SQLite database using SQLModel

## Task 2 API Endpoints

### Event APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events` | Create a new event |
| GET | `/events` | Get all events |
| GET | `/events/{event_id}` | Get an event by ID |
| PUT | `/events/{event_id}` | Update an event |
| DELETE | `/events/{event_id}` | Delete an event |

### Reservation APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events/{event_id}/reserve` | Create a reservation |
| GET | `/events/{event_id}/reservations` | Get event reservations |
| DELETE | `/reservations/{reservation_id}` | Cancel a reservation |
| GET | `/events/{event_id}/availability` | Check seat availability |

## Task 2 Business Logic

Before creating a reservation, the API:

1. Checks whether the event exists.
2. Checks whether the event is open.
3. Counts existing reservations.
4. Checks the event capacity.
5. Rejects the reservation if the event is full.
6. Creates the reservation if seats are available.

## Task 2 Validation

- Event capacity must be greater than zero.
- Event title, venue, and organizer cannot be empty.
- Student name cannot be empty.
- Roll number cannot be empty.
- Email format is validated.
- Reservation must reference an existing event.
- Reservations are not allowed for closed events.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/gauriagarwal5211/FastAPI.git
cd FastAPI
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## 4. Run Task 1

From the project root:

```powershell
uvicorn task1.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Stop the server with:

```text
Ctrl + C
```

## 5. Run Task 2

From the project root:

```powershell
uvicorn task2.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Database

Both applications use SQLite and SQLModel.

The database engine is created using:

```python
create_engine()
```

Database tables are automatically created when the respective FastAPI application starts.

## API Testing

The APIs were tested using FastAPI Swagger UI.

The `screenshots` directory contains screenshots demonstrating successful API execution and error/validation handling for the assessment requirements.

## GitHub Repository

Source code, configuration files, and API execution screenshots are included in this repository.