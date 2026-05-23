"""
Sidebar Component for Smart Notes Organizer.
Contains the note search panel and a custom scrollable, interactive notes list.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Callable
import config

class Sidebar(ttk.Frame):
    """
    Left-hand sidebar module. Hosts the search bar and the list of notes.
    Constructs dynamic cards for each note, supporting live filtering, hovers,
    and selection highlights.
    """
    def __init__(self, parent, on_note_selected: Callable[[int], None]):
        super().__init__(parent, style="Sidebar.TFrame")
        self.on_note_selected = on_note_selected
        self.selected_note_id = None
        self.note_cards: Dict[int, tk.Frame] = {}
        self.card_widgets: Dict[int, List[tk.Widget]] = {} # Inner card widgets to change bg on hover
        
        self._create_widgets()

    def _create_widgets(self):
        """Construct the sidebar layout components."""
        # 1. Branding Header
        header_frame = tk.Frame(self, bg=config.BG_SIDEBAR, pady=20, padx=15)
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame, 
            text="Smart Notes", 
            style="SidebarTitle.TLabel"
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(
            header_frame, 
            text="Organize your thoughts", 
            font=config.FONT_SUBTEXT,
            foreground=config.TEXT_MUTED,
            background=config.BG_SIDEBAR
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))

        # 2. Modern Search Frame
        search_frame = tk.Frame(self, bg=config.BG_SIDEBAR, padx=15, pady=(0, 15))
        search_frame.pack(fill=tk.X)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            style="TEntry"
        )
        self.search_entry.pack(fill=tk.X)
        self._add_placeholder(self.search_entry, "Search notes...")
        
        # 3. Dynamic Scrollable Note List container
        list_container = tk.Frame(self, bg=config.BG_SIDEBAR)
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Canvas & Scrollbar setup for scrolling arbitrary cards
        self.canvas = tk.Canvas(
            list_container,
            bg=config.BG_SIDEBAR,
            bd=0,
            highlightthickness=0,
            yscrollincrement=5
        )
        
        self.scrollbar = ttk.Scrollbar(
            list_container,
            orient=tk.VERTICAL,
            command=self.canvas.yview,
            style="Vertical.TScrollbar"
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame inside canvas to place all the note cards
        self.scroll_content = tk.Frame(self.canvas, bg=config.BG_SIDEBAR)
        self.scroll_content_window = self.canvas.create_window(
            (0, 0),
            window=self.scroll_content,
            anchor="nw"
        )

        # Pack scroll elements
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Event bindings for scrolling and responsive canvas resizing
        self.scroll_content.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind mousewheel globally over sidebar components
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _add_placeholder(self, entry: ttk.Entry, placeholder: str):
        """Standard placeholder behavior for the search bar entry."""
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
        self.search_placeholder = placeholder

    def _on_frame_configure(self, event):
        """Update scroll region size to fit dynamically added cards."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Make the content frame expand to match the canvas's width."""
        canvas_width = event.width
        self.canvas.itemconfig(self.scroll_content_window, width=canvas_width)

    def _on_mousewheel(self, event):
        """Process standard vertical mousewheel scrolling."""
        # Only scroll if mouse is actually over the sidebar region
        x, y = self.winfo_pointerxy()
        widget = self.winfo_containing(x, y)
        if widget and (self in widget.winfo_hierarchy() or widget == self):
            # Windows scroll is typically multiples of 120
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def populate_notes(self, notes: List[Dict[str, Any]], keep_selection: bool = True):
        """
        Dynamically render note cards inside the sidebar.
        
        Args:
            notes: A list of dictionary notes retrieved from the DB.
            keep_selection: If True, preserves active selection highlights if note still exists.
        """
        # Clear existing cards
        for card in self.note_cards.values():
            card.destroy()
            
        self.note_cards.clear()
        self.card_widgets.clear()

        # Render placeholder label if list is empty
        if not notes:
            placeholder_label = tk.Label(
                self.scroll_content,
                text="No notes found.",
                font=config.FONT_BODY,
                fg=config.TEXT_MUTED,
                bg=config.BG_SIDEBAR,
                pady=40
            )
            placeholder_label.pack(fill=tk.X)
            # Register inside cards to easily clean later
            self.note_cards[-1] = placeholder_label
            return

        # Render cards
        for idx, note in enumerate(notes):
            note_id = note['id']
            title = note['title']
            category = note['category']
            content = note['content'] or ""
            updated_at = note['updated_at']
            
            # Format preview snippet
            snippet = content.replace('\n', ' ').strip()
            if len(snippet) > 42:
                snippet = snippet[:40] + "..."
            if not snippet:
                snippet = "No additional text"

            # Create the card outer frame (use standard tk.Frame for color control)
            card = tk.Frame(
                self.scroll_content,
                bg=config.BG_CARD,
                padx=15,
                pady=12,
                cursor="hand2"
            )
            card.pack(fill=tk.X, pady=(0, 8), padx=(5, 5))
            self.note_cards[note_id] = card
            self.card_widgets[note_id] = []

            # Determine category tag color
            tag_color = config.ACCENT_COLOR
            if category == "Work":
                tag_color = config.COLOR_WARNING
            elif category == "Todo":
                tag_color = config.COLOR_SUCCESS
            elif category == "Important":
                tag_color = config.COLOR_DANGER
            elif category == "Ideas":
                tag_color = "#a855f7" # Modern Purple

            # Card Header: Category indicator & modified date
            header_panel = tk.Frame(card, bg=config.BG_CARD)
            header_panel.pack(fill=tk.X)
            self.card_widgets[note_id].append(header_panel)

            cat_lbl = tk.Label(
                header_panel,
                text=category.upper(),
                font=config.FONT_SUBTEXT_BOLD,
                fg=tag_color,
                bg=config.BG_CARD
            )
            cat_lbl.pack(side=tk.LEFT)
            self.card_widgets[note_id].append(cat_lbl)

            date_lbl = tk.Label(
                header_panel,
                text=updated_at.split(' ')[0], # Show only Date YYYY-MM-DD
                font=config.FONT_SUBTEXT,
                fg=config.TEXT_MUTED,
                bg=config.BG_CARD
            )
            date_lbl.pack(side=tk.RIGHT)
            self.card_widgets[note_id].append(date_lbl)

            # Card Title
            title_lbl = tk.Label(
                card,
                text=title,
                font=config.FONT_BODY_BOLD,
                fg=config.TEXT_PRIMARY,
                bg=config.BG_CARD,
                anchor="w",
                justify=tk.LEFT
            )
            title_lbl.pack(fill=tk.X, pady=(4, 2))
            self.card_widgets[note_id].append(title_lbl)

            # Card Excerpt Snippet
            snippet_lbl = tk.Label(
                card,
                text=snippet,
                font=config.FONT_SUBTEXT,
                fg=config.TEXT_SECONDARY,
                bg=config.BG_CARD,
                anchor="w",
                justify=tk.LEFT
            )
            snippet_lbl.pack(fill=tk.X)
            self.card_widgets[note_id].append(snippet_lbl)

            # Define hover animations and click actions
            self._bind_card_events(note_id, card)

        # Restore highlight if previously selected note is still in the active list
        if keep_selection and self.selected_note_id in self.note_cards:
            self.select_note(self.selected_note_id)

    def _bind_card_events(self, note_id: int, card: tk.Frame):
        """Register hover and mouse click events recursively onto note cards."""
        widgets = [card] + self.card_widgets[note_id]
        
        # Closures to capture correct note_id variables
        def on_enter(event, nid=note_id):
            if nid != self.selected_note_id:
                self._set_card_bg(nid, config.BG_CARD_HOVER)

        def on_leave(event, nid=note_id):
            if nid != self.selected_note_id:
                self._set_card_bg(nid, config.BG_CARD)

        def on_click(event, nid=note_id):
            self.select_note(nid)
            self.on_note_selected(nid)

        for widget in widgets:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

    def _set_card_bg(self, note_id: int, bg_color: str):
        """Helper to modify backgrounds of a note card and all nested labels."""
        if note_id in self.note_cards:
            self.note_cards[note_id].configure(bg=bg_color)
            for widget in self.card_widgets[note_id]:
                try:
                    widget.configure(bg=bg_color)
                except tk.TclError:
                    pass # Skip styling if widget has been destroyed

    def select_note(self, note_id: int):
        """Highlight a card as active and deselect prior selection."""
        # Deselect old note card
        if self.selected_note_id is not None and self.selected_note_id in self.note_cards:
            self._set_card_bg(self.selected_note_id, config.BG_CARD)

        # Select new note card
        self.selected_note_id = note_id
        if note_id is not None and note_id in self.note_cards:
            self._set_card_bg(note_id, config.BG_CARD_SELECTED)
            
            # Auto-scroll canvas to ensure selected card is visible
            card = self.note_cards[note_id]
            self.update_idletasks()
            
            # Retrieve heights/bounds
            y_top = card.winfo_y()
            y_bottom = y_top + card.winfo_height()
            canvas_height = self.canvas.winfo_height()
            
            # Check scroll content height
            content_height = self.scroll_content.winfo_height()
            if content_height > canvas_height:
                scroll_pos = y_top / content_height
                # Center-ish scrolling behavior
                self.canvas.yview_moveto(max(0.0, scroll_pos - 0.2))

    def clear_selection(self):
        """Deselect currently highlighted card."""
        if self.selected_note_id is not None and self.selected_note_id in self.note_cards:
            self._set_card_bg(self.selected_note_id, config.BG_CARD)
        self.selected_note_id = None
        
    def get_search_query(self) -> str:
        """Retrieve cleaned string query from search entry, ignoring placeholder."""
        val = self.search_var.get().strip()
        if val == self.search_placeholder:
            return ""
        return val
