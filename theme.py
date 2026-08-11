"""Theme palettes for light & dark mode.

Views reference colors through this module (e.g. ``theme.APP_BG``) so that
``set_theme()`` re-points every color name at once, app-wide.
"""

PALETTES = {
    "light": {
        "APP_BG": "#eaf2fb",        # light blue page
        "PANEL": "#ffffff",         # white cards
        "PANEL_TINT": "#e3eef9",    # very light blue
        "BORDER": "#bcd6ee",        # soft blue border
        "TEXT": "#123a5f",          # deep navy
        "MUTED": "#5b7e9f",         # muted slate blue
        "ACCENT": "#2f7fe0",        # vivid blue for primary buttons
        "ACCENT_DARK": "#1f5fb8",   # hover for accent
        "SKY": "#bfe0ff",           # pale sky
        "WIN_COLOR": "#0f9d6b",     # green for the match winner
    },
    "dark": {
        "APP_BG": "#0b1526",        # deep navy page
        "PANEL": "#12203a",         # dark cards
        "PANEL_TINT": "#182a4c",    # slightly lighter card
        "BORDER": "#27406b",        # steel blue border
        "TEXT": "#e4eefc",          # pale text
        "MUTED": "#8aa3c4",         # slate text
        "ACCENT": "#3b82f6",        # vivid blue
        "ACCENT_DARK": "#6ba8ff",   # lighter hover for accent
        "SKY": "#1e3a63",           # deep sky
        "WIN_COLOR": "#37d99a",     # bright green
    },
}

CURRENT_THEME = "light"


def set_theme(name):
    """Apply a palette to this module's color globals."""
    global CURRENT_THEME
    CURRENT_THEME = name
    globals().update(PALETTES[name])


def is_dark():
    return CURRENT_THEME == "dark"


set_theme(CURRENT_THEME)
