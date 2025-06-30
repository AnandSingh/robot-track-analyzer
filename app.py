# robot_plotter/app.py
import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from utils import process_csv_and_plot

UPLOAD_FOLDER = 'uploads'
PLOT_FOLDER = 'static/plots'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PLOT_FOLDER'] = PLOT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

# Initialize database
conn = sqlite3.connect('robot.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        student_name TEXT,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_name = request.form['student_name']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Save to database
            conn = sqlite3.connect('robot.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO uploads (filename, student_name) VALUES (?, ?)",
                           (filename, student_name))
            conn.commit()
            conn.close()

            # Process file
            plot_path = process_csv_and_plot(filepath, app.config['PLOT_FOLDER'])

            return render_template('index.html', plot_path=plot_path, uploaded=True)

    return render_template('index.html', uploaded=False)

if __name__ == '__main__':
    app.run(debug=True)
