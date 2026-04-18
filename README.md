# 📝 Django Todo App — Study Tracker

A personal study tracker built with Django that helps you manage tasks, track consistency, and stay motivated.

---

## 🚀 Features

- ✅ Task Management (Create, Read, Update, Delete)
- 🔐 User Authentication (Login / Register)
- 📊 Dashboard with Charts
- 🔥 Streak System (track consecutive study days)
- 📧 Weekly Email Report
- 🔔 Daily Reminder API
- 📈 Consistency Checker (On Track / Off Track)

---

## 🛠️ Tech Stack

- **Backend:** Django 5.2
- **Database:** SQLite3
- **Frontend:** HTML, Bootstrap 5, Chart.js
- **Email:** Gmail SMTP
- **API Testing:** Postman

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/AshishChaubey2003/ToDo.git
cd ToDo
```

### 2. Create virtual environment
```bash
python -m venv todoenv
todoenv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
SECRET_KEY=tumhara-secret-key
EMAIL_HOST_USER=tumhari_gmail@gmail.com
EMAIL_HOST_PASSWORD=tumhara_app_password

### 5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run server
```bash
python manage.py runserver
```

---

## 🌐 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Task List |
| POST | `/add/` | Create Task |
| GET/POST | `/edit/<id>/` | Update Task |
| GET | `/delete/<id>/` | Delete Task |
| GET | `/toggle/<id>/` | Toggle Complete |
| GET | `/dashboard/` | Dashboard |
| GET | `/check-consistency/` | Consistency Check |
| GET | `/daily-reminder/` | Daily Reminder |
| GET | `/weekly-report/` | Weekly Email Report |
| GET | `/streak/` | Current Streak |
| GET | `/login/` | Login |
| GET | `/register/` | Register |
| GET | `/logout/` | Logout |

---

## 📸 Screenshots

> Dashboard, Task List aur Login screenshots yahan add karo!

---

## 👨‍💻 Author

**Ashish Kumar Chaubey**  
GitHub: [@AshishChaubey2003](https://github.com/AshishChaubey2003)
