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
