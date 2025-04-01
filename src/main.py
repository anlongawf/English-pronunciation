import random
from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


def check_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="english"
        )
        return db
    except Error as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối DB: {e}")
        return None


def register():
    register_window = Toplevel()
    register_window.title("Đăng ký")
    register_window.geometry("400x300")

    Label(register_window, text="Tài khoản").pack()
    account_entry = Entry(register_window)
    account_entry.pack()

    Label(register_window, text="Email").pack()
    email_entry = Entry(register_window)
    email_entry.pack()

    Label(register_window, text="Mật khẩu").pack()
    password_entry = Entry(register_window, show="*")
    password_entry.pack()

    def attempt_register():
        account = account_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not account or not email or not password:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        db = check_database()
        if db is None:
            return

        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (account, email))
            if cursor.fetchone():
                messagebox.showwarning("Lỗi", "Tài khoản hoặc email đã tồn tại!")
            else:
                cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)",
                               (account, email, password))
                db.commit()
                messagebox.showinfo("Thành công", "Tạo tài khoản thành công!")
                register_window.destroy()
        except Error as e:
            messagebox.showerror("Lỗi", f"Lỗi SQL: {e}")
        finally:
            cursor.close()
            db.close()

    Button(register_window, text="Đăng ký", command=attempt_register).pack()


def login():
    login_window = Toplevel()
    login_window.title("Đăng nhập")
    login_window.geometry("400x300")

    Label(login_window, text="Tài khoản hoặc Email").pack()
    account_entry = Entry(login_window)
    account_entry.pack()

    Label(login_window, text="Mật khẩu").pack()
    password_entry = Entry(login_window, show="*")
    password_entry.pack()

    def attempt_login():
        account = account_entry.get().strip()
        password = password_entry.get().strip()

        if not account or not password:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tài khoản và mật khẩu!")
            return

        db = check_database()
        if db is None:
            return

        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE (username = %s OR email = %s) AND password = %s",
                           (account, account, password))
            if cursor.fetchone():
                messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                login_window.destroy()
                main_window()
            else:
                messagebox.showwarning("Lỗi", "Sai tài khoản hoặc mật khẩu!")
        except Error as e:
            messagebox.showerror("Lỗi", f"Lỗi SQL: {e}")
        finally:
            cursor.close()
            db.close()

    Button(login_window, text="Đăng nhập", command=attempt_login).pack()


def get_random_word():
    db = check_database()
    if db is None:
        return None

    try:
        cursor = db.cursor()
        cursor.execute("SELECT word, meaning FROM words")
        words = cursor.fetchall()

        if not words:
            messagebox.showwarning("Lỗi", "Không có từ nào trong cơ sở dữ liệu.")
            return None, None

        return random.choice(words)
    except Error as e:
        messagebox.showerror("Lỗi", f"Lỗi SQL: {e}")
        return None, None
    finally:
        cursor.close()
        db.close()


def main_window():
    learn_window = Toplevel()
    learn_window.geometry('1024x768')
    learn_window.title('Learning English')

    word, meaning = get_random_word()
    if word:
        Label(learn_window, text=f"Từ vựng: {word}", font=("Arial", 18)).pack(pady=20)
        Label(learn_window, text=f"Nghĩa: {meaning}", font=("Arial", 16)).pack()

    learn_window.mainloop()


def main():
    root = Tk()
    root.title("Học tiếng Anh")
    root.geometry("400x300")

    Label(root, text="Chào mừng bạn đến với ứng dụng học tiếng Anh", font=("Arial", 12)).pack(pady=10)
    Button(root, text="Đăng nhập", width=20, command=login).pack(pady=5)
    Button(root, text="Đăng ký", width=20, command=register).pack(pady=5)
    Button(root, text="Thoát", width=20, command=root.quit).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()