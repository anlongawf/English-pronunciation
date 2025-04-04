from tkinter import *
from database import check_database
from tkinter import messagebox
from mysql.connector import Error


def get_word(word):
    db = check_database()
    if db is None:
        return None

    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute("SELECT word FROM words WHERE word = %s", (word,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Error as e:
        print(f"Lỗi cơ sở dữ liệu: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def data_entry(word_entry, meaning_entry):
    new_word = word_entry.get().strip()
    new_meaning = meaning_entry.get().strip()

    if not new_word or not new_meaning:
        messagebox.showerror("Thieu du lieu", "Ban can nhap du word va meaning")
        return

    existing_word = get_word(new_word)
    if existing_word:
        messagebox.showwarning("Từ đã tồn tại", f"Từ '{new_word}' đã tồn tại trong từ điển!")
        return

    db = check_database()
    if db is None:
        messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến cơ sở dữ liệu")
        return

    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO words (word, meaning) VALUES (%s, %s)", (new_word, new_meaning))
        db.commit()
        messagebox.showinfo("Thêm từ mới thành công", f"Bạn vừa thêm từ '{new_word}' có nghĩa '{new_meaning}'")

        word_entry.delete(0, END)
        meaning_entry.delete(0, END)

    except Error as e:
        if db:
            db.rollback()
        messagebox.showerror("Lỗi cơ sở dữ liệu", f"Không thể thêm từ mới: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def admin_window(root):
    admin = Toplevel(root)
    admin.title("Admin Dashboard")
    admin.geometry("400x300")

    Label(admin, text="Chào mừng Admin!", font=("Arial", 14)).grid(column=0, row=0, columnspan=2)

    Label(admin, text="New word:", font=("Arial", 12)).grid(column=0, row=1, sticky="w", padx=10, pady=5)
    word_entry = Entry(admin, width=30)
    word_entry.grid(column=1, row=1, padx=10, pady=5)

    Label(admin, text="Meaning:", font=("Arial", 12)).grid(column=0, row=2, sticky="w", padx=10, pady=5)
    meaning_entry = Entry(admin, width=30)
    meaning_entry.grid(column=1, row=2, padx=10, pady=5)

    add_button = Button(
        admin, text="Thêm từ", font=("Arial", 12),
        command=lambda: data_entry(word_entry, meaning_entry))
    add_button.grid(column=0, row=3, columnspan=2, pady=10)

    return admin


if __name__ == "__main__":
    root = Tk()
    admin_win = admin_window(root)
    root.mainloop()