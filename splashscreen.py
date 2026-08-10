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

