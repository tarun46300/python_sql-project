# 🎬 Movie Theatre Database Management System

## 📖 Overview
The **Movie Theatre Database Management System** is a Python-based application designed to simplify and automate theatre operations such as movie scheduling, staff management, and ticket booking.  
Built using **Python (Tkinter)** for the graphical user interface and **MySQL** as the backend database, this system allows administrators to manage data efficiently without requiring SQL expertise.

🧑‍💻 Author

Developed by: Tarun Sharma
Guide: Ms. Gurpreet Kaur
Institution: Chandigarh University, Department of MCA
---

## 🧩 Features
- 🎞️ **View and Manage Tables** – Display all database tables directly from MySQL.  
- ➕ **Add New Records** – Insert movie, booking, or staff data easily through GUI forms.  
- ✏️ **Edit Existing Records** – Modify details of selected entries in real-time.  
- 🗑️ **Delete Records** – Remove unwanted or outdated data securely.  
- 🔄 **Refresh Data** – Instantly reload tables to view the latest updates.  
- ⚙️ **Error Handling** – Gracefully handles connection or input errors.  
- 🎨 **Modern GUI** – Styled using `ttk` for a clean, responsive interface.  
- 💾 **Database Integration** – Uses `mysql.connector` for seamless communication with MySQL.  

---

## 🖼️ Interface Preview
*(Add a screenshot or GIF of your Tkinter interface here)*

```bash
![App Screenshot](screenshot.png)
System Architecture

The system consists of the following major components:

Frontend (Tkinter GUI): User interface for interacting with database records.

Backend (Python): Handles logic, event processing, and query execution.

Database (MySQL): Stores movie, customer, booking, and staff details.

⚙️ Installation & Setup
Prerequisites

Python 3.x installed

MySQL Server running locally

mysql.connector module installed

Update your database configuration in the script:
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "movie_theatre"
}
Future Enhancements

🌐 Online ticket booking system

💳 Payment gateway integration

📊 Dashboard for data analytics and sales insights

🔐 Role-based user authentication (Admin, Staff, Customer)

☁️ Cloud-based database support for remote access

