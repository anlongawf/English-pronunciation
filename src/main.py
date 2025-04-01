import random
import time
from tkinter import *
import mysql.connector
from mysql.connector import Error


def check_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="English"
        )

        if mydb.is_connected():
            print('Connection successful!')
            return mydb
        else:
            print('Connection failed!')
            return None

    except Error as e:
        print(f"Error: {e}")
        return None

def check_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="your_database"
        )
        return db
    except Error as e:
        print(f"Error: {e}")
        return None

def first_page():
    first_page = Tk()
    first_page.title('Trang chu')
    first_page.geometry('1200x800')
    b1 = Button(first_page, text='Dang ky', command=create_account).pack()
    b2 = Button(first_page, text='Dang nhap', command=login).pack()
    b3 = Button(first_page, text='Thoat', command=first_page.destroy).pack()
    first_page.mainloop()

def create_account():
    db = check_database()
    if not db:
        print("Could not connect to the database.")
        return

    create_window = Tk()
    create_window.title('Đăng ký')
    create_window.geometry('400x300')

    Label(create_window, text='Tạo tài khoản mới').pack()
    Label(create_window, text='Nhập tài khoản mới').pack()
    account_entry = Entry(create_window)
    account_entry.pack()

    Label(create_window, text='Nhập email').pack()
    email_entry = Entry(create_window)
    email_entry.pack()

    Label(create_window, text='Nhập mật khẩu mới').pack()
    password_entry = Entry(create_window, show="*")
    password_entry.pack()

    Label(create_window, text='Nhập lại mật khẩu').pack()
    check_password_entry = Entry(create_window, show="*")
    check_password_entry.pack()

    def attempt_register():
        account = account_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        check_password = check_password_entry.get().strip()

        if password != check_password:
            print("Mật khẩu không khớp!")
            return

        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (account, email))
            existing_user = cursor.fetchone()

            if existing_user:
                print("Tài khoản hoặc email đã tồn tại!")
            else:
                query = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
                cursor.execute(query, (account, email, password))
                db.commit()
                print("Tài khoản đã tạo thành công!")

        except Error as e:
            print(f"Lỗi: {e}")

    Button(create_window, text="Đăng ký", command=attempt_register).pack()

    create_window.mainloop()


def check_database():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="english"
        )
    except mysql.connector.Error as e:
        print(f"Lỗi kết nối DB: {e}")
        return None

def login():
    db = check_database()
    login_window = Tk()
    login_window.title('Đăng nhập')
    login_window.geometry('400x300')

    if db:
        Label(login_window, text="Tài khoản hoặc Email: ").pack()
        account_entry = Entry(login_window)
        account_entry.pack()

        Label(login_window, text="Nhập mật khẩu: ").pack()
        password_entry = Entry(login_window, show="*")
        password_entry.pack()

        def attempt_login():
            account = account_entry.get().strip()
            password = password_entry.get().strip()
            cursor = db.cursor()

            try:
                cursor.execute(
                    "SELECT * FROM user WHERE (username = %s OR email = %s) AND password = %s",
                    (account, account, password)
                )
                user = cursor.fetchone()
                if user:
                    print("Đăng nhập thành công!")
                else:
                    print("Tên tài khoản/email hoặc mật khẩu không đúng!")
            except mysql.connector.Error as e:
                print(f"Lỗi: {e}")

        Button(login_window, text="Đăng nhập", command=attempt_login).pack()

    else:
        print("Không thể kết nối đến cơ sở dữ liệu.")
    login_window.mainloop()


def number_input():
    home = Tk()
    home.title('Home')
    home.geometry('1024x768')
    number_Label = Label(home, text='Nhập số lượng từ')
    number_Label.grid(row=0, column=0)
    number_entry = Entry(home)
    number_entry.grid(row=0, column=1)
    number_button = Button(home, text='Xac nhan', width=25, command=main_window)
    number_button.grid(row=0, column=2)
    exit_buttom = Button(home, text='Thoat', width=25, command=home.destroy)
    exit_buttom.grid(row=0, column=3)
    home.mainloop()

def get_random_word():
    db = check_database()
    if db is None:
        print("Error: Database connection failed!")
        return None

    try:
        cursor = db.cursor()
        cursor.execute("SELECT word FROM words")
        words = cursor.fetchall()

        if not words:
            print("Error: No words found in database.")
            return None

        random_word = random.choice(words)[0]
        print("Random word:", random_word)
        return random_word

    except mysql.connector.Error as e:
        print("SQL Error:", str(e))
        return None


def get_word_definition(word):
    word = word.strip()
    if not isinstance(word, str):
        print("Error: word is not a string!")
        return None

    db = check_database()
    if db is None:
        print("Error: Database connection failed!")
        return None

    try:
        cursor = db.cursor()
        cursor.execute('SELECT word, meaning FROM words WHERE word = %s', (word,))
        result = cursor.fetchone()
        if result:
            print(f"Meaning of '{result[0]}': {result[1]}")
            return {'word': result[0], 'meaning': result[1]}
        return None
    except Exception as e:
        print("SQL Error:", str(e))

def main_window():
    learn_window = Toplevel()
    learn_window.geometry('1024x768')
    learn_window.title('Learning english')


def main():
    word = get_random_word()
    get_word_definition(word)
main()