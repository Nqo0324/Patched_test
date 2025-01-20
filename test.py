import sqlite3
from flask import Flask, request

app = Flask(__name__)

# SQLiteデータベースの接続
def connect_db():
    return sqlite3.connect('example.db')

@app.route('/search')
def search():
    # ユーザーからの入力を取得
    username = request.args.get('username')

    # ユーザー入力をSQLクエリに直接埋め込んでしまう（脆弱）
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    # データベース接続とクエリ実行
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    return str(results)

if __name__ == '__main__':
    app.run(debug=True)