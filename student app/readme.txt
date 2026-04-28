========================================
📌 School Management System - README
====================================

📖 Description:
This project is a School Management System built using Python, Tkinter (CustomTkinter), and SQLite.
It allows administrators to manage students, teachers, marks, and import/export data بسهولة.

---

## ⚙️ Features:

✔ Login System (Admin / Roles)
✔ Student Management (Add / Update / Delete / Search)
✔ Teachers Management
✔ Marks Management for multiple subjects
✔ Import Data from CSV / Excel
✔ Statistics Dashboard
✔ Role-based permissions system

---

## 📂 Project Structure:

* login.py              → Login & Sign Up system 
* dashboard.py          → Main dashboard
* studentspage.py       → Students navigation page 
* firststudent.py       → Students + Marks system 
* importpage.py         → Import students & grades 
* teachers.py           → Teachers management 
* statistics.py         → System statistics 
* school.db             → SQLite database

---

## 🛠 Requirements:

* Python 3.x
* customtkinter
* pillow (PIL)
* tkcalendar
* sqlite3

Install dependencies:
pip install customtkinter pillow tkcalendar

---

## 🚀 How to Run:

1. Open project folder in VS Code

2. Run main file:
   python login.py

3. Login with admin account

---

## 🗄 Database:

* Uses SQLite database (school.db)
* Tables include:

  * students (first_student)
  * teachers
  * marks for each subject
  * admin accounts

---

## 📊 Subjects Supported:

* Arabic
* English
* Mathematics
* Physics
* Chemistry
* Biology
* Social Studies
* Civic Education

---

## 🔐 Roles:

* Admin → full control
* User   → limited access
* Viewer → read-only

---

## 📥 Import Feature:

* Supports CSV & Excel files
* Validates data before inserting
* Skips invalid rows automatically

---

## ⚠️ Notes:

* Make sure "school.db" exists before running
* Images folder must be in correct path
* Some features require admin permissions

---

## 👨‍💻 Author:

Developed as a School Management System Project

========================================
END OF FILE
===========
