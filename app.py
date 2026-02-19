import sqlite3
import os
from flask import Flask, request, render_template, redirect, url_for
from flask_login import (
    LoginManager, UserMixin,
    login_user, logout_user,
    login_required, current_user
)
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "main"

# ---------------- DATABASE INITIALIZATION ----------------

def init_qr_db():
    """Initialize QR code database for food tracking"""
    conn = sqlite3.connect("qrcodes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id TEXT PRIMARY KEY,
            breakfast INTEGER DEFAULT 0,
            lunch INTEGER DEFAULT 0,
            dinner INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def init_teams_db():
    """Initialize teams database for judging"""
    conn = sqlite3.connect("teams.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            team_name TEXT PRIMARY KEY,
            creativity INTEGER DEFAULT 0,
            innovation INTEGER DEFAULT 0,
            code_quality INTEGER DEFAULT 0,
            problem_solving INTEGER DEFAULT 0
        )
    """)
    
    # Pre-populate with demo teams if empty
    c.execute("SELECT COUNT(*) FROM teams")
    if c.fetchone()[0] == 0:
        demo_teams = [
            "Team 1", "Team 2", "Team 3", "Team 4",
            "Team 5", "Team 6", "Team 7", "Team 8"
        ]
        for team in demo_teams:
            c.execute("""
                INSERT INTO teams (team_name, creativity, innovation, code_quality, problem_solving)
                VALUES (?, 0, 0, 0, 0)
            """, (team,))
    
    conn.commit()
    conn.close()

# ---------------- USERS ----------------

class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def verify(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

users = {
    "foodadmin": User("1", "foodadmin",
        bcrypt.generate_password_hash("food123").decode(), "food"),
    "judge": User("2", "judge",
        bcrypt.generate_password_hash("judge123").decode(), "logistics"),
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

# ---------------- ROUTES -----------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/admin/db")
def view_db():
    import sqlite3
    conn = sqlite3.connect("qrcodes.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM participants")
    data = cur.fetchall()
    conn.close()
    return str(data)

@app.route("/")
def main():
    return render_template("main.html")

# ---- FOOD LOGIN -----------------------------------------------------------------------------------------------------------------------------------------
@app.route("/login-food", methods=["GET", "POST"])
def login_food():
    if request.method == "POST":
        u = users.get(request.form["username"])
        if u and u.role == "food" and u.verify(request.form["password"]):
            login_user(u)
            return redirect(url_for("scanner"))
    return render_template("login.html")

# ---- LOGISTICS LOGIN -----------------------------------------------------------------------------------------------------------------------------------------
@app.route("/login-logistics", methods=["GET", "POST"])
def login_logistics():
    if request.method == "POST":
        u = users.get(request.form["username"])
        if u and u.role == "logistics" and u.verify(request.form["password"]):
            login_user(u)
            return redirect(url_for("judges"))
    return render_template("loginL.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main"))

# ---------------- PAGES ---------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route("/scanner")
@login_required
def scanner():
    if current_user.role != "food":
        return redirect(url_for("main"))
    return render_template("scanner.html")

@app.route("/judges")
@login_required
def judges():
    if current_user.role != "logistics":
        return redirect(url_for("main"))

    # Fetch all team names from teams.db
    conn = sqlite3.connect("teams.db")
    c = conn.cursor()
    c.execute("SELECT team_name FROM teams ORDER BY team_name")
    teams = [row[0] for row in c.fetchall()]
    conn.close()

    return render_template("judges.html", teams=teams)


@app.route("/submit-judging", methods=["POST"])
@login_required
def submit_judging():
    if current_user.role != "logistics":
        return redirect(url_for("main"))

    team = request.form["team"].strip()
    creativity = int(request.form["creativity"])
    innovation = int(request.form["innovation"])
    code_quality = int(request.form["code_quality"])
    problem_solving = int(request.form["problem_solving"])

    
    conn = sqlite3.connect("teams.db")
    c = conn.cursor()
    c.execute("""
        UPDATE teams 
        SET creativity = ?, innovation = ?, code_quality = ?, problem_solving = ?
        WHERE team_name = ?
    """, (creativity, innovation, code_quality, problem_solving, team))
    conn.commit()
    conn.close()

    return redirect(url_for("judges"))


# ---------------- QR LOGIC ---------------------------------------------------------------------------------------------------------

def get_current_meal():
    now = datetime.now().time()
    if datetime.strptime("06:00", "%H:%M").time() <= now < datetime.strptime("10:00", "%H:%M").time():
        return "breakfast"
    if datetime.strptime("12:00", "%H:%M").time() <= now < datetime.strptime("15:00", "%H:%M").time():
        return "lunch"
    if datetime.strptime("18:00", "%H:%M").time() <= now < datetime.strptime("21:00", "%H:%M").time():
        return "dinner"
    return None

@app.route("/scan_qr", methods=["POST"])
@login_required
def scan_qr():
    if current_user.role != "food":
        return "Unauthorized", 403

    pid = request.form["id"]
    meal = get_current_meal()
    if not meal:
        return "Not meal time", 400

    conn = sqlite3.connect("qrcodes.db")
    c = conn.cursor()

    c.execute(f"SELECT {meal} FROM participants WHERE id=?", (pid,))
    row = c.fetchone()

    if not row:
        conn.close()
        return "Invalid QR", 400

    if row[0] == 1:
        conn.close()
        return "Already used", 400

    c.execute(f"UPDATE participants SET {meal}=1 WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return "Food can be served", 200

# ---------------- RUN ----------------

if __name__ == "__main__":
    init_qr_db()
    init_teams_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
