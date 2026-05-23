"""
Configuration file for Smart Notes Organizer.
Contains global constants, visual style settings, and file paths.
"""
import os

# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "notes.db")

# Predefined categories for note classification
CATEGORIES = ["Personal", "Work", "Ideas", "Todo", "Important", "Uncategorized"]

# ==========================================
# Visual Style Tokens (Slate Dark Theme)
# ==========================================
BG_PRIMARY = "#0f172a"       # Sleek slate dark background
BG_SIDEBAR = "#1e293b"       # Sidebar panel color
BG_CARD = "#334155"          # Default note card background
BG_CARD_HOVER = "#475569"    # Hovered note card color
BG_CARD_SELECTED = "#2563eb" # Highlighted selected note card color

TEXT_PRIMARY = "#f8fafc"     # Primary text (almost white)
TEXT_SECONDARY = "#cbd5e1"   # Secondary label text (light gray)
TEXT_MUTED = "#94a3b8"       # Secondary subtext/dates (slate gray)
TEXT_INVERSE = "#ffffff"     # White text for high contrast

ACCENT_COLOR = "#3b82f6"     # Slate blue primary color
ACCENT_HOVER = "#1d4ed8"     # Darker blue for hovers
COLOR_SUCCESS = "#10b981"    # Emerald green for success feedback
COLOR_WARNING = "#f59e0b"    # Warm amber for warnings
COLOR_DANGER = "#ef4444"     # Red for deletion actions
COLOR_DANGER_HOVER = "#b91c1c"# Darker red for deletion hovers

# Border and separator lines
BORDER_COLOR = "#334155"

# Fonts (Modern Sans-Serif family)
FONT_FAMILY = "Segoe UI"
FONT_TITLE_LARGE = (FONT_FAMILY, 18, "bold")
FONT_TITLE_MEDIUM = (FONT_FAMILY, 12, "bold")
FONT_BODY = (FONT_FAMILY, 10, "normal")
FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
FONT_SUBTEXT = (FONT_FAMILY, 9, "normal")
FONT_SUBTEXT_BOLD = (FONT_FAMILY, 9, "bold")
FONT_EDITOR = ("Consolas", 11, "normal")  # Clean monospace font for writing notes
