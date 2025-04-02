import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

db_connection = None

def init_database():
    global db_connection
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="english"
        )
        print("Đã kết nối cơ sở dữ liệu!")
    except Error as e:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới cơ sở dữ liệu: {e}")
        db_connection = None

def check_database():
    global db_connection
    if db_connection is None or not db_connection.is_connected():
        init_database()
    return db_connection

def get_random_word():
    db = check_database()
    if db is None:
        return None, None
    try:
        cursor = db.cursor()
        cursor.execute("SELECT word, meaning FROM words")
        words = cursor.fetchall()
        if not words:
            messagebox.showwarning("Lỗi", "Không có từ nào trong cơ sở dữ liệu!")
            return None, None
        import random
        return random.choice(words)
    except Error as e:
        messagebox.showerror("Lỗi SQL", f"Không thể lấy từ: {e}")
        return None, None
    finally:
        cursor.close()