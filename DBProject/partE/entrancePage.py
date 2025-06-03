import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "1234":
        messagebox.showinfo("Login Success", "Welcome to the system!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

root = ctk.CTk()
root.title("✈️ AirSystem Login")
root.geometry("400x350")

label_title = ctk.CTkLabel(root, text="✈️ Welcome to AirSystem", font=ctk.CTkFont(size=24, weight="bold"))
label_title.pack(pady=30)

entry_username = ctk.CTkEntry(root, placeholder_text="Username", width=280, height=40, corner_radius=15, border_color="#4a90e2")
entry_username.pack(pady=10)

entry_password = ctk.CTkEntry(root, placeholder_text="Password", show="*", width=280, height=40, corner_radius=15, border_color="#4a90e2")
entry_password.pack(pady=10)

btn_login = ctk.CTkButton(root, text="Login", width=280, height=40, corner_radius=15, command=login)
btn_login.pack(pady=30)

root.mainloop()
