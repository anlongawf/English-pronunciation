# English Learning Application

This is a simple application for practicing English pronunciation and vocabulary. It is built with Python and features a graphical interface (Tkinter), speech recognition, text-to-speech functionality, and user management via a MariaDB/MySQL database.

## Features
- **User Authentication**: Users can register and log in with admin/user roles.
- **Vocabulary Learning**: Displays random words with meanings, supports text-to-speech playback, and pronunciation checking.
- **Admin Dashboard**: Allows administrators to manage words and users (add/delete words, manage accounts).

## Requirements
### Software
- Python
- MariaDB (or MySQL)
- Microphone (for speech recognition)

### Python Libraries
The application requires the following libraries:
```bash
pip install mysql-connector-python pyttsx3 SpeechRecognition pynput
```
- `tkinter`: GUI framework
- `mysql-connector-python`: Database connectivity
- `pyttsx3`: Text-to-speech
- `speech_recognition`: Speech recognition
- `threading`: Handles speech recognition in a separate thread
- `pynput`: Potential keyboard/mouse control (not actively used)

## Project Structure
```
project/
│
├── main.py              # Main entry point of the application
├── database.py          # Handles database connection and queries
├── speech.py            # Manages speech recognition and text-to-speech
├── gui.py               # Login and registration interface
├── learn_window.py      # Vocabulary learning interface
├── admin_window.py      # Admin interface
├── english.sql          # Database schema and table creation script
└── README.md            # Usage instructions
```

## Installation
1. **Set Up the Database**
   - Install MariaDB/MySQL on your machine.
   - Run the `english.sql` script to create the necessary database and tables.
   
2. **Run the Application**
```bash
python main.py
```

## Build Application (Convert to Executable)
To package the application into an executable file, use `pyinstaller`:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```
This will generate an executable file in the `dist/` folder.

For a full GUI-based executable:
```bash
pyinstaller --onefile --windowed --name EnglishApp main.py
```

## Usage
### Login Credentials
- **Admin:** Username: `andeptrai` / Password: `andeptrai`
- **User:** Can register manually via the application

### Vocabulary Learning
- Click **"Listen"** to hear the word and its meaning.
- Click **"New Word"** to generate a random word.
- Click **"Speak"** to test pronunciation (requires a microphone).

## Operating System Notes
- On **Linux/macOS**, additional setup may be required:
  - Install `espeak` for `pyttsx3`
  - Install `portaudio` for `speech_recognition`
- Ensure your microphone is properly configured and permissions are granted.

## Debugging
If errors occur, check the following:
- **Database Connection**: Ensure MariaDB/MySQL is running and credentials are correct.
- **Microphone Access**: Test with a simple recording app first to verify functionality.

## Author
Created by **anlongawf**

📧 Contact: anan123456a123@gmail.com

## License
This project is open-source. Feel free to modify and use it as needed.

