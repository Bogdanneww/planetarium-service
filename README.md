# 🌌 Planetarium Service

**Planetarium Service** is a backend service built with **Django REST Framework** for managing a planetarium's operations.  
It covers all aspects — from astronomy shows and domes to sessions, tickets, and reservations.

This project demonstrates a **complete CRUD architecture**, **custom access permissions**, and **automated API testing**.

---

## ✨ Core Features
- **Planetarium Domes** — Manage domes, sizes, and seating capacities.
- **Astronomy Shows** — Create, edit, and view show details.
- **Show Sessions** — Schedule sessions with unique dome/time validation.
- **Reservations** — Users can book tickets for sessions.
- **Tickets** — Manage tickets linked to reservations.
- **Show Themes** — Organize shows by specific themes.

---

## 🚀 Technologies
- **Backend:** Python 3.12+
- **Framework:** Django 5.2
- **API:** Django REST Framework 3.16
- **Documentation:** drf-spectacular (OpenAPI)
- **Testing:** pytest & unittest
- **Additional:** Pillow, python-dotenv

---

## 🔒 Access Permissions
- **Admin** — Full CRUD access for all models.  
- **Authenticated User** — Read-only access to public data + ability to create their own reservations.  
- **Guest** — Read-only access to public endpoints.  

---

## 📄 API Documentation
If **drf-spectacular** is enabled, you can access the API docs at:
- **OpenAPI Schema:** `/api/schema/`
- **Swagger UI:** `/api/docs/`

---

## 📥 Installation & Run

### Local Run (without Docker)
1. Clone the repository:
   ```bash
   git clone https://github.com/Bogdanneww/planetarium-service.git
   cd planetarium-service
   
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux / Mac
   .venv\Scripts\activate     # Windows

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Create a .env file (see .env.example for reference) and set up your database credentials.
   
5. Apply migrations:
   ```bash
   python manage.py migrate
   
6. Run the server:
   ```bash
   python manage.py runserver

### Run with Docker

1. Install dependencies:
   ```bash
   git clone https://github.com/Bogdanneww/planetarium-service.git
   cd planetarium-service
   
2. Create a .env file based on .env.example.
   
3. Start the containers:
   ```bash
   docker-compose up --build
   
4. The API will be available at:
   ```bash
   http://127.0.0.1:8001/api/v1/planetarium/
   
5. To run without cache:
   ```bash
   docker-compose down --volumes --remove-orphans
   docker-compose build --no-cache
   docker-compose up

🔑 Getting Access

Register a new user http://127.0.0.1:8000//user/register/.

Log in and obtain a token http://127.0.0.1:8000//user/token/.

Add the following header to your requests:
   ```bash
   Authorization: Token <your_token>
