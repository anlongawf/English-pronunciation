import random
from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import pyttsx3
import speech_recognition as sr
import threading

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

def speak(spoken_word_label, learn_window):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            spoken_word_label.config(text="Đang lắng nghe...")
            print('Đang lắng nghe...')
            recognizer.energy_threshold = 100
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=4)
        recognized_text = recognizer.recognize_google(audio, language="en-US")
        print('Bạn đã nói: ', recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        spoken_word_label.config(text="Không nhận diện được âm thanh")
        print("Không thể nhận diện được âm thanh.")
        return ""
    except sr.RequestError as e:
        spoken_word_label.config(text="Lỗi kết nối mạng")
        print(f"Lỗi kết nối với dịch vụ nhận diện giọng nói: {e}")
        return ""
    except sr.WaitTimeoutError:
        spoken_word_label.config(text="Hết thời gian chờ")
        print("Hết thời gian chờ âm thanh.")
        return ""

def on_speak_button_threaded(current_word, spoken_word_label, learn_window):
    def run_speak():
        result = speak(spoken_word_label, learn_window)
        if result:
            spoken_word_label.config(text=f"Bạn đã nói: {result}")
            # Dam bao lean_window luon nam o tren truoc truoc khi thong bao
            learn_window.lift()
            if result.strip().lower() == current_word.strip().lower():
                messagebox.showinfo("Kết quả", "Phát âm đúng! 🎉", parent=learn_window)
            else:
                messagebox.showwarning("Kết quả", f"Phát âm sai!\nBạn nói: '{result}'\nĐúng phải là: '{current_word}'", parent=learn_window)
            learn_window.after(2000, lambda: spoken_word_label.config(text="Bạn đã nói: "))

    if not current_word:
        messagebox.showwarning("Lỗi", "Không có từ nào để kiểm tra!", parent=learn_window)
        return

    thread = threading.Thread(target=run_speak)
    thread.start()

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
        except Error as e:
            messagebox.showerror("Lỗi SQL", f"Không thể đăng ký: {e}", parent=register_window)
        finally:
            cursor.close()

    Button(register_window, text="Đăng ký", command=attempt_register, width=15, bg="green", fg="white").pack(pady=20)

def login(root):
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
                root.withdraw()  # An di main_window()
                if user['admin'] == 1:
                    messagebox.showinfo("Thành công", "Đăng nhập Admin thành công!")
                    admin_window(root)
                else:
                    messagebox.showinfo("Thành công", "Đăng nhập thành công!")
                    main_window(root)
            else:
                messagebox.showwarning("Lỗi", "Sai tài khoản hoặc mật khẩu!", parent=login_window)
        except Error as e:
            messagebox.showerror("Lỗi SQL", f"Không thể đăng nhập: {e}", parent=login_window)
        finally:
            if cursor:
                cursor.close()

    Button(login_window, text="Đăng nhập", command=attempt_login, width=15, bg="blue", fg="white").pack(pady=20)

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

        return random.choice(words)
    except Error as e:
        messagebox.showerror("Lỗi SQL", f"Không thể lấy từ: {e}")
        return None, None
    finally:
        cursor.close()

def main_window(root):
    learn_window = Toplevel(root)
    learn_window.geometry('1024x768')
    learn_window.title('Learning English')
    learn_window.resizable(False, False)

    current_word, current_meaning = get_random_word()
    if current_word is None:
        current_word, current_meaning = "", ""

    word_label = Label(learn_window, text=f"Từ vựng: {current_word}", font=("Arial", 20, "bold"), fg="darkblue")
    word_label.pack(pady=30)

    meaning_label = Label(learn_window, text=f"Nghĩa: {current_meaning}", font=("Arial", 18), fg="black")
    meaning_label.pack(pady=20)

    spoken_word_label = Label(learn_window, text="Bạn đã nói: ", font=("Arial", 16), fg="blue")
    spoken_word_label.pack(pady=20)

    def read_current_word():
        engine = pyttsx3.init()
        engine.setProperty('rate', 120)
        if current_word and current_meaning:
            engine.say(current_word)
            engine.runAndWait()
            learn_window.after(500, lambda: [engine.say(current_meaning), engine.runAndWait()])
        else:
            engine.say("Không có từ nào để đọc.")
            engine.runAndWait()

    def get_new_word():
        nonlocal current_word, current_meaning
        current_word, current_meaning = get_random_word()
        if current_word is None:
            current_word, current_meaning = "", ""
        word_label.config(text=f"Từ vựng: {current_word}")
        meaning_label.config(text=f"Nghĩa: {current_meaning}")
        spoken_word_label.config(text="Bạn đã nói: ")

    def on_closing():
        root.deiconify()
        learn_window.destroy()

    learn_window.protocol("WM_DELETE_WINDOW", on_closing)  # Xử lý khi đóng cửa sổ

    Button(learn_window, text="Nghe", command=read_current_word, width=15, bg="orange", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(learn_window, text="Từ mới", command=get_new_word, width=15, bg="purple", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(learn_window, text="Nói", command=lambda: on_speak_button_threaded(current_word, spoken_word_label, learn_window), width=15, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

    learn_window.mainloop()

def admin_window(root):
    admin = Toplevel(root)
    admin.title("Admin Dashboard")
    admin.geometry("400x300")

    Label(admin, text="Chào mừng Admin!", font=("Arial", 14)).pack(pady=20)

    def on_closing():
        root.deiconify()
        admin.destroy()

    admin.protocol("WM_DELETE_WINDOW", on_closing)

    admin.mainloop()


def main():
    root = Tk()
    root.title("Học tiếng Anh")
    root.geometry("1200x800")
    root.resizable(False, False)

    Label(root, text="Chào mừng bạn đến với ứng dụng học tiếng Anh", font=("Arial", 14, "bold"), fg="darkgreen").pack(pady=20)
    Button(root, text="Đăng nhập", width=20, command=lambda: login(root), bg="blue", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(root, text="Đăng ký", width=20, command=lambda: register(root), bg="green", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(root, text="Thoát", width=20, command=root.quit, bg="red", fg="white", font=("Arial", 12)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    init_database()
    main()