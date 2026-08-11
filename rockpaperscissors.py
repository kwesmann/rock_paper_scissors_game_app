"""Entry point - keeps the original run command working.

    python rockpaperscissors.py
"""

from main import RPSApp

if __name__ == "__main__":
    app = RPSApp()
    app.mainloop()
