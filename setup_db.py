import sqlite3

def setup_database():
    with sqlite3.connect('example.db') as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )
        ''')
        
        # Insert some test data
        cursor.execute('DELETE FROM users')  # Clear existing data
        test_users = [
            ('alice',),
            ('bob',),
            ('test',),
        ]
        cursor.executemany('INSERT INTO users (username) VALUES (?)', test_users)
        conn.commit()

if __name__ == '__main__':
    setup_database()