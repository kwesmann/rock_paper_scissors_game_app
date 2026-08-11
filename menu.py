"""Main menu - pick a game mode."""

import customtkinter as ctk

import theme
from helpers import F


class MenuView(ctk.CTkFrame):
    def __init__(self, master, on_start, on_toggle, **kw):
        super().__init__(master, **kw)
        self.on_start = on_start
        self.on_toggle = on_toggle

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        box = ctk.CTkFrame(
            self,
            fg_color=theme.PANEL,
            corner_radius=18,
            border_width=1,
            border_color=theme.BORDER,
        )
        box.grid(row=0, column=0, padx=20, pady=20)

        ctk.CTkLabel(
            box,
            text="Rock · Paper · Scissors",
            font=F(28, "bold"),
            text_color=theme.TEXT,
        ).grid(row=0, column=0, padx=60, pady=(34, 2))

        ctk.CTkLabel(
            box,
            text="Choose your battlefield.",
            font=F(15),
            text_color=theme.MUTED,
        ).grid(row=1, column=0, padx=20, pady=(2, 20))

        modes = [
            ("Single Player", "You vs a random computer opponent", 1),
            ("Two Players",   "Hotseat duel - two heads, one screen", 2),
            ("Three Players", "Three-way hotseat chaos", 3),
        ]
        for i, (txt, desc, m) in enumerate(modes):
            b = ctk.CTkButton(
                box,
                text=f"{txt}\n{desc}",
                height=64,
                corner_radius=12,
                font=F(15, "bold"),
                fg_color=theme.PANEL_TINT,
                hover_color=theme.SKY,
                text_color=theme.TEXT,
                border_width=1,
                border_color=theme.BORDER,
                command=lambda m=m: self.on_start(m),
            )
            b.grid(row=2 + i, column=0, sticky="ew", padx=46, pady=7)

        ctk.CTkLabel(
            box,
            text="First to 5 round-wins takes the match.",
            font=F(13),
            text_color=theme.MUTED,
        ).grid(row=6, column=0, pady=(16, 10))

        toggle = ctk.CTkButton(
            box,
            text="Switch to light mode" if theme.is_dark() else "Switch to dark mode",
            width=220,
            height=38,
            corner_radius=10,
            font=F(13),
            fg_color=theme.PANEL_TINT,
            hover_color=theme.SKY,
            text_color=theme.TEXT,
            border_width=1,
            border_color=theme.BORDER,
            command=self.on_toggle,
        )
        toggle.grid(row=7, column=0, pady=(0, 20))
