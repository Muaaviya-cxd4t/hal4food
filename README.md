# 🍴 QR-Based Food Service System

A Flask-based web application developed for a **24-hour National Hackathon with 300+ participants HAL-3.0**, designed to streamline **meal distribution using QR codes**.

---

## ✨ Features
- **QR Generation:** Generates unique QR codes from registration CSV file.
- **Time-Based Validation:** Same QR used securely across breakfast, lunch, and dinner.
- **Database Integration:** SQL backend to track and validate scans.
- **Deployment:** Hosted on OnRender for live use during the hackathon.
- **Caterer Support:** Automatically counted meals served, helping caterers manage food efficiently.

---

## ⚡ Challenges Solved
- Managed **timezone mismatch** on OnRender servers to ensure correct meal-time tracking.
- Implemented **robust validation** to prevent duplicate usage of QR codes.

---

## 📌 Outcome
- Successfully deployed system used by **300+ participants**.
- Improved **efficiency, accuracy, and transparency** in food distribution.

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQL
- **Frontend:** Flask Templates (HTML/CSS)
- **Deployment:** OnRender
- **QR Handling:** Python libraries (qrcode, etc.)

---

## 🚀 How It Works
1. Upload participant registration CSV file.
2. System generates unique QR codes for each participant.
3. QR codes are pasted on ID cards for participants.
4. On scanning, system validates time and ensures meal is recorded correctly.
5. Caterers get real-time meal counts for efficient serving.

---

## 📂 Repository Structure
- `app.py` → Main Flask application.
- `templates/` → HTML templates for UI.
- `static/` → Static files (CSS, images, etc.).
- `generate.py` → Generates QR codes from CSV data.
- `database/` → SQL database setup and schema.
- `README.md` → Project documentation (this file).

---

## 👨‍💻 Author
Developed and deployed by **[Abhishek R]** as part of the organizing team of a national-level hackathon.

---

## 📜 License
This project is for educational and event-management purposes. Free to use and adapt with attribution.
