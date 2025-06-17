import customtkinter as ctk
from tkinter import messagebox

def open_update_form(cursor, table_name, column_names, row_data, refresh_callback, primary_key_column):
    update_win = ctk.CTkToplevel()
    update_win.title(f"Update {table_name}")
    update_win.geometry("500x700")
    update_win.configure(fg_color="#eaf0ff")
    update_win.grab_set()

    entry_widgets = {}
    disabled_fields = set()

    form_frame = ctk.CTkFrame(update_win, fg_color="#f0f4ff")
    form_frame.pack(padx=20, pady=10, fill="both", expand=True)

    pk_index = column_names.index(primary_key_column)
    pk_val = row_data[pk_index]

    for i, (col, val) in enumerate(zip(column_names, row_data)):
        lbl = ctk.CTkLabel(form_frame, text=col.replace("_", " ").title(), font=("Segoe UI", 13))
        lbl.grid(row=i, column=0, sticky="w", padx=10, pady=8)
        if col == primary_key_column:
            pk_frame = ctk.CTkFrame(form_frame, fg_color="#e0e0e0", corner_radius=8)
            pk_frame.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
            pk_label = ctk.CTkLabel(pk_frame, text=str(val), font=("Segoe UI", 12, "bold"), text_color="#888")
            pk_label.pack(side="left", padx=8, pady=4)
            pk_note = ctk.CTkLabel(pk_frame, text="(Primary key - cannot change)", font=("Segoe UI", 10),
                                   text_color="#b22")
            pk_note.pack(side="left", padx=8)
            entry_widgets[col] = None
        else:
            if val is None or str(val).strip() == "":
                # שדה ריק – לא ניתן לעריכה
                entry = ctk.CTkEntry(form_frame, font=("Segoe UI", 12), state="disabled")
                entry.insert(0, "")
                entry.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
                form_frame.grid_columnconfigure(1, weight=1)
                entry_widgets[col] = entry
                disabled_fields.add(col)
                # הערה לשדה
                note = ctk.CTkLabel(form_frame, text="(Field is empty - cannot add value)", font=("Segoe UI", 10), text_color="#b22")
                note.grid(row=i, column=2, sticky="w", padx=4)
            else:
                entry = ctk.CTkEntry(form_frame, font=("Segoe UI", 12))
                entry.insert(0, str(val))
                entry.grid(row=i, column=1, sticky="ew", padx=10, pady=8)
                form_frame.grid_columnconfigure(1, weight=1)
                entry_widgets[col] = entry

    def update_record():
        try:
            update_cols = []
            update_vals = []
            for col in column_names:
                if col == primary_key_column:
                    continue
                if col in disabled_fields:
                    continue  # שדה ריק במקור – לא שולחים אותו בכלל
                user_val = entry_widgets[col].get()
                if user_val.strip() == "":
                    # היה ערך קודם, ועכשיו ריק – לא תקין!
                    messagebox.showerror("Error", f"The field '{col}' is required and cannot be empty!")
                    return
                update_cols.append(f"{col} = %s")
                update_vals.append(user_val)
            if not update_cols:
                messagebox.showinfo("Nothing to update", "No fields to update.")
                return
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