"""
UI Theme and Styles configurations for Smart Notes Organizer.
Defines style rules for custom visual aesthetics in Tkinter.
"""
import tkinter as tk
from tkinter import ttk
import config

def apply_global_styles(root: tk.Tk):
    """
    Configure custom styles for standard ttk widgets and apply general window configurations.
    Uses 'clam' theme to override system defaults and enable high-fidelity customization.
    """
    root.configure(bg=config.BG_PRIMARY)
    
    style = ttk.Style()
    
    # Use 'clam' as a base because it is highly customizable and consistent cross-platform
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass # Fallback to default if clam is not available
        
    # Standard Frame configuration
    style.configure(
        "TFrame",
        background=config.BG_PRIMARY
    )
    style.configure(
        "Sidebar.TFrame",
        background=config.BG_SIDEBAR
    )
    style.configure(
        "Card.TFrame",
        background=config.BG_CARD
    )
    
    # Custom Labels
    style.configure(
        "TLabel",
        background=config.BG_PRIMARY,
        foreground=config.TEXT_PRIMARY,
        font=config.FONT_BODY
    )
    style.configure(
        "Title.TLabel",
        background=config.BG_PRIMARY,
        foreground=config.TEXT_PRIMARY,
        font=config.FONT_TITLE_LARGE
    )
    style.configure(
        "SidebarTitle.TLabel",
        background=config.BG_SIDEBAR,
        foreground=config.TEXT_PRIMARY,
        font=config.FONT_TITLE_MEDIUM
    )
    style.configure(
        "Muted.TLabel",
        background=config.BG_PRIMARY,
        foreground=config.TEXT_MUTED,
        font=config.FONT_SUBTEXT
    )
    style.configure(
        "CardTitle.TLabel",
        background=config.BG_CARD,
        foreground=config.TEXT_PRIMARY,
        font=config.FONT_BODY_BOLD
    )
    style.configure(
        "CardDate.TLabel",
        background=config.BG_CARD,
        foreground=config.TEXT_MUTED,
        font=config.FONT_SUBTEXT
    )
    style.configure(
        "CardCategory.TLabel",
        background=config.BG_CARD,
        foreground=config.ACCENT_COLOR,
        font=config.FONT_SUBTEXT_BOLD
    )

    # Modern Entry Styling
    style.configure(
        "TEntry",
        fieldbackground=config.BG_PRIMARY,
        background=config.BORDER_COLOR,
        foreground=config.TEXT_PRIMARY,
        bordercolor=config.BORDER_COLOR,
        lightcolor=config.BORDER_COLOR,
        darkcolor=config.BORDER_COLOR,
        font=config.FONT_BODY,
        insertcolor=config.TEXT_PRIMARY
    )
    style.map(
        "TEntry",
        bordercolor=[('focus', config.ACCENT_COLOR)],
        lightcolor=[('focus', config.ACCENT_COLOR)],
        darkcolor=[('focus', config.ACCENT_COLOR)]
    )

    # ComboBox styling
    style.configure(
        "TCombobox",
        fieldbackground=config.BG_PRIMARY,
        background=config.BG_SIDEBAR,
        foreground=config.TEXT_PRIMARY,
        bordercolor=config.BORDER_COLOR,
        lightcolor=config.BORDER_COLOR,
        darkcolor=config.BORDER_COLOR,
        font=config.FONT_BODY,
        arrowcolor=config.TEXT_PRIMARY
    )
    style.map(
        "TCombobox",
        fieldbackground=[('readonly', config.BG_PRIMARY)],
        foreground=[('readonly', config.TEXT_PRIMARY)]
    )

    # Custom Flat Scrollbar Styling
    style.configure(
        "Vertical.TScrollbar",
        gripcount=0,
        background=config.BG_SIDEBAR,
        troughcolor=config.BG_PRIMARY,
        bordercolor=config.BG_PRIMARY,
        lightcolor=config.BG_PRIMARY,
        darkcolor=config.BG_PRIMARY,
        arrowsize=10
    )
    style.map(
        "Vertical.TScrollbar",
        background=[('active', config.BG_CARD), ('pressed', config.ACCENT_COLOR)]
    )


# Helper function to create gorgeous modern buttons
def create_flat_button(
    parent, 
    text: str, 
    bg_color: str, 
    hover_color: str, 
    fg_color: str = config.TEXT_INVERSE, 
    command=None,
    font=config.FONT_BODY_BOLD
) -> tk.Button:
    """
    Creates a highly polished flat Button using standard tk.Button.
    Standard tk.Button allows borderless flat designs with custom state changes 
    which are extremely clean and cross-platform compared to default OS buttons.
    """
    btn = tk.Button(
        parent,
        text=text,
        bg=bg_color,
        fg=fg_color,
        font=font,
        activebackground=hover_color,
        activeforeground=fg_color,
        bd=0,
        relief="flat",
        padx=12,
        pady=8,
        cursor="hand2",
        command=command
    )
    
    # Add modern hover animations
    def on_enter(event):
        btn.configure(bg=hover_color)
        
    def on_leave(event):
        btn.configure(bg=bg_color)
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn
