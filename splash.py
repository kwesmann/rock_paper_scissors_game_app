"""Splash screen shown before the main window appears."""

import os
import customtkinter as ctk
from PIL import Image

import theme
from helpers import F, BASE_DIR

SPLASH_TIME = 2200


class SplashScreen(ctk.CTkToplevel):
    """A simple, elegant splash shown before the main window appears."""

    def __init__(self, on_done):
        super().__init__()
        self.on_done = on_done
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=theme.APP_BG)

        logo = Image.open(os.path.join(BASE_DIR, "images", "rpslogo.jpg"))
        logo = ctk.CTkImage(light_image=logo, dark_image=logo, size=(150, 150))

        w, h = 500, 400
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        frame = ctk.CTkFrame(
            self,
            fg_color=theme.PANEL,
            corner_radius=24,
            border_width=1,
            border_color=theme.BORDER,
        )
        frame.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(
            frame,
            text="Rock · Paper · Scissors",
            font=F(30, "bold"),
            text_color=theme.TEXT,
        ).pack(pady=(46, 4))

        ctk.CTkLabel(frame, image=logo, text="").pack(pady=10)

        bar = ctk.CTkProgressBar(
            frame,
            mode="indeterminate",
            width=280,
            height=8,
            corner_radius=4,
            fg_color=theme.SKY,
            progress_color=theme.ACCENT,
        )
        bar.pack(pady=(0, 6))
        bar.start()

        ctk.CTkLabel(
            frame,
            text="Let's play!",
            font=F(13),
            text_color=theme.MUTED,
        ).pack(pady=(6, 0))

        self.after(SPLASH_TIME, self._close)

    def _close(self):
        self.destroy()
        self.on_done()
