from tkinter import *

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