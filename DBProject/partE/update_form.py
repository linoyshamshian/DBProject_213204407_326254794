import customtkinter as ctk
from tkinter import messagebox

def open_update_form(cursor, table_name, column_names, row_data, refresh_callback, primary_key_column):
    update_win = ctk.CTkToplevel() # יצירת חלון Toplevel חדש לעדכון
    update_win.title(f"Update {table_name}")
    update_win.geometry("500x700")
    update_win.configure(fg_color="#eaf0ff")
    update_win.grab_set()

    # מילון לאחסון ווידג'טים של שדות קלט (CTkEntry) לפי שם עמודה
    entry_widgets = {}

    # קבוצה לאחסון שמות עמודות שהן ריקות במקור ולכן מושבתות לעריכה
    disabled_fields = set()

    form_frame = ctk.CTkFrame(update_win, fg_color="#f0f4ff") # יצירת פריים (מסגרת) לשדות הטופס
    form_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # מציאת האינדקס של עמודת המפתח הראשי
    pk_index = column_names.index(primary_key_column)

    # קבלת הערך של המפתח הראשי מהנתונים הנוכחיים
    pk_val = row_data[pk_index]

    # לולאה על כל עמודה וערכה ברשומה
    for i, (col, val) in enumerate(zip(column_names, row_data)):
        # יצירת לייבל לשם העמודה
        lbl = ctk.CTkLabel(form_frame, text=col.replace("_", " ").title(), font=("Segoe UI", 13))
        lbl.grid(row=i, column=0, sticky="w", padx=10, pady=8)
        # אם העמודה היא המפתח הראשי
        if col == primary_key_column:
            pk_frame = ctk.CTkFrame(form_frame, fg_color="#e0e0e0", corner_radius=8) # יצירת פריים מיוחד למפתח ראשי
            pk_frame.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
            pk_label = ctk.CTkLabel(pk_frame, text=str(val), font=("Segoe UI", 12, "bold"), text_color="#888")
            pk_label.pack(side="left", padx=8, pady=4)
            pk_note = ctk.CTkLabel(pk_frame, text="(Primary key - cannot change)", font=("Segoe UI", 10),
                                   text_color="#b22") # הערה שהמפתח הראשי לא ניתן לשינוי
            pk_note.pack(side="left", padx=8)
            entry_widgets[col] = None
        # עבור עמודות שאינן מפתח ראשי
        else:
            if val is None or str(val).strip() == "":
                # שדה ריק – לא ניתן לעריכה
                entry = ctk.CTkEntry(form_frame, font=("Segoe UI", 12), state="disabled")
                entry.insert(0, "")
                entry.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
                form_frame.grid_columnconfigure(1, weight=1)
                entry_widgets[col] = entry
                disabled_fields.add(col) # הוספת העמודה לרשימת השדות המושבתים
                # הערה לשדה
                note = ctk.CTkLabel(form_frame, text="(Field is empty - cannot add value)", font=("Segoe UI", 10), text_color="#b22")
                note.grid(row=i, column=2, sticky="w", padx=4)
            # אם לשדה יש ערך קיים
            else:
                entry = ctk.CTkEntry(form_frame, font=("Segoe UI", 12))
                entry.insert(0, str(val))
                entry.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
                form_frame.grid_columnconfigure(1, weight=1)
                entry_widgets[col] = entry

    def update_record():
     #פונקציה המטפלת בלוגיקת עדכון הרשומה בבסיס הנתונים
        try:
            update_cols = [] # רשימה לאחסון מחרוזות העדכון עבור שאילתת ה-SQL
            update_vals = [] # רשימה לאחסון הערכים שיש לעדכן
            for col in column_names:
                if col == primary_key_column:
                    continue # מדלג על המפתח הראשי (לא מעדכנים אותו)
                if col in disabled_fields:
                    continue  # שדה ריק במקור – לא שולחים אותו בכלל
                user_val = entry_widgets[col].get()
                if user_val.strip() == "":
                    # אם השדה היה עם ערך קודם, ועכשיו המשתמש ניסה לרוקן אותו – זו שגיאה
                    messagebox.showerror("Error", f"The field '{col}' is required and cannot be empty!")
                    return
                update_cols.append(f"{col} = %s") # הוספת חלק העדכון לשאילתה
                update_vals.append(user_val) # הוספת הערך לרשימת הערכים
            if not update_cols:
                messagebox.showinfo("Nothing to update", "No fields to update.")
                return
            update_vals.append(pk_val) # הוספת ערך המפתח הראשי לרשימת הערכים (לשימוש בתנאי WHERE)
            update_sql = f"UPDATE {table_name} SET {', '.join(update_cols)} WHERE {primary_key_column} = %s"
            cursor.execute(update_sql, update_vals)  # ביצוע השאילתה
            cursor.connection.commit()
            messagebox.showinfo("Success", "Record updated successfully!")
            refresh_callback()
            update_win.destroy()
        except Exception as e:
            cursor.connection.rollback()
            messagebox.showerror("Error", f"Failed to update record:\n{e}")
    # כפתור עדכון
    ctk.CTkButton(update_win, text="Update", command=update_record, fg_color="#3cb371", width=120).pack(pady=20)
    #כפתור ביטול 
    ctk.CTkButton(update_win, text="Cancel", command=update_win.destroy, fg_color="#dc3545", width=120).pack(pady=5)
