"""
Editor Component for Smart Notes Organizer.
Provides a rich and sleek interface for reading, writing, and modifying notes.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import config
from ui.styles import create_flat_button

class NoteEditor(ttk.Frame):
    """
    Panel representing the note workspace. Handles displaying selected note
    details, editing text, switching categories, and firing save/delete events.
    """
    def __init__(self, parent, on_save_callback, on_delete_callback, on_new_callback):
        super().__init__(parent)
        self.on_save_callback = on_save_callback
        self.on_delete_callback = on_delete_callback
        self.on_new_callback = on_new_callback
        
        self.current_note_id = None
        self._create_widgets()

    def _create_widgets(self):
        """Build editor interface controls."""
        # Main vertical padding frame
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        # 1. Header Area: Category Selector and Action Buttons
        header_frame = ttk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # Category selection Label & Combobox
        cat_label = ttk.Label(header_frame, text="Category:", font=config.FONT_SUBTEXT_BOLD)
        cat_label.pack(side=tk.LEFT, padx=(0, 8))

        self.category_var = tk.StringVar(value="Uncategorized")
        self.cat_combobox = ttk.Combobox(
            header_frame,
            textvariable=self.category_var,
            values=config.CATEGORIES,
            state="readonly",
            width=15
        )
        self.cat_combobox.pack(side=tk.LEFT)

        # Status Label (Shows last saved date/time)
        self.status_var = tk.StringVar(value="New Note (Unsaved)")
        self.status_label = ttk.Label(
            header_frame, 
            textvariable=self.status_var, 
            font=config.FONT_SUBTEXT, 
            foreground=config.TEXT_MUTED
        )
        self.status_label.pack(side=tk.RIGHT)

        # 2. Title Field (Large styled input)
        title_frame = ttk.Frame(container)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(
            title_frame,
            textvariable=self.title_var,
            font=config.FONT_TITLE_LARGE,
            style="TEntry"
        )
        self.title_entry.pack(fill=tk.X)
        self._add_placeholder(self.title_entry, "Enter Note Title Here...")

        # 3. Content Text Area (Monospace editor with custom scrollbar)
        text_container = ttk.Frame(container)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # We use a standard text widget since ttk doesn't offer a text widget,
        # but style it manually to match the slate theme flawlessly.
        self.content_text = tk.Text(
            text_container,
            bg=config.BG_PRIMARY,
            fg=config.TEXT_PRIMARY,
            insertbackground=config.TEXT_PRIMARY,  # Caret cursor color
            selectbackground=config.BG_CARD_SELECTED,
            selectforeground=config.TEXT_INVERSE,
            font=config.FONT_EDITOR,
            relief="flat",
            borderwidth=1,
            highlightbackground=config.BORDER_COLOR,
            highlightcolor=config.ACCENT_COLOR,
            highlightthickness=1,
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        
        scrollbar = ttk.Scrollbar(
            text_container, 
            orient=tk.VERTICAL, 
            command=self.content_text.yview,
            style="Vertical.TScrollbar"
        )
        self.content_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 4. Action Command Buttons at the Bottom
        actions_frame = ttk.Frame(container)
        actions_frame.pack(fill=tk.X)

        # Primary Save Button
        self.btn_save = create_flat_button(
            actions_frame,
            text="Save Note",
            bg_color=config.ACCENT_COLOR,
            hover_color=config.ACCENT_HOVER,
            command=self._handle_save
        )
        self.btn_save.pack(side=tk.LEFT, padx=(0, 10))

        # Secondary "New" Button
        self.btn_new = create_flat_button(
            actions_frame,
            text="New Note",
            bg_color=config.BG_SIDEBAR,
            hover_color=config.BG_CARD,
            fg_color=config.TEXT_SECONDARY,
            command=self._handle_new
        )
        self.btn_new.pack(side=tk.LEFT)

        # Destructive Delete Button
        self.btn_delete = create_flat_button(
            actions_frame,
            text="Delete Note",
            bg_color=config.COLOR_DANGER,
            hover_color=config.COLOR_DANGER_HOVER,
            command=self._handle_delete
        )
        self.btn_delete.pack(side=tk.RIGHT)

    def _add_placeholder(self, entry: ttk.Entry, placeholder: str):
        """Helper to assign a modern interactive greyed placeholder to an Entry."""
        entry.insert(0, placeholder)
        entry.configure(foreground=config.TEXT_MUTED)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.configure(foreground=config.TEXT_PRIMARY)

        def on_focus_out(event):
            if not entry.get().strip():
                entry.insert(0, placeholder)
                entry.configure(foreground=config.TEXT_MUTED)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        self.title_placeholder = placeholder

    def load_note(self, note_id: int, title: str, content: str, category: str, updated_at: str):
        """Populate the editor fields with note data."""
        self.current_note_id = note_id
        
        # Enable and configure normal colors for title
        self.title_entry.configure(foreground=config.TEXT_PRIMARY)
        self.title_var.set(title)
        
        # Populate category combobox
        if category in config.CATEGORIES:
            self.category_var.set(category)
        else:
            self.category_var.set("Uncategorized")
            
        # Update text field
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", content)
        
        # Set status tracker
        self.status_var.set(f"Last updated: {updated_at}")
        
    def clear_editor(self):
        """Reset the editor states back to empty/new note."""
        self.current_note_id = None
        self.title_var.set("")
        self._add_placeholder(self.title_entry, self.title_placeholder)
        self.category_var.set("Uncategorized")
        self.content_text.delete("1.0", tk.END)
        self.status_var.set("New Note (Unsaved)")

    def _handle_save(self):
        """Validate and dispatch note save callback."""
        try:
            title = self.title_var.get().strip()
            content = self.content_text.get("1.0", "end-1c")
            category = self.category_var.get()
            
            # Prevent saving default placeholder text
            if not title or title == self.title_placeholder:
                messagebox.showwarning("Validation Error", "Note title cannot be blank!")
                return

            self.on_save_callback(self.current_note_id, title, content, category)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred while saving: {e}")

    def _handle_new(self):
        """Dispatch event to create a blank new note."""
        try:
            self.clear_editor()
            self.on_new_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create new note: {e}")

    def _handle_delete(self):
        """Confirm and dispatch deletion of the active note."""
        if self.current_note_id is None:
            messagebox.showinfo("Information", "This note is not saved yet.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete", 
            "Are you absolutely sure you want to delete this note?",
            icon=messagebox.WARNING
        )
        
        if confirm:
            try:
                self.on_delete_callback(self.current_note_id)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete note: {e}")
