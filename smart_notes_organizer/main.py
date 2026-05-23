"""
Smart Notes Organizer
A complete, modular, and modern note-taking application.
Developed using Python, Tkinter, and SQLite.
"""
import sys
import logging
from tkinter import messagebox
from ui.app import SmartNotesApp

def main():
    """Application bootstrap entry point."""
    # Configure root logging format
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info("Starting Smart Notes Organizer bootstrap...")
    
    try:
        # Create and run the Tkinter application
        app = SmartNotesApp()
        logging.info("Application initialized successfully. Running mainloop.")
        app.mainloop()
        logging.info("Application closed normally.")
    except Exception as e:
        logging.critical("Fatal application crash during bootstrap:", exc_info=True)
        try:
            messagebox.showerror(
                "Fatal Startup Error",
                f"A critical error occurred while starting the application:\n\n{e}\n\nPlease check your installation."
            )
        except Exception:
            pass # Standard tk might not be initialized, ignore display failures
        sys.exit(1)

if __name__ == "__main__":
    main()
