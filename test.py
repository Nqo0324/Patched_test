import sqlite3

def login(username, password):
    # 连接到数据库
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # 不安全的 SQL 查询，容易受到 SQL 注入攻击
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")

# 演示调用
user_input_username = input("Enter username: ")
user_input_password = input("Enter password: ")

login(user_input_username, user_input_password)
