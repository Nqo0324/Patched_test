import os
import sqlite3
from flask import Flask, request, jsonify
from contextlib import contextmanager

# Initialize Flask app
app = Flask(__name__)

@contextmanager
def get_db_connection():
    """Context manager for database connections to ensure proper cleanup"""
    conn = None
    try:
        conn = sqlite3.connect('example.db')
        yield conn
    finally:
        if conn is not None:
            conn.close()

def init_db():
    """Initialize the database with test data"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )''')
        cursor.execute('DELETE FROM users')
        test_data = [('test',), ('alice',), ('bob',)]
        cursor.executemany('INSERT INTO users (username) VALUES (?)', test_data)
        conn.commit()

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

@app.route('/search')
def search():
    """Search endpoint with SQL injection protection"""
    username = request.args.get('username')
    if username is None:
        return jsonify({'error': 'Username parameter is required'}), 400

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Using parameterized query to prevent SQL injection
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            results = cursor.fetchall()
            return jsonify({'results': results})
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error occurred'}), 500

if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Get debug mode from environment, default to False
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Flask app:")
    print(f"* Debug mode: {debug_mode}")
    print(f"* Port: 5050")
    
    # Run the app with the specified configuration
    app.run(
        debug=debug_mode,
        host='127.0.0.1',
        port=5050,
        use_reloader=False
    )