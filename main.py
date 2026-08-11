"""Application window that wires the views together."""

import os
import customtkinter as ctk

import theme
from helpers import BASE_DIR
from splash import SplashScreen
from menu import MenuView
from game import GameView


class RPSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Rock · Paper · Scissors")
        self.geometry("580x680")
        self.resizable(True, True)
        self.configure(fg_color=theme.APP_BG)

        try:
            self.iconbitmap(os.path.join(BASE_DIR, 'images', 'rpslogo.ico'))
        except Exception:
            pass

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, fg_color=theme.APP_BG, corner_radius=0)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.center_window()
        self.withdraw()                     # stay hidden until splash is done
        self.splash = SplashScreen(self._boot)

    def _boot(self):
        self.show_menu()
        self.deiconify()

    def center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def clear_container(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_menu(self):
        self.clear_container()
        MenuView(self.container, self.start_game, self.toggle_theme,
                 fg_color=theme.APP_BG).pack(fill="both", expand=True)

    def toggle_theme(self):
        """Swap the palette and rebuild the menu with the new colors."""
        name = "light" if theme.is_dark() else "dark"
        ctk.set_appearance_mode(name)
        theme.set_theme(name)
        self.configure(fg_color=theme.APP_BG)
        self.container.configure(fg_color=theme.APP_BG)
        self.show_menu()

    def start_game(self, mode):
        self.clear_container()
        GameView(self.container, mode, self.show_menu,
                 fg_color=theme.APP_BG).pack(fill="both", expand=True)


if __name__ == "__main__":
    app = RPSApp()
    app.mainloop()
