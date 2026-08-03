import customtkinter as ctk

#creating a window
app = ctk.CTk()
app.title('ROCK-PAPER-SICISSORS')
app.geometry('500x650')
app.resizable(False,False)

app.iconbitmap('rpslogo.ico')

app.configure(fg_color = 'lightblue')









app.mainloop()