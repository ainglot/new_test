# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask import send_from_directory
import sqlite3
import os

app = Flask(__name__)

@app.route('/BIB.html')
def serve_bib():
    return send_from_directory('.', 'BIB.html')

@app.route('/api/search', methods=['POST'])
def search():
    if request.method == 'POST':
        data = request.get_json()
        year = data.get('year')
        entries = []
        rows = []  # Initialize rows here

        # Połączenie z bazą danych SQLite i wykonanie zapytania
        try:
            conn = sqlite3.connect(r'/app/api/test.db')  # Użyj swojej bazy danych
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, author, year FROM Bibliografia WHERE year = ?', (year,))
            rows = cursor.fetchall()  # Assign rows here
        except Exception as e:
            print("Database error:", e)
        finally:
            conn.close()

        # Przekształcenie wyników w listę słowników
        entries = [{'ID':row[0], 'title': row[1], 'author': row[2], 'year': row[3]} for row in rows]
        return jsonify(entries)
    
    # For GET request, return some information or sample response
    return jsonify({"message": "Send a POST request with a year to search."})

@app.route('/')
def home():
    return "Welcome to the API! Visit /BIB.html or use /api/search to query data."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
