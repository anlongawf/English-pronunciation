from tkinter import *
from tkinter import messagebox
from database import check_database
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace

def register(root):
    register_window = Toplevel(root)
    register_window.title("Đăng ký")
    register_window.geometry("400x300")
    register_window.resizable(False, False)

    Label(register_window, text="Tài khoản", font=("Arial", 12)).pack(pady=5)
    account_entry = Entry(register_window, width=30)
    account_entry.pack(pady=5)

    Label(register_window, text="Email", font=("Arial", 12)).pack(pady=5)
    email_entry = Entry(register_window, width=30)
    email_entry.pack(pady=5)

    Label(register_window, text="Mật khẩu", font=("Arial", 12)).pack(pady=5)
    password_entry = Entry(register_window, show="*", width=30)
    password_entry.pack(pady=5)

    def attempt_register():
        account = account_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not account or not email or not password:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!", parent=register_window)
            return

        db = check_database()
        if db is None:
            return

        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (account, email))
            if cursor.fetchone():
                messagebox.showwarning("Lỗi", "Tài khoản hoặc email đã tồn tại!", parent=register_window)
            else:
                cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)",
                               (account, email, password))
                db.commit()
                messagebox.showinfo("Thành công", "Đăng ký thành công!", parent=register_window)
                register_window.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi SQL", f"Không thể đăng ký: {e}", parent=register_window)
        finally:
            cursor.close()

    Button(register_window, text="Đăng ký", command=attempt_register, width=15, bg="green", fg="white").pack(pady=20)

def login(root, main_window_callback, admin_window_callback):
    login_window = Toplevel(root)
    login_window.title("Đăng nhập")
    login_window.geometry("400x300")
    login_window.resizable(False, False)

    Label(login_window, text="Tài khoản hoặc Email", font=("Arial", 12)).pack(pady=5)
    account_entry = Entry(login_window, width=30)
    account_entry.pack(pady=5)

    Label(login_window, text="Mật khẩu", font=("Arial", 12)).pack(pady=5)
    password_entry = Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)

    def attempt_login():
        account = account_entry.get().strip()
        password = password_entry.get().strip()

        if not account or not password:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!", parent=login_window)
            return

        db = check_database()
        if db is None:
            return

        cursor = None
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE (username = %s OR email = %s) AND password = %s",
                           (account, account, password))
            user = cursor.fetchone()

            if user:
                login_window.destroy()
                root.withdraw()
                if user['admin'] == 1:
                    messagebox.showinfo("Thành công", "Đăng nhập Admin thành công!")
                    admin_window_callback(root)
                else:
                    messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                    main_window_callback(root)
            else:
                messagebox.showwarning("Lỗi", "Sai tài khoản hoặc mật khẩu!", parent=login_window)
        except Exception as e:
            messagebox.showerror("Lỗi SQL", f"Không thể đăng nhập: {e}", parent=login_window)
        finally:
            if cursor:
                cursor.close()
    Button(login_window, text="Đăng nhập", command=attempt_login, width=15, bg="blue", fg="white").pack(pady=20)

def login_faceid(root, main_window_callback, admin_window_callback):
    login_window = Toplevel(root)
    login_window.title("Đăng nhập bằng FaceID")
    login_window.geometry("500x400")

    video_label = Label(login_window)
    video_label.pack(pady=10)

    Button(login_window, text="Kiểm tra FaceID", command=lambda: check_face(), width=15, bg="blue", fg="white").pack(pady=5)
    Button(login_window, text="Hủy", command=login_window.destroy, width=15, bg="red", fg="white").pack(pady=5)

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        messagebox.showerror("Lỗi", "Không thể truy cập webcam!", parent=login_window)
        login_window.destroy()
        return

    current_frame = None
    is_running = True  # Cờ để kiểm soát update_video

    def update_video():
        nonlocal current_frame, is_running
        if not is_running:  # Dừng nếu không còn chạy
            return
        ret, frame = camera.read()
        if ret:
            frame = cv2.flip(frame, 1)
            current_frame = frame.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        login_window.after(10, update_video)

    def check_face():
        nonlocal is_running
        if current_frame is None:
            messagebox.showwarning("Lỗi", "Không có khung hình để kiểm tra!", parent=login_window)
            return

        db = check_database()
        if db is None:
            return



    update_video()

    def on_closing():
        nonlocal is_running
        is_running = False  # Dừng update_video khi đóng cửa sổ
        camera.release()
        login_window.destroy()

    login_window.protocol("WM_DELETE_WINDOW", on_closing)