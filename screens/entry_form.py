import tkinter as tk
from tkinter import messagebox
from db.database import add_entry

class EntryForm(tk.Toplevel):
    def __init__(self, master, refresh_callback):
        super().__init__(master)

        self.refresh_callback = refresh_callback

        self.title("Add Entry")
        self.geometry("350x300")

        self.build_ui()

    def build_ui(self):
        tk.Label(self, text="Website").pack()
        self.site = tk.Entry(self)
        self.site.pack()

        tk.Label(self, text="Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Label(self, text="Notes").pack()
        self.notes = tk.Entry(self)
        self.notes.pack()

        tk.Button(
            self,
            text="Save",
            command=self.save_data
        ).pack(pady=10)

    def save_data(self):
        site = self.site.get()
        username = self.username.get()
        password = self.password.get()
        notes = self.notes.get()

        if not site or not username or not password:
            messagebox.showerror("Error", "All required fields")
            return

        add_entry(site, username, password, notes)

        messagebox.showinfo("Success", "Entry saved")

        self.refresh_callback()
        self.destroy()