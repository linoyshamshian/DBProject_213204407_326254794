import customtkinter as ctk
from connectToPostgres import get_connection
from data import open_table_screen


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Security System ✈️")
root.geometry("600x400")
root.configure(fg_color="#eaf0ff")

conn = get_connection()

if not conn:
    error_label = ctk.CTkLabel(
        root,
        text="❌ Failed to connect to the database.\nPlease check your connection settings.",
        font=("Segoe UI", 14),
        text_color="#a94442",
        fg_color="#eaf0ff",
        justify="center"
    )
    error_label.pack(expand=True)
    root.mainloop()
    exit()

cursor = conn.cursor()

def show_message(name):
    popup = ctk.CTkToplevel()
    popup.title("Opening")
    popup.geometry("300x100")
    popup.configure(fg_color="#eaf0ff")
    ctk.CTkLabel(popup, text=f"Opening {name} screen...", font=("Segoe UI", 12), fg_color="#eaf0ff", text_color="#2a3f77").pack(pady=20)

title = ctk.CTkLabel(root, text="Security System ✈️", font=("Segoe UI", 24, "bold"), text_color="#2a3f77", fg_color="#eaf0ff")
title.pack(pady=30)

btn_frame = ctk.CTkFrame(root, fg_color="#eaf0ff")
btn_frame.pack()

buttons = [
    ("Assignment", lambda: open_table_screen(cursor,"Assigment",conn)),
    ("Area", lambda: open_table_screen(cursor,"Area",conn)),
    ("Shifts", lambda: open_table_screen(cursor,"Shifts",conn)),
    ("Person", lambda: open_table_screen(cursor,"Person",conn)),
    ("Queries & Procedures", lambda: show_message(cursor,"Queries & Procedures")),  # או מסך אחר
]


for i in range(4):
    row = i // 2
    col = i % 2
    btn = ctk.CTkButton(
        btn_frame,
        text=buttons[i][0],
        command=buttons[i][1],
        font=("Segoe UI", 14),
        fg_color="#c9d2ff",
        text_color="black",
        hover_color="#abbcff",
        corner_radius=15,
        width=200,
        height=50
    )
    btn.grid(row=row, column=col, padx=15, pady=10)

last_btn = ctk.CTkButton(
    root,
    text=buttons[4][0],
    command=buttons[4][1],
    font=("Segoe UI", 14),
    fg_color="#c9d2ff",
    text_color="black",
    hover_color="#abbcff",
    corner_radius=15,
    width=430,
    height=50
)
last_btn.pack(pady=10)

root.mainloop()