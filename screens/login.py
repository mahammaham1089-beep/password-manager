import tkinter as tk
from tkinter import messagebox
from db.database import is_master_set, set_master_password, verify_master_password

class LoginScreen(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, bg="#1a1a2e")
        self.master = master
        self.on_success = on_success
        self.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text="Password Vault",
            font=("Arial", 24, "bold"),
            bg="#1a1a2e",
            fg="white"
        ).pack(pady=30)

        self.password_var = tk.StringVar()

        tk.Label(self, text="Enter Password", bg="#1a1a2e", fg="white").pack()

        self.entry = tk.Entry(
            self,
            textvariable=self.password_var,
            show="*",
            width=30
        )
        self.entry.pack(pady=10)

        tk.Button(
            self,
            text="Login",
            command=self.handle_login
        ).pack(pady=10)

    def handle_login(self):
        password = self.password_var.get()

        if not password:
            messagebox.showerror("Error", "Password required")
            return

        if not is_master_set():
            set_master_password(password)
            messagebox.showinfo("Success", "Master password created")
            self.on_success()

        else:
            if verify_master_password(password):
                messagebox.showinfo("Success", "Login successful")
                self.on_success()
            else:
                messagebox.showerror("Error", "Wrong password")