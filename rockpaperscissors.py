import random
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk


SPLASH_TIME = 2200

def center(win, w, h):
    win.update_idletasks()
    x = (win.winfo_screenwidth() - w) // 2
    y = (win.winfo_screenheight() - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


class RPS_game(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ROCK-PAPER-SCISSORS")
        center(self, 650, 500)
        #self.geometry("500x650")
        self.resizable(False, False)

        self.iconbitmap("rpslogo.ico")
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













def show_splash():
    splash = ctk.CTk()
    splash.overrideredirect(True)                    
    splash.configure(fg_color = "white")
    center(splash, 500, 380)

    image1 = Image.open('rpslogo.jpg')
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


