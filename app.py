# main.py (Flask app for web-based CSV plotting)
import os
import re
import math
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename

# Constants
UPLOAD_FOLDER = 'uploads'
PLOT_FOLDER = 'static/plots'
DB_FILE = 'database.db'
WHEEL_DIAMETER = 56  # mm
DEGREE_TO_MM = (math.pi * WHEEL_DIAMETER) / 360  # mm per degree

# App Setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

# Database Setup
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            group_name TEXT
        )''')
        conn.commit()

init_db()

# Parser and plot logic
def parse_log_csv(filepath):
    x, y = 0.0, 0.0
    X_path, Y_path = [x], [y]
    last_l, last_r = None, None

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        match = re.search(r"(\d*),? L: ([\-0-9.]+)°.*, R: ([\-0-9.]+)°.*, Yaw: ([\-0-9.e]+)", line)
        if match:
            _, l_angle, r_angle, yaw_deg = match.groups()
            l_angle = float(l_angle)
            r_angle = float(r_angle)
            yaw_rad = math.radians(float(yaw_deg))

            if last_l is not None and last_r is not None:
                delta_l = (l_angle - last_l) * DEGREE_TO_MM
                delta_r = (r_angle - last_r) * DEGREE_TO_MM
                dist = (delta_l + delta_r) / 2

                dx = dist * math.cos(yaw_rad)
                dy = dist * math.sin(yaw_rad)
                x += dx
                y += dy
                X_path.append(x)
                Y_path.append(y)

            last_l, last_r = l_angle, r_angle

    return X_path, Y_path

def save_plot(X, Y, label):
    plt.figure(figsize=(6, 5))
    plt.plot(X, Y, 'o-', label=label)
    plt.title(f"Robot Run: {label}")
    plt.xlabel("X Position (mm)")
    plt.ylabel("Y Position (mm)")
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    filename = f"{secure_filename(label)}.png"
    path = os.path.join(PLOT_FOLDER, filename)
    plt.savefig(path)
    plt.close()
    return filename

@app.route('/')
def index():
    group = request.args.get('group')
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        if group:
            c.execute("SELECT id, filename, group_name FROM logs WHERE group_name = ?", (group,))
        else:
            c.execute("SELECT id, filename, group_name FROM logs")
        files = c.fetchall()
        c.execute("SELECT DISTINCT group_name FROM logs")
        groups = [g[0] for g in c.fetchall() if g[0]]
    return render_template('index.html', files=files, groups=groups)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    group = request.form.get('group')
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        X, Y = parse_log_csv(path)
        save_plot(X, Y, filename)

        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO logs (filename, group_name) VALUES (?, ?)", (filename, group))
            conn.commit()
    return redirect(url_for('index'))

@app.route('/plot/<filename>')
def plot(filename):
    plot_file = f"{secure_filename(filename)}.png"
    return send_from_directory(PLOT_FOLDER, plot_file)

if __name__ == '__main__':
    app.run(debug=True)
