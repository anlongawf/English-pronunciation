import pyttsx3
import speech_recognition as sr
import threading
from tkinter import messagebox

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

def read_current_word(current_word, current_meaning):
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)
    if current_word and current_meaning:
        engine.say(current_word)
        engine.runAndWait()
        engine.say(current_meaning)
        engine.runAndWait()
    else:
        engine.say("Không có từ nào để đọc.")
        engine.runAndWait()