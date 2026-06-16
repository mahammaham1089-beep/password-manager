import tkinter as tk
from db.database import initialize_db
from screens.login import LoginScreen
from screens.vault import VaultScreen

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager")
        self.geometry("500x400")

        initialize_db()

        self.show_login()

    def show_login(self):
        LoginScreen(self, self.show_vault)

    def show_vault(self):
        for widget in self.winfo_children():
            widget.destroy()

        VaultScreen(self)

if __name__ == "__main__":
    App().mainloop()