# English Learning Application

This is a simple application to practice speaking pronunciation and learn English.  built with Python, featuring a graphical interface (Tkinter), speech recognition, text-to-speech for vocabulary, and user management via a MariaDB/MySQL database.

## Features
- **Register/Login**: Users can create an account or log in (with admin/user roles).
- **Vocabulary Learning**: Displays random words with meanings, supports listening to words, and checks pronunciation.
- **Admin Dashboard**: Separate interface for administrators. Administrators can add new words or delete words and manage users.
## Requirements
### Software
- Python
- MariaDB (or MySQL)
- Microphone (for speech recognition)

### Python Libraries
The application uses the following libraries:
- `tkinter`: For the graphical user interface.
- `mysql-connector-python`: For database connectivity.
- `pyttsx3`: For text-to-speech functionality.
- `speech_recognition`: For speech recognition.
- `threading`: For running speech recognition in a separate thread.
- `pynput`: For potential keyboard/mouse control (not actively used in current code).

Install them with:
```bash
pip install mysql-connector-python pyttsx3 SpeechRecognition pynput

Project Structure

project/
│
├── main.py              # Main file to run the application
├── database.py          # Handles database connection and queries
├── speech.py            # Manages speech recognition and text-to-speech
├── gui.py               # Login and registration interface
├── learn_window.py      # Vocabulary learning interface
├── admin_window.py      # Admin interface
├── english.sql          # SQL file to create database and tables
└── README.md            # Usage instructions

Installation
1. Set Up the Database
Install MariaDB/MySQL on your machine.
Run file  createdata.sql 

Run:
python main.py

Usage
Login:
Admin: andeptrai / andeptrai

User: U can register

Vocabulary Learning:
Click "Listen" to hear the word and its meaning.

Click "New Word" to get a random word.

Click "Speak" to test your pronunciation (requires a microphone).

Operating System: 
On Linux/macOS, speech features may require additional setup (e.g., install espeak for pyttsx3 and portaudio for speech_recognition).

Ensure your microphone is configured and permissions are granted.

Debugging: If errors occur, check:
Database connection (MariaDB/MySQL running, correct credentials).

Microphone access (test with a simple recording app first).

Author
Created by anlongawf.

Contact: anan123456a123@gmail.com

License
This project is open-source; feel free to modify and use it as needed.

---
