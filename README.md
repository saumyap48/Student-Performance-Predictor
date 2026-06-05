# AI-Powered Student Performance Prediction System

🚀 **Live Demo:**  
👉 https://ai-student-performance-predictor.netlify.app/login.html

A full-stack web application designed for students and educators to predict academic performance using machine learning. This project features a robust FastAPI backend, a secure JWT-based authentication system, and a modern, responsive frontend.

## 🚀 Features

-   **User Authentication**: Secure signup and login using JWT (JSON Web Tokens) and password hashing (bcrypt).
-   **AI Performance Prediction**: Uses a **RandomForestRegressor** model trained on study hours, attendance, previous scores, and assignments completed.
-   **Dashboard**: Interactive dashboard with a prediction form and result visualization.
-   **History Tracking**: Keep track of all previous predictions in a dynamic table.
-   **Data Visualization**: Trends visualized using **Chart.js**.
-   **Export Capability**: Download your prediction history as a CSV file.
-   **Modern UI**: Premium design with **Glassmorphism**, smooth animations, and **Dark/Light mode** support.

## 🛠️ Tech Stack

-   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+), Chart.js.
-   **Backend**: FastAPI (Python), SQLAlchemy.
-   **Database**: SQLite.
-   **Machine Learning**: Scikit-learn, Pandas, NumPy.
-   **Security**: Python-jose (JWT), Passlib (Bcrypt).

## 📂 Project Structure

```text
student-performance-predictor/
├── backend/
│   ├── main.py            # FastAPI entry point
│   ├── database.py       # SQL Alchemy connection
│   ├── models.py         # DB Models (User, History)
│   ├── schemas.py        # Pydantic validation
│   ├── crud.py           # DB Operations
│   ├── security.py       # Auth utilities
│   ├── routers/          # Modular API routes
│   │   ├── auth.py
│   │   ├── prediction.py
│   │   └── profile.py
│   ├── utils/
│   │   └── csv_export.py # CSV utility
│   ├── ml_model/
│   │   └── predictor.py  # RandomForest logic
│   └── requirements.txt
├── frontend/
│   ├── index.html, login.html, signup.html, dashboard.html
│   ├── style.css
│   └── script.js
└── README.md
```

## ⚙️ Installation & Setup

### 1. Prerequisite
Ensure you have Python 3.8+ installed.

### 2. Backend Setup
```bash
cd backend
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```
The server will start at `http://localhost:8000`.

### 3. Frontend Setup
Simply open `frontend/index.html` in your browser. (Alternatively, use a local server like Live Server in VS Code).

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |
| POST | `/predict/` | Predict score and save history |
| GET | `/predict/history` | Get user prediction history |
| GET | `/predict/export` | Download history as CSV |
| GET | `/profile/` | Get current user info |

## 🌟 Future Improvements

-   [ ] Add more ML features (socio-economic factors, mental health survey).
-   [ ] Integration with Google Calendar for study scheduling.
-   [ ] Email notifications for trend alerts.
-   [ ] Deployment to Render (Backend) and Netlify (Frontend).

## 📝 License
Distributed under the MIT License.
