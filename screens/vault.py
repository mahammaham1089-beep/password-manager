import tkinter as tk
from tkinter import messagebox
import pyperclip

from db.database import get_all_entries, delete_entry
from utils.encryption import decrypt_password
from screens.entry_form import EntryForm


class VaultScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#1a1a2e")
        self.master = master
        self.pack(fill="both", expand=True)

        self.data_map = {}

        self.build_ui()
        self.load_data()

    def build_ui(self):
        tk.Label(
            self,
            text="🔐 Your Vault",
            font=("Arial", 22, "bold"),
            bg="#1a1a2e",
            fg="white"
        ).pack(pady=10)

        # SEARCH BAR
        self.search_var = tk.StringVar()
        tk.Entry(
            self,
            textvariable=self.search_var,
            width=40
        ).pack(pady=5)

        self.search_var.trace("w", lambda *args: self.load_data())

        # BUTTONS
        tk.Button(
            self,
            text="➕ Add Entry",
            command=self.open_form
        ).pack(pady=3)

        tk.Button(
            self,
            text="🗑 Delete Selected",
            command=self.delete_entry
        ).pack(pady=3)

        tk.Button(
            self,
            text="📋 Copy Password",
            command=self.copy_password
        ).pack(pady=3)

        # LISTBOX
        self.listbox = tk.Listbox(self, width=70)
        self.listbox.pack(pady=15)

    def open_form(self):
        EntryForm(self.master, self.load_data)

    def load_data(self):
        self.listbox.delete(0, tk.END)
        self.data_map = {}

        query = self.search_var.get().lower()

        data = get_all_entries()

        if not data:
            self.listbox.insert(tk.END, "No entries yet")
            return

        for index, row in enumerate(data):
            _id, site, username, password, notes = row

            if query and query not in site.lower() and query not in username.lower():
                continue

            try:
                decrypted = decrypt_password(password)
            except:
                decrypted = password

            display = f"{site} | {username} | {decrypted}"

            self.listbox.insert(tk.END, display)
            self.data_map[index] = _id

    def delete_entry(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "Select an entry first")
            return

        index = selected[0]
        entry_id = self.data_map[index]

        confirm = messagebox.askyesno("Confirm", "Delete this entry?")

        if confirm:
            delete_entry(entry_id)
            self.load_data()

    def copy_password(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showerror("Error", "Select an entry first")
            return

        index = selected[0]
        entry_id = self.data_map[index]

        data = get_all_entries()

        for row in data:
            if row[0] == entry_id:
                decrypted = decrypt_password(row[3])
                pyperclip.copy(decrypted)
                messagebox.showinfo("Copied", "Password copied!")
                return