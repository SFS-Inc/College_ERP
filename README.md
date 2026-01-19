# 📘 College ERP System

A role-based College ERP backend built using Django.
The system models real academic workflows such as faculty, departments, and subjects, and is designed to be extended with a frontend interface.


## 🚀 Project Status
### ✅ Phase 1 — Completed

- Custom User model (Faculty, Admin, Student-ready)
- Department management
- Subject management
- Faculty ↔ Department (Many-to-Many)
- Faculty ↔ Subject (Many-to-Many)
- Admin panel for full control

Phase 1 focuses on data modeling and relationships and is now locked.


### 🟡 Phase 2 — In Progress (Current)

- [x] Django views
- [x] HTML-based frontend (Django templates)
- [x] Authentication (login/logout)
- [x] Faculty Dashboard
- [x] Class Logging Module
- [x] Log History with Statistics & Filtering
- [ ] Admin Module (Routing implemented, Logic in progress)

Frontend is being implemented using server-rendered HTML for faster development.


## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Database**: SQLite (PostgreSQL planned later)
- **Frontend**: HTML, CSS (Django Templates)
- **Authentication**: Django Auth System


## ▶️ How to Run the Project Locally
```bash
git clone <repo-url>
cd College_ERP/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Access admin panel at:
`http://127.0.0.1:8000/admin/`


## 📌 Notes

- Student functionality is planned for later phases
- PostgreSQL and REST APIs will be added in future phases
- Phase 1 models will not be modified unless a bug is found


## 📅 Roadmap

- **Phase 1**: Data Models & Relationships ✅
- **Phase 2**: HTML Frontend & Views 🟡
- **Phase 3**: APIs (Optional)
- **Phase 4**: PostgreSQL + Deployment


## � Project Structure

This project uses a **decoupled architecture** where the Django backend and HTML frontend live in separate directories. This structure is cleaner and prepares the project for future scalability.

```text
College_ERP/
├── backend/                # 🧠 The Brain (Django Logic)
│   ├── config/             #    - Settings & Main URLs
│   ├── accounts/           #    - Users & Auth Logic
│   ├── core/               #    - Academic Data (Subjects, Departments)
│   └── engagement/         #    - Business Logic (Class Logs, Attendance)
│
├── frontend/               # 🎨 The Face (UI Layer)
│   ├── static/             #    - CSS (Bootstrap), JS, Images
│   └── templates/          #    - HTML Files (Dashboard, Log forms)
│
└── README.md               # 📄 Project Documentation
```

### 🏗 Architecture Decisions
- **`backend/` vs `frontend/`**: 
We intentionally moved templates out of the inner app directories. This makes it easier for frontend developers to work on HTML/CSS without navigating through complex Python backend folders.

- **Modular Apps**: 
Logic is split into `accounts` (people), `core` (university structure), and `engagement` (daily work). This prevents giant, unmaintainable files.


## �👨💻 Author
**Johan Joseph**

**ERP Project Members/Contributors:**
- Johan Joseph
- Rajaneesh
- Pranav
- Asritha
