# 🧩 Social Media API — Work in Progress

A **FastAPI-based backend** for a social media application designed with scalability, modularity, and clean architecture in mind.
The project currently implements core features like **user authentication (JWT)**, **secure password hashing**, **CRUD operations for posts**, and a **voting system** where users can upvote or remove their votes on posts.

---

## 🚀 Features

* **User Authentication & Authorization**

  * JWT-based token generation and verification
  * Secure password hashing and validation
* **Posts Management**

  * Create, read, update, and delete posts
  * Each post linked to its author via SQLAlchemy ORM
* **Voting System**

  * Users can vote (like/unlike) posts
  * Enforced one-vote-per-user logic
* **Database Layer**

  * SQLAlchemy 2.0 with `DeclarativeBase`
  * PostgreSQL via Docker container
  * Dependency-injected database sessions using `Depends`
* **API Design**

  * Modular router structure (`users`, `posts`, `votes`, `auth`)
  * Pydantic schemas for validation and clean response models

---

## 🛠️ Tech Stack

| Layer            | Technology                  |
| ---------------- | --------------------------- |
| Framework        | FastAPI                     |
| ORM              | SQLAlchemy 2.0              |
| Database         | PostgreSQL (Dockerized)     |
| Auth             | JWT (using `python-jose`)   |
| Password Hashing | `passlib[bcrypt]`           |
| Environment      | Python 3.11+, WSL + VS Code |

---

## ⚙️ Setup

1. **Run PostgreSQL via Docker Compose**

   ```bash
   docker-compose up -d
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI server**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access API docs**

   ```
   http://127.0.0.1:8000/docs
   ```

---

## 🧱 Project Structure

```
app/
 ├── main.py                # Entry point, creates tables, includes routers
 ├── database.py            # Engine, SessionLocal, DB dependency
 ├── models.py              # SQLAlchemy models (User, Post, Vote)
 ├── schemas.py             # Pydantic models
 ├── utils.py               # Password hashing utilities
 ├── security.py            # JWT creation and validation
 ├── routers/
 │    ├── users.py
 │    ├── posts.py
 │    ├── auth.py
 │    └── votes.py
 └── __init__.py
```

---

## 🥪 Work in Progress

This project is **actively being developed**.
Upcoming additions include:

* Role-based access control (admin/moderator)
* Comments and post categorization
* Unit and integration tests with `pytest`
* Complete API documentation and diagrams using **PlantUML**

---

## 📚 Learning Goals

This repository serves as a **learning + portfolio project** to:

* Master FastAPI and modern backend architecture
* Gain hands-on understanding of dependency injection and database design
* Build production-ready systems from scratch

---


