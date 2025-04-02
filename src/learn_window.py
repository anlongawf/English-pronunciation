from tkinter import *
from database import get_random_word
from speech import on_speak_button_threaded, read_current_word

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

    learn_window.protocol("WM_DELETE_WINDOW", on_closing)

    Button(learn_window, text="Nghe", command=lambda: read_current_word(current_word, current_meaning), width=15, bg="orange", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(learn_window, text="Từ mới", command=get_new_word, width=15, bg="purple", fg="white", font=("Arial", 12)).pack(pady=10)
    Button(learn_window, text="Nói", command=lambda: on_speak_button_threaded(current_word, spoken_word_label, learn_window), width=15, bg="green", fg="white", font=("Arial", 12)).pack(pady=10)

    learn_window.mainloop()