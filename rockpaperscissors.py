import random
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk


SPLASH_TIME = 2200

APP_BG = "lightblue"
PANEL = "white"
PANEL_LIGHT = "grey"
BORDER = "blue"
TEXT = "black"
MUTED = "cream" 
ACCENT = "#6d5cff"

SYMBOLS = ("rock", "paper", "scissors")
EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
NAME = {"rock": "Rock", "paper": "Paper", "scissors": "Scissors"}
COLOR = {"rock": "#9aa7bd", "paper": "#43c6f2", "scissors": "#f2647a"}
BEATS = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
BEATEN_BY = {v: k for k, v in BEATS.items()}
WIN_SCORE = 5

def center(win, w, h):
    win.update_idletasks()
    x = (win.winfo_screenwidth() - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

def round_winners(choices):
    """Return the list of player indices that won the round.

    All same        -> [] (tie)
    All different   -> [] (cycle, tie)
    Two of a kind   -> whoever's symbol beats the duplicated one
    """
    groups = {}
    for i, c in enumerate(choices):
        groups.setdefault(c, []).append(i)
    if len(groups) == 1:
        return []
    kinds = list(groups)
    if len(kinds) >= 3:
        return []  # full cycle of distinct symbols -> tie
    # exactly two kinds present: one symbol beats the other
    if BEATS[kinds[0]] == kinds[1]:
        return groups[kinds[0]]
    return groups[kinds[1]]

def cpu_pick(player_choice):
    """Beat the human's last move 40% of the time, otherwise play random."""
    if player_choice is None:
        return random.choice(SYMBOLS)
    if random.random() < 0.40:
        return BEATEN_BY[player_choice]
    return random.choice(SYMBOLS)


# ----------------------------------------------------------------------------
# Fonts
# ----------------------------------------------------------------------------
def F(size, weight="normal", family="Segoe UI"):
    return ctk.CTkFont(family=family, size=size, weight=weight)


def EMO(size):
    return ctk.CTkFont(family="Segoe UI Emoji", size=size)


class MenuView(ctk.CTkFrame):
    def __init__(self, master, on_start, **kw):
        super().__init__(master, **kw)
        self.on_start = on_start

        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        box = ctk.CTkFrame(
            self, 
            fg_color = PANEL, 
            corner_radius = 18,
            border_width = 1, 
            border_color = BORDER
        )
        box.grid(row=0, column=0)

        title = ctk.CTkLabel(
            box, 
            text="ROCK · PAPER · SCISSORS",
            font=F(30, "bold"), 
            text_color=TEXT
        )
        title.grid(row=0, column=0, padx=70, pady=(38, 2))

        hands = ctk.CTkLabel(
            box, 
            text="🪨   📄   ✂️", 
            font=EMO(54)
        )
        hands.grid(row=1, column=0, pady=4)

        sub = ctk.CTkLabel(
            box, 
            text="Pick your battlefield.",
            font=F(15), 
            text_color = MUTED
        )
        sub.grid(row=2, column=0, pady=(0, 22))

        modes = [
            ("Solo vs CPU", "Face off against a clever opponent", 1),
            ("Two Players", "Hotseat duel — first to 5 wins", 2),
            ("Three Players", "Three-way chaos on one screen", 3),
        ]
        for i, (title_txt, desc, m) in enumerate(modes):
            b = ctk.CTkButton(
                box, 
                text = f"{title_txt}\n{desc}", 
                height = 66, 
                corner_radius = 12,
                font = F(16, "bold"), 
                fg_color = PANEL_LIGHT,
                hover_color ="#232c3d", 
                text_color = TEXT,
                border_width=1, 
                border_color = BORDER,
                command=lambda m=m: self.on_start(m)
            )
            b.grid(row=3 + i, column=0, sticky="ew", padx=50, pady=8)

        hint = ctk.CTkLabel(
            box, 
            text="First to 5 points wins the match.",
            font=F(12), 
            text_color = MUTED
        )
        hint.grid(row=6, column=0, pady=(14, 26))



class GameView(ctk.CTkFrame):
    def __init__(self, master, mode, on_menu, **kw):
        super().__init__(master, **kw)
        self.mode = mode
        self.on_menu = on_menu

        if mode == 1:
            names = ["You", "CPU"]
            self.is_cpu = [False, True]
        elif mode == 2:
            names = ["Player 1", "Player 2"]
            self.is_cpu = [False, False]
        else:
            names = ["Player 1", "Player 2", "Player 3"]
            self.is_cpu = [False, False, False]

        self.n = len(names)
        self.players = [{"name": n, "score": 0, "badge": None, "score_lbl": None}    for n in names]
        self.round = 0
        self.phase = "idle"          # idle | picking | rotating | revealed
        self.choices = [None] * self.n
        self.pick_index = 0
        self.match_over = False
        self._rot_id = None
        self._frames = 0

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

        back = ctk.CTkButton(
            header, 
            text="← Menu", 
            width=110, 
            height=40,
            corner_radius=10, 
            font=F(14, "bold"),
            fg_color=PANEL_LIGHT, 
            hover_color="#232c3d",
            text_color=TEXT, 
            command=self.go_menu)
        back.grid(row=0, column=0, padx=12, pady=10)

        title = ctk.CTkLabel(
            header, 
            text="ROCK · PAPER · SCISSORS",
            font=F(17, "bold"), 
            text_color=TEXT
        )
        title.grid(row=0, column=1)

        self.round_lbl = ctk.CTkLabel(
            header, 
            text="", 
            font=F(15, "bold"),  
            text_color=ACCENT
        )
        self.round_lbl.grid(row=0, column=2, padx=12, pady=10)

        # --- scoreboard ---
        board = ctk.CTkFrame(self, fg_color="transparent")
        board.pack(fill="x", padx=16, pady=(0, 8))
        for i in range(self.n):
            board.grid_columnconfigure(i, weight=1)

        for i, pl in enumerate(self.players):
            chip = ctk.CTkFrame(
                board, 
                fg_color=PANEL, 
                corner_radius=12,
                border_width=1, 
                border_color=BORDER
            )
            chip.grid(row=0, column=i, padx=6, sticky="nsew")

            name_lbl = ctk.CTkLabel(
                chip, 
                text=pl["name"].upper(),
                font=F(12, "bold"), 
                text_color=MUTED
            )
            name_lbl.pack(pady=(10, 0))

            badge = ctk.CTkLabel(chip, text="✊", font=EMO(30), text_color=MUTED)
            badge.pack()

            score_lbl = ctk.CTkLabel(
                chip, 
                text="0", 
                font=F(34, "bold"), 
                text_color=TEXT
            )
            score_lbl.pack(pady=(0, 8))

            pl["badge"] = badge
            pl["score_lbl"] = score_lbl

        # --- middle: prompt + stage + banner ---
        middle = ctk.CTkFrame(self, fg_color="transparent")
        middle.pack(fill="both", expand=True, padx=16, pady=(0, 6))

        self.prompt = ctk.CTkLabel(
            middle, 
            text="", 
            font=F(19, "bold"),
            text_color=TEXT
        )
        self.prompt.pack(pady=(12, 6))

        stage = ctk.CTkFrame(
            middle, 
            fg_color=PANEL, 
            corner_radius=22, 
            border_width=2, 
            border_color=BORDER
        )
        stage.pack(expand=True, fill="both", padx=12, pady=6)

        self.big_label = ctk.CTkLabel(
            stage, 
            text="✊", 
            font=EMO(120),
            text_color=TEXT
        )
        self.big_label.pack(expand=True)

        self.banner = ctk.CTkLabel(
            middle, 
            text="", 
            font=F(22, "bold"),
            text_color=ACCENT, 
            wraplength=760
        )
        self.banner.pack(pady=(4, 10))

        # --- move buttons ---
        moves = ctk.CTkFrame(self, fg_color="transparent")
        moves.pack(fill="x", padx=16, pady=(0, 10))
        for i in range(3):
            moves.grid_columnconfigure(i, weight=1)

        self.move_buttons = []
        for j, s in enumerate(SYMBOLS):
            card = ctk.CTkFrame(
                moves, 
                fg_color=PANEL, 
                corner_radius=14,
                border_width=1, 
                border_color = BORDER
            )
            card.grid(row=0, column=j, padx=8, pady=6, sticky="nsew")

            icon = ctk.CTkLabel(card, text=EMOJI[s], font=EMO(46))
            icon.pack(pady=(10, 2))

            btn = ctk.CTkButton(
                card, 
                text=NAME[s], 
                height=46, 
                corner_radius=10,
                font=F(15, "bold"), 
                fg_color=PANEL_LIGHT,
                hover_color="#232c3d", 
                text_color=TEXT,border_width=2, 
                border_color=COLOR[s],
                command=lambda s=s: self.on_pick(s)
            )
            btn.pack(fill="x", padx=10, pady=(4, 12))
            self.move_buttons.append(btn)

        self.next_btn = ctk.CTkButton(
            moves, text="Next Round ▶", height=46, corner_radius=12,
            font=F(16, "bold"), fg_color=ACCENT, hover_color="#5b4ce0",
            text_color="#ffffff", command=self.advance)
        self.next_btn.grid(row=1, column=0, columnspan=3, sticky="ew",
                           padx=8, pady=(6, 4))
        self.next_btn.configure(state="disabled")

    # ------------------------------------------------------------ helpers
    def set_buttons(self, state):
        for b in self.move_buttons:
            b.configure(state=state)

    def cancel_rotation(self):
        if self._rot_id is not None:
            self.after_cancel(self._rot_id)
            self._rot_id = None

    def go_menu(self):
        self.cancel_rotation()
        self.on_menu()

    def turn_text(self, i):
        if self.mode == 1:
            return "You vs CPU — choose your move!"
        name = self.players[i]["name"]
        if self.n == 3:
            return f"{name}, choose your move… (don't let the others peek!)"
        return f"{name}, choose your move… (no peeking!)"

    # ------------------------------------------------------------ flow
    def new_match(self):
        self.cancel_rotation()
        self.match_over = False
        for pl in self.players:
            pl["score"] = 0
            pl["score_lbl"].configure(text="0")
        self.round = 0
        self.start_round()

    def start_round(self):
        self.cancel_rotation()
        self.round += 1
        self.phase = "picking"
        self.choices = [None] * self.n
        self.pick_index = 0

        self.round_lbl.configure(text=f"Round {self.round}")
        self.banner.configure(text="")
        self.big_label.configure(text="✊", text_color=TEXT)
        for pl in self.players:
            pl["badge"].configure(text="?", text_color=MUTED)

        self.set_buttons("normal")
        self.next_btn.configure(state="disabled", text="Next Round ▶")
        self.prompt.configure(text=self.turn_text(0))

    def on_pick(self, choice):
        if self.phase != "picking":
            return
        i = self.pick_index
        self.choices[i] = choice

        # vs CPU: human picks first, CPU answers instantly
        if i == 0 and self.is_cpu[1]:
            self.choices[1] = cpu_pick(choice)
            self.pick_index = self.n
            self.set_buttons("disabled")
            self.prompt.configure(text="CPU is thinking…")
            self._rot_id = self.after(350, self.start_rotation)
            return

        self.pick_index += 1
        if self.pick_index >= self.n:
            self.set_buttons("disabled")
            self.start_rotation()
        else:
            self.prompt.configure(text=self.turn_text(self.pick_index))

    def start_rotation(self):
        self.cancel_rotation()
        self.phase = "rotating"
        self.next_btn.configure(state="disabled")
        self._frames = 0
        self._rot_id = self.after(0, self.rotate)

    def rotate(self):
        s = random.choice(SYMBOLS)
        self.big_label.configure(text=EMOJI[s], text_color=COLOR[s])
        self._frames += 1
        if self._frames < 14:
            self._rot_id = self.after(80, self.rotate)
        else:
            self._rot_id = None
            self.reveal()

    def reveal(self):
        self.phase = "revealed"
        for i, pl in enumerate(self.players):
            c = self.choices[i]
            pl["badge"].configure(text=EMOJI[c], text_color=COLOR[c])
        self.big_label.configure(
            text=EMOJI[self.choices[0]],
            text_color=COLOR[self.choices[0]]
        )

        winners = round_winners(self.choices)
        if not winners:
            msg, col = "Tie round!", MUTED
        else:
            names = " & ".join(self.players[i]["name"] for i in winners)
            msg = f"{names} wins the round!" if len(winners) == 1 else f"{names} win the round!"
            col = ACCENT
            for i in winners:
                self.players[i]["score"] += 1
                self.players[i]["score_lbl"].configure(
                    text = str(self.players[i]["score"])
                )

        champ = next(
            (i for i in winners if self.players[i]["score"] >= WIN_SCORE), 
            None
        )
        self.match_over = champ is not None

        if champ is not None:
            self.banner.configure(
                text=f"🏆  {self.players[champ]['name']} wins the match!  🏆",
                text_color=GOLD
            )
            self.next_btn.configure(state="normal", text="New Match")
        else:
            self.banner.configure(text=msg, text_color=col)
            self.next_btn.configure(state="normal", text="Next Round ▶")

    def advance(self):
        if self.phase != "revealed":
            return
        if self.match_over:
            self.new_match()
        else:
            self.start_round()



class RPS_game(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ROCK-PAPER-SCISSORS")
        center(self, 650, 500)
        #self.geometry("500x650")
        self.resizable(False, False)

        self.iconbitmap("images/rpslogo.ico")
        self.configure(fg_color = "lightblue")

        self.build_ui()

    def build_ui(self):
        header = ctk.CTkFrame(self, corner_radius = 0, fg_color = "blue")
        header.pack(fill = "x") 

        ctk.CTkLabel(
            header,
            text = "LET'S ROCK PAPER SCISSORS ;)"
            #font = ()
        ).pack(expand = True)


    def show_menu(self):
        self.clear_container()
        MenuView(
            self.container, 
            self.start_game,
            fg_color = APP_BG
        ).pack(fill="both", expand=True)

    def start_game(self, mode):
        self.clear_container()
        GameView(
            self.container, 
            mode, 
            self.show_menu,
            fg_color = APP_BG
        ).pack(fill="both", expand=True)














def show_splash():
    splash = ctk.CTk()
    splash.overrideredirect(True)                    
    splash.configure(fg_color = "white")
    center(splash, 500, 380)

    image1 = Image.open('images/rpslogo.jpg')
    image1 = image1.resize((200, 200),)
    image1=ImageTk.PhotoImage(image1)

    image_label = ctk.CTkLabel(
        splash,
        text='',
        image=image1
    )
    image_label.pack(pady=10)


    ctk.CTkLabel(
        splash, 
        text="ROCK-PAPER-SCISSORS", 
        font=("Segoe UI", 34, "bold"), 
        text_color = "lightblue"
    ).pack(expand=True)
    bar = ctk.CTkProgressBar(
        splash, 
        mode="indeterminate", 
        width=260, 
        height=8, 
        corner_radius=4
    )
    bar.pack(pady=24)
    bar.start()                                      

    splash.after(SPLASH_TIME, close_splash, splash)
    splash.mainloop()

def close_splash(splash):
    splash.destroy()          
    app = RPS_game()
    app.mainloop()            


show_splash()


