# Adminova Consulting Services System

A comprehensive web-based system for managing service bookings, customer requests, and staff roles for Adminova Consulting Services.

## 🚀 Features
- **Landing Page:** Animated hero section showcasing all 10 service categories.
- **Authentication:** Secure login system (Accounts created by Super Admin only).
- **Service Booking:** Customers can browse services and submit booking requests.
- **Admin Dashboard:** Admins can manage bookings, update statuses, set prices, and add notes.
- **User Management:** Super Admin can create, deactivate, and assign roles (Customer, Worker, Admin).
- **Service Management:** Super Admin can add, edit, and hide services.
- **PDF Generation:** Automatically generate Quotations, Receipts, and Confirmation documents using WeasyPrint.
- **Responsive Design:** Fully responsive UI built with Bootstrap 5.

## 🛠️ Tech Stack
- **Backend:** Django 5.x (Python)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **PDF Library:** WeasyPrint
- **Config:** python-decouple

## ⚙️ Installation Guide

### Prerequisites
- Python 3.10+
- PostgreSQL
- GTK libraries (for WeasyPrint on Windows)

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/adminova-consulting.git
   cd adminova-consulting
Create and activate virtual environment:

bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
Install dependencies:

bash
pip install -r requirements.txt
Set up environment variables:
Copy .env.example to .env and fill in your details:

bash
cp .env.example .env
Set up PostgreSQL database:

sql
CREATE DATABASE Adminova_db;
Run migrations:

bash
python manage.py makemigrations
python manage.py migrate
Create Super Admin:

bash
python manage.py createsuperuser
Run the server:

bash
python manage.py runserver
Access the system:
Open http://127.0.0.1:8000/ in your browser.

📁 Project Structure
config/ - Django project settings.

core/ - Home and landing pages.

accounts/ - User authentication and management.

bookings/ - Service booking and management logic.

templates/ - HTML templates for all pages.

static/ - CSS, JS, and images (including logo and favicon).

🔒 Security
Environment variables (.env) are hidden from Git.

Passwords are hashed using Django's built-in security.

Role-based access control prevents unauthorized access to admin pages.

📞 Contact
For support, email adminovaconsulting@gmail.com or call +255 613 950 508.
