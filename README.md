# 🔐 FastAPI JWT Authentication

A simple FastAPI application that provides user registration and login functionality using JWT tokens for secure authentication.

## 🚀 Features

- Register new users
- Secure login with JWT token generation
- Protected route to get current logged-in user
- Password hashing using `passlib`
- SQLite database using SQLModel

## 📦 Tech Stack

- Python
- FastAPI
- SQLModel
- SQLite
- Pydantic
- Passlib (for password hashing)
- JWT (PyJWT or jose)

## 🔧 Installation

```bash
git clone <your-repo-url>
cd <repo-folder>
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
