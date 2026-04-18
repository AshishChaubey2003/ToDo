# 🗒️ ToDo — Personal Study Tracker

> *"Consistency beats intensity."* — Track your study habits, stay on streak, and never miss a day.

---

## 🌟 What is this?

This is not just a todo app.  
It's a **personal study accountability system** built with Django.  
Add your daily study tasks, mark them complete, and let the app tell you if you're **On Track** or **Off Track**.

---

## ✨ Features at a Glance

| Feature | Description |
|--------|-------------|
| 📝 Task Manager | Add, edit, delete, and complete tasks |
| 🔐 Auth System | Register & login — your data stays yours |
| 📊 Dashboard | Visual chart of your last 30 days |
| 🔥 Streak Tracker | See how many days in a row you've studied |
| 📈 Consistency Check | On Track if 10+ days studied in last 15 |
| 🔔 Daily Reminder | API tells you if you studied today or not |
| 📧 Weekly Report | Get your weekly summary on email |

---

## 🛠️ Built With
Django 5.2  •  Bootstrap 5  •  Chart.js  •  SQLite3  •  Gmail SMTP

---

## ⚡ Quick Start

```bash
# Clone karo
git clone https://github.com/AshishChaubey2003/ToDo.git
cd ToDo

# Virtual env banao
python -m venv todoenv
todoenv\Scripts\activate    # Windows
source todoenv/bin/activate # Mac/Linux

# Dependencies install karo
pip install -r requirements.txt

# .env file banao
SECRET_KEY=tumhara-secret-key
EMAIL_HOST_USER=tumhari@gmail.com
EMAIL_HOST_PASSWORD=app_password_here

# Database setup
python manage.py migrate

# Server chalao
python manage.py runserver
```

---

## 🌐 API Reference
GET  /                     → All tasks
POST /add/                 → Create task (JSON supported)
GET  /dashboard/           → Dashboard + graph
GET  /streak/              → Current streak 🔥
GET  /check-consistency/   → On Track / Off Track
GET  /daily-reminder/      → Studied today?
GET  /weekly-report/       → Email report bhejo
GET  /login/               → Login
GET  /register/            → Register

---

## 📁 Project Structure
Main_ToDo/
├── App_Todo/
│   ├── templates/        → HTML files
│   ├── models.py         → Task model
│   ├── views.py          → All logic
│   └── urls.py           → URL routes
├── Main_ToDo/
│   ├── settings.py       → Config
│   └── urls.py           → Main URLs
├── requirements.txt
└── manage.py

---

## 👨‍💻 Author

**Ashish Kumar Chaubey**  
[@AshishChaubey2003](https://github.com/AshishChaubey2003)

---

⭐ *Agar helpful laga toh star do!*
