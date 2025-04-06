from tkinter import *
from database import init_database
from gui import login_faceid, login, register
from learn_window import main_window
from admin_window import admin_window

def main():
    root = Tk()
    root.title("Học tiếng Anh")
    root.geometry("1200x800")
    root.resizable(False, False)

    Label(root, text="Chào mừng bạn đến với ứng dụng học tiếng Anh", font=("Arial", 14, "bold"), fg="darkgreen").pack(pady=20)
    Button(root, text="Đăng nhập", width=20, command=lambda: login(root, main_window, admin_window), bg="blue", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(root, text="Đăng nhập Faceid", width=20, command=lambda: login_faceid(root, main_window, admin_window), bg="green",fg="white", font=("Arial", 12)).pack(pady=10)
    Button(root, text="Đăng ký", width=20, command=lambda: register(root), bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(root, text="Thoát", width=20, command=root.quit, bg="red", fg="white", font=("Arial", 12)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    init_database()
    main()