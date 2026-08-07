import os
import random
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw

# ----------------------------------------------------------------------------
# Theme - a light blue family
# ----------------------------------------------------------------------------
APP_BG     = "#eaf2fb"   # light blue page
PANEL      = "#ffffff"   # white cards
PANEL_TINT = "#e3eef9"   # very light blue
BORDER     = "#bcd6ee"   # soft blue border
TEXT       = "#123a5f"   # deep navy
MUTED      = "#5b7e9f"   # muted slate blue
ACCENT     = "#2f7fe0"   # vivid blue for primary buttons
ACCENT_DARK = "#1f5fb8"  # hover for accent
SKY        = "#bfe0ff"   # pale sky
WIN_COLOR  = "#0f9d6b"   # green for the match winner

# ----------------------------------------------------------------------------
# Game rules
# ----------------------------------------------------------------------------
SYMBOLS = ("rock", "paper", "scissors")
NAME = {"rock": "Rock", "paper": "Paper", "scissors": "Scissors"}
BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
WIN_SCORE = 5

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIC_DIR = os.path.join(BASE_DIR, "images")


def load_symbol_images(prefix, size):
    """Return {rock, paper, scissors} -> CTkImage for a prefix."""
    out = {}
    for sym in SYMBOLS:
        path = os.path.join(PIC_DIR, f"{prefix}-{sym}.png")
        if os.path.exists(path):
            im = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
        else:
            im = placeholder_image(sym, size)
        out[sym] = ctk.CTkImage(light_image=im, dark_image=im, size=size)
    return out


# ----------------------------------------------------------------------------
# Fonts
# ----------------------------------------------------------------------------
def F(size, weight="normal"):
    return ctk.CTkFont(family="Segoe UI", size=size, weight=weight)


# ----------------------------------------------------------------------------
# Splash screen
# ----------------------------------------------------------------------------
SPLASH_TIME = 2200


class SplashScreen(ctk.CTkToplevel):
    """A simple, elegant splash shown before the main window appears."""

    def __init__(self, on_done):
        super().__init__()
        self.on_done = on_done
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=APP_BG)

        image1 = Image.open(os.path.join(BASE_DIR, 'images', 'rpslogo.jpg'))
        image1 = image1.resize((150, 150),)
        image1 = ImageTk.PhotoImage(image1)

        w, h = 500, 400
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        frame = ctk.CTkFrame(
            self, 
            fg_color=PANEL, 
            corner_radius=24, 
            border_width=1, 
            border_color=BORDER
        )
        frame.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(
            frame, 
            text="Rock · Paper · Scissors", 
            font=F(30, "bold"), 
            text_color=TEXT
        ).pack(pady=(46, 4))

        ctk.CTkLabel(
            frame, 
            image=image1 
        ).pack(pady=10)
        '''
        ctk.CTkLabel(
            frame, 
            text="✊  ✋  ✌", 
            font=F(40), 
            text_color=ACCENT
        ).pack(pady=(0, 24))
        '''
        bar = ctk.CTkProgressBar(
            frame, 
            mode="indeterminate", 
            width=280, 
            height=8, 
            corner_radius=4, 
            fg_color=SKY, 
            progress_color=ACCENT
        )
        bar.pack(pady=(0, 6))
        bar.start()

        ctk.CTkLabel(
            frame, 
            text="Let's play!", 
            font=F(13), 
            text_color=MUTED
        ).pack(pady=(6, 0))

        self.after(SPLASH_TIME, self._close)

    def _close(self):
        self.destroy()
        self.on_done()


# ----------------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------------
class MenuView(ctk.CTkFrame):
    def __init__(self, master, on_start, **kw):
        super().__init__(master, **kw)
        self.on_start = on_start

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        box = ctk.CTkFrame(
            self, 
            fg_color=PANEL, 
            corner_radius=18,
            border_width=1, 
            border_color=BORDER
        )
        box.grid(row=0, column=0, padx=20, pady=20)

        ctk.CTkLabel(
            box, 
            text="Rock · Paper · Scissors", 
            font=F(28, "bold"), 
            text_color=TEXT
        ).grid( row=0, column=0, padx=60, pady=(34, 2))

        ctk.CTkLabel(
            box, 
            text="Choose your battlefield.", 
            font=F(15), 
            text_color=MUTED
        ).grid( row=1, column=0, padx=20, pady=(2, 20))

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
                fg_color=PANEL_TINT,
                hover_color=SKY, 
                text_color=TEXT,
                border_width=1, 
                border_color=BORDER,
                command=lambda m=m: self.on_start(m)
            )
            b.grid(row=2 + i, column=0, sticky="ew", padx=46, pady=7)

        ctk.CTkLabel(
            box, 
            text="First to 5 round-wins takes the match.",
            font=F(13), 
            text_color=MUTED
        ).grid(row=6, column=0, pady=(16, 28))


# ----------------------------------------------------------------------------
# Game
# ----------------------------------------------------------------------------
class GameView(ctk.CTkFrame):
    """Complete game board, reused for all three modes."""

    def __init__(self, master, mode, on_menu, **kw):
        super().__init__(master, **kw)
        self.mode = mode
        self.on_menu = on_menu

        if mode == 1:
            self.display_names = ["You", "CPU"]
            self.prefixes = ["p", "c"]
        elif mode == 2:
            self.display_names = ["Player 1", "Player 2"]
            self.prefixes = ["p", "p"]
        else:
            self.display_names = ["Player 1", "Player 2", "Player 3"]
            self.prefixes = ["p", "p", "p"]

        self.n = len(self.display_names)
        self.round = 0
        self.phase = "picking"            # picking | shuffling | revealed
        self.choices = [None] * self.n
        self.scores = [0] * self.n
        self._rot_id = None
        self._frames = 0

        self.arena_imgs = [load_symbol_images(p, (150, 150)) for p in self.prefixes]
        self.slot_imgs = [load_symbol_images(p, (52, 52)) for p in self.prefixes]

        # widgets created by _build
        self.round_lbl = None
        self.banner = None
        self.prompt = None
        self.arena = []          # per player: (image label, text label)
        self.score_chips = []    # per player: (slot label, score label)
        self.move_buttons = []
        self.go_btn = None
        self.next_btn = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build()
        self.new_match()

    # ------------------------------------------------------------------ UI
    def _build(self):
        # --- header ---
        header = ctk.CTkFrame(
            self, 
            fg_color=PANEL, 
            corner_radius=14,
            border_width=1, 
            border_color=BORDER
        )
        header.pack(fill="x", padx=16, pady=(14, 8))
        header.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            header, 
            text="< Menu", 
            width=96, 
            height=38,
            corner_radius=10, 
            font=F(14, "bold"),
            fg_color=PANEL_TINT, 
            hover_color=SKY,
            text_color=TEXT, 
            command=self.go_menu
        ).grid(row=0, column=0, padx=12, pady=10)

        ctk.CTkLabel(
            header, 
            text="Rock · Paper · Scissors", 
            font=F(17, "bold"), 
            text_color=TEXT
        ).grid(row=0, column=1)

        self.round_lbl = ctk.CTkLabel(
            header, 
            text="", 
            font=F(15, "bold"),
            text_color=ACCENT
        )
        self.round_lbl.grid(row=0, column=2, padx=12)

        # --- scoreboard ---
        board = ctk.CTkFrame(self, fg_color="transparent")
        board.pack(fill="x", padx=16, pady=(0, 8))
        for i in range(self.n):
            board.grid_columnconfigure(i, weight=1)

        for i in range(self.n):
            chip = ctk.CTkFrame(
                board, 
                fg_color=PANEL, 
                corner_radius=12,
                border_width=1, 
                border_color=BORDER
            )
            chip.grid(row=0, column=i, padx=6, sticky="nsew")
            ctk.CTkLabel(
                chip, 
                text=self.display_names[i].upper(),
                font=F(12, "bold"), 
                text_color=MUTED
            ).pack(pady=(10, 0))
            slot = ctk.CTkLabel(chip, text="?", font=F(16, "bold"), text_color=MUTED)
            slot.pack(pady=(2, 0))
            sc = ctk.CTkLabel(chip, text="0", font=F(30, "bold"), text_color=TEXT)
            sc.pack(pady=(0, 8))
            self.score_chips.append((slot, sc))

        # --- middle: prompt + arena + banner ---
        middle = ctk.CTkFrame(self, fg_color="transparent")
        middle.pack(fill="both", expand=True, padx=16, pady=(0, 6))

        self.prompt = ctk.CTkLabel(middle, text="", font=F(19, "bold"), text_color=TEXT)
        self.prompt.pack(pady=(12, 6))

        arena = ctk.CTkFrame(
            middle, 
            fg_color=PANEL, 
            corner_radius=20, 
            border_width=2, 
            border_color=BORDER
        )
        arena.pack(expand=True, fill="both", padx=12, pady=6)
        for i in range(self.n):
            arena.grid_columnconfigure(i, weight=1)

        for i in range(self.n):
            panel = ctk.CTkFrame(
                arena, 
                fg_color=PANEL_TINT, 
                corner_radius=14, 
                border_width=1, 
                border_color=BORDER
            )
            panel.grid(row=0, column=i, sticky="nsew", padx=10, pady=14)
            img = ctk.CTkLabel(panel, text="?", font=F(60), text_color=SKY)
            img.pack(expand=True, pady=(18, 0))
            txt = ctk.CTkLabel(panel, text="", font=F(13), text_color=MUTED)
            txt.pack(pady=(0, 16))
            self.arena.append((img, txt))

        self.banner = ctk.CTkLabel(
            middle, 
            text="", 
            font=F(22, "bold"), 
            text_color=ACCENT, 
            wraplength=780
        )
        self.banner.pack(pady=(4, 8))

        # --- move buttons ---
        moves = ctk.CTkFrame(self, fg_color="transparent")
        moves.pack(fill="x", padx=16, pady=(0, 10))
        for i in range(3):
            moves.grid_columnconfigure(i, weight=1)

        for j, s in enumerate(SYMBOLS):
            b = ctk.CTkButton(
                moves, 
                text=NAME[s], 
                height=54, 
                corner_radius=12, 
                font=F(16, "bold"), 
                fg_color=PANEL_TINT, 
                hover_color=SKY, 
                text_color=TEXT, 
                border_width=2, 
                border_color=ACCENT, 
                command=lambda s=s: self.on_pick(s)
            )
            b.grid(row=0, column=j, sticky="ew", padx=8, pady=6)
            self.move_buttons.append(b)

        ctrl = ctk.CTkFrame(moves, fg_color="transparent")
        ctrl.grid(row=1, column=0, columnspan=3, sticky="ew", padx=8, pady=(4, 0))
        ctrl.grid_columnconfigure(0, weight=1)
        ctrl.grid_columnconfigure(1, weight=1)

        self.go_btn = ctk.CTkButton(
            ctrl, 
            text="Go!", 
            height=48, 
            corner_radius=12, 
            font=F(17, "bold"),
            fg_color=ACCENT, 
            hover_color=ACCENT_DARK, 
            text_color="#ffffff",
            command=self.go_click
        )
        self.go_btn.grid(row=0, column=0, sticky="ew", padx=(0, 4))

        self.next_btn = ctk.CTkButton(
            ctrl, text="Next Round", 
            height=48, 
            corner_radius=12,
            font=F(17, "bold"), 
            fg_color=PANEL_TINT, 
            hover_color=SKY,
            text_color=TEXT, 
            command=self.advance
        )
        self.next_btn.grid(row=0, column=1, sticky="ew", padx=(4, 0))
        self.next_btn.configure(state="disabled")

    # ------------------------------------------------------------------ flow
    def new_match(self):
        self.cancel_rotation()
        for i in range(self.n):
            self.scores[i] = 0
            self.score_chips[i][1].configure(text="0")
        self.round = 0
        self.start_round()

    def start_round(self):
        self.cancel_rotation()
        self.round += 1
        self.phase = "picking"
        self.choices = [None] * self.n

        self.round_lbl.configure(text=f"Round {self.round}")
        self.banner.configure(text="")
        self.go_btn.configure(state="disabled", text="Go!", fg_color=ACCENT, hover_color=ACCENT_DARK)

        for i, (img, txt) in enumerate(self.arena):
            img.configure(image="", text="?")
            txt.configure(text=self.display_names[i])
            self.score_chips[i][0].configure(image="", text="?")

        self._set_moves("normal")
        self.prompt.configure(text=self._turn_text(0))

    def _set_moves(self, state):
        for b in self.move_buttons:
            b.configure(state=state)

    def _turn_text(self, i):
        if self.mode == 1:
            return "Pick your move - the CPU is watching…"
        name = self.display_names[i]
        if self.n == 3:
            return f"{name}, pick a move… (keep it secret!)"
        return f"{name}, pick a move… (no peeking!)"

    def on_pick(self, choice):
        if self.phase != "picking":
            return
        i = self.choices.index(None)
        self.choices[i] = choice

        # keep the pick hidden - just mark the slot as locked
        self.score_chips[i][0].configure(image="", text="✓", text_color=WIN_COLOR)

        if self.mode == 1 and i == 0:
            # CPU gets a random pick, only revealed after the shuffle
            self.choices[1] = random.choice(SYMBOLS)
            self._set_moves("disabled")
            self.prompt.configure(text="Your move is locked. Hit Go to face the CPU!")
            self.go_btn.configure(state="normal")
            return

        remaining = [j for j in range(self.n) if self.choices[j] is None]
        if not remaining:
            self._set_moves("disabled")
            if self.mode == 1:
                self.prompt.configure(text="Your move is locked. Hit Go!")
            else:
                self.prompt.configure(text=f"{self.display_names[-1]} picked. Hit Go to reveal!")
            self.go_btn.configure(state="normal")
        else:
            self.prompt.configure(text=self._turn_text(remaining[0]))

    def go_click(self):
        if self.phase != "picking":
            return
        self.phase = "shuffling"
        self._set_moves("disabled")
        self.go_btn.configure(state="disabled")
        self.next_btn.configure(state="disabled")
        self.prompt.configure(text="Shuffling…")

        if self.mode == 1:
            self.choices[1] = random.choice(SYMBOLS)

        self._frames = 0
        self._rot_id = self.after(0, self._shuffle)

    def _shuffle(self):
        # briefly flick every panel between all symbols, then stop and reveal
        self._frames += 1
        for i in range(self.n):
            pic = random.choice(SYMBOLS)
            self.arena[i][0].configure(image=self.arena_imgs[i][pic], text="")
        if self._frames < 14:
            self._rot_id = self.after(70, self._shuffle)
        else:
            self._rot_id = None
            self.reveal()

    def reveal(self):
        self.phase = "revealed"
        winners = self._round_winners(self.choices)

        for i, (img, txt) in enumerate(self.arena):
            c = self.choices[i]
            img.configure(image=self.arena_imgs[i][c], text="")
            txt.configure(text=f"{self.display_names[i]}: {NAME[c]}")
            self.score_chips[i][0].configure(image=self.slot_imgs[i][c], text="")

        if not winners:
            self.banner.configure(text="Tie round!", text_color=MUTED)
        else:
            for i in winners:
                self.scores[i] += 1
                self.score_chips[i][1].configure(text=str(self.scores[i]))
            names = " & ".join(self.display_names[i] for i in winners)
            verb = "wins" if len(winners) == 1 else "win"
            self.banner.configure(text=f"{names} {verb} the round!", text_color=ACCENT)

        # match winner?
        champions = [i for i in range(self.n) if self.scores[i] >= WIN_SCORE]
        if champions:
            c = champions[0]
            self.banner.configure(
                text=f"{self.display_names[c]} wins the match!",
                text_color=WIN_COLOR)
            self.next_btn.configure(state="normal", text="New Match")
        else:
            self.next_btn.configure(state="normal", text="Next Round")

    def advance(self):
        if self.phase != "revealed":
            return
        if self.banner.cget("text").endswith("the match!"):
            self.new_match()
        else:
            self.start_round()

    @staticmethod
    def _round_winners(choices):
        """Indices that win this round. Empty list means a tie."""
        groups = {}
        for i, c in enumerate(choices):
            groups.setdefault(c, []).append(i)
        kinds = list(groups.keys())
        if len(kinds) == 1 or len(kinds) >= 3:
            return []
        # exactly two distinct symbols -> the one that beats the other
        if BEATS[kinds[0]] == kinds[1]:
            return groups[kinds[0]]
        return groups[kinds[1]]

    # ------------------------------------------------------------------ utils
    def cancel_rotation(self):
        if self._rot_id is not None:
            self.after_cancel(self._rot_id)
            self._rot_id = None

    def go_menu(self):
        self.cancel_rotation()
        self.on_menu()


# ----------------------------------------------------------------------------
# App
# ----------------------------------------------------------------------------
class RPSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Rock · Paper · Scissors")
        self.geometry("960x720")
        self.resizable(False, False)
        self.configure(fg_color=APP_BG)

        try:
            self.iconbitmap(os.path.join(BASE_DIR, 'images', 'rpslogo.ico'))
        except Exception:
            pass

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)



        self.container = ctk.CTkFrame(self, fg_color=APP_BG, corner_radius=0)
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
        MenuView(self.container, self.start_game, fg_color=APP_BG).pack(fill="both", expand=True)

    def start_game(self, mode):
        self.clear_container()
        GameView(
            self.container, 
            mode, 
            self.show_menu, 
            fg_color=APP_BG
        ).pack(fill="both", expand=True)


if __name__ == "__main__":
    app = RPSApp()
    app.mainloop()
