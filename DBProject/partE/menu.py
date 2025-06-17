#menu.py
import customtkinter as ctk
from connectToPostgres import get_connection
from data import open_table_screen
from queries_procedures_screen import open_queries_procedures_screen


def open_menu_window():
    # הגדרות כלליות למראה
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    # יצירת חלון ראשי של התוכנית
    root = ctk.CTk()
    root.title("Security System ✈️") # כותרת החלון
    root.geometry("600x400") # גודל החלון
    root.configure(fg_color="#eaf0ff") # צבע רקע

    # התחברות למסד הנתונים
    conn = get_connection()

    # טיפול במצב שבו אין חיבור למסד הנתונים
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
        root.mainloop() # הפעלת חלון שגיאה
        exit() # יציאה מהתוכנית

    # קבלת Cursor לביצוע שאילתות
    cursor = conn.cursor()

    # כותרת למסך הראשי
    title = ctk.CTkLabel(root, text="Security System ✈️", font=("Segoe UI", 24, "bold"), text_color="#2a3f77", fg_color="#eaf0ff")
    title.pack(pady=30)

    # מסגרת ללחצני הטבלאות
    btn_frame = ctk.CTkFrame(root, fg_color="#eaf0ff")
    btn_frame.pack()

    # רשימת כפתורים (טקסט, פעולה)
    buttons = [
        ("Assignment", lambda: open_table_screen(cursor,"Assigment","assigmentid")),
        ("Area", lambda: open_table_screen(cursor,"Area","areaid")),
        ("Shifts", lambda: open_table_screen(cursor,"Shifts","shiftid")),
        ("Person", lambda: open_table_screen(cursor,"Person","personid")),
        ("Queries & Procedures", lambda: open_queries_procedures_screen(cursor)),
    ]

    # יצירת 4 כפתורים ראשונים (טבלאות) בשתי עמודות
    for i in range(4):
        row = i // 2
        col = i % 2
        btn = ctk.CTkButton(
            btn_frame,
            text=buttons[i][0], # שם הכפתור
            command=buttons[i][1], # פעולה שתרוץ בלחיצה
            font=("Segoe UI", 14),
            fg_color="#c9d2ff",
            text_color="black",
            hover_color="#abbcff",
            corner_radius=15,
            width=200,
            height=50
        )
        btn.grid(row=row, column=col, padx=15, pady=10)


    # יצירת כפתור חמישי בגודל מלא מתחת לכפתורים
    last_btn = ctk.CTkButton(
        root,
        text=buttons[4][0],# "Queries & Procedures"
        command=buttons[4][1], # פעולה שפותחת את המסך המתאים
        font=("Segoe UI", 14),
        fg_color="#c9d2ff",
        text_color="black",
        hover_color="#abbcff",
        corner_radius=15,
        width=430,
        height=50
    )
    last_btn.pack(pady=10)

    # התחלת הלולאה הראשית של הממשק
    root.mainloop()

open_menu_window()