# Smart Notes Organizer 📝✨

A sleek, modern, and highly modular desktop note-taking application written in **Python 3** using the **Tkinter GUI toolkit** and powered by an embedded **SQLite database**. 

Designed with rich, slate-dark aesthetics, seamless search capabilities, and a beginner-friendly architecture, this project adheres to strict Object-Oriented Programming (OOP) concepts, robust exception-handling paradigms, and comprehensive automated unit-testing suites.

---

## 🌟 Features

*   **Create Notes**: Instantly spin up a new note canvas, type a title, assign a category, and draft your thoughts.
*   **Read & Select**: Click dynamically rendered "Note Cards" in the sidebar with smooth hover indicators and active highlights.
*   **Update Notes**: Make edits and hit "Save". The app updates details instantly, tracks modified dates, and auto-orders cards by date (newest first).
*   **Delete Notes**: Safely delete unwanted notes with standard verification dialog warnings.
*   **Real-Time Search**: Type in the search box to filter your notes instantly by title, content, or category (no manual refresh buttons needed!).
*   **Categorization**: Organize notes under tags like *Personal, Work, Ideas, Todo, Important, or Uncategorized* with distinct tag-color treatments.
*   **Sleek Modern UI**: Complete design overhaul of retro Tkinter themes using a slate-blue color palette, borderless flat buttons with hover effects, responsive layouts, and custom scrollable canvasses.
*   **Robust Stability**: Global exception hook blocks raw trace crashes and informs users with interactive popup dialogs.

---

## 📂 Project Directory Structure

The project follows a standard, GitHub-friendly modular organization:

```
smart_notes_organizer/
├── README.md                  # Comprehensive user and developer manual
├── requirements.txt           # File detailing runtime dependencies (standard library)
├── config.py                  # Global color palettes, typography, and constants
├── main.py                    # Main bootstrap entry point script
├── database/
│   ├── __init__.py            # Database module export declarations
│   └── db_manager.py          # SQLite database setup and transactional CRUD operations
├── ui/
│   ├── __init__.py            # UI components packaging
│   ├── app.py                 # Main Window, controller, and global error boundaries
│   ├── styles.py              # Visual themes and widget customization helpers
│   └── components/
│       ├── __init__.py        # Individual UI panels packaging
│       ├── sidebar.py         # Search frame and scrollable note card list
│       └── editor.py          # Note reading/writing workspace and action buttons
└── tests/
    ├── __init__.py            # Test package declarations
    └── test_db.py             # Unit tests for checking SQLite operations in isolation
```

---

## 🚀 Setup & Execution Guide

### Prerequisites
*   **Python 3.8 or higher** installed. You can check your version by running:
    ```bash
    python --version
    ```

### Step 1: Clone or Open the Directory
Navigate to the root directory where the folder `smart_notes_organizer` is located.
```bash
cd smart_notes_organizer
```

### Step 2: Running the Application
Since the application relies **100% on the Python Standard Library**, there are absolutely no external packages to install! Simply run:
```bash
python main.py
```

---

## 🧪 Automated Testing

We have built a thorough, isolated unit-testing suite under `tests/test_db.py` to validate CRUD behavior, empty checks, index integrity, and text search metrics without altering your local database file (it runs in-memory).

To run the unit tests, execute:
```bash
python -m unittest tests/test_db.py -v
```

---

## 📦 Deployment Instructions

As a Python desktop GUI application, deployment is straightforward:

### Option 1: Standard Python Execution (Recommended)
Distribute the `smart_notes_organizer` directory to users. As long as they have Python installed, they can double-click `main.py` or run `python main.py` in their terminal to launch the app. The database (`notes.db`) will automatically generate in their folder on first startup!

### Option 2: Build a Standalone Executable (Windows/macOS)
If you want to bundle the app into a single `.exe` file so users can run it without installing Python, use **PyInstaller**:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the single-file bundle:
   ```bash
   pyinstaller --noconsole --onefile main.py
   ```
   *Note: `--noconsole` prevents the command prompt window from popping up behind the GUI.*
3. Locate the finished app inside the generated `dist/` directory! Share `main.exe` directly with your users.

---

## 🛠️ Version Control with Git

If you are committing this project to a remote repository (like GitHub), follow this standard step-by-step checklist:

### 1. Initialize Git
From the root of your project directory, initialize a new Git repository:
```bash
git init
```

### 2. Create a `.gitignore` File
To avoid tracking unnecessary files, databases, or compile folders, create a `.gitignore` file:
```bash
# Windows system files
Thumbs.db
Desktop.ini

# Python bytecode caches
__pycache__/
*.pyc
*.pyo
*.pyd

# SQLite Database created at runtime
notes.db

# PyInstaller build files
build/
dist/
*.spec
```

### 3. Add and Commit
Stage all files to be committed:
```bash
git add .
```

Commit the staged files with an informative message:
```bash
git commit -m "feat: initial commit of modular Smart Notes Organizer"
```

### 4. Push to GitHub
Create a new blank repository on GitHub (without initializing README/license) and link it:
```bash
# Associate the remote repo (replace with your actual URL)
git remote add origin https://github.com/YOUR_USERNAME/smart-notes-organizer.git

# Set active branch to main
git branch -M main

# Push code to remote origin
git push -u origin main
```
