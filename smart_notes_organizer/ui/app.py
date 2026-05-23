"""
Main Application Coordinator for Smart Notes Organizer.
Integrates the Database Layer and UI Components into a cohesive OOP system.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import logging
import sys
import config
from database.db_manager import DatabaseManager, DatabaseError
from ui.styles import apply_global_styles
from ui.components.sidebar import Sidebar
from ui.components.editor import NoteEditor

class SmartNotesApp(tk.Tk):
    """
    Main application window and coordinator.
    Acts as the controller in an MVC-like architecture: routes database queries,
    relays events between components, and handles top-level operations.
    """
    def __init__(self):
        super().__init__()
        
        # Configure logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        
        # Register global crash handler override to fulfill exception handling everywhere
        self.report_callback_exception = self.handle_global_exception
        
        self.title("Smart Notes Organizer")
        self.geometry("1100x700")
        self.min_width = 800
        self.min_height = 500
        self.minsize(self.min_width, self.min_height)
        
        # Center the window on display
        self._center_window()
        
        # Initialize Database Layer
        try:
            self.db_manager = DatabaseManager(config.DATABASE_PATH)
        except DatabaseError as e:
            messagebox.showerror("Critical Error", f"Failed to initialize database:\n{e}\nThe application will now close.")
            self.destroy()
            sys.exit(1)
            
        # Apply visual tokens and modern themes
        apply_global_styles(self)
        
        # Build UI Components
        self._build_layout()
        
        # Load initial note collection
        self.refresh_notes_list()
        
        # Bind typing search trace for interactive live filtering
        self.sidebar.search_var.trace_add("write", self._on_search_typing)

    def _center_window(self):
        """Center the window frame on the user's screen."""
        self.update_idletasks()
        width = 1100
        height = 700
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_layout(self):
        """Create and place the main structural layout components."""
        # We use a stylish ttk.Panedwindow to let users resize the sidebar width!
        self.paned_window = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # 1. Left Sidebar Component
        self.sidebar = Sidebar(self.paned_window, on_note_selected=self.handle_note_selected)
        self.paned_window.add(self.sidebar, weight=1)

        # 2. Right Editor Component
        self.editor = NoteEditor(
            self.paned_window,
            on_save_callback=self.handle_save_note,
            on_delete_callback=self.handle_delete_note,
            on_new_callback=self.handle_new_note
        )
        self.paned_window.add(self.editor, weight=3)

    def refresh_notes_list(self, keep_selection: bool = True):
        """Fetch matching notes based on current search input and update sidebar."""
        try:
            query = self.sidebar.get_search_query()
            if query:
                notes = self.db_manager.search_notes(query)
            else:
                notes = self.db_manager.get_all_notes()
            
            self.sidebar.populate_notes(notes, keep_selection=keep_selection)
        except DatabaseError as e:
            logging.error(f"Error fetching notes: {e}")
            messagebox.showerror("Database Error", f"Could not retrieve notes: {e}")

    def _on_search_typing(self, *args):
        """Event fired dynamically as the user types in the search box."""
        # As they type, perform instantaneous reload (keeping active selection if matching)
        self.refresh_notes_list(keep_selection=True)

    def handle_note_selected(self, note_id: int):
        """Action handler when a note card is clicked in the sidebar."""
        try:
            note = self.db_manager.get_note_by_id(note_id)
            if note:
                # Load note details into right-hand editor pane
                self.editor.load_note(
                    note_id=note['id'],
                    title=note['title'],
                    content=note['content'] or "",
                    category=note['category'],
                    updated_at=note['updated_at']
                )
            else:
                messagebox.showerror("Error", "Selected note was not found in the database.")
                self.refresh_notes_list(keep_selection=False)
        except DatabaseError as e:
            logging.error(f"Failed to load note {note_id}: {e}")
            messagebox.showerror("Database Error", f"Could not load note: {e}")

    def handle_save_note(self, note_id: int, title: str, content: str, category: str):
        """Action handler when save note button is clicked in the editor."""
        try:
            if note_id is None:
                # 1. Create operations
                new_id = self.db_manager.add_note(title, content, category)
                messagebox.showinfo("Success", f"Note '{title}' created successfully!", parent=self)
                # Select the new note after reloading
                self.refresh_notes_list(keep_selection=False)
                self.sidebar.select_note(new_id)
                self.handle_note_selected(new_id)
            else:
                # 2. Update operations
                success = self.db_manager.update_note(note_id, title, content, category)
                if success:
                    # Select same note after reload
                    self.refresh_notes_list(keep_selection=True)
                    # Re-load to update modified timestamp
                    self.handle_note_selected(note_id)
                else:
                    messagebox.showerror("Save Failed", "Failed to update note. It may have been deleted.")
                    self.refresh_notes_list(keep_selection=False)
                    self.editor.clear_editor()
        except DatabaseError as e:
            logging.error(f"Database operation failed: {e}")
            messagebox.showerror("Database Error", f"Operation failed:\n{e}")

    def handle_delete_note(self, note_id: int):
        """Action handler when delete note button is clicked in the editor."""
        try:
            success = self.db_manager.delete_note(note_id)
            if success:
                # Clear active panels
                self.editor.clear_editor()
                self.sidebar.clear_selection()
                # Reload list
                self.refresh_notes_list(keep_selection=False)
            else:
                messagebox.showerror("Delete Failed", "The requested note could not be found.")
        except DatabaseError as e:
            logging.error(f"Database operation failed: {e}")
            messagebox.showerror("Database Error", f"Failed to delete note:\n{e}")

    def handle_new_note(self):
        """Action handler when editor commands a fresh canvas."""
        # Simply deselect the active card to indicate a new note is being written
        self.sidebar.clear_selection()

    def handle_global_exception(self, exc_type, exc_value, exc_traceback):
        """Global Tkinter error catcher to prevent silent trace crashes."""
        logging.critical("Uncaught Exception intercepted:", exc_info=(exc_type, exc_value, exc_traceback))
        
        # Display a neat warning modal to user instead of raw terminal dump
        err_msg = f"An unexpected system exception occurred:\n\n{exc_value}\n\nThe app will try to remain stable."
        messagebox.showerror("Unexpected System Error", err_msg)
