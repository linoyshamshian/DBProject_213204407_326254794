# update_form.py
import customtkinter as ctk
from tkinter import messagebox

# def open_update_form(cursor, table_name, column_names, row_data, refresh_callback):
#     update_win = ctk.CTkToplevel()
#     update_win.title(f"Update {table_name}")
#     update_win.geometry("500x700")
#     update_win.configure(fg_color="#eaf0ff")
#     update_win.grab_set()  # שמירת פוקוס
#
#     # מילון לשדות
#     entry_widgets = {}
#
#     # כותרת
#     ctk.CTkLabel(update_win, text=f"Update {table_name}", font=("Segoe UI", 20, "bold"), text_color="#2a3f77").pack(pady=20)
#
#     # טופס
#     form_frame = ctk.CTkFrame(update_win, fg_color="#f0f4ff")
#     form_frame.pack(padx=20, pady=10, fill="both", expand=True)
#
#     # יצירת שדות קלט
#     for i, (col, val) in enumerate(zip(column_names, row_data)):
#         lbl = ctk.CTkLabel(form_frame, text=col.replace("_", " ").title(), font=("Segoe UI", 13))
#         lbl.grid(row=i, column=0, sticky="w", padx=10, pady=8)
#         entry = ctk.CTkEntry(form_frame, font=("Segoe UI", 12))
#         entry.insert(0, str(val) if val is not None else "")
#         entry.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
#         form_frame.grid_columnconfigure(1, weight=1)
#         entry_widgets[col] = entry
#
#     # כפתור עדכון
#     def update_record():
#         try:
#             # הנח שמפתח ראשי הוא העמודה הראשונה
#             pk_col = column_names[0]
#             pk_val = row_data[0]
#             update_cols = []
#             update_vals = []
#             for col in column_names[1:]:  # לא לעדכן את המפתח הראשי
#                 update_cols.append(f"{col} = %s")
#                 update_vals.append(entry_widgets[col].get())
#             update_vals.append(pk_val)
#             update_sql = f"UPDATE {table_name} SET {', '.join(update_cols)} WHERE {pk_col} = %s"
#             cursor.execute(update_sql, update_vals)
#             cursor.connection.commit()
#             messagebox.showinfo("Success", "Record updated successfully!")
#             refresh_callback()
#             update_win.destroy()
#         except Exception as e:
#             cursor.connection.rollback()
#             messagebox.showerror("Error", f"Failed to update record:\n{e}")
#
#     ctk.CTkButton(update_win, text="Update", command=update_record, fg_color="#3cb371", width=120).pack(pady=20)
#     ctk.CTkButton(update_win, text="Cancel", command=update_win.destroy, fg_color="#dc3545", width=120).pack(pady=5)
def open_update_form(cursor, table_name, column_names, row_data, refresh_callback, primary_key_column):
    update_win = ctk.CTkToplevel()
    update_win.title(f"Update {table_name}")
    update_win.geometry("500x700")
    update_win.configure(fg_color="#eaf0ff")
    update_win.grab_set()

    entry_widgets = {}

    # יצירת טופס (frame) לשדות
    form_frame = ctk.CTkFrame(update_win, fg_color="#f0f4ff")
    form_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # מצא את האינדקס של המפתח הראשי
    pk_index = column_names.index(primary_key_column)
    pk_val = row_data[pk_index]

    # יצירת שדות קלט

    for i, (col, val) in enumerate(zip(column_names, row_data)):
        lbl = ctk.CTkLabel(form_frame, text=col.replace("_", " ").title(), font=("Segoe UI", 13))
        lbl.grid(row=i, column=0, sticky="w", padx=10, pady=8)
        if col == primary_key_column:
            # תצוגה בלוקית לשדה מפתח ראשי (לא ניתן לעריכה)
            pk_frame = ctk.CTkFrame(form_frame, fg_color="#e0e0e0", corner_radius=8)
            pk_frame.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
            pk_label = ctk.CTkLabel(pk_frame, text=str(val), font=("Segoe UI", 12, "bold"), text_color="#888")
            pk_label.pack(side="left", padx=8, pady=4)
            pk_note = ctk.CTkLabel(pk_frame, text="(Primary key - cannot change)", font=("Segoe UI", 10),
                                   text_color="#b22")
            pk_note.pack(side="left", padx=8)
            entry_widgets[col] = None  # לא צריך קלט
        else:
            entry = ctk.CTkEntry(form_frame, font=("Segoe UI", 12))
            entry.insert(0, str(val) if val is not None else "")
            entry.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
            form_frame.grid_columnconfigure(1, weight=1)
            entry_widgets[col] = entry

    # כפתור עדכון
    def update_record():
        try:
            update_cols = []
            update_vals = []
            for col in column_names:
                if col == primary_key_column:
                    continue  # לא לעדכן את המפתח הראשי
                update_cols.append(f"{col} = %s")
                update_vals.append(entry_widgets[col].get())
            update_vals.append(pk_val)
            update_sql = f"UPDATE {table_name} SET {', '.join(update_cols)} WHERE {primary_key_column} = %s"
            cursor.execute(update_sql, update_vals)
            cursor.connection.commit()
            messagebox.showinfo("Success", "Record updated successfully!")
            refresh_callback()
            update_win.destroy()
        except Exception as e:
            cursor.connection.rollback()
            messagebox.showerror("Error", f"Failed to update record:\n{e}")

    ctk.CTkButton(update_win, text="Update", command=update_record, fg_color="#3cb371", width=120).pack(pady=20)
    ctk.CTkButton(update_win, text="Cancel", command=update_win.destroy, fg_color="#dc3545", width=120).pack(pady=5)
